# Fonctions utilitaires génériques pour le projet AVY

import re
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def extraire_jeux_texte(texte):
    """Extrait les jeux, descriptions, notes et critiques d'un texte structuré."""
    jeux_brut = re.findall(
        r"\d+\.\s*([^\n]+)\n(.*?)(?:Note\s*:\s*(\d+/10))?\s*(?:Critique\s*:\s*(.*?))?(?=\n\d+\.|$)",
        texte, re.DOTALL)
    jeux = []
    for nom, desc, note, critique in jeux_brut:
        nom_ligne = nom.strip()
        nom_ligne = re.sub(r"^[*_`]+|[*_`]+$", "", nom_ligne)
        nom_ligne = re.sub(r"^(le )?nom\s*[:\-]*\s*", "", nom_ligne, flags=re.IGNORECASE)
        if re.match(r"^(le )?nom du jeu\s*:?$", nom_ligne, re.IGNORECASE):
            desc_lignes = desc.strip().split('\n', 1)
            vrai_nom = desc_lignes[0].strip()
            desc = desc[len(vrai_nom):].lstrip('\n').lstrip() if len(desc_lignes) > 1 else ''
        else:
            vrai_nom = nom_ligne
        jeux.append((vrai_nom, desc, note, critique))
    return jeux

def img_to_base64(path):
    """Encode une image en base64 pour affichage dans Streamlit."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def send_welcome_email(receiver_email, username):
    """Envoie un email de bienvenue à un nouvel utilisateur."""
    sender_email = "ludrun.contact@gmail.com"
    sender_password = "khil hpbn unny cpzy"
    subject = "Bienvenue sur notre site !"
    body = f"""Salut {username} ,
    
    Bravo ! Tu viens d’entrer dans le QG des gamers indécis — aka Ludrun.
    Ici, c’est simple : fini les débats à rallonge du style “On joue à quoi ce soir ?”, les scrolls infinis sur Steam et les ragequits de fin de soirée. Grâce à toi (et un peu à nous), tu vas pouvoir trouver le jeu parfait pour ta vibe du moment. 
    Que tu sois plutôt FPS nerveux, RPG planant, rogue-like exigeant ou simulateur de chèvre (oui oui, on juge pas), on est là pour t’aiguiller avec style.

    Merci d’avoir rejoint notre aventure ! On espère que tu t’y sentiras comme dans un lobby où tout le monde est OP.

    À très vite sur Ludrun,
    L’équipe qui ne ragequit jamais ... Oh grand jamais ... !!! 

    PS : Si tu veux nous faire un coucou, une reco ou un bug report digne d’un boss final, réponds à ce mail !"""
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email envoyé !")
    except Exception as e:
        print(f"Erreur envoi mail : {e}")
