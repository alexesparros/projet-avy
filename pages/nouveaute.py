import streamlit as st
import requests
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
        st.error("Aucun jeu trouvé cette semaine via RAWG.")
        st.stop()


    for idx, game in enumerate(games):
        name = game.get("name", "Jeu inconnu")
        img_url = game.get("background_image", None)
        platforms = ", ".join([plat["platform"]["name"] for plat in game.get("platforms", [])]) if "platforms" in game else "?"
        genres = ", ".join([genre["name"] for genre in game.get("genres", [])]) if "genres" in game else "?"

        # Prompt personnalisé PAR jeu
        prompt = (
            f"Tu es un expert du jeu vidéo. Présente '{name}' avec : "
            f"une description fun (2 à 5 lignes, ambiance, gameplay, humour), "
            f"la plateforme principale (si tu sais), le genre (si tu sais), "
            f"et une phrase d’accroche originale pour gamer. Sois aéré et complice."
        )
            # f"""Tu es un expert du jeu vidéo. je vais te présenter une liste de jeux
            # on role est de me fournir une description fun (2 à 5 lignes, ambiance, gameplay, humour) pour chaque jeu "
            # a plateforme principale (si tu sais), le genre (si tu sais), "
            # et une phrase d’accroche originale pour gamer. Sois aéré et complice."
            # Voici un exemple de ce que tu dois me renvoyer :
            # {"jeu1": "nomjeu", "short_des":"....","plateforme":"pc","genres":[aventure,action],"accroche:"accroche",
            # "jeu2"...}
            # Voici les deux jeux pour lesquels tu dois me renvoyer UNIQUEMENT le json
            # ratchet & clank 2, hogwarts legacy, inscryption
            # """
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            st.write("DEBUT")
            response = model.generate_content(prompt)
            st.write("FIN")
            description = response.text
        except Exception as e:
            description = f"Impossible d'obtenir la description Gemini. Erreur : {e}"

        with st.container():
            st.markdown(f"<div style='font-size:1.3em;font-weight:bold;'>{idx+1}. {name}</div>", unsafe_allow_html=True)
            if img_url:
                st.image(img_url, use_container_width=True)
            st.markdown(f"**Plateformes RAWG** : {platforms}")
            st.markdown(f"**Genres RAWG** : {genres}")
            st.markdown(description)
            st.markdown("---")
