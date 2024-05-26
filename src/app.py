from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
import sqlalchemy as sa
import jwt

from src.config import Config
import os
import datetime as dt
from datetime import datetime
from functools import wraps

from src.db.models import db, FoodItem, User, EstimatedExpiry
import src.utils as utils

app = Flask(
    __name__, template_folder="../alpine-app/templates", static_folder="../alpine-app"
)

CORS(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/receipt")
def receipt_page():
    return render_template("receipt.html")


@app.route("/login-page")
def login_page():
    return render_template("login.html")


@app.route("/register-page")
def register_page():
    return render_template("register.html")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = db.session.get(User, data["user_id"])
        except:
            return jsonify({"message": "Token is invalid!"}), 403

        return f(current_user, *args, **kwargs)

    return decorated


def generate_token(user):
    token = jwt.encode(
        {
            "user_id": user.user_id,
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return token


@app.route("/login", methods=["GET", "POST"])
@cross_origin()
def login_fn():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = db.session.scalar(sa.select(User).where(User.name == username))

    if user is None or not user.check_password(password):
        return jsonify({"message": "Login Failed"}), 401

    token = generate_token(user)
    return jsonify({"token": token}), 200


@app.route("/register", methods=["GET", "POST"])
@cross_origin()
def register_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    new_user = User(name=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 200


@app.route("/items", methods=["GET"])
@cross_origin()
@token_required
def get_items(current_user):
    food_items = FoodItem.query.filter_by(user_id=current_user.user_id).all()
    food_items = [item.to_dict() for item in food_items]
    response = jsonify(food_items)
    return response


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET", "POST"])
@cross_origin()
@token_required
def upload_file(current_user):
    file = request.files["receipt"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        basedir = os.path.abspath(os.path.dirname(__file__))
        f_path = os.path.join(basedir, app.config["UPLOAD_FOLDER"], filename)
        file.save(f_path)
        food_items = utils.process_receipt(f_path)
        response = jsonify(food_items)
        return response, 200

    return jsonify({"error": "File type not allowed"}), 400


@app.route("/updatedb", methods=["POST"])
@cross_origin()
@token_required
def update_db(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    try:
        for item in data:
            existing_item = EstimatedExpiry.query.filter_by(
                food_name=item["name"]
            ).first()
            if existing_item:
                food_item = FoodItem(
                    food_name=item["name"],
                    current_count=item["quantity"],
                    actual_expiry=datetime.strptime(
                        item["estimated_expiry_date"], "%Y-%m-%d"
                    ).date(),
                    estimated_expiry_id=existing_item.expiry_id,
                    user_id=current_user.user_id,
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
                    user_id=current_user.user_id,
                )
                db.session.add(food_item)
        db.session.commit()

        return jsonify({"message": "Database updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
