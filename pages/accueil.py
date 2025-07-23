import streamlit as st
from PIL import Image
import time

def accueil():
    _, col2, _ = st.columns([3, 3, 3])
    with col2:
        st.image("images/ludrun.png", width=1000)
        st.markdown("<h2 style='text-align:center;font-size:1.75em'>Le QG des gamers indécis</h2>", unsafe_allow_html=True)
    
    st.markdown("""Trois amis, une passion dévorante pour les jeux vidéo… et trop de soirées à se demander "On joue à quoi ce soir ?". C’est comme ça qu’est né ce site : un outil de recommandation de jeux fait par des gamers, pour les gamers (et pour tous ceux qui passent plus de temps à scroller leur bibliothèque qu'à jouer).
    Notre mission ? Vous aider à trouver le bon jeu plus vite que votre pote ne ragequit. FPS, RPG, jeux indé ou simulateur de chèvre… Il y en a pour tous les goûts (même les plus chelous).
    Allez, faites comme chez vous. Et surtout : ne blamez pas le site si vous devenez accro 😄
    """)

    st.markdown("## Le projet")
    st.write("Ce projet a été réalisé dans le cadre de notre formation en Data Analysis. Il s'articule autour de plusieurs composantes :")

    # Ligne 1 : Questionnaire & Visualisation
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/questionnaire.png", width=150)
        st.markdown("""**Questionnaire ludique**  
        Dressez votre **profil de joueur** à travers quelques questions funs et rapides.""")
    with col2:
        st.image("images/visualisation.png", width=150)
        st.markdown("""**Visualisation interactive**  
        Explorez vos préférences grâce à un **radar chart dynamique**.""")

    # Ligne 2 : IA & Base de données
    col3, col4 = st.columns(2)
    with col3:
        st.image("images/IA.png", width=150)
        st.markdown("""**Moteur de recommandation**  
        Une **IA** qui vous propose des jeux adaptés à votre style.""")
    with col4:
        st.image("images/stockage.png", width=150)
        st.markdown("""**Stockage structuré**  
        Sauvegarde de vos choix dans une **base SQLite**, parce qu’on aime les données bien rangées.""")



    st.markdown("---")

    st.markdown("""
    ## Nos ambitions
    - Créer une interface accessible et fun
    - Utiliser des techniques de machine learning pour affiner la recommandation
    - Pousser l’analyse de données sur les comportements des joueurs

    """)


    st.markdown("---")
    _, col2, _ = st.columns([2, 4, 1])
    with col2:
        st.markdown("📫 **Contactez-nous** : si vous voulez en savoir plus ou tester nos modèles 👉 [ludrun.contact@gmail.com](mailto:ludrun.contact@gmail.com)")

        st.markdown("📍 **Projet réalisé à Toulouse** — Wild Code School — Juillet 2025")
    _, col2, _ = st.columns([7, 2, 7])
    with col2:
        try:
            logo = Image.open("images/ludrun.png").convert("RGBA")
        except FileNotFoundError:
            st.error("❌ L'image 'ludrun.png' est introuvable.")
            return

        imgslot = st.empty()  # zone d'affichage dynamique
        angles = list(range(0, 360, 15))
        delay = 0.2

        for _ in range(2):
            for angle in angles:
                rotated = logo.rotate(angle, resample=Image.BICUBIC, expand=True)
                resized = rotated.resize((300, 300), Image.LANCZOS)
                imgslot.image(resized)
                time.sleep(delay)

        imgslot.image(logo.resize((300, 300), Image.LANCZOS))

if __name__ == "__main__":
    main()
