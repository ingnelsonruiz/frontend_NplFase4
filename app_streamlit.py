import streamlit as st
import requests
import time

# --- CONFIGURACIÓN ESTÉTICA DE ALTO NIVEL ---
st.set_page_config(
    page_title="UNAD NLP Assistant Pro",
    page_icon="🧠",
    layout="wide"
)

# Estilo CSS Avanzado para estética de Dashboard Profesional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e9ecef; }
    [data-testid="stSidebar"] { background-image: linear-gradient(#002d4b, #005691); color: white; }
    .stChatInput { border-radius: 10px; }
    .header-logo { display: block; margin-left: auto; margin-right: auto; width: 25%; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: IDENTIFICACIÓN INSTITUCIONAL ---
with st.sidebar:
    # Logo Institucional UNAD
    st.image("Logo_unad_color.png", use_container_width=True)
    
    st.markdown("### 🎓 Identificación del Proyecto")
    st.info(f"""
    **Fase 4:** Fundamentals of Natural Language Processing
    
    **Estudiante:** Nelson Javier Ruiz Lozano
    
    **Tutor:** Andrés Felipe Hernández Giraldo
    
    **Curso:** Natural Language Processing
    **Código:** 203238430 
    
    **Programa:**
    Maestría en Ciencia de Datos y Analítica
    
    **Institución:**
    UNAD - ECBTI
    
    **Fecha:** Diciembre – 2025
    """)
    
    st.markdown("---")
    st.write("### 🛠️ Control de Sesión")
    if st.button("🗑️ Limpiar Memoria de Chat"):
        st.session_state.messages = []
        st.rerun()

# --- CUERPO PRINCIPAL ---

# La "Cereza del Pastel": Logo de Ciencia de Datos arriba del título
col_left, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    st.image("logo_datos.png", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>🧠 Advanced NLP Interface</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Sistema RAG (Retrieval-Augmented Generation) optimizado para Ciencia de Datos</p>", unsafe_allow_html=True)

# URL de tu API en Render
API_URL = "https://nlpfase4.onrender.com/chat"

# Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Contenedor dinámico para el chat
chat_placeholder = st.container()

with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- INPUT PROFESIONAL (Auto-limpiable) ---
if prompt := st.chat_input("Consulte aquí información sobre la Fase 4 o conceptos de NLP..."):
    
    # 1. Mostrar mensaje del usuario inmediatamente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    # 2. Generar respuesta del Asistente
    with chat_placeholder:
        with st.chat_message("assistant"):
            status_msg = st.empty()
            status_msg.markdown("🔎 *Consultando base de conocimientos vectorial (ChromaDB)...*")
            
            try:
                # Petición al Backend en Render
                response = requests.post(API_URL, json={"question": prompt})
                
                if response.status_code == 200:
                    raw_answer = response.json().get("respuesta", "Lo siento, no pude encontrar una respuesta precisa en la base de datos.")
                    
                    # Efecto de escritura (Typing effect)
                    full_response = ""
                    message_placeholder = st.empty()
                    status_msg.empty() 
                    
                    for chunk in raw_answer.split():
                        full_response += chunk + " "
                        time.sleep(0.04) # Velocidad de escritura profesional
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                else:
                    full_response = "⚠️ Error de comunicación: El backend en Render no respondió correctamente."
                    st.error(full_response)
            
            except Exception as e:
                full_response = f"❌ Error de red: No se pudo conectar con la API ({str(e)})"
                st.error(full_response)

    # 3. Guardar en el historial para persistencia de la sesión
    st.session_state.messages.append({"role": "assistant", "content": full_response})
