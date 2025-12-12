import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Tabla Periódica del Científico de la Tierra",
    layout="wide",
    page_icon="🌍"
)

# --- Diccionario de Datos Geoquímicos (Railsback) ---
# Datos basados en L. Bruce Railsback's "An Earth Scientist's Periodic Table of the Elements and Their Ions"
# Radios iónicos (r) en Angstroms (Shannon-Prewitt, Coordinación VI generalmente)
# Carga (z)
# IP = z / r

data = [
    # --- CATIONES DUROS (Tipo A) ---
    # Gases Nobles (Configuración) - Lithophiles
    {"Simbolo": "K+", "Nombre": "Potasio", "Carga": 1, "Radio": 1.38, "Grupo": "Duros (Tipo A)", "Nota": "Soluble, Nutriente mayor", "Z": 19},
    {"Simbolo": "Na+", "Nombre": "Sodio", "Carga": 1, "Radio": 1.02, "Grupo": "Duros (Tipo A)", "Nota": "Muy Soluble, Agua Salada", "Z": 11},
    {"Simbolo": "Ca2+", "Nombre": "Calcio", "Carga": 2, "Radio": 1.00, "Grupo": "Duros (Tipo A)", "Nota": "Soluble, Carbonatos", "Z": 20},
    {"Simbolo": "Mg2+", "Nombre": "Magnesio", "Carga": 2, "Radio": 0.72, "Grupo": "Duros (Tipo A)", "Nota": "Soluble, Clorofila", "Z": 12},
    {"Simbolo": "Sr2+", "Nombre": "Estroncio", "Carga": 2, "Radio": 1.18, "Grupo": "Duros (Tipo A)", "Nota": "Traza, sustituye Ca", "Z": 38},
    {"Simbolo": "Ba2+", "Nombre": "Bario", "Carga": 2, "Radio": 1.35, "Grupo": "Duros (Tipo A)", "Nota": "Barita (Insoluble SO4)", "Z": 56},
    
    # Alta Carga / Radio Pequeño (Insolubles/Hidrolizados)
    {"Simbolo": "Al3+", "Nombre": "Aluminio", "Carga": 3, "Radio": 0.54, "Grupo": "Duros (Tipo A)", "Nota": "Insoluble, Arcillas", "Z": 13},
    {"Simbolo": "Si4+", "Nombre": "Silicio", "Carga": 4, "Radio": 0.26, "Grupo": "Aniones (Formadores)", "Nota": "Insoluble (SiO2) / Silicatos", "Z": 14}, # Si4+ a veces se trata aparte
    {"Simbolo": "Ti4+", "Nombre": "Titanio", "Carga": 4, "Radio": 0.61, "Grupo": "Duros (Tipo A)", "Nota": "Muy Insoluble (Rutilo)", "Z": 22},
    {"Simbolo": "Zr4+", "Nombre": "Circonio", "Carga": 4, "Radio": 0.72, "Grupo": "Duros (Tipo A)", "Nota": "Muy Insoluble (Circón)", "Z": 40},
    
    # --- INTERMEDIOS (Transición) ---
    {"Simbolo": "Fe2+", "Nombre": "Hierro (II)", "Carga": 2, "Radio": 0.78, "Grupo": "Intermedios", "Nota": "Soluble en anoxia", "Z": 26},
    {"Simbolo": "Fe3+", "Nombre": "Hierro (III)", "Carga": 3, "Radio": 0.65, "Grupo": "Intermedios", "Nota": "Insoluble (Óxidos rojos)", "Z": 26},
    {"Simbolo": "Mn2+", "Nombre": "Manganeso (II)", "Carga": 2, "Radio": 0.83, "Grupo": "Intermedios", "Nota": "Móvil en reducción", "Z": 25},
    {"Simbolo": "Zn2+", "Nombre": "Zinc", "Carga": 2, "Radio": 0.74, "Grupo": "Intermedios", "Nota": "Nutriente traza / Sulfuros", "Z": 30},
    {"Simbolo": "Ni2+", "Nombre": "Níquel", "Carga": 2, "Radio": 0.69, "Grupo": "Intermedios", "Nota": "Siderófilo/Calcófilo", "Z": 28},
    
    # --- CATIONES BLANDOS (Tipo B) ---
    # Afinidad por el Azufre (Calcófilos)
    {"Simbolo": "Cu+", "Nombre": "Cobre (I)", "Carga": 1, "Radio": 0.77, "Grupo": "Blandos (Tipo B)", "Nota": "Sulfuros insolubles", "Z": 29},
    {"Simbolo": "Ag+", "Nombre": "Plata", "Carga": 1, "Radio": 1.15, "Grupo": "Blandos (Tipo B)", "Nota": "Metales preciosos", "Z": 47},
    {"Simbolo": "Au+", "Nombre": "Oro", "Carga": 1, "Radio": 1.37, "Grupo": "Blandos (Tipo B)", "Nota": "Inerte / Complejos", "Z": 79},
    {"Simbolo": "Hg2+", "Nombre": "Mercurio", "Carga": 2, "Radio": 1.02, "Grupo": "Blandos (Tipo B)", "Nota": "Tóxico, líquido", "Z": 80},
    {"Simbolo": "Pb2+", "Nombre": "Plomo", "Carga": 2, "Radio": 1.19, "Grupo": "Blandos (Tipo B)", "Nota": "Tóxico, Galena", "Z": 82},
    {"Simbolo": "Cd2+", "Nombre": "Cadmio", "Carga": 2, "Radio": 0.95, "Grupo": "Blandos (Tipo B)", "Nota": "Tóxico, sustituye Zn", "Z": 48},
    
    # --- ANIONES (Formadores de Complejos) ---
    # Alto Potencial Iónico -> Forman oxianiones
    {"Simbolo": "C4+", "Nombre": "Carbono", "Carga": 4, "Radio": 0.15, "Grupo": "Aniones (Formadores)", "Nota": "Forma CO3-- (soluble/carb)", "Z": 6},
    {"Simbolo": "S6+", "Nombre": "Azufre (VI)", "Carga": 6, "Radio": 0.29, "Grupo": "Aniones (Formadores)", "Nota": "Forma SO4-- (soluble)", "Z": 16},
    {"Simbolo": "N5+", "Nombre": "Nitrógeno", "Carga": 5, "Radio": 0.13, "Grupo": "Aniones (Formadores)", "Nota": "Forma NO3- (muy soluble)", "Z": 7},
    {"Simbolo": "P5+", "Nombre": "Fósforo", "Carga": 5, "Radio": 0.38, "Grupo": "Aniones (Formadores)", "Nota": "Forma PO4--- (nutriente)", "Z": 15},
    {"Simbolo": "B3+", "Nombre": "Boro", "Carga": 3, "Radio": 0.27, "Grupo": "Aniones (Formadores)", "Nota": "Forma Boratos", "Z": 5},
]

