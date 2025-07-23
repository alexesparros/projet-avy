import streamlit as st
from pages.accueil import accueil
from pages.questionnaire import questionnaire
from pages.recco_ia import reco_ia
from pages.nouveaute import nouveaute
from pages.chatbot import chatbot
from pages.inscription import inscription
from pages.connexion import connexion

pages = [
    st.Page(accueil, icon=":material/home:", title="Accueil"),
    st.Page(inscription, icon=":material/person_add:", title="Inscription"),
    st.Page(connexion, icon=":material/login:", title="Connexion"),
    st.Page(reco_ia, icon=":material/person_celebrate:", title="Recommandation"),
    st.Page(nouveaute, icon=":material/fiber_new:", title="Nouveautés"),
    st.Page(questionnaire, icon=":material/psychology_alt:", title="Questionnaire"),
    st.Page(chatbot, icon=":material/robot_2:", title="Chatbot")
]

current_page = st.navigation(pages=pages, position="hidden")

st.set_page_config(layout="wide")

num_cols = max(len(pages) + 1, 8)

columns = st.columns(num_cols, vertical_alignment="bottom")

# Affiche le nom d'utilisateur connecté ou 'Ludrun' par défaut
if "username" in st.session_state:
    columns[0].write(f"👤 {st.session_state['username']}")
else:
    columns[0].write("Ludrun")

for col, page in zip(columns[1:], pages):
    col.page_link(page, icon=page.icon)

st.title(f"{current_page.icon}")

current_page.run()