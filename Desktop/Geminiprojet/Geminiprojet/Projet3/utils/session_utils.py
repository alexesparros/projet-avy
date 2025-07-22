import streamlit as st

def init_session_key(key, default=None):
    if key not in st.session_state:
        st.session_state[key] = default

# Ajoute ici les fonctions :
# - vérification de connexion
# - initialisation username, etc. 