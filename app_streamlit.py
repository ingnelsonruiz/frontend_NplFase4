import streamlit as st
import requests
import time

# --- CONFIGURACIÓN ESTÉTICA DE ALTO NIVEL ---
st.set_page_config(
    page_title="UNAD NLP Assistant Pro",
    page_icon="🧠",
    layout="wide"
)

# Estilo CSS Avanzado: Corrección de color de texto en Sidebar y estética Pro
st.markdown("""
    <style>
    /* Fondo principal */
    .main { background-color: #f8f9fa; }
    
    /* Burbujas de chat */
    .stChatMessage { border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e9ecef; }
    
    /* Configuración de la Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(#002d4b, #005691);
        color: white !important;
    }
    
    /* Forzar color blanco en todos los textos de la Sidebar */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Estilo para el contenedor de información en la Sidebar */
    .info-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 10px;
    }

    .stChatInput { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: IDENTIFICACIÓN INSTITUCIONAL ---
with st.sidebar:
    # Logo Institucional UNAD
    st.image("Logo_unad_color.png", use_container_width=True)
    
    st.markdown("### 🎓 Identificación del Proyecto")
    
    # Contenedor con texto forzado en blanco para máxima legibilidad
    st.markdown(f"""
    <div class="info-box">
        <p style="margin:0;"><strong>Fase 4:</strong> Fundamentals of NLP</p>
        <p style="margin:0;"><strong>Estudiante:</strong> Nelson Javier Ruiz Lozano</p>
        <p style="margin:0;"><strong>Tutor:</strong> Andrés Felipe Hernández Giraldo</p>
        <p style="margin:0;"><strong>Curso:</strong> Natural Language Processing</p>
        <p style="margin:0;"><strong>Código:</strong> 203238430</p>
        <p style="margin:0;"><strong>Programa:</strong> Maestría en Ciencia de Datos y Analítica</p>
        <p style="margin:0;"><strong>Institución:</strong> UNAD - ECBTI</p>
        <p style="margin:0;"><strong>Fecha:</strong> Diciembre – 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("### 🛠️ Control de Sesión")
    if st.button("🗑️ Limpiar Memoria de Chat"):
        st.session_state.messages = []
        st.rerun()

# --- CUERPO PRINCIPAL ---

# Logo de Ciencia de Datos arriba del título (La Cereza del Pastel)
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
                    raw_answer = response.json().get("respuesta", "Lo siento, no pude encontrar una respuesta precisa.")
                    
                    # Efecto de escritura (Typing effect) profesional
                    full_response = ""
                    message_placeholder = st.empty()
                    status_msg.empty() 
                    
                    for chunk in raw_answer.split():
                        full_response += chunk + " "
                        time.sleep(0.04) 
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                else:
                    full_response = "⚠️ Error de comunicación: El backend no respondió correctamente."
                    st.error(full_response)
            
            except Exception as e:
                full_response = f"❌ Error de red: No se pudo conectar con la API ({str(e)})"
                st.error(full_response)

    # 3. Guardar en el historial
    st.session_state.messages.append({"role": "assistant", "content": full_response})
