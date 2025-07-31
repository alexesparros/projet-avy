import streamlit as st
import sqlite3
from time import sleep
import os
from datetime import datetime

def connexion():
    # Initialiser la connexion à la base de données si elle n'existe pas déjà
    if "connection" not in st.session_state:
        try:
            db_path = os.path.join("projet-avy", "database_clients.db")
            st.session_state["connection"] = sqlite3.connect(db_path, check_same_thread=False)
        except Exception as e:
            st.error(f"Erreur de connexion à la base de données : {e}")
            return
    
    try:
        c = st.session_state["connection"].cursor()
        
        # Ajouter les colonnes si elles n'existent pas
        try:
            c.execute("ALTER TABLE users ADD COLUMN derniere_connexion TEXT;")
        except Exception:
            pass
        try:
            c.execute("ALTER TABLE users ADD COLUMN date_inscription TEXT;")
        except Exception:
            pass
        st.session_state["connection"].commit()
        
    except Exception as e:
        st.error(f"Erreur lors de l'initialisation de la base de données : {e}")
        return

    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        login_button = st.form_submit_button("Se connecter")
        
        if login_button:
            try:
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
                else:
                    st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")
                    
            except Exception as e:
                st.error(f"Erreur lors de la connexion : {e}")
