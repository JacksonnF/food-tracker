import sqlite3

connection = sqlite3.connect("database.sqlite")


with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    """ 
    INSERT INTO EstimatedExpiry (food_name, estimated_days)
    VALUES ('Milk', 7), ('Eggs', 21), ('Cheese', 30)
    """
)
cur.execute(
    """
    INSERT INTO FoodItem (food_name, purchase_date, current_count, actual_expiry, estimated_expiry_id)
    VALUES ('Milk', DATE('2024-05-22'), 2, DATE('2024-05-29'), 
    (SELECT id FROM EstimatedExpiry WHERE food_name = 'Milk'))
    """
)

connection.commit()
connection.close()
