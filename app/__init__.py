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

# URL de production backend
PROD_BASE_URL = "https://hbnb-v2-backend.onrender.com"


# ==============================
# 🕓 Keep Alive interne Render
# ==============================
def keep_alive():
    """Empêche Render de mettre le conteneur en veille"""
    try:
        requests.get(PROD_BASE_URL)
        print("[KeepAlive] 🔄 Ping réussi ✅")
    except Exception as e:
        print(f"[KeepAlive] ⚠️ Échec du ping : {e}")
    Timer(300, keep_alive).start()  # Relance toutes les 5 minutes (300s)


# ==============================
# 🔧 Fonction pour corriger les URLs
# ==============================
def fix_urls_on_startup():
    """Corrige automatiquement les URLs locales ou relatives dans la BDD"""
    from app.models.user import User
    from app.models.place import PlaceImage

    updated_users = 0
    for u in User.query.all():
        if u.avatar:
            if u.avatar.startswith("http://127.0.0.1:5000"):
                u.avatar = u.avatar.replace("http://127.0.0.1:5000", PROD_BASE_URL)
                updated_users += 1
            elif u.avatar.startswith("/uploads"):
                u.avatar = f"{PROD_BASE_URL}{u.avatar}"
                updated_users += 1

    updated_images = 0
    for img in PlaceImage.query.all():
        if img.url:
            if img.url.startswith("http://127.0.0.1:5000"):
                img.url = img.url.replace("http://127.0.0.1:5000", PROD_BASE_URL)
                updated_images += 1
            elif img.url.startswith("/uploads"):
                img.url = f"{PROD_BASE_URL}{img.url}"
                updated_images += 1

    db.session.commit()
    print(f"[✔] {updated_users} avatars utilisateurs mis à jour.")
    print(f"[✔] {updated_images} images de lieux mises à jour.")


# ==============================
# 🔧 Application Factory
# ==============================
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
        resources={r"/api/*": {"origins": [
            "https://hbnb-v2-frontend-79ym.vercel.app",
            "http://localhost:5173",
        ]}},
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

    # -----------------------------
    # 🔧 Correction automatique des URLs
    # -----------------------------
    with app.app_context():
        fix_urls_on_startup()

    return app
