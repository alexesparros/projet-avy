import streamlit as st

st.title("Test Formulaire Streamlit")

with st.form("test_form"):
    pseudo = st.text_input("Pseudo")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    submit = st.form_submit_button("S'inscrire")
    if submit:
        st.success(f"Formulaire soumis avec pseudo={pseudo}, email={email}")
