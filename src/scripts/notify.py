from twilio.rest import Client
import os
from dotenv import load_dotenv
import sqlite3
import argparse


def main(args):
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, "../..", ".env"))
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    db_path = os.getenv("DATABASE_URL")
    t_number = os.getenv("TWILIO_NUMBER")
    my_number = os.getenv("MY_NUMBER")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT food_name, purchase_date, actual_expiry, 
        (julianday(actual_expiry) - julianday(purchase_date)) AS diff_days 
    FROM food_item 
    WHERE (julianday(actual_expiry) - julianday(purchase_date)) < {days}
    AND user_id = {u_id}
    ORDER BY diff_days ASC
    """.format(
        days=args.expiry_threshold, u_id=args.user_id
    )
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        return

    sms_message = "Expiring Foods:\n\n"
    for row in rows:
        name, p_d, exp_d, d_left = row
        sms_message += "{name}: Expiring in {d_left} days\n- purchase date: {p_d}\n- estimated expiry: {exp_d}\n\n".format(
            name=name, d_left=d_left, p_d=p_d, exp_d=exp_d
        )
    conn.close()

    print(sms_message)
    client = Client(account_sid, auth_token)
    message = client.messages.create(from_=t_number, body=sms_message, to=my_number)
    print(message.sid)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_id", help="Id of user to notify")
    parser.add_argument(
        "--expiry_threshold", help="Days to include in warning sms", default=5
    )
    args = parser.parse_args()

    main(args)
