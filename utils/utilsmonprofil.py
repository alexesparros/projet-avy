import streamlit as st
import sqlite3
import pandas as pd
import os
from utils.plotting import plot_radar

def afficher_mon_profil():
    # 1. Vérification de connexion utilisateur
    if "username" not in st.session_state:
        st.warning("Merci de vous connecter pour accéder à votre profil.")
        return

    username = st.session_state["username"]

    # 2. Connexion base utilisateur
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath("database_clients.db")))
    db_path = os.path.join(base_dir, "projet-avy", "database_clients.db")
    if not os.path.exists(db_path):
        st.error(f"Base de données introuvable : {db_path}")
        return
    conn_user = sqlite3.connect(db_path)
    cur_user = conn_user.cursor()
    cur_user.execute("SELECT id, email, date_inscription, derniere_connexion FROM users WHERE username = ?", (username,))
    row = cur_user.fetchone()

    if not row:
        st.error("Utilisateur introuvable.")
        return

    id_user, email, date_inscription, derniere_connexion = row

    # 3. Connexion base profil
    db_profil_path = os.path.join("projet-avy", "database_clients.db")
    os.makedirs(os.path.dirname(db_profil_path), exist_ok=True)
    conn_profil = sqlite3.connect(db_profil_path)
    cur_profil = conn_profil.cursor()
    cur_profil.execute("""
        CREATE TABLE IF NOT EXISTS mon_profil (
            id_user INTEGER PRIMARY KEY,
            pseudo TEXT,
            avatar TEXT,
            type_joueur TEXT
        )
    """)
    cur_profil.execute("SELECT pseudo, avatar, type_joueur FROM mon_profil WHERE id_user = ?", (id_user,))
    profil_data = cur_profil.fetchone()

    # 4. Affichage UI profil
    st.title("👤 Mon Profil")
    col1, col2 = st.columns([1, 5])
    avatars = ["🙂", "🎮", "🐱", "🐉", "👾", "🧙‍♂️"]
    avatar = col1.selectbox("Avatar", avatars, index=avatars.index(profil_data[1]) if profil_data else 0)
    pseudo = col2.text_input("Pseudo", profil_data[0] if profil_data else username)

    st.markdown(f"📧 **Email** : `{email}`")
    if date_inscription:
        st.markdown(f"🗓️ **Inscription** : {date_inscription[:10]}")
    if derniere_connexion:
        st.markdown(f"⏰ **Dernière connexion** : {derniere_connexion.replace('T', ' ')[:16]}")

    type_joueur = st.radio("🧠 Type de joueur", ["Occasionnel", "Régulier", "Passionné", "Hardcore"],
                           index=["Occasionnel", "Régulier", "Passionné", "Hardcore"].index(profil_data[2]) if profil_data else 0)

    # 5. Historique jeux favoris (depuis la base, plus de CSV)
    st.subheader("🎮 Mes jeux favoris")
    profil_gamer_path = os.path.join("projet-avy", "database_clients.db")
    try:
        conn_fav = sqlite3.connect(profil_gamer_path)
        c = conn_fav.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS jeux_recommandes (
                username TEXT,
                nom_jeu TEXT,
                description TEXT,
                note TEXT,
                critique TEXT,
                date_ajout TEXT
            )
        ''')
        conn_fav.commit()
        df_fav = pd.read_sql_query(
            "SELECT nom_jeu, note, date_ajout FROM jeux_recommandes WHERE username = ? ORDER BY date_ajout DESC",
            conn_fav, params=(username,)
        )
        conn_fav.close()
        if not df_fav.empty:
            for i, row in df_fav.iterrows():
                c1, c2 = st.columns([5, 1])
                c1.markdown(f"- {row['nom_jeu']} ({row['note']}/10)")
                if c2.button("🗑️ Retirer", key=f"deletefav{username}_{i}"):
                    conn_del = sqlite3.connect(profil_gamer_path)
                    c_del = conn_del.cursor()
                    c_del.execute(
                        "DELETE FROM jeux_recommandes WHERE username = ? AND nom_jeu = ? AND date_ajout = ?",
                        (username, row['nom_jeu'], row['date_ajout'])
                    )
                    conn_del.commit()
                    conn_del.close()
                    st.rerun()
        else:
            st.info("Aucun favori pour l’instant.")
    except Exception as e:
        st.error(f"Erreur jeux favoris : {e}")

    with st.form("ajouter_jeu"):
        nom = st.text_input("Nom du jeu")
        note = st.slider("Note", 1, 10, 7)
        if st.form_submit_button("Ajouter"):
            df = pd.concat([df, pd.DataFrame([{"nom": nom, "note": note}])], ignore_index=True)
            df.to_csv(path_csv, index=False)
            st.success(f"{nom} ajouté à tes favoris.")
            st.rerun()

    # 6. Radar chart depuis la base profil_gamer.db
    st.subheader("📊 Mon profil de joueur")
    try:
        radar_db_path = os.path.join("projet-avy", "database_clients.db")
        conn_radar = sqlite3.connect(radar_db_path)
        c = conn_radar.cursor()
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
        conn_radar.commit()
        df_radar = pd.read_sql_query("""
            SELECT competition, narration, exploration, creativite, detente, social, immersion, curiosite
            FROM reponses
            WHERE username = ?
            ORDER BY timestamp DESC LIMIT 1
        """, conn_radar, params=(username,))
        conn_radar.close()

        if not df_radar.empty:
            fig = plot_radar(df_radar.columns.tolist(), df_radar.iloc[0].tolist(), username)
            st.pyplot(fig)
        else:
            st.info("Tu n’as pas encore répondu au questionnaire.")
    except Exception as e:
        st.error(f"Erreur radar : {e}")

    # 5bis. Affichage des jeux recommandés IA (table jeux_recommandes)
    st.subheader("✨ Mes favoris")
    profil_gamer_path = os.path.join("projet-avy", "database_clients.db")
    try:
        conn_reco = sqlite3.connect(profil_gamer_path)
        c = conn_reco.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS jeux_recommandes (
                username TEXT PRIMARY KEY,
                nom_jeu TEXT,
                description TEXT,
                note TEXT,
                critique TEXT,
                date_ajout TEXT
            )
        ''')
        conn_reco.commit()
        df_reco = pd.read_sql_query(
            "SELECT nom_jeu, description, note, critique, date_ajout FROM jeux_recommandes WHERE username = ? ORDER BY date_ajout DESC",
            conn_reco, params=(username,)
        )
        conn_reco.close()
        if not df_reco.empty:
            for i, row in df_reco.iterrows():
                c1, c2 = st.columns([5, 1])
                c1.markdown(f"**{row['nom_jeu']}** — {row['note']}<br/>{row['description']}<br/><i>{row['critique']}</i>", unsafe_allow_html=True)
                if c2.button("🗑️ Retirer", key=f"delete_reco_{username}_{i}"):
                    conn_reco_del = sqlite3.connect(profil_gamer_path)
                    c_del = conn_reco_del.cursor()
                    c_del.execute(
                        "DELETE FROM jeux_recommandes WHERE username = ? AND nom_jeu = ? AND date_ajout = ?",
                        (username, row['nom_jeu'], row['date_ajout'])
                    )
                    conn_reco_del.commit()
                    conn_reco_del.close()
                    st.rerun()
        else:
            st.info("Aucun jeu dans mes favoris.")
    except Exception as e:
        st.error(f"Erreur jeux recommandés : {e}")

    # 7. Sauvegarde du profil
    if st.button("💾 Sauvegarder mon profil"):
        if profil_data:
            cur_profil.execute("UPDATE mon_profil SET pseudo = ?, avatar = ?, type_joueur = ? WHERE id_user = ?",
                               (pseudo, avatar, type_joueur, id_user))
        else:
            cur_profil.execute("INSERT INTO mon_profil (id_user, pseudo, avatar, type_joueur) VALUES (?, ?, ?, ?)",
                               (id_user, pseudo, avatar, type_joueur))
        conn_profil.commit()
        st.success("Profil mis à jour !")

    # 8. Déconnexion
    if st.button("🔓 Se déconnecter"):
        st.session_state.clear()
        st.rerun()

    conn_user.close()
    conn_profil.close()
