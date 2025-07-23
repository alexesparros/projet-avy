import streamlit as st
<<<<<<< HEAD
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
=======
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
>>>>>>> 156dd6839024693ecdf72da4780ba6498b37b0da
