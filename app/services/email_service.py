# app/services/email_service.py
import os
import requests

# CLÉS API BREVO
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER = os.getenv("BREVO_SENDER", "TECKIVOIRE@GMAIL.COM")

# Vérification initiale
if not BREVO_API_KEY:
    print("❌ ERREUR: BREVO_API_KEY non définie !")
if not BREVO_SENDER:
    print("❌ ERREUR: BREVO_SENDER non défini !")

def send_email(subject: str, to: str, body: str):
    """ENVOIE UN E-MAIL VIA L’API BREVO AVEC LOGS DÉTAILLÉS"""
    if not BREVO_API_KEY or not BREVO_SENDER:
        print("❌ Impossible d’envoyer l’e-mail: clé ou expéditeur manquant")
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    payload = {
        "sender": {"email": BREVO_SENDER, "name": "HBNB AUTH"},
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
        print("DEBUG - Brevo Response:", response.status_code, response.text)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        print(f"❌ ERREUR HTTP Brevo ({response.status_code}): {response.text}")
    except Exception as e:
        print("❌ ERREUR GÉNÉRALE ENVOI E-MAIL:", e)
    return False


def send_2fa_code(email, code):
    """ENVOIE LE CODE DE VÉRIFICATION 2FA"""
    subject = "VOTRE CODE DE VÉRIFICATION HBNB"
    body = f"Votre code de vérification est : <b>{code}</b>. Il expire dans 10 minutes."
    return send_email(subject, email, body)


def send_reset_code(email, code):
    """ENVOIE LE CODE DE RÉINITIALISATION DU MOT DE PASSE"""
    subject = "RÉINITIALISATION DE VOTRE MOT DE PASSE"
    body = f"Voici votre code de réinitialisation : <b>{code}</b>. Il expire dans 10 minutes."
    return send_email(subject, email, body)
