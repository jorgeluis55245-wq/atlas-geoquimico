import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import math

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Atomic Soil Lab",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Motor de Física (Physics Engine) ---

class Particle:
    def __init__(self, id, x, y, type_name, charge, radius, mass, is_hard):
        self.id = id
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.type_name = type_name
        self.charge = charge
        self.radius = radius # Visual radius mainly, acts as collision boundary
        self.mass = mass
        self.is_hard = is_hard # True for Hard (Ionic), False for Soft (Covalent/Polarizable)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

class PhysicsWorld:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.particles = []
        self.k_coulomb = 100.0 # Fuerza electrostática constante
        self.k_repulsion = 200.0 # Fuerza de repulsión de Pauli (evitar colapso)
        self.k_attraction_soft = 150.0 # "Pegamento" covalente para blandos
        self.damping = 0.90 # Fricción para estabilizar el sistema (energía disipada)

    def add_particle(self, p):
        self.particles.append(p)

    def step(self, dt):
        # 1. Calcular Fuerzas
        forces = {p.id: [0.0, 0.0] for p in self.particles}
        
        for i, p1 in enumerate(self.particles):
            for j, p2 in enumerate(self.particles):
                if i >= j: continue # Evitar doble conteo y auto-interacción

                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dist_sq = dx*dx + dy*dy
                dist = math.sqrt(dist_sq)

                if dist < 0.1: dist = 0.1 # Evitar división por cero

                ux = dx / dist
                uy = dy / dist

                fx, fy = 0.0, 0.0

                # A. Fuerza de Coulomb (q1 * q2 / r^2)
                # Cargas opuestas se atraen (-), iguales se repelen (+)
                f_coulomb = -(self.k_coulomb * p1.charge * p2.charge) / dist_sq
                
                # B. Repulsión de Corto Alcance (Pauli) ~ 1/r^12 simplificado a 1/r^6 para simulación visual
                # Solo actúa si están muy cerca (tocándose)
                contact_dist = (p1.radius + p2.radius) * 0.8 # Un poco de solape permitido
                if dist < contact_dist:
                    f_repulsion = self.k_repulsion / (dist**4)
                    fx += f_repulsion * -ux # Empuja lejos
                    fy += f_repulsion * -uy

                # C. Atracción Específica "HSAB" (Simulación de covalencia/polarización)
                # Si ambos son BLANDOS y de carga OPUESTA, atracción extra (enlaces covalentes fuertes)
                if not p1.is_hard and not p2.is_hard and (p1.charge * p2.charge < 0):
                    # Potencial tipo Lennard-Jones atractivo simplificado
                    if dist > contact_dist and dist < contact_dist * 3:
                         f_soft = self.k_attraction_soft / (dist**2)
                         fx += f_soft * ux
                         fy += f_soft * uy

                # Sumar Coulomb
                fx += f_coulomb * ux
                fy += f_coulomb * uy

                # Aplicar fuerzas (Acción/Reacción)
                forces[p1.id][0] += -fx
                forces[p1.id][1] += -fy
                forces[p2.id][0] += fx
                forces[p2.id][1] += fy

        # 2. Integrar Movimiento (Euler con Amortiguación)
        for p in self.particles:
            fx, fy = forces[p.id]
            ax = fx / p.mass
            ay = fy / p.mass

            p.vx = (p.vx + ax * dt) * self.damping
            p.vy = (p.vy + ay * dt) * self.damping

            # Paredes (Rebote simple)
            if p.x < 0: p.x = 0; p.vx *= -1
            if p.x > self.width: p.x = self.width; p.vx *= -1
            if p.y < 0: p.y = 0; p.vy *= -1
            if p.y > self.height: p.y = self.height; p.vy *= -1

            p.update(dt)

# --- Funciones Auxiliares UI ---

