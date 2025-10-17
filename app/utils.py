# app/utils.py
import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_file(file, subfolder=""):
    """
    Sauvegarde un fichier dans /uploads (ou sous-dossier)
    et retourne son URL publique complète.
    """
    upload_folder = os.path.join(current_app.root_path, "uploads")
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)

    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # ✅ Détection d'environnement et génération d'URL correcte
    base_url = os.getenv("BASE_URL")

    if not base_url:
        # Si aucune variable d'environnement, on choisit automatiquement
        if os.getenv("RENDER"):  # Variable automatique sur Render
            base_url = "https://hbnb-v2-backend.onrender.com"
        else:
            base_url = "http://127.0.0.1:5000"

    # 🧩 Retourne une URL propre
    if subfolder:
        return f"{base_url}/uploads/{subfolder}/{filename}"
    return f"{base_url}/uploads/{filename}"
