import streamlit as st
import pages.connexion as connexion
import pages.inscription as inscription
from pages.accueil import accueil
from pages.questionnaire import questionnaire
from pages.inscription import inscription
from pages.connexion import connexion
from pages.recco_ia import reco_ia
from pages.nouveaute import nouveaute
from pages.chatbot import chatbot

st.set_page_config(layout="wide")

# Barre latérale pour la navigation
st.sidebar.title("Navigation")

# HARDCODE
# st.session_state["page"] = "Recommandation"
# st.session_state["username"] = "Tagalog"
if "page" not in st.session_state:
    st.session_state["page"] = "Accueil"

liste_pages = ["Accueil", "Inscription", "Connexion", "Recommandation","Nouveautés", "Questionnaire", "Chatbot"]

page = st.sidebar.selectbox("Aller à :", liste_pages, index=liste_pages.index(st.session_state["page"]))

# Afficher la page choisie
if page == "Accueil":
    accueil()
elif page == "Inscription":
    inscription()
elif page == "Connexion":
    connexion()
elif page == "Recommandation":
    reco_ia()
elif page == "Nouveautés":
    nouveaute()
elif page == "Questionnaire":
    questionnaire()
elif page == "Chatbot":
    chatbot()
