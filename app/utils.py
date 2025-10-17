# app/utils.py
import os
from werkzeug.utils import secure_filename
from flask import current_app


def save_file(file, subfolder=""):
    """
    Sauvegarde un fichier dans /uploads (ou sous-dossier)
    et retourne une URL publique HTTPS pour la production Render uniquement.
    """
    upload_folder = os.path.join(current_app.root_path, "uploads")
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)

    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # 🌍 Production uniquement (Render)
    base_url = "https://hbnb-v2-backend.onrender.com"

    # 🔗 URL publique finale
    if subfolder:
        return f"{base_url}/uploads/{subfolder}/{filename}"
    return f"{base_url}/uploads/{filename}"
