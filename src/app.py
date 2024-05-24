from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from config import Config
import os

from db.models import db, FoodItem
from utils import process_receipt

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

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join('/Users/jacksonf/personal/food-tracker/src/uploads', filename))
        process_receipt()
        return jsonify({"message": "File successfully uploaded"}), 200

    return jsonify({"error": "File type not allowed"}), 400


def process_receipt():
    pass


if __name__ == "__main__":
    app.run(debug=True)
