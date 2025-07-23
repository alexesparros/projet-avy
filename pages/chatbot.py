import streamlit as st
from streamlit_chat import message
import google.generativeai as genai
<<<<<<< HEAD
from keys import GEMINI_API_KEY
=======
>>>>>>> 156dd6839024693ecdf72da4780ba6498b37b0da


def chatbot():

    # Configuration Gemini
<<<<<<< HEAD
    genai.configure(api_key=GEMINI_API_KEY)
=======
    genai.configure(api_key="AIzaSyCvo4ShDeNoDeLnoEII9HgPPP7pGkBjR2o")
>>>>>>> 156dd6839024693ecdf72da4780ba6498b37b0da

    if "history" not in st.session_state:
        st.session_state["history"] = []

    st.title("💬 Chatbot jeux vidéo")

    user_input = st.text_input("Pose ta question :", key="chatbox")

    def get_gemini_response(user_msg):
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        prompt = (
            "Tu es un assistant expert jeux vidéo, fun et accessible, "
            "prêt à répondre à toutes les questions du visiteur (même hors jeux vidéo !)."
            f"\nQuestion : {user_msg}\n"
        )
        response = model.generate_content(prompt)
        return response.text

    if user_input:
        st.session_state["history"].append(("user", user_input))
        bot_answer = get_gemini_response(user_input)
        st.session_state["history"].append(("assistant", bot_answer))

    for role, msg in st.session_state["history"]:
        is_user = role == "user"
        message(msg, is_user=is_user)

    # Message d'accueil
    if not st.session_state["history"]:
        message("👋 Salut ! Je suis ton assistant jeux vidéo (et + si affinités). Demande-moi n'importe quoi : conseils gaming, blagues, actus, tout !", is_user=False)