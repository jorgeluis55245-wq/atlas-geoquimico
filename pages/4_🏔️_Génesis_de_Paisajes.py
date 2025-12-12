import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Génesis de Paisajes: El Gran Filtro",
    page_icon="🏔️",
    layout="wide"
)

# --- CSS Personalizado ---
st.markdown("""
<style>
    .big-font { font-size: 18px !important; color: #e0e0e0; font-family: sans-serif; }
    .highlight { color: #FFD700; font-weight: bold; }
    .insight-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4FC3F7;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏔️ Génesis de Paisajes: El Gran Filtro Geoquímico")
st.markdown("---")

# --- Estructura Narrativa (Fases) ---
tab1, tab2, tab3 = st.tabs(["1. La Meteorización (Montaña)", "2. El Transporte (Río)", "3. La Deposición (Mar)"])

with tab1:
    st.markdown("""
    ### ⛈️ Fase 1: El Ataque Químico (Hidrólisis)
    La lluvia no es solo agua; es un **ácido débil** (H₂CO₃) que ataca la roca.
    
    El **Granito** (la roca continental más común) se descompone así:
    $$ \text{Granito} + \text{Agua} \rightarrow \textbf{Arcilla} (Al) + \textbf{Iones} (Ca, Na) + \textbf{Arena} (Si) $$
    
    *   Los enlaces **Duros (Si-O)** resisten (se quedan como Cuarzo).
    *   Los enlaces **Medios (Al-O)** se hidratan (forman Arcillas).
    *   Los enlaces **Débiles (Ca-O)** se rompen (se disuelven).
    """)

with tab2:
    st.markdown("""
    ### 🌊 Fase 2: El Gran Filtro (Transporte)
    El río actúa como una cinta transportadora selectiva basándose en el **Potencial Iónico ($z/r$)**.
    
    *   **Resistatos (Sólidos)**: Viajan rodando por el fondo. (Ej. Arena, Oro).
    *   **Solutos (Disueltos)**: Viajan invisibles en el agua. (Ej. Sal, Calcio).
    """)

with tab3:
    st.markdown("""
    ### 🏖️ Fase 3: El Destino Final
    ¿Por qué el mar es salado y las playas son de arena?
    
    *   **Playas**: Cementerios de **Cuarzo** (lo único que sobrevivió).
    *   **Fondo Marino**: Cementerios de **Carbonatos** (Calcio precipitándose) y Salmueras.
    """)

st.markdown("---")

# --- Lógica de Visualización 3D Avanzada ---
col_viz, col_ctrl = st.columns([0.7, 0.3])

with col_ctrl:
    st.subheader("🔬 Lente de Rayos X")
    view_mode = st.radio(
        "Filtra la realidad:",
        ["Todo (Vista Real)", "Resistatos (Esqueleto)", "Solutos (El Mar/Sal)", "Hidrolizados (Suelo)"]
    )
    
    st.markdown("### 💡 Insight")
    if view_mode == "Todo (Vista Real)":
        st.info("Ves el ciclo completo. Observa cómo la montaña (Marrón) 'pierde' masa que termina en el mar.")
    elif view_mode == "Resistatos (Esqueleto)":
        st.warning("**Cuarzo ($Si^{4+}$)**\n\nEl esqueleto de la Tierra. El enlace Si-O es tan fuerte ($z/r$ extremo) que sobrevive al viaje físico y químico, acumulándose en la costa.")
    elif view_mode == "Solutos (El Mar/Sal)":
        st.success("**Sodio y Calcio ($Na^+, Ca^{2+}$)**\n\nEl sabor del mar. Estos iones fueron lavados de las montañas durante eones debido a su bajo Potencial Iónico ($z/r$ bajo).")
    elif view_mode == "Hidrolizados (Suelo)":
        st.error("**Arcillas ($Al^{3+}$)**\n\nEl Aluminio se hidroliza. No es soluble pero tampoco inerte. Se queda en la ladera formando el suelo fértil (Pedogénesis).")

with col_viz:
    # 1. Generación de Terreno
    x = np.linspace(-10, 10, 50) # -10 a 0 = Montaña, 0 a 10 = Mar
    y = np.linspace(-5, 5, 25)
    X, Y = np.meshgrid(x, y)
    
    # Función de Altura (Sigmoide modificada)
    # Si x < 0: Montaña alta que baja. Si x > 0: Fondo marino profundo.
    Z_terrain = -5 * np.tanh(X/4) # Genera una pendiente suave de +5 a -5
    Z_terrain += 0.5 * np.sin(Y) * np.exp(-(X)**2 / 10) # Añadir "valles" en la montaña
    
    # Plano del Agua (Z=0 para X>0)
    Z_water = np.zeros_like(Z_terrain)
    # Hacemos que el agua solo sea visible en X > -1 (Costa)
    water_mask = X > -1.5 
    Z_water[~water_mask] = np.nan # Ocultar agua en la montaña alta
    
    fig = go.Figure()
    
    # Capa Terreno
    fig.add_trace(go.Surface(
        z=Z_terrain, x=X, y=Y,
        colorscale='Earth',
        showscale=False,
        name='Corteza Terrestre',
        opacity=1.0
    ))
    
    # Capa Agua (Solo si no estamos viendo solo sólidos, opcional, pero mejor visual)
    if view_mode != "Hidrolizados (Suelo)" and view_mode != "Resistatos (Esqueleto)":
         fig.add_trace(go.Surface(
            z=Z_water, x=X, y=Y,
            colorscale=[[0, 'rgba(0,100,255,0.4)'], [1, 'rgba(0,100,255,0.4)']],
            showscale=False,
            name='Océano',
            # hoverinfo='skip'
        ))

    # --- Generación de Actores Químicos (Partículas) ---
    
    # A. Cuarzo (Arena) - En la costa (X ~ 0)
    if view_mode in ["Todo (Vista Real)", "Resistatos (Esqueleto)"]:
        # Acumulación en la "playa" (X entre -1 y 1)
        x_q = np.random.normal(0, 1.5, 100)
        y_q = np.random.uniform(-5, 5, 100)
        z_q = -5 * np.tanh(x_q/4) + 0.3 # Encima del terreno
        
        fig.add_trace(go.Scatter3d(
            x=x_q, y=y_q, z=z_q,
            mode='markers',
            marker=dict(size=4, color='#FFD700', opacity=0.9),
            name='Cuarzo (SiO₂)',
            hovertemplate="Cuarzo (Insoluble)<br>Se acumula en playas"
        ))

    # B. Arcillas (Suelo) - En la montaña (X < -2)
    if view_mode in ["Todo (Vista Real)", "Hidrolizados (Suelo)"]:
        x_c = np.random.uniform(-9, -2, 100)
        y_c = np.random.uniform(-5, 5, 100)
        z_c = -5 * np.tanh(x_c/4) + 0.3
        
        fig.add_trace(go.Scatter3d(
            x=x_c, y=y_c, z=z_c,
            mode='markers',
            marker=dict(size=4, color='#8D6E63', opacity=0.8), # Marrón
            name='Arcillas (Al)',
            hovertemplate="Arcillas (Hidrolizados)<br>Forman el suelo"
        ))

    # C. Solutos (Iones) - En el mar (X > 1)
    if view_mode in ["Todo (Vista Real)", "Solutos (El Mar/Sal)"]:
        x_s = np.random.uniform(2, 9, 150)
        y_s = np.random.uniform(-5, 5, 150)
        z_s = np.random.uniform(-4, -0.5, 150) # Debajo del agua
        
        fig.add_trace(go.Scatter3d(
            x=x_s, y=y_s, z=z_s,
            mode='markers',
            marker=dict(size=3, color='#E0F7FA', opacity=0.6),
            name='Iones (Na, Ca)',
            hovertemplate="Solutos (Na/Ca)<br>Disueltos en el mar"
        ))

    # Configuración de Cámara y Escena
    camera = dict(
        eye=dict(x=0.1, y=-2.0, z=0.5) # Vista casi a nivel del mar pero lateral
    )
    
    fig.update_layout(
        title="Simulación 3D: Ciclo Exógeno",
        scene=dict(
            xaxis=dict(title="Montaña ← → Mar", range=[-10, 10], showgrid=False),
            yaxis=dict(title="", range=[-5, 5], showgrid=False),
            zaxis=dict(title="Altitud", range=[-6, 6], showgrid=False),
            aspectratio=dict(x=3, y=1, z=1),
            camera=camera,
            bgcolor='#0e1117'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=600,
        paper_bgcolor='#0e1117',
    )
    
    st.plotly_chart(fig, use_container_width=True)

# --- Sección Curiosidades ---
st.markdown("### 🌍 ¿Sabías qué?")
with st.expander("El termostato de la Tierra (Cambio Climático)"):
    st.write("""
    La meteorización de los silicatos (como se ve en la Fase 1) es clave para el clima global a largo plazo.
    
    $$ CaSiO_3 + CO_2 + H_2O \\rightarrow CaCO_3 + SiO_2 + H_2O $$
    
    Este proceso **consume CO₂** de la atmósfera y lo encierra en piedra caliza ($CaCO_3$) en el fondo del mar. Sin este proceso, la Tierra sería un infierno caliente como Venus.
    """)
