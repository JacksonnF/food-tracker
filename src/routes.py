from flask import render_template

from auth import token_required


def init_routes(app):
    @app.route("/")
    @token_required
    def index_page(current_user):
        return render_template("index.html")

    @app.route("/receipt")
    @token_required
    def receipt_page(current_user):
        return render_template("receipt.html")

    @app.route("/login-page")
    def login_page():
        return render_template("login.html")

    @app.route("/register-page")
    # @token_required
    def register_page():
        return render_template("register.html")
