from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from config import Config
import os
import sqlite3


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def get_db_connection():
    print("DATABASE URL: ", app.config["DATABASE_URL"])
    conn = sqlite3.connect(app.config["DATABASE_URL"])

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory
    return conn


@app.route("/items", methods=["GET"])
@cross_origin()
def get_items():
    conn = get_db_connection()
    food_items = conn.execute("SELECT * FROM FoodItem").fetchall()
    conn.close()
    for row in food_items:
        print(row)
    response = jsonify(food_items)
    return response


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET", "POST"])
@cross_origin(support_credentials=True)
def upload_file():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return jsonify({"message": "File successfully uploaded"}), 200

    return jsonify({"error": "File type not allowed"}), 400


if __name__ == "__main__":
    app.run(debug=True)
