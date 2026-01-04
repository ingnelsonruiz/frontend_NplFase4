import streamlit as st
import requests
import time

# --- CONFIGURACIÓN ESTÉTICA DE ALTO NIVEL ---
st.set_page_config(
    page_title="UNAD NLP Assistant Pro",
    page_icon="🧠",
    layout="wide"
)

# Estilo CSS para profesionalismo visual (Modo Moderno)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stChatMessage { border-radius: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#052b5e); color: white; }
    div[data-testid="stExpander"] { border: none; box-shadow: none; background-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: IDENTIFICACIÓN INSTITUCIONAL (Tu Información) ---
with st.sidebar:
    # Logo de la UNAD (Usando el archivo que tienes en GitHub)
    st.image("Logo_unad_color.png", use_container_width=True)
    
    st.markdown("### 🎓 Identificación del Proyecto")
    st.info(f"""
    **Fase 4:** Fundamentals of Natural Language Processing [cite: 6, 7]
    
    **Estudiante:** Nelson Javier Ruiz Lozano
    
    **Tutor:** Andrés Felipe Hernández Giraldo
    
    **Curso:** Natural Language Processing [cite: 7]
    **Código:** 203238430 
    
    **Programa:**
    Maestría en Ciencia de Datos y Analítica
    
    **Institución:**
    UNAD - ECBTI [cite: 4, 11]
    
    **Fecha:** Diciembre – 2025
    """)
    
    st.markdown("---")
    if st.button("🗑️ Limpiar Memoria de Chat"):
        st.session_state.messages = []
        st.rerun()

# --- CUERPO PRINCIPAL ---
st.title("🧠 Advanced NLP Interface")
st.write("Sistema RAG con recuperación de información en tiempo real.")

# URL de tu API en Render
API_URL = "https://nlpfase4.onrender.com/chat"

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Contenedor para el historial de chat
chat_placeholder = st.container()

with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- INPUT PROFESIONAL (Auto-limpiable y con Botón de Envío) ---
# st.chat_input ya incluye el botón de envío y limpia el texto automáticamente
if prompt := st.chat_input("Escribe aquí tu consulta técnica..."):
    
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Respuesta del bot con efecto de "escritura"
    with chat_placeholder:
        with st.chat_message("assistant"):
            status_msg = st.empty()
            status_msg.markdown("🔎 *Consultando base de conocimientos local...*")
            
            try:
                # Petición a tu API en Render
                response = requests.post(API_URL, json={"question": prompt})
                
                if response.status_code == 200:
                    raw_answer = response.json().get("respuesta", "Sin respuesta.")
                    
                    # Efecto de typing para mayor profesionalismo
                    full_response = ""
                    message_placeholder = st.empty()
                    status_msg.empty() # Quitamos el mensaje de "consultando"
                    
                    for chunk in raw_answer.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                else:
                    full_response = "⚠️ Error de comunicación con el Backend de Render."
                    st.error(full_response)
            
            except Exception as e:
                full_response = f"❌ Error de conexión: {str(e)}"
                st.error(full_response)

    # Guardar en el historial
    st.session_state.messages.append({"role": "assistant", "content": full_response})
