import streamlit as st
import sqlite3
from time import sleep
<<<<<<< HEAD
import os

def inscription():
    db_path = "database_clients.db"
    if "connection" not in st.session_state:
        st.session_state["connection"] = sqlite3.connect(db_path, check_same_thread=False)
    c = st.session_state["connection"].cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    st.session_state["connection"].commit()

    st.title("Page d'inscription")
    with st.form("signup_form"):
        new_username = st.text_input("Nom d'utilisateur")
        new_email = st.text_input("Email")
        new_password = st.text_input("Mot de passe", type="password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password")
        signup_button = st.form_submit_button("S'inscrire")
        if signup_button:
            if new_password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas.")
            elif len(new_password) < 8:
                st.error("❌ Le mot de passe doit contenir au moins 8 caractères.")
            else:
                # Vérifier si l'utilisateur existe déjà
                c = st.session_state["connection"].cursor()
                c.execute("SELECT * FROM users WHERE email = ?", (new_email,))
                if c.fetchone():
                    st.error("❌ Adresse mail déjà existante.")
                else:
                    try:
                        c.execute(
                            "INSERT INTO users (email, password, username) VALUES (?, ?, ?)",
                            (new_email, new_password, new_username)
                        )
                        st.session_state["connection"].commit()
                        st.success("✅ Inscription réussie ! Vous pouvez maintenant vous connecter.")
                        sleep(2)
                    except Exception as e:
                        st.error(f"Erreur lors de l'inscription : {e}")
=======
from pages.envoi_mail_auto import send_welcome_email



# Connexion à la base de données
if "connection" not in st.session_state:
    st.session_state["connection"] = sqlite3.connect("database_clients", check_same_thread=False)

c = st.session_state["connection"].cursor()

# Créer la table si elle n'existe pas
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT
    )
''')
st.session_state["connection"].commit()


def inscription():

    # Titre
    st.title("Page d'inscription")

    # Formulaire d'inscription
    with st.form("signup_form"):
        new_email = st.text_input("Adresse mail")
        new_password = st.text_input("Choisis un mot de passe", type="password")
        confirm_password = st.text_input("Confirme le mot de passe", type="password")
        new_username = st.text_input("Quel est ton pseudo ?")
        signup_button = st.form_submit_button("S'inscrire")

    if signup_button:
        if new_password != confirm_password:
            st.error("❌ Les mots de passe ne correspondent pas.")
        elif len(new_password) < 8:
            st.error("❌ Le mot de passe doit contenir au moins 8 caractères.")
        else:
            # Vérifier si l'utilisateur existe déjà
            c = st.session_state["connection"].cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (new_email,))
            if c.fetchone():
                st.error("❌ Adresse mail déjà existant.")
            else:
                # Insérer le nouvel utilisateur avec mot de passe haché
                
                c = st.session_state["connection"].cursor()
                c.execute(
                    "INSERT INTO users (email, password, username) VALUES (?, ?, ?)",
                    (new_email, new_password, new_username)
                )
                st.session_state["connection"].commit()
                st.success("✅ Inscription réussie ! Vous pouvez maintenant vous connecter.")
                send_welcome_email(new_email, new_username)
                sleep(3)
                st.session_state["page"] = "Connexion"
                st.rerun()

    # 👉 Bouton pour accéder à la page de connexion
    if st.button("J'ai déjà un compte, je me connecte"):
        st.session_state["page"] = "Connexion"
        st.rerun()
>>>>>>> 156dd6839024693ecdf72da4780ba6498b37b0da
