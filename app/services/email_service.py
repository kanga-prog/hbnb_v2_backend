# app/services/email_service.py
import os
import requests

# Clés API Brevo
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER = os.getenv("BREVO_SENDER", "teckivoire@gmail.com")

# Debug temporaire pour vérifier la lecture des variables
print("DEBUG - BREVO_API_KEY:", BREVO_API_KEY)
print("DEBUG - BREVO_SENDER:", BREVO_SENDER)

def send_email(subject: str, to: str, body: str):
    """Envoie un e-mail via l’API Brevo"""
    url = "https://api.brevo.com/v3/smtp/email"
    payload = {
        "sender": {"email": BREVO_SENDER, "name": "HBnB Auth"},
        "to": [{"email": to}],
        "subject": subject,
        "htmlContent": f"<p>{body}</p>"
    }
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return True
    except Exception as e:
        print("❌ Erreur envoi e-mail:", e)
        return False


def send_2fa_code(email, code):
    """Envoie le code de vérification 2FA"""
    subject = "Votre code de vérification HBnB"
    body = f"Votre code de vérification est : <b>{code}</b>. Il expire dans 10 minutes."
    return send_email(subject, email, body)


def send_reset_code(email, code):
    """Envoie le code de réinitialisation du mot de passe"""
    subject = "Réinitialisation de votre mot de passe"
    body = f"Voici votre code de réinitialisation : <b>{code}</b>. Il expire dans 10 minutes."
    return send_email(subject, email, body)