# --- Procesamiento de Datos ---
df = pd.DataFrame(data)
df['Potencial_Ionico'] = df['Carga'] / df['Radio']

# Asignar coordenadas X categóricas simuladas para el gráfico
# Mapeo de grupos a posiciones base en X
group_map = {
    "Duros (Tipo A)": 1,
    "Intermedios": 2,
    "Blandos (Tipo B)": 3,
    "Aniones (Formadores)": 1.5 # Posicionarlos estratégicamente o filtrarlos
}

# Filtrar o ajustar Aniones para visualización principal si se desea
# En Railsback suelen estar muy arriba a la izquierda o derecha.
# Para este gráfico simplificado de 3 columnas, los pondremos como una categoría especial o en Duros (alto IP)
# Vamos a mantenerlos pero darles una X específica.
df['X_Base'] = df['Grupo'].map(group_map)

# Manejar los que no mapearon bien (por seguridad)
df['X_Base'] = df['X_Base'].fillna(2)

# Añadir Jitter (Ruido aleatorio) para evitar superposición
np.random.seed(42) # Para reproducibilidad
df['X_Final'] = df['X_Base'] + np.random.uniform(-0.15, 0.15, size=len(df))

# --- Título y Header ---
st.title("🌍 Tabla Periódica del Científico de la Tierra")
st.markdown("""
Esta herramienta interactiva visualiza el comportamiento geoquímico de los iones basándose en su **Potencial Iónico** ($z/r$).
Los elementos se clasifican según su afinidad electrónica y dureza química (Teoría HSAB).
""")

# --- Sidebar / Filtros ---
st.sidebar.header("Configuración")
grupos_seleccionados = st.sidebar.multiselect(
    "Filtrar por Grupo:",
    options=df['Grupo'].unique(),
    default=df['Grupo'].unique()
)

df_filtered = df[df['Grupo'].isin(grupos_seleccionados)]

# --- Visualización Principal ---
col_grafico, col_info = st.columns([3, 1])

