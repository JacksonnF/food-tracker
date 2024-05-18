import os
from dotenv import load_dotenv


class Config:
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

    # CORS_HEADERS = "Content-Type"
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
