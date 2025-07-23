import streamlit as st
from pages.inscription import inscription
from pages.connexion import connexion

def mon_compte():

    left, right = st.columns(2)
    if left.button("Inscription", icon=":material/person_add:", use_container_width=True):
        inscription()
    if right.button("Connexion", icon=":material/person_edit:", use_container_width=True):
        connexion()