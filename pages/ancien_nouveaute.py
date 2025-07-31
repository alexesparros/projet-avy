import streamlit as st
import requests
import json
import google.generativeai as genai
from datetime import datetime, timedelta
from keys import GEMINI_API_KEY, RAWG_API_KEY

def nouveaute():

    genai.configure(api_key=GEMINI_API_KEY)

    today = datetime.today()
    start_date = (today - timedelta(days=14)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    RAWG_URL = (
        f"https://api.rawg.io/api/games"
        f"?dates={start_date},{end_date}&ordering=-released&page_size=7"
        f"&key={RAWG_API_KEY}"
    )

    resp = requests.get(RAWG_URL)
    if resp.status_code != 200:
        st.error("Impossible d'accéder à l'API RAWG.")
        st.stop()

    data = resp.json()
    games = data.get("results", [])
    if not games:
        st.error("Aucun jeu trouvé cette semaine.")
        st.stop()

    for idx, game in enumerate(games):
        name = game.get("name", "Jeu inconnu")
        img_url = game.get("background_image", None)
        platforms = ", ".join([plat["platform"]["name"] for plat in game.get("platforms", [])]) if "platforms" in game else "?"
        genres = ", ".join([genre["name"] for genre in game.get("genres", [])]) if "genres" in game else "?"

    #  Construire UN SEUL prompt
    game_names = [game["name"] for game in games]

    prompt = (
        f"""Tu es un expert du jeu vidéo. voici une liste de jeux '{game_names}'"""+"""Pour chaque jeu, génère :
        - une description fun (2 à 5 lignes, ambiance, gameplay, humour)
        - la plateforme principale si tu la devines
        - le genre si tu le devines
        - une phrase d’accroche originale pour gamer. Sois aéré et complice.
        Je veux que tu me renvoies UNIQUEMENT un fichier JSON contenant l'info de chaque jeu.
        Le JSON devra suivre STRICTEMENT ce modèle :
        [{"nom": "nomjeu", "short_des":"....","plateforme":"pc","genres":["aventure","action"],"accroche":"accroche",
        "jeu2":...}]
        """)
    prompt += prompt.join(f"- {name}" for name in game_names)

    # Une seule requête Gemini
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)

    # Parser la réponse JSON
    try:
        reponse_nettoyee = response.text.strip().replace("```json", "").replace("```", "")
        result = json.loads(reponse_nettoyee)
    except json.JSONDecodeError:
        st.error("La réponse n'est pas un JSON valide")
        st.write(response.text)
        st.stop()

    for idx, game in enumerate(result):
        name = game.get("nom", "Jeu inconnu")
        short_des = game.get("short_des", "Jeu inconnu")
        plateforme = game.get("plateforme", "Jeu inconnu")
        genres = game.get("genres", "Jeu inconnu")
        accroche = game.get("accroche", "Jeu inconnu")
        img_url = games[idx].get("background_image", None)

        with st.container():
            st.markdown(f"<div style='font-size:1.3em;font-weight:bold;'>{idx+1}. {name}</div>", unsafe_allow_html=True)
            if img_url:
                st.image(img_url, use_container_width=True)
            st.markdown(short_des)
            st.markdown(f"**Plateforme** : {plateforme}")
            st.markdown(f"**Genres** : {genres}")
            st.markdown(f"*{accroche}*")
            st.markdown("---")