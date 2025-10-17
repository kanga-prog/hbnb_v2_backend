# app/utils.py
import os
from werkzeug.utils import secure_filename
from flask import current_app


def save_file(file, subfolder=""):
    """
    Sauvegarde un fichier dans /uploads (ou sous-dossier)
    et retourne son URL publique complète (HTTPS en production).
    """
    # 📁 Dossier de destination
    upload_folder = os.path.join(current_app.root_path, "uploads")
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)
    os.makedirs(upload_folder, exist_ok=True)

    # 💾 Sauvegarde du fichier localement
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # 🌍 Détection automatique de l’environnement
    # En production (Render) → HTTPS obligatoire
    if os.getenv("RENDER") or "onrender.com" in os.getenv("BASE_URL", ""):
        base_url = "https://hbnb-v2-backend.onrender.com"
    else:
        # En local uniquement
        base_url = "http://127.0.0.1:5000"

    # 🔗 Construction de l’URL publique complète
    if subfolder:
        return f"{base_url}/uploads/{subfolder}/{filename}"
    return f"{base_url}/uploads/{filename}"
