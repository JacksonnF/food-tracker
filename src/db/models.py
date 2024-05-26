import flask_sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = flask_sqlalchemy.SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.name

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id


class FoodItem(db.Model):
    food_id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(80), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    current_count = db.Column(db.Integer, nullable=False)
    actual_expiry = db.Column(db.Date, nullable=False)
    estimated_expiry_id = db.Column(
        db.Integer, db.ForeignKey("estimated_expiry.expiry_id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    def __repr__(self):
        return "<FoodItem %r>" % self.food_name

    def to_dict(self):
        return {
            "food_id": self.food_id,
            "food_name": self.food_name,
            "purchase_date": self.purchase_date,
            "current_count": self.current_count,
            "actual_expiry": self.actual_expiry,
            "estimated_expiry_id": self.estimated_expiry_id,
            "user_id": self.user_id,
        }


class EstimatedExpiry(db.Model):
    expiry_id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(80), unique=True, nullable=False)
    estimated_days = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<EstimatedExpiry %r>" % self.food_name
