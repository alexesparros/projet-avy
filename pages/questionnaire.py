import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from datetime import datetime

def questionnaire():
    # 🔧 Initialiser la base SQLite avec username unique
    def init_db():
        conn = sqlite3.connect("profil_gamer.db")
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
        conn = sqlite3.connect("profil_gamer.db")
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

    st.set_page_config(page_title="Profil de joueur connecté", page_icon="🎮")
    init_db()

    # 🔐 Vérifie la connexion utilisateur
    if "username" not in st.session_state:
        st.warning("🚧 Aucun utilisateur connecté. Définis `st.session_state['username']` avant de répondre.")

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

    # Bouton final
    if st.button("📊 Générer mon profil de joueur"):
        st.success("Voici ton profil radar 🎯")

    # Radar
    categories = list(profil.keys())
    values = list(profil.values())
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_title(f"🧠 Profil de {username}", size=14, pad=20)
    st.pyplot(fig)

    # Résumé
    st.markdown("### 📋 Résumé")
    st.markdown(f"- 👤 **Utilisateur** : `{username}`")
    st.markdown(f"- 🎮 **Années de jeu** : {q1_years}")
    st.markdown(f"- 🕹️ **Type de joueur** : {q2_type}")
    st.markdown(f"- 💸 **Budget mensuel** : {q8_budget} €")
    st.markdown(f"- 🧠 **Jeu marquant** : {q10_impact}")
    st.markdown(f"- 🤖 **Critères IA** : {q20_criteria}")

    df = pd.DataFrame({"Note /10": list(profil.values())}, index=profil.keys())
    st.markdown("### 🎚️ Tes notes")
    st.dataframe(df)

    # 💾 Sauvegarde BDD
    enregistrer_ou_mettre_a_jour(username, q1_years, q2_type, q8_budget, q10_impact, q20_criteria, profil)
    st.success("✅ Ton profil a bien été enregistré ou mis à jour !")
