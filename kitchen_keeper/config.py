import os
from pathlib import Path


def required_env(name):
    value = os.environ.get(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    WTF_CSRF_ENABLED = True
    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOAD_FOLDER = BASE_DIR / "instance" / "uploads"
    RECIPE_IMAGE_UPLOAD_FOLDER = UPLOAD_FOLDER / "recipes"

    @classmethod
    def configure(cls):
        database_uri = os.environ.get("DATABASE_URI")
        if not database_uri:
            database_uri = (
                f"postgresql+psycopg://"
                f"{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}"
                f"@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}")

        cls.SQLALCHEMY_DATABASE_URI = database_uri


class DevelopmentConfig(Config):
    DEBUG = True
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres_admin")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "dev_admin_password")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "kitchen_keeper_dev")


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def configure(cls):
        cls.POSTGRES_HOST = required_env("POSTGRES_HOST")
        cls.POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
        cls.POSTGRES_USER = required_env("POSTGRES_USER")
        cls.POSTGRES_PASSWORD = required_env("POSTGRES_PASSWORD")
        cls.POSTGRES_DB = required_env("POSTGRES_DB")

        super().configure()