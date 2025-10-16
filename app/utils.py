# app/utils.py
import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_file(file, subfolder=""):
    """
    Sauvegarde un fichier dans /uploads (ou sous-dossier) et retourne son URL publique complète.
    """
    upload_folder = os.path.join(current_app.root_path, "uploads")
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)

    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # 🔗 Génère une URL absolue HTTPS (selon environnement)
    if "onrender.com" in os.getenv("BASE_URL", "") or os.getenv("RENDER"):
          base_url = "BASE_URL", "https://hbnb-v2-backend.onrender.com"
    else:
        base_url = "http://127.0.0.1:5000"   
           
    return f"{base_url}/uploads/{subfolder}/{filename}" if subfolder else f"{base_url}/uploads/{filename}"
