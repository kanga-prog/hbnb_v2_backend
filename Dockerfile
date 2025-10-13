# 🔹 Image Python légère
FROM python:3.11-slim

# 🔹 Variables d'environnement pour pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 🔹 Répertoire de travail
WORKDIR /app

# 🔹 Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 🔹 Copier et installer les requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Copier le code de l'application
COPY . .

# 🔹 Exposer le port défini par Render
EXPOSE $PORT

# 🔹 Lancer Gunicorn en écoutant sur le port de Render
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "run:app"]
