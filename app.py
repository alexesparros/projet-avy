import streamlit as st
from pages.accueil import accueil
from pages.questionnaire import questionnaire
from pages.reco_ia import reco_ia
from pages.nouveaute import nouveaute
from pages.chatbot import chatbot
from pages.mon_compte import mon_compte
from pages.mon_profil import mon_profil

pages = [
    st.Page(accueil, icon=":material/home:", title="Accueil"),
    st.Page(reco_ia, icon=":material/person_celebrate:", title="Recommandation"),
    st.Page(nouveaute, icon=":material/fiber_new:", title="Nouveautés"),
    st.Page(questionnaire, icon=":material/psychology_alt:", title="Questionnaire"),
    st.Page(chatbot, icon=":material/robot_2:", title="Chatbot"),
    st.Page(mon_compte, icon=":material/for_you:", title="Mon Compte")
]

if "username" in st.session_state:
    pages.append(st.Page(mon_profil, icon=":material/person:", title="Mon Profil"))

current_page = st.navigation(pages=pages, position="hidden")

st.set_page_config(layout="wide")

num_cols = max(len(pages) + 1, 8)

columns = st.columns(num_cols, vertical_alignment="bottom")

# Affiche le nom d'utilisateur connecté ou 'Ludrun' par défaut
if "username" in st.session_state:
    columns[0].write(f"👤 {st.session_state['username']}")
    if columns[0].button("Se déconnecter", key="logout_btn"):
        del st.session_state["username"]
        st.rerun()
else:
    columns[0].write("Ludrun")

for col, page in zip(columns[1:], pages):
    col.page_link(page, icon=page.icon)

st.title(f"{current_page.icon}")

current_page.run()
