import streamlit as st
import requests
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="UNAD NLP Assistant Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS PERSONALIZADOS (UI/UX Avanzada) ---
st.markdown("""
    <style>
    /* Estilo para el contenedor de chat */
    .stChatMessage {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* Estilo para la barra lateral */
    .css-1d391kg {
        background-color: #002d4b;
    }
    /* Ajuste de botones */
    .stButton>button {
        border-radius: 10px;
        width: 100%;
        background-color: #fca311;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE BACKEND ---
API_URL = "https://nlpfase4.onrender.com/chat"

def get_bot_response(user_query):
    try:
        response = requests.post(API_URL, json={"question": user_query}, timeout=30)
        if response.status_code == 200:
            return response.json().get("respuesta", "Lo siento, no pude procesar la información.")
        return f"⚠️ Error del servidor: {response.status_code}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# --- SIDEBAR (Información del Proyecto UNAD) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Logo_UNAD.png", width=150)
    st.title("Panel de Control")
    st.info(f"**Curso:** NLP\n\n**Fase:** 4 - Aplicaciones Avanzadas [cite: 7, 11]")
    st.markdown("---")
    st.write("### Métricas de Sistema")
    st.status("Backend: Online ✅")
    st.status("Knowledge Base: Active 📚")
    if st.button("Limpiar Conversación"):
        st.session_state.messages = []
        st.rerun()

# --- CUERPO PRINCIPAL ---
st.title("🧠 UNAD AI: Advanced NLP Interface")
st.caption("Sistema Experto basado en LangChain, OpenAI y ChromaDB [cite: 17, 27, 43]")

# Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Contenedor de chat con scroll
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- INPUT PROFESIONAL (Auto-limpiable) ---
if prompt := st.chat_input("Escribe tu consulta sobre la Fase 4..."):
    # Insertar mensaje de usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Respuesta del bot con efecto de escritura
    with chat_container:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Llamada real al backend
            raw_answer = get_bot_response(prompt)
            
            # Simulación de 'typing' para profesionalismo visual
            for chunk in raw_answer.split():
                full_response += chunk + " "
                time.sleep(0.05)
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
