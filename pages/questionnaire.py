import streamlit as st
import pandas as pd
from utils.data_loader import init_db_profil, enregistrer_ou_mettre_a_jour_profil
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from datetime import datetime
import os

def questionnaire():
    # 🔧 Initialiser la base SQLite avec username unique
    def init_db():
        db_path = os.path.join("projet-avy", "database_clients.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS reponses (
        username TEXT PRIMARY KEY,
        timestamp TEXT,
        annee_jeu INTEGER,
        type_joueur TEXT,
        budget_mensuel INTEGER,
        jeu_marquant TEXT,
        critere_ia TEXT,
        competition INTEGER,
        narration INTEGER,
        exploration INTEGER,
        creativite INTEGER,
        detente INTEGER,
        social INTEGER,
        immersion INTEGER,
        curiosite INTEGER
        )
        ''')
        conn.commit()
        conn.close()

    # 🔄 Enregistrement intelligent (INSERT ou UPDATE)
    def enregistrer_ou_mettre_a_jour(username, annee_jeu, type_joueur, budget_mensuel, jeu_marquant, critere_ia, profil_scores):
        db_path = os.path.join("projet-avy", "database_clients.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Vérifie si le profil existe déjà
        c.execute("SELECT * FROM reponses WHERE username = ?", (username,))
        exist = c.fetchone()

        if exist:
            # 🔁 Met à jour les réponses existantes
            c.execute('''
            UPDATE reponses SET
                timestamp = ?, annee_jeu = ?, type_joueur = ?, budget_mensuel = ?,
                jeu_marquant = ?, critere_ia = ?,
                competition = ?, narration = ?, exploration = ?, creativite = ?,
                detente = ?, social = ?, immersion = ?, curiosite = ?
            WHERE username = ?
            ''', (
            datetime.now().isoformat(), annee_jeu, type_joueur, budget_mensuel,
            jeu_marquant, critere_ia,
            profil_scores["Compétition"],
            profil_scores["Narration"],
            profil_scores["Exploration"],
            profil_scores["Créativité"],
            profil_scores["Détente"],
            profil_scores["Social"],
            profil_scores["Immersion"],
            profil_scores["Curiosité"],
            username
            ))
        else:
            # ➕ Insère une nouvelle réponse
            c.execute('''
            INSERT INTO reponses (
                username, timestamp, annee_jeu, type_joueur, budget_mensuel,
                jeu_marquant, critere_ia,
                competition, narration, exploration, creativite,
                detente, social, immersion, curiosite
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            username, datetime.now().isoformat(), annee_jeu, type_joueur, budget_mensuel,
            jeu_marquant, critere_ia,
            profil_scores["Compétition"],
            profil_scores["Narration"],
            profil_scores["Exploration"],
            profil_scores["Créativité"],
            profil_scores["Détente"],
            profil_scores["Social"],
            profil_scores["Immersion"],
            profil_scores["Curiosité"]
            ))

        conn.commit()
        conn.close()

    # 🎮 Interface principale

    init_db()

    # 🔐 Vérifie la connexion utilisateur
    if "username" not in st.session_state:
        st.warning("Merci de vous connecter pour accéder au questionnaire.")
        st.stop()

    username = st.session_state["username"]
    st.title(f"🎮 Bienvenue, {username} ! Découvrons ton profil de joueur")
    st.caption("Note chaque affirmation de 0 (pas du tout) à 10 (à fond !)")

    # Questions générales
    st.markdown("### 🔍 Ton profil général")
    q1_years = st.number_input("📅 Depuis combien d'années joues-tu aux jeux vidéo ?", min_value=0, step=1)
    q2_type = st.radio("👤 Tu te considères comme :", [
    "Joueur occasionnel", "Joueur régulier", "Joueur passionné", "Hardcore gamer"
    ])
    q8_budget = st.slider("💸 Quel est ton budget mensuel jeux vidéo (€) ?", 0, 500, 30, step=5)
    q10_impact = st.text_input("🎮 Quel est le dernier jeu qui t’a vraiment marqué ? Pourquoi ?")

    # Sliders du profil radar
    st.markdown("### 🕹️ Tes préférences de jeu")
    profil = {
    "Compétition": st.slider("🏆 J’adore me mesurer aux autres", 0, 10, 5),
    "Narration": st.slider("📖 Une bonne histoire, c’est le plus important", 0, 10, 5),
    "Exploration": st.slider("🧭 Je kiffe explorer de vastes mondes ouverts", 0, 10, 5),
    "Créativité": st.slider("🎨 J’adore construire, personnaliser, créer", 0, 10, 5),
    "Détente": st.slider("🧘 Je joue pour me détendre", 0, 10, 5),
    "Social": st.slider("🎤 Jouer avec d'autres, c'est ma came", 0, 10, 5),
    "Immersion": st.slider("🕶️ Je veux une immersion totale (VR, graphismes, RP...)", 0, 10, 5),
    "Curiosité": st.slider("🔍 J'aime tester des jeux chelous ou originaux", 0, 10, 5),
    }

    # IA
    q20_criteria = st.text_area("🤖 Si une IA devait te recommander **le jeu parfait**, que devrait-elle absolument prendre en compte ?")

    # Résumé
    st.markdown("### 📋 Résumé")
    st.markdown(f"- 👤 **Utilisateur** : `{username}`")
    st.markdown(f"- 🎮 **Années de jeu** : {q1_years}")
    st.markdown(f"- 🕹️ **Type de joueur** : {q2_type}")
    st.markdown(f"- 💸 **Budget mensuel** : {q8_budget} €")
    st.markdown(f"- 🧠 **Jeu marquant** : {q10_impact}")
    st.markdown(f"- 🤖 **Critères IA** : {q20_criteria}")

    df = pd.DataFrame({"Note /10": list(profil.values())}, index=profil.keys())
    st.markdown("### 🎯 Tes notes")
    st.dataframe(df)

    # Bouton d'enregistrement
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("💾 Enregistrer mon profil", type="primary", use_container_width=True):
            # 💾 Sauvegarde BDD
            enregistrer_ou_mettre_a_jour(username, q1_years, q2_type, q8_budget, q10_impact, q20_criteria, profil)
            st.success("✅ Ton profil a bien été enregistré !")
            st.balloons()
            
            # Confirmation de succès
            st.markdown("### 🎮 Ton profil est prêt !")
            st.markdown("✅ Tes données ont été sauvegardées avec succès.")
            st.markdown("💡 Tu peux maintenant aller dans la page **'Mon Profil'** pour voir ton radar chart et tes statistiques.")
