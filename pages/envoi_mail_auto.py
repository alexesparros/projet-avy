from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
#from utils.helpers import send_welcome_email


def send_welcome_email(receiver_email, username):
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
