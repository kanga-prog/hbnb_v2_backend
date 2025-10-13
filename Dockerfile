# 🔹 Image Python légère
FROM python:3.11-slim

# 🔹 Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 🔹 Répertoire de travail
WORKDIR /app

# 🔹 Installer dépendances système (pour mysqlclient)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 🔹 Copier et installer les requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Copier le code de l'application
COPY . .

# 🔹 Exposer le port (Render utilisera $PORT)
EXPOSE $PORT

# 🔹 Lancer Gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT run:app
