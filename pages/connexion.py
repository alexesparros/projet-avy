import streamlit as st
import sqlite3
from time import sleep
import os
from datetime import datetime

st.session_state["connection"] = sqlite3.connect(os.path.join("projet-avy", "database_clients.db"), check_same_thread=False)
c = st.session_state["connection"].cursor()

try:
    c.execute("ALTER TABLE users ADD COLUMN derniere_connexion TEXT;")
except Exception:
    pass
try:
    c.execute("ALTER TABLE users ADD COLUMN date_inscription TEXT;")
except Exception:
    pass
st.session_state["connection"].commit()

def connexion():

    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        login_button = st.form_submit_button("Se connecter")
        if login_button:
            # Vérifier si l'utilisateur existe et si le mot de passe est correct
            c.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            result = c.fetchone()

            if result:
                # Met à jour la date de dernière connexion
                c.execute("UPDATE users SET derniere_connexion = ? WHERE username = ?", (datetime.now().isoformat(), username))
                st.session_state["connection"].commit()
                st.success(f"✅ Connexion réussie ! Bienvenue, {username} 🎉")
                sleep(2)
                st.session_state["username"] = username
                st.session_state["just_logged_in"] = True  # Pour affichage sur la page reco
                st.session_state["page"] = "Recommandation"
                st.rerun()
                # Ici tu peux afficher du contenu réservé ou rediriger vers une autre page
            else:
                st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")
