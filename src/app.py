from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from config import Config
import os

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config.from_object(Config)

# Sample data
items = [
    {"id": 1, "name": "Milk"},
    {"id": 2, "name": "Bread"},
    {"id": 3, "name": "Eggs"},
]
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


@app.route("/items", methods=["GET"])
@cross_origin()
def get_items():
    return jsonify(items)


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
