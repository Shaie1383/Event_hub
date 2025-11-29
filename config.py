# config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # Secret Key (fallback provided)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # Database (SQLite by default, can override with DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{BASE_DIR / 'app_data.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Template & Static directories (Flask detects automatically)
    TEMPLATES_AUTO_RELOAD = True

    # Safe UTF-8 handling to avoid unicode decode errors
    JSON_AS_ASCII = False

    # Where user-uploaded ZIP (images) will be checked
    UPLOADED_IMAGES_ZIP = os.environ.get(
        "UPLOADED_IMAGES_ZIP",
        str(BASE_DIR / "all_event_images.zip")
    )

    # Enable debug mode through env variable (optional)
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # In production you should override SECRET_KEY and DATABASE_URL using env variables


# Select config based on FLASK_ENV
def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
