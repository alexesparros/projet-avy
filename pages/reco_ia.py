import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import NotFound
from utils.helpers import img_to_base64
from keys import GEMINI_API_KEY as API_KEY
import re

def reco_ia():

    if "username" not in st.session_state:
        st.warning("Merci de vous connecter pour accéder à la recommandation de jeux.")
        st.stop()

    if st.session_state.get("just_logged_in", False):
        st.success(f"✅ Bienvenue, {st.session_state['username']} ! 🎉")
        st.session_state["just_logged_in"] = False

    if not API_KEY:
        st.error("❌ Clé API Gemini manquante. Renseigne-la dans le code.")
        st.stop()

    genai.configure(api_key=API_KEY)

    st.title(f"🎮 Quels jeux pour {st.session_state['username']} ?")
    st.markdown("""
    Entrez un **nom de jeu**, un **type de jeu** (ex : roguelike, FPS, aventure narrative...) ou une **expérience recherchée** (ex : jeux coopératifs, ambiance relaxante...).
    Vous recevrez 5 suggestions de jeux correspondants, avec une courte description pour chacun.
    """)

    if "reco_requete" not in st.session_state:
        st.session_state["reco_requete"] = ""
    if "reco_resultats" not in st.session_state:
        st.session_state["reco_resultats"] = None

    requete = st.text_input("Votre recherche :", st.session_state["reco_requete"])
    rechercher = st.button("Rechercher")

    if "favoris" not in st.session_state:
        st.session_state["favoris"] = []

    st.sidebar.header("Mes jeux favoris")
    if st.session_state["favoris"]:
        for fav in st.session_state["favoris"]:
            st.sidebar.markdown(f"**{fav['nom']}**")
            if st.sidebar.button(f"Retirer {fav['nom']}", key=f"remove_{fav['nom']}"):
                st.session_state["favoris"] = [
                    f for f in st.session_state["favoris"] if f['nom'] != fav['nom']
                ]
            st.sidebar.markdown("---")
    else:
        st.sidebar.info("Aucun favori pour l’instant.")

    if rechercher:
        if requete.strip() == "":
            st.warning("Veuillez entrer un mot-clé avant de lancer la recherche.")
            st.stop()

        if (
            st.session_state.get("reco_resultats") is None
            or st.session_state.get("reco_requete") != requete
        ):
            st.session_state["reco_requete"] = requete
            with st.spinner("🔎 Votre recommandation est au four..."):
                prompt = (
                    f"Tu es un expert passionné du jeu vidéo, critique reconnu dans la presse spécialisée, "
                    f"mais aussi le pote de soirée qui conseille toujours le bon jeu. "
                    f"Réponds avec expertise, humour, et beaucoup de références. "
                    f"Propose-moi 5 jeux vidéo correspondant à : {requete}. "
                    "Pour chaque jeu, donne :\n"
                    "- Le nom du jeu (en gras),\n"
                    "- Une description fun, immersive, pleine d'anecdotes et de références, d'au moins 5 lignes.\n"
                    "- Une note sur 10 (format : Note : X/10),\n"
                    "- Une mini-critique subjective (2 phrases max, commence par 'Critique :').\n"
                    "Présente la liste de façon bien structurée, numérotée, et aérée. Termine par une phrase bonus drôle ou complice pour gamer, précédée de 'Phrase bonus :'."
                )

                try:
                    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
                    reco_chunks = model.generate_content(prompt, stream=True)

                    recommandations_brutes = ""
                    for chunk in reco_chunks:
                        recommandations_brutes += chunk.text

                    match = re.search(
                        r"Phrase bonus\s*:(.*)$",
                        recommandations_brutes,
                        re.IGNORECASE | re.DOTALL
                    )
                    if match:
                        st.session_state["phrase_humoristique"] = match.group(1).strip()
                        recommandations = recommandations_brutes[:match.start()].strip()
                    else:
                        st.session_state["phrase_humoristique"] = None
                        recommandations = recommandations_brutes

                    st.session_state["reco_resultats"] = recommandations

                except NotFound:
                    st.error("❌ Modèle Gemini introuvable ou non supporté.")
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération : {e}")

        else:
            st.info("✅ Résultat déjà généré pour cette recherche !")

    recommandations = st.session_state["reco_resultats"]
    if recommandations:
        lignes = recommandations.splitlines()
        start_idx = next((i for i, l in enumerate(lignes) if re.match(r"^1\. ", l)), 0)
        lignes = lignes[start_idx:]
        pattern_jeu = re.compile(r"^(\d+)\.\s*(.+)")

        for i, ligne in enumerate(lignes):
            m = pattern_jeu.match(ligne)
            if m:
                idx, nom = m.groups()
                nom_clean = re.sub(r"^[*_`]+|[*_`]+$", "", nom).strip()
                nom_clean = re.sub(r"^Nom\s*[:\-]*\s*", "", nom_clean, flags=re.IGNORECASE)

                with st.container():
                    st.markdown(
                        f"""
                        <div style='
                            background:#23293110;
                            border-radius:1.2em;
                            box-shadow:0 2px 16px #0001;
                            padding:1.2em 1.2em 1em 1.2em;
                            margin-bottom:2.5em;'>
                            <span style='font-size:1.5em;font-weight:bold;color:#87CEFA'>{idx}. {nom_clean}</span>
                        """,
                        unsafe_allow_html=True,
                    )

                    j = i + 1
                    bloc = []
                    while j < len(lignes) and not pattern_jeu.match(lignes[j]) and not lignes[j].strip().startswith('Phrase bonus'):
                        bloc.append(lignes[j])
                        j += 1

                    description = ""
                    note = ""
                    critique = ""
                    for b in bloc:
                        b = b.strip()
                        if b.lower().startswith("note"):
                            note = b
                        elif b.lower().startswith("critique"):
                            critique = b
                        elif b:
                            description += b + " "

                    # Nettoyage pour éviter doublon "Description :"
                    description = re.sub(r'^[Dd]escription\s*:\s*', '', description).strip()

                    st.markdown(
                        f"""
                        <div style='margin-top:0.5em;font-size:1.08em;color:#FAFAFA'>
                            <span style='display:block;margin-bottom:0.4em;'>
                                <strong>Description :</strong><br>
                                {description}
                            </span>
                            <span style='display:block;margin-bottom:0.4em;'>
                                <strong>{note.strip()}</strong>
                            </span>
                            <span style='display:block;margin-top:0.4em;'>
                                <strong>Critique :</strong><br>
                                <em>{critique.replace('Critique :', '').strip()}</em>
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    nom_url = nom_clean.replace(' ', '+')
                    youtube_url = f"https://www.youtube.com/results?search_query={nom_url}+trailer+officiel"
                    google_b64 = img_to_base64("static/google.png")
                    steam_b64 = img_to_base64("static/steam.png")
                    youtube_b64 = img_to_base64("static/youtube.png")

                    html_code = f"""
                        <div style='margin-top:0.5em;'>
                            <a href='https://www.google.com/search?q={nom_url}+jeu+vidéo' target='_blank'>
                                <img src='data:image/png;base64,{google_b64}' alt='Google' style='height:20px; vertical-align:middle;'> Google
                            </a> &nbsp|&nbsp
                            <a href='https://store.steampowered.com/search/?term={nom_url}' target='_blank'>
                                <img src='data:image/png;base64,{steam_b64}' alt='Steam' style='height:20px; vertical-align:middle;'> Steam
                            </a> &nbsp|&nbsp
                            <a href='{youtube_url}' target='_blank'>
                                <img src='data:image/png;base64,{youtube_b64}' alt='YouTube' style='height:20px; vertical-align:middle;'> YouTube Trailer
                            </a>
                        </div>
                    """

                    st.markdown("<div style='height: 1.8em'></div>", unsafe_allow_html=True)
                    if st.button(f"⭐ Ajouter {nom_clean} aux favoris", key=f"fav_{idx}"):
                        if not any(f["nom"] == nom_clean for f in st.session_state["favoris"]):
                            st.session_state["favoris"].append({
                                "nom": nom_clean,
                                "desc": description.strip(),
                                "note": note.strip() if note else None,
                                "critique": critique.strip() if critique else None
                            })
                            # Ajout dans la base database_clients.db (table jeux_recommandes)
                            import sqlite3
                            from datetime import datetime
                            import os
                            db_path = os.path.join("projet-avy", "database_clients.db")
                            conn = sqlite3.connect(db_path)
                            c = conn.cursor()
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
                            c.execute(
                                "INSERT INTO jeux_recommandes (username, nom_jeu, description, note, critique, date_ajout) VALUES (?, ?, ?, ?, ?, ?)",
                                (st.session_state["username"], nom_clean, description.strip(), note.strip(), critique.strip(), datetime.now().isoformat())
                            )
                            conn.commit()
                            conn.close()

                    st.markdown(html_code, unsafe_allow_html=True)

        for ligne in lignes:
            if ligne.strip().lower().startswith('phrase bonus'):
                st.markdown(
                    f"<div style='margin-top:2em;font-size:1.15em;color:#444;font-style:italic;text-align:center;background:#efe6ff;padding:1em 2em;border-radius:1.2em'>{ligne.split(':',1)[-1].strip()}</div>",
                    unsafe_allow_html=True
                )
                break

    st.markdown("<div style='text-align:center;margin-top:40px;color:#aaa;font-size:0.95em'>Propulsé par Gemini. Fait avec ❤️ pour les gamers.</div>", unsafe_allow_html=True) 