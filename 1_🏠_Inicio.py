import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Atlas Geoquímico",
    page_icon="🏠",
    layout="centered", # Centrado para lectura tipo artículo/móvil
    initial_sidebar_state="expanded"
)

# --- CSS Personalizado (Sidebar y Estilo General) ---
st.markdown("""
<style>
    /* Estilo para el Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22; /* Ligeramente más claro que el fondo principal */
    }
    
    /* Aumentar tamaño de fuente en navegación (Mobile Friendly) */
    .css-1n76uvr, [data-testid="stSidebarNav"] a {
        font-size: 1.2rem !important;
        padding-top: 15px !important;
        padding-bottom: 15px !important;
    }
    
    /* Eliminar espacio blanco superior */
    .css-18e3th9 {
        padding-top: 0rem;
    }
    
    /* Línea divisoria en sidebar */
    [data-testid="stSidebarNav"]::after {
        content: "";
        display: block;
        margin-top: 20px;
        border-bottom: 1px solid #30363D;
    }

    /* Estilo del Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #0E1117;
        color: #8b949e;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
        z-index: 100;
    }
    
    /* Títulos Hero */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #4FC3F7, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #8b949e;
        font-style: italic;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- Contenido Principal (Columna Única) ---

# Hero Section
st.markdown('<h1 class="hero-title">Atlas Geoquímico</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Entendiendo el lenguaje químico de la Tierra</p>', unsafe_allow_html=True)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Blue_Marble_2002.png/640px-Blue_Marble_2002.png", use_container_width=True)

st.markdown("""
<p style="text-align: center; font-style: italic; color: #8b949e;">
"La corteza terrestre no es un museo de protones, es un campo de batalla de cargas y radios." <br>
— Adaptado de V.M. Goldschmidt
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Sección 1: El Dilema del Geólogo
st.header("1. El Dilema del Geólogo")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚫 El Problema")
    st.error("""
    **La Tabla de Mendeleev falla en la naturaleza.**
    
    Agrupa elementos por **electrones de valencia**, lo cual es útil en un laboratorio estéril, pero ignora la realidad del magma y el agua.
    
    *   ¿Por qué el Oro no se disuelve?
    *   ¿Por qué el Uranio se pega al Carbono?
    *   La tabla clásica no tiene respuestas obvias.
    """)

with col2:
    st.markdown("### ✅ La Solución")
    st.success("""
    **El Modelo de Railsback.**
    
    Organiza los elementos como la Tierra los "ve": por **Carga (Z)** y **Tamaño (r)**.
    
    Esto revela el "comportamiento social" de los iones:
    *   **Litófilos**: Forman rocas.
    *   **Hidrófilos**: Viven en el mar.
    *   **Calcófilos**: Se esconden en menas metálicas.
    """)

st.markdown("---")

# Sección 2: Geoquímica en el Mundo Real
st.header("2. Geoquímica en el Mundo Real")
tab_energy, tab_pollution, tab_climate = st.tabs(["🔋 Transición Energética", "☠️ Contaminación", "🌍 Cambio Climático"])

with tab_energy:
    st.subheader("La Minería del Futuro")
    st.markdown("""
    La transición verde depende de saber dónde buscar.
    
    *   **Litio ($Li^+$)**: Es un ión **Duro** y muy soluble. 
        *   *Dónde buscar*: Salares y aguas termales (donde el agua se evaporó).
    *   **Cobalto ($Co^{2+}$)**: Es ión **Intermedio**.
        *   *Dónde buscar*: Rocas sulfuradas profundas (asociado a procesos magmáticos).
        
    ¡La tabla predice la ubicación de la mina!
    """)

with tab_pollution:
    st.subheader("Metales Pesados Asesinos")
    st.markdown("""
    ¿Por qué el Mercurio ($Hg$) o el Plomo ($Pb$) son tan tóxicos y persistentes?
    
    Son iones **Blandos** o intermedios grandes.
    *   A diferencia del Sodio (que el agua lava fácilmente), estos metales se "pegan" (forman complejos fuertes) con la materia orgánica y los sulfuros del suelo.
    *   **Resultado**: No se lavan. Se bioacumulan.
    """)

with tab_climate:
    st.subheader("El Termostato Global")
    st.markdown("""
    La **Meteorización de Silicatos** es el aire acondicionado de la Tierra.
    
    Los iones **Duros** ($Ca^{2+}, Mg^{2+}$) de las montañas reaccionan con el $CO_2$ atmosférico disuelto en la lluvia.
    
    $$ CaSiO_3 + CO_2 \\rightarrow CaCO_3 + SiO_2 $$
    
    Este proceso convierte el gas de efecto invernadero en **roca sólida** (Caliza) en el fondo del mar.
    """)

# Sección 3: Fronteras
st.info("""
**🚀 Fronteras del Descubrimiento:**
Áreas como la minería de **Tierras Raras** en "arcillas iónicas" (donde los iones se adsorben débilmente) o el uso de isótopos para trazar el origen del agua en Marte dependen enteramente de entender estos principios de Potencial Iónico.
""")

# --- Sidebar Footer ---
with st.sidebar:
    st.markdown("---")
    st.caption("Herramienta didáctica para geólogos en formación.")
    st.markdown("<small style='color: #8b949e;'>© 2025 Iniciativa Académica.</small>", unsafe_allow_html=True)
