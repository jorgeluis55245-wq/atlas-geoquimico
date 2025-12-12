# Diccionario Maestro de Comportamiento Geoquímico
# Basado en Railsback (Earth Scientist's Periodic Table)

ELEMENTS = {
    "Si4+": {
        "type": "Hard", "ip": 15.4, "role": "Network Former",
        "atomic_behavior": "Atrae oxígenos rígidamente (Tetraedros).",
        "mineral": "Cuarzo (SiO2)",
        "landscape": "Playas de arena blanca, picos de montañas resistentes (no se disuelve).",
        "color": "#E0E0E0", # Blanco/Gris claro
        "radius": 0.26
    },
    "Ca2+": {
        "type": "Hard", "ip": 2.0, "role": "Network Modifier",
        "atomic_behavior": "Enlace iónico medio. Soluble en ácido.",
        "mineral": "Calcita (CaCO3)",
        "landscape": "Paisajes Kársticos (Cuevas, Cenotes) por disolución.",
        "color": "#90CAF9", # Azul claro
        "radius": 1.00
    },
    "Fe3+": {
        "type": "Intermediate", "ip": 4.6, "role": "Pigment/Cement",
        "atomic_behavior": "Insoluble al oxidarse. Forma 'pegamento' de óxidos.",
        "mineral": "Hematita (Fe2O3)",
        "landscape": "Suelos rojos tropicales (Lateritas), desiertos rojos.",
        "color": "#D32F2F", # Rojo
        "radius": 0.65
    },
    "Na+": {
        "type": "Hard", "ip": 0.98, "role": "Solute",
        "atomic_behavior": "Esfera hidratada muy laxa. No se pega a nada.",
        "mineral": "Halita (NaCl) - solo al secarse.",
        "landscape": "Océanos salados y Salares (se lava de las montañas y termina en el mar).",
        "color": "#4FC3F7", # Azul Cyan
        "radius": 1.02
    },
    # Añadimos estos para la simulación del Oro
    "Au+": {
        "type": "Soft", "ip": 0.73, "role": "Chalcophile",
        "atomic_behavior": "Nube electrónica difusa. Enlaces covalentes con S.",
        "mineral": "Oro Nativo / Sulfuros",
        "landscape": "Vetas profundas, no en agua.",
        "color": "#FFD700", # Oro
        "radius": 1.37
    },
    "S2-": {
        "type": "Soft", "ip": 0.5, "role": "Ligand", # IP approx para aniones grandes
        "atomic_behavior": "Gran nube polarizable.",
        "mineral": "Sulfuros",
        "landscape": "Ambientes reductores.",
        "color": "#FFEB3B", # Amarillo
        "radius": 1.84
    },
    "O2-": {
        "type": "Hard", "ip": 1.5, "role": "Ligand", # IP approx
        "atomic_behavior": "Pequeño y duro.",
        "mineral": "Óxidos / Silicatos",
        "landscape": "Ambientes oxidantes.",
        "color": "#FF5252", # Rojo claro
        "radius": 1.40
    }
}
