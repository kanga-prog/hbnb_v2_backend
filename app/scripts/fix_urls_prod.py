#!/usr/bin/env python3
"""
Script de correction des URLs pour la production Render.
Convertit toutes les URLs locales (http://127.0.0.1:5000) en HTTPS vers le backend Render.
"""

import os
from app import create_app, db
from app.models.user import User
from app.models.place import Place

# 🔧 Crée l'app Flask en mode production
app = create_app()
app.app_context().push()

# URL de production Render
PROD_BASE_URL = "https://hbnb-v2-backend.onrender.com"

def fix_user_avatars():
    """Met à jour les avatars des utilisateurs"""
    users = User.query.all()
    updated = 0
    for user in users:
        if user.avatar_url and user.avatar_url.startswith("http://127.0.0.1:5000"):
            user.avatar_url = user.avatar_url.replace(
                "http://127.0.0.1:5000", PROD_BASE_URL
            )
            updated += 1
    db.session.commit()
    print(f"[✔] {updated} avatars utilisateurs mis à jour.")

def fix_place_images():
    """Met à jour les images des lieux"""
    places = Place.query.all()
    updated = 0
    for place in places:
        if place.images_urls:
            new_urls = []
            for url in place.images_urls:
                if url.startswith("http://127.0.0.1:5000"):
                    url = url.replace("http://127.0.0.1:5000", PROD_BASE_URL)
                    updated += 1
                new_urls.append(url)
            place.images_urls = new_urls
    db.session.commit()
    print(f"[✔] {updated} images de lieux mises à jour.")

if __name__ == "__main__":
    fix_user_avatars()
    fix_place_images()
    print("[✅] Toutes les URLs locales ont été remplacées par l'URL de production Render.")
