# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # charge automatiquement les variables .env si présent

class Config:
    # Base de données PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://myuser:mypassword@localhost:5432/hbnb_v2_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"options": "-csearch_path=public"}
    }

    # Sécurité
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

    # Configuration e-mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'teckivoire@gmail.com'
    MAIL_PASSWORD = 'ynsbluupsuxntxrr'
    MAIL_DEFAULT_SENDER = 'teckivoire@gmail.com'