def create_scenario(scenario_type):
    world = PhysicsWorld(width=15, height=15)
    
    if scenario_type == "A": # Fertilidad (Ca + CO3) - Ordenado
        # Grid inicial aleatorio
        for i in range(8):
            # Cationes Ca2+ (Duros)
            world.add_particle(Particle(
                id=f"Ca_{i}", 
                x=np.random.uniform(2, 13), y=np.random.uniform(2, 13),
                type_name="Ca²⁺", charge=2, radius=0.6, mass=40, is_hard=True
            ))
            # Aniones CO3-- (Duros)
            world.add_particle(Particle(
                id=f"CO3_{i}", 
                x=np.random.uniform(2, 13), y=np.random.uniform(2, 13),
                type_name="CO₃²⁻", charge=-2, radius=0.7, mass=60, is_hard=True
            ))
            
    elif scenario_type == "B": # Contaminación (Hg + S) - Clumping
        for i in range(8):
            # Cationes Hg2+ (Blandos)
            world.add_particle(Particle(
                id=f"Hg_{i}", 
                x=np.random.uniform(2, 13), y=np.random.uniform(2, 13),
                type_name="Hg²⁺", charge=2, radius=0.8, mass=200, is_hard=False
            ))
            # Aniones S2- (Blandos)
            world.add_particle(Particle(
                id=f"S_{i}", 
                x=np.random.uniform(2, 13), y=np.random.uniform(2, 13),
                type_name="S²⁻", charge=-2, radius=0.9, mass=32, is_hard=False
            ))

    elif scenario_type == "C": # Competencia (Arcilla vs K vs Pb)
        # Suelo Arcilloso (Aniones fijos en el fondo)
        for i in range(6):
            p = Particle(id=f"Clay_{i}", x=2.5 + i*2, y=2, type_name="Arcilla⁻", charge=-1, radius=1.0, mass=1000, is_hard=True) # Muy pesada = Fija
            world.add_particle(p)
        
        # Invasores K+ (Duro, ligero) y Pb2+ (Blando, pesado)
        for i in range(4):
            world.add_particle(Particle(id=f"K_{i}", x=np.random.uniform(2, 13), y=np.random.uniform(5, 13), type_name="K⁺", charge=1, radius=0.7, mass=39, is_hard=True))
            world.add_particle(Particle(id=f"Pb_{i}", x=np.random.uniform(2, 13), y=np.random.uniform(5, 13), type_name="Pb²⁺", charge=2, radius=0.9, mass=207, is_hard=False))

    return world

def run_simulation(world, frames=60, dt=0.05):
    history = []
    for _ in range(frames):
        world.step(dt)
        frame_data = []
        for p in world.particles:
            frame_data.append({
                "id": p.id, "x": p.x, "y": p.y, "type": p.type_name, 
                "radius": p.radius, "is_hard": p.is_hard, "charge": p.charge
            })
        history.append(frame_data)
    return history

# --- Interfaz de Usuario ---
st.title("🧪 Atomic Soil Lab")
st.markdown("Experimenta con la química del suelo a nivel atómico. **Teoría HSAB** (Ácidos y Bases Duros y Blandos).")

# Sidebar
st.sidebar.header("Configuración del Experimento")
scenario_choice = st.sidebar.selectbox(
    "Selecciona un Escenario:",
    [
        "Escenario A: Fertilidad (Ca²⁺ + CO₃²⁻)",
        "Escenario B: Contaminación (Hg²⁺ + S²⁻)",
        "Escenario C: Competencia (Arcilla + K⁺ vs Pb²⁺)"
    ]
)

scenario_code = "A"
if "Escenario B" in scenario_choice: scenario_code = "B"
if "Escenario C" in scenario_choice: scenario_code = "C"

# Estado de la sesión para mantener la simulación
if 'simulation_data' not in st.session_state or st.session_state.current_scenario != scenario_code:
    st.session_state.current_scenario = scenario_code
    # Generar simulación inicial (pre-calculada)
    world = create_scenario(scenario_code)
    st.session_state.simulation_data = run_simulation(world, frames=80, dt=0.05) # 80 frames
    st.session_state.world_initial = create_scenario(scenario_code) # Para info estática

