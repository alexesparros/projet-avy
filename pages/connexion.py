import streamlit as st
import sqlite3
from time import sleep


# Connexion à la base de données
st.session_state["connection"] = sqlite3.connect("database_clients", check_same_thread=False)
c = st.session_state["connection"].cursor()

def connexion():

    st.title("Connecte-toi")

    # Formulaire de connexion
    with st.form("login_form"):
        username = st.text_input("Pseudo")
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
            st.success(f"✅ Bienvenue, {username} ! 🎉")
            sleep(1)
            st.session_state["username"] = username
            st.session_state["page"] = "Recommandation"
            st.rerun()
            # Ici tu peux afficher du contenu réservé ou rediriger vers une autre page
        else:
            st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")
