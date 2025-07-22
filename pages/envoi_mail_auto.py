from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from utils.helpers import send_welcome_email


def send_welcome_email(receiver_email, username):
    sender_email = "ludrun.contact@gmail.com"
    sender_password = "khil hpbn unny cpzy"

    subject = "Bienvenue sur notre site !"
    body = f"Bonjour {username},\n\nMerci de t'être inscrit ! 🎉\n\nÀ bientôt !"

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
