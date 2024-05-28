from flask import jsonify, request
from flask_cors import cross_origin
from datetime import datetime

from db.models import db, FoodItem, EstimatedExpiry
from auth import token_required
import scripts.openai_utils as openai_utils


def init_api(app):
    @app.route("/items", methods=["GET"])
    @cross_origin()
    @token_required
    def get_items(current_user):
        food_items = FoodItem.query.filter_by(user_id=current_user.user_id).all()
        food_items = [item.to_dict() for item in food_items]
        response = jsonify(food_items)
        return response

    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @app.route("/upload", methods=["GET", "POST"])
    @cross_origin()
    @token_required
    def upload_file(current_user):
        file = request.files["receipt"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            food_items = openai_utils.process_receipt(file.read())
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
                                datetime.strptime(
                                    item["estimated_expiry_date"], "%Y-%m-%d"
                                )
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