with col_grafico:
    fig = go.Figure()

    # == ZONIFICACIÓN DE FONDO (Rectángulos) ==
    # Zona Alta: Formación de Aniones Solubles (IP > 10)
    fig.add_hrect(
        y0=10, y1=45, 
        fillcolor="rgba(200, 230, 255, 0.3)", layer="below", line_width=0,
        annotation_text="Formación de Aniones Solubles (CO3, SO4)", annotation_position="top left"
    )
    
    # Zona Media: Hidrolizados / Insolubles (3 < IP < 10)
    fig.add_hrect(
        y0=3, y1=10, 
        fillcolor="rgba(255, 240, 200, 0.3)", layer="below", line_width=0,
        annotation_text="Hidrolizados / Precipitados (Suelos)", annotation_position="left"
    )
    
    # Zona Baja: Cationes Solubles (IP < 3)
    fig.add_hrect(
        y0=0, y1=3, 
        fillcolor="rgba(200, 255, 200, 0.3)", layer="below", line_width=0,
        annotation_text="Cationes Solubles (Agua de Mar)", annotation_position="bottom left"
    )

    # == PUNTOS DE DATOS ==
    # Colores por grupo
    color_map = {
        "Duros (Tipo A)": "#1f77b4",     # Azul
        "Intermedios": "#2ca02c",        # Verde
        "Blandos (Tipo B)": "#d62728",   # Rojo
        "Aniones (Formadores)": "#9467bd" # Morado
    }

    for grupo in df_filtered['Grupo'].unique():
        df_g = df_filtered[df_filtered['Grupo'] == grupo]
        fig.add_trace(go.Scatter(
            x=df_g['X_Final'],
            y=df_g['Potencial_Ionico'],
            mode='markers+text',
            name=grupo,
            text=df_g['Simbolo'],
            textposition="top center",
            marker=dict(
                size=25,
                symbol='square',
                color=color_map.get(grupo, "grey"),
                line=dict(width=1, color='DarkSlateGrey')
            ),
            hovertemplate=(
                "<b>%{text}</b> (%{customdata[0]})<br>" +
                "Carga: +%{customdata[1]}<br>" +
                "Radio: %{customdata[2]} Å<br>" +
                "IP (z/r): %{y:.2f}<br>" +
                "<i>%{customdata[3]}</i><extra></extra>"
            ),
            customdata=df_g[['Nombre', 'Carga', 'Radio', 'Nota']]
        ))

    # Configuración de Ejes
    fig.update_layout(
        title="Potencial Iónico vs. Clasificación Geoquímica",
        xaxis=dict(
            title="Clasificación (Duros → Intermedios → Blandos)",
            tickmode='array',
            tickvals=[1, 2, 3],
            ticktext=["<b>Cationes Duros</b><br>(Litófilos)", "<b>Intermedios</b><br>(Transición)", "<b>Cationes Blandos</b><br>(Calcófilos)"],
            range=[0.5, 3.5],
            showgrid=False
        ),
        yaxis=dict(
            title="Potencial Iónico (z/r)",
            range=[0, 30], # Ajustado para visualización, aniones como C4+ estarán arriba
            showgrid=True
        ),
        height=700,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        margin=dict(l=40, r=40, t=60, b=40),
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Panel Didáctico ---
with col_info:
    st.subheader("💡 Conceptos Clave")
    
    with st.expander("¿Qué es el Potencial Iónico?", expanded=True):
        st.write("""
        Es la relación entre la carga eléctrica ($z$) y el radio iónico ($r$).
        
        $$ IP = \\frac{z}{r} $$
        
        Determina qué tan fuertemente un ion atrae a las moléculas de agua cercanas.
        """)

    with st.expander("Duros vs. Blandos"):
        st.write("""
        **Duros (Tipo A)**: Iones pequeños y de alta carga, o iones alcalinos. Tienen nubes electrónicas rígidas. Prefieren enlaces iónicos con Oxígeno.
        
        **Blandos (Tipo B)**: Iones grandes y polarizables. Tienen nubes electrónicas deformables. Prefieren enlaces covalentes con Azufre.
        """)
        
    st.info("""
    **Paradoja del Oro vs. Potasio**
    
    Ambos tienen carga +1.
    *   **Potasio ($K^+$)**: Es 'duro', ama el oxígeno y es muy soluble en el océano.
    *   **Oro ($Au^+$)**: Es 'blando', prefiere el azufre y se encuentra en vetas de cuarzo/sulfuros, no en el agua.
    """)

# --- Tabla de Datos ---
st.markdown("### 📊 Datos Crudos")

column_config = {
    "Simbolo": "Ion",
    "Potencial_Ionico": st.column_config.NumberColumn("Potencial Iónico", format="%.2f"),
    "Radio": st.column_config.NumberColumn("Radio (Å)", format="%.2f"),
}

st.dataframe(
    df_filtered[['Simbolo', 'Nombre', 'Grupo', 'Carga', 'Radio', 'Potencial_Ionico', 'Nota']],
    use_container_width=True,
    column_config=column_config,
    hide_index=True
)
