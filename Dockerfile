# Utiliser une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer curl pour tester depuis le conteneur
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copier l'application
COPY . .

# Exposer le port
EXPOSE 5000

# Commande par défaut
CMD ["python", "run.py","--host=0.0.0.0", "--port=5000"]