if st.sidebar.button("🔄 Reiniciar Simulación"):
    world = create_scenario(scenario_code)
    st.session_state.simulation_data = run_simulation(world, frames=80, dt=0.05)
    st.rerun()

# --- Construir Animación Plotly ---
sim_data = st.session_state.simulation_data

# Definir estilo por tipo de partículas (Colores y Tamaños)
# Duros (Azules/Cyan), Blandos (Rojos/Gold), Aniones Duros (Verdes)
def get_color(type_name, is_hard, charge):
    if charge < 0: return "#2ca02c" # Aniones genéricos (Verde)
    if not is_hard: return "#d62728" # Blandos (Rojo)
    return "#1f77b4" # Duros (Azul)

# Frame Base (Frame 0)
initial_frame = sim_data[0]
fig = go.Figure(
    data=[
        # Capa 1: Nubes Electrónicas (Grandes, transparentes)
        go.Scatter(
            x=[p['x'] for p in initial_frame],
            y=[p['y'] for p in initial_frame],
            mode='markers',
            marker=dict(
                size=[p['radius'] * 40 for p in initial_frame], # Escalar para visualización
                color=[get_color(p['type'], p['is_hard'], p['charge']) for p in initial_frame],
                opacity=0.3,
                line=dict(width=0)
            ),
            hoverinfo='skip'
        ),
        # Capa 2: Núcleos (Puntos sólidos)
        go.Scatter(
            x=[p['x'] for p in initial_frame],
            y=[p['y'] for p in initial_frame],
            mode='markers+text',
            text=[p['type'] for p in initial_frame],
            textposition="top center",
            marker=dict(
                size=8,
                color='white',
                line=dict(width=1, color='black')
            ),
            hoverinfo='text'
        )
    ],
    layout=go.Layout(
        xaxis=dict(range=[0, 15], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 15], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='#0e1117', # Fondo oscuro tipo Streamlit
        paper_bgcolor='#0e1117',
        height=600,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="▶️ Iniciar Reacción",
                          method="animate",
                          args=[None, {"frame": {"duration": 50, "redraw": True},
                                       "fromcurrent": True, "transition": {"duration": 0}}])]
        )]
    ),
    frames=[
        go.Frame(
            data=[
                go.Scatter(x=[p['x'] for p in f], y=[p['y'] for p in f]), # Update nubes
                go.Scatter(x=[p['x'] for p in f], y=[p['y'] for p in f], text=[p['type'] for p in f])  # Update núcleos
            ]
        ) for f in sim_data
    ]
)

# Layout de dos columnas
col_main, col_info = st.columns([3, 1])

with col_main:
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.markdown("### 📝 Notas de Lab")
    
    if scenario_code == "A":
        st.info("**Fertilidad (Ca²⁺ + CO₃²⁻)**")
        st.write("Observa la **cristalización rápida**.")
        st.write("Ambos iones son 'Duros' (alta densidad de carga). La atracción electrostática pura domina, formando estructuras rígidas y ordenadas (como la Calcita).")
        
    elif scenario_code == "B":
        st.error("**Contaminación (Hg²⁺ + S²⁻)**")
        st.write("Observa el **'clumping' o segregación**.")
        st.write("Ambos son 'Blandos' (polarizables). Forman enlaces covalentes fuertes. Se agrupan desordenadamente, imitando cómo el Mercurio se fija al Azufre en la materia orgánica, siendo muy tóxico y difícil de remover.")

    elif scenario_code == "C":
        st.warning("**La Competencia**")
        st.write("Potasio (Duro) vs Plomo (Blando) sobre Arcilla.")
        st.write("La arcilla suele tener cargas negativas en su superficie. Nota quién se adhiere más fuertemente o cómo compiten por el espacio.")

    st.markdown("---")
    st.markdown("**Leyenda Visual:**")
    st.markdown("🔵 **Halo Azul**: Catión Duro (Compacto)")
    st.markdown("🔴 **Halo Rojo**: Catión Blando (Difuso/Polarizable)")
    st.markdown("🟢 **Halo Verde**: Anión")
