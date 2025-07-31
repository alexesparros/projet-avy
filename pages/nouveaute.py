import streamlit as st
import requests
from datetime import datetime, timedelta
from keys import RAWG_API_KEY
from utils.helpers import traduire_texte

def nouveaute():

    today = datetime.today()
    start_date = (today - timedelta(days=14)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    RAWG_URL = (
        f"https://api.rawg.io/api/games"
        f"?dates={start_date},{end_date}&ordering=-released&page_size=7"
        f"&key={RAWG_API_KEY}&lang=fr"
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
        st.markdown(f"## {game.get('name', 'Jeu inconnu')}")
        # Récupérer plus d'infos via /games/{id} en français
        game_id = game.get('id')
        details = None
        if game_id:
            detail_url = f"https://api.rawg.io/api/games/{game_id}?key={RAWG_API_KEY}&lang=fr"
            detail_resp = requests.get(detail_url)
            if detail_resp.status_code == 200:
                details = detail_resp.json()
        # Déterminer le lien cible (site officiel ou fiche RAWG)
        site_officiel = details.get('website') if details else None
        rawg_url = f"https://rawg.io/games/{game.get('slug')}" if game.get('slug') else None
        lien_jeu = site_officiel if site_officiel else rawg_url
        # Image cliquable
        if game.get("background_image") and lien_jeu:
            st.markdown(f"<a href='{lien_jeu}' target='_blank'><img src='{game['background_image']}' width='400' style='border-radius:1em;box-shadow:0 2px 16px #0002;'/></a>", unsafe_allow_html=True)
        elif game.get("background_image"):
            st.image(game["background_image"], width=400)
        st.write(f"**Date de sortie :** {game.get('released', 'N/A')}")
        # Badges plateformes
        plateformes = [plat["platform"]["name"] for plat in game.get("platforms", [])]
        if plateformes:
            st.markdown("<span style='font-weight:600'>Plateformes :</span> " + " ".join([
                f"<span style='background:#e0e7ff;color:#2d3a6b;padding:0.3em 0.8em;border-radius:1em;margin-right:0.3em;font-size:0.95em'>{p}</span>" for p in plateformes
            ]), unsafe_allow_html=True)
        # Badges genres
        genres = [genre["name"] for genre in game.get("genres", [])]
        if genres:
            st.markdown("<span style='font-weight:600'>Genres :</span> " + " ".join([
                f"<span style='background:#ffe0e0;color:#a12d2d;padding:0.3em 0.8em;border-radius:1em;margin-right:0.3em;font-size:0.95em'>{g}</span>" for g in genres
            ]), unsafe_allow_html=True)
            
        if details:
            desc = details.get('description_raw', '')
            if desc:
                desc_fr = traduire_texte(desc)
                st.markdown(f"**Description (FR) :** {desc_fr[:400]}{'...' if len(desc_fr)>400 else ''}")
            devs = ", ".join([d['name'] for d in details.get('developers', [])])
            pubs = ", ".join([p['name'] for p in details.get('publishers', [])])
            st.write(f"**Développeur(s) :** {devs if devs else 'N/A'}")
            st.write(f"**Éditeur(s) :** {pubs if pubs else 'N/A'}")
            tags = ", ".join([t['name'] for t in details.get('tags', [])[:5]])
            st.write(f"**Tags :** {tags if tags else 'N/A'}")
            if details.get('website'):
                st.write(f"[Site officiel]({details['website']})")
            # Screenshots
            screenshots = details.get('short_screenshots', [])
            if screenshots:
                st.write("**Screenshots :**")
                for sc in screenshots[:3]:
                    st.image(sc['image'], width=250)
        st.markdown("---")