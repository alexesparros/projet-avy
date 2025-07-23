import streamlit as st
from pages.inscription import inscription
from pages.connexion import connexion

def mon_compte():

    # Initialiser l'état
    if "compte_page" not in st.session_state:
        st.session_state["compte_page"] = "menu"

    # ✅ Boutons toujours visibles
    col1, col2 = st.columns(2)
    if col1.button("S'inscrire", use_container_width=True):
        st.session_state["compte_page"] = "inscription"
        st.rerun()
    if col2.button("Se connecter", use_container_width=True):
        st.session_state["compte_page"] = "connexion"
        st.rerun()

    # ✅ Contenu dynamique en dessous
    if st.session_state["compte_page"] == "menu":
        st.info("")
    elif st.session_state["compte_page"] == "inscription":
        inscription()
    elif st.session_state["compte_page"] == "connexion":
        connexion()