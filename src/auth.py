from flask import request, redirect, url_for, session, jsonify
from flask_cors import cross_origin
import jwt
from functools import wraps
import sqlalchemy as sa

from db.models import User, db
from config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
        if "token" in session:
            token = session["token"]
        if not token:
            return redirect(url_for("login_page"))
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = db.session.get(User, data["user_id"])
            if not current_user:
                redirect(url_for("login_page"))
        except:
            return redirect(url_for("login_page"))

        return f(current_user, *args, **kwargs)

    return decorated


def generate_token(user):
    token = jwt.encode(
        {
            "user_id": user.user_id,
        },
        Config.SECRET_KEY,
        algorithm="HS256",
    )
    return token


def init_auth(app):
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
        session["token"] = f"Bearer {token}"

        return jsonify({"token": token}), 200

    @app.route("/register", methods=["GET", "POST"])
    @cross_origin()
    @token_required
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

    @app.route("/logout", methods=["POST"])
    def logout_fn():
        session.pop("token", None)
        return jsonify({"message": "Logged out successfully"}), 200
