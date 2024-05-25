from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from config import Config
import os
import importlib
from datetime import datetime

from db.models import db, FoodItem, EstimatedExpiry
import utils

importlib.reload(utils)

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


@app.route("/items", methods=["GET"])
@cross_origin()
def get_items():
    food_items = FoodItem.query.all()
    food_items = [item.to_dict() for item in food_items]
    response = jsonify(food_items)
    return response


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET", "POST"])
@cross_origin()
def upload_file():
    file = request.files["receipt"]
    print(file)

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        f_path = os.path.join(
            "/Users/jacksonfraser/Desktop/projects/food-tracker/src/uploads", filename
        )
        file.save(f_path)
        food_items = utils.process_receipt(f_path)
        response = jsonify(food_items)
        print("OPENAI RESPONSE: ", response)
        return response, 200

    return jsonify({"error": "File type not allowed"}), 400


@app.route("/updatedb", methods=["POST"])
@cross_origin()
def update_db():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    try:
        print(data)
        for item in data:
            print(item)
            existing_item = EstimatedExpiry.query.filter_by(
                food_name=item["name"]
            ).first()
            print(existing_item)
            if existing_item:
                food_item = FoodItem(
                    food_name=item["name"],
                    current_count=item["quantity"],
                    actual_expiry=datetime.strptime(
                        item["estimated_expiry_date"], "%Y-%m-%d"
                    ).date(),
                    estimated_expiry_id=existing_item.expiry_id,
                    user_id=1,
                )
                db.session.add(food_item)
            else:
                est_exp_item = EstimatedExpiry(
                    food_name=item["name"],
                    estimated_days=(
                        (
                            datetime.strptime(item["estimated_expiry_date"], "%Y-%m-%d")
                            - datetime.now()
                        ).days
                    ),
                )
                db.session.add(est_exp_item)
                db.session.commit()
                food_item = FoodItem(
                    food_name=item["name"],
                    current_count=item["quantity"],
                    actual_expiry=datetime.strptime(
                        item["estimated_expiry_date"], "%Y-%m-%d"
                    ).date(),
                    estimated_expiry_id=est_exp_item.expiry_id,
                    user_id=1,
                )
                db.session.add(food_item)
        db.session.commit()

        return jsonify({"message": "Database updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
