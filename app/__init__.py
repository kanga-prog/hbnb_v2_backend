import os
import requests
from threading import Timer
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_restx import Api
from flask_cors import CORS

from .extensions import db, migrate, mail, jwt

# Import des namespaces
from app.routes.places import api as PLACES_NS
from app.routes.amenities import api as AMENITIES_NS
from app.routes.reservations import api as RESERVATIONS_NS
from app.routes.reviews import api as REVIEWS_NS
from app.routes.users import api as USERS_NS
from app.routes.auth import api as AUTH_NS

# Charger les variables d'environnement
load_dotenv()


# ==============================
# 🕓 Keep Alive interne Render
# ==============================
def keep_alive():
    """Empêche Render de mettre le conteneur en veille"""
    try:
        requests.get("https://hbnb-v2-backend.onrender.com/")
        print("[KeepAlive] 🔄 Ping réussi ✅")
    except Exception as e:
        print(f"[KeepAlive] ⚠️ Échec du ping : {e}")
    Timer(300, keep_alive).start()  # Relance toutes les 5 minutes (300s)


def create_app():
    """Application Factory Flask pour HBnB."""
    app = Flask(__name__)

    # -----------------------------
    # 🔧 CONFIGURATION
    # -----------------------------
    app.config.from_object("config.Config")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", app.config.get("SECRET_KEY"))
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    if os.getenv("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    # -----------------------------
    # ⚙️ INITIALISATION DES EXTENSIONS
    # -----------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)

    # -----------------------------
    # 🌍 CORS GLOBAL
    # -----------------------------
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "https://hbnb-v2-frontend-79ym.vercel.app",
                    "http://localhost:5173",
                ]
            }
        },
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # -----------------------------
    # 📦 IMPORT DES MODÈLES
    # -----------------------------
    from app.models import user, place, amenity, associations, reservation, review

    # -----------------------------
    # 🚀 API REST
    # -----------------------------
    api = Api(app, version="1.0", title="HBnB API", description="API HBnB avec Flask-RESTx")

    api.add_namespace(PLACES_NS, path="/api/places")
    api.add_namespace(AMENITIES_NS, path="/api/amenities")
    api.add_namespace(RESERVATIONS_NS, path="/api/reservations")
    api.add_namespace(REVIEWS_NS, path="/api/reviews")
    api.add_namespace(USERS_NS, path="/api/users")
    api.add_namespace(AUTH_NS, path="/api/auth")

    # -----------------------------
    # 🧩 Fix global CORS headers
    # -----------------------------
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "https://hbnb-v2-frontend-79ym.vercel.app"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    # -----------------------------
    # 🖼️ ROUTES POUR LES FICHIERS UPLOADÉS
    # -----------------------------
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        upload_folder = os.path.join(app.root_path, "uploads")
        return send_from_directory(upload_folder, filename)

    # -----------------------------
    # 🕓 Lancement du keep-alive
    # -----------------------------
    if os.getenv("RENDER") or os.getenv("KEEP_ALIVE", "true") == "true":
        print("[KeepAlive] Service de ping activé 🚀")
        Timer(10, keep_alive).start()  # Démarre 10 secondes après lancement

    return app
