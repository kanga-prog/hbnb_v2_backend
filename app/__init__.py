# APP/__INIT__.PY
import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_restx import Api
from flask_cors import CORS  # ⚡ CORS direct ici

from .extensions import db, migrate, mail, jwt

# Import des namespaces
from app.routes.places import api as PLACES_NS
from app.routes.amenities import api as AMENITIES_NS
from app.routes.reservations import api as RESERVATIONS_NS
from app.routes.reviews import api as REVIEWS_NS
from app.routes.users import api as USERS_NS
from app.routes.auth import api as AUTH_NS

# Charger les variables d'environnement (.env)
load_dotenv()


def create_app():
    """Application Factory Flask pour HBnB."""
    app = Flask(__name__)

    # -----------------------------
    # 🔧 CONFIGURATION
    # -----------------------------
    app.config.from_object("config.Config")

    # Clé JWT
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", app.config.get("SECRET_KEY")
    )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    # ✅ Ne remplace la valeur que si la variable est définie
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
    CORS(app, resources={r"/api/*": {
        "origins": [
            "https://hbnb-v2-frontend-79ym.vercel.app",
            "http://localhost:5173"  # pour le dev local
        ]
    }}, supports_credentials=True)

    # -----------------------------
    # 📦 IMPORT DES MODÈLES
    # -----------------------------
    from app.models import user, place, amenity, associations, reservation, review

    # -----------------------------
    # 🚀 API REST
    # -----------------------------
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="API HBnB avec Flask-RESTx",
    )

    # Enregistrement des namespaces
    api.add_namespace(PLACES_NS, path="/api/places")
    api.add_namespace(AMENITIES_NS, path="/api/amenities")
    api.add_namespace(RESERVATIONS_NS, path="/api/reservations")
    api.add_namespace(REVIEWS_NS, path="/api/reviews")
    api.add_namespace(USERS_NS, path="/api/users")
    api.add_namespace(AUTH_NS, path="/api/auth")

    # -----------------------------
    # 🖼️ ROUTES POUR LES FICHIERS UPLOADÉS
    # -----------------------------
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        """Servir les fichiers uploadés depuis /uploads"""
        upload_folder = os.path.join(app.root_path, "uploads")
        return send_from_directory(upload_folder, filename)

    return app
