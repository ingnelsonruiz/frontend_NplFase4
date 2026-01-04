import streamlit as st
import requests

st.title("Chatbot NLP - Fase 4 UNAD")
pregunta = st.text_input("Haz una pregunta sobre la guía:")

if pregunta:
    # Conexión directa a tu API en Render
    response = requests.post("https://nlpfase4.onrender.com/chat", json={"question": pregunta})
    if response.status_code == 200:
        st.write(response.json()["respuesta"])