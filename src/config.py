import os
from dotenv import load_dotenv


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, "..", ".env"))

    # CORS_HEADERS = "Content-Type"
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TWILIO_SID = os.getenv("TWILIO_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
