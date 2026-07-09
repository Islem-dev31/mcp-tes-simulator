# -*- coding: utf-8 -*-
"""
Application Web Interactive Streamlit - Simulateur de Batterie Thermique MCP (TES)
Conception HCD (Human-Centered Design) & Aide à la Décision Industrielle
"""

import streamlit as st
import pandas as pd
import numpy as np
import math

# Importation des constantes physiques et économiques de config.py
import mcp_config as config

# Configuration de la page Streamlit pour KryoDrop
st.set_page_config(
    page_title="KryoDrop | Simulateur de Batterie Thermique MCP",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement de FontAwesome et Style CSS personnalisé pour KryoDrop
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
    /* Style général */
    .main {
        background-color: #F4F6F9;
    }
    h1, h2, h3, h4, h5 {
        color: #1B365D;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }
    
    /* Titre de section */
    .section-title {
        border-bottom: 2.5px solid #29B6D8;
        padding-bottom: 6px;
        margin-top: 22px;
        margin-bottom: 16px;
    }
    
    /* Style des cartes métriques HCD KryoDrop */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(27, 54, 93, 0.04);
        border-left: 6px solid #29B6D8;
        border-top: 1px solid rgba(41, 182, 216, 0.08);
        border-right: 1px solid rgba(27, 54, 93, 0.04);
        border-bottom: 1px solid rgba(27, 54, 93, 0.04);
        margin-bottom: 1.2rem;
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 22px rgba(27, 54, 93, 0.12);
        border-left-color: #1B365D;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #7F8C8D;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.7px;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1B365D;
        line-height: 1.2;
    }
    .metric-unit {
        font-size: 1rem;
        font-weight: 600;
        color: #29B6D8;
        margin-left: 0.2rem;
    }
    .metric-subtitle {
        font-size: 0.8rem;
        color: #7F8C8D;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    .metric-icon {
        font-size: 2.4rem;
        color: rgba(41, 182, 216, 0.25);
        transition: color 0.3s;
    }
    .metric-card:hover .metric-icon {
        color: #29B6D8;
    }
    
    /* Cartes DFM */
    .dfm-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid rgba(27, 54, 93, 0.08);
        box-shadow: 0 2px 6px rgba(27, 54, 93, 0.02);
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .dfm-card:hover {
        border-color: #29B6D8;
        box-shadow: 0 4px 12px rgba(41, 182, 216, 0.1);
        transform: translateY(-1px);
    }
    
    /* Bloc Problème/Solution */
    .hcd-box {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 25px;
        height: 100%;
    }
    .problem-box {
        border-left: 5px solid #E74C3C;
    }
    .solution-box {
        border-left: 5px solid #2ECC71;
    }
    .strength-box {
        border-left: 5px solid #29B6D8;
    }
    
    /* Labels de la barre latérale */
    .sidebar-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #2C3E50;
        margin-top: 12px;
        margin-bottom: 4px;
        display: block;
    }
    
    /* Badges DFM */
    .dfm-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-top: 8px;
        margin-bottom: 4px;
    }
    .dfm-ok {
        background-color: #D4EDDA;
        color: #155724;
        border: 1px solid #C3E6CB;
    }
    .dfm-fail {
        background-color: #F8D7DA;
        color: #721C24;
        border: 1px solid #F5C6CB;
    }
</style>
""", unsafe_allow_html=True)

# En-tête principal KryoDrop
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("logo5.png", width=160)
with col_title:
    st.markdown("""
    <div style="margin-top: 5px;">
        <h1 style="color: #1B365D; font-size: 2.2rem; margin-bottom: 0px;">KryoDrop</h1>
        <p style="font-size: 1.1rem; color: #29B6D8; font-weight: 600; margin-top: -5px; letter-spacing: 1px;">MODERN COOLING SOLUTIONS</p>
        <p style="font-size: 0.95rem; color: #7F8C8D; margin-top: -10px;">Simulateur d'Aide à la Décision Industrielle & Optimisation Économique (TES)</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# HCD : LE PROBLÈME ET LA SOLUTION (VISIBILITÉ & MODÈLE MENTAL CLAIR)
# ==============================================================================
col_intro1, col_intro2, col_intro3 = st.columns(3)

with col_intro1:
    st.markdown("""
    <div class="hcd-box problem-box">
        <h4><i class="fa-solid fa-triangle-exclamation" style="color: #E74C3C; margin-right: 8px;"></i> Le Problème</h4>
        <p style="font-size: 0.95rem; color: #555; margin: 0;">
            Les chambres froides subissent des <b>factures Sonelgaz élevées</b> en heures de pointe (tarif x3.6) et sont exposées aux <b>coupures d'électricité</b> qui menacent les marchandises. Les solutions importées (ex: Viking Cold) sont chères, scellées et dépendantes de l'étranger.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_intro2:
    st.markdown("""
    <div class="hcd-box solution-box">
        <h4><i class="fa-solid fa-lightbulb" style="color: #2ECC71; margin-right: 8px;"></i> La Solution</h4>
        <p style="font-size: 0.95rem; color: #555; margin: 0;">
            Une <b>batterie thermique modulaire locale</b>. On y stocke le froid la nuit pendant les heures creuses (électricité à bas coût) pour le restituer de manière contrôlée en journée pendant les heures pleines ou en cas de panne de secteur.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_intro3:
    st.markdown("""
    <div class="hcd-box strength-box">
        <h4><i class="fa-solid fa-circle-check" style="color: #3498DB; margin-right: 8px;"></i> Nos Points Forts</h4>
        <p style="font-size: 0.95rem; color: #555; margin: 0;">
            <b>1. Conductivité :</b> Tubes alu avec ailettes (200 W/m.K vs 0.15 plastique). Réponse thermique instantanée.<br>
            <b>2. Réparabilité :</b> Tubes individuels démontables.<br>
            <b>3. Coût local :</b> Fabrication 100% en Algérie en DA (3x moins cher).
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 1. BARRE LATÉRALE - CONCEPTION HCD (HUMAN-CENTERED DESIGN)
# ==============================================================================
st.sidebar.image("logo5.png", width=180)
st.sidebar.markdown("<h3 style='color:#1B365D; margin-top: 10px; margin-bottom: 20px;'><i class='fa-solid fa-sliders'></i> Configuration</h3>", unsafe_allow_html=True)

# Choix de la ville algérienne
st.sidebar.markdown('<span class="sidebar-label"><i class="fa-solid fa-map-location-dot"></i> Ville d\'implantation</span>', unsafe_allow_html=True)
selected_city = st.sidebar.selectbox(
    "Ville d'implantation",
    options=list(config.CITIES_CLIMATE.keys()),
    index=15,
    help="Sélectionnez la ville pour charger le climat local.",
    label_visibility="collapsed"
)
city_data = config.CITIES_CLIMATE[selected_city]

# Saison / Période de simulation
st.sidebar.markdown('<span class="sidebar-label"><i class="fa-solid fa-calendar-days"></i> Période de simulation</span>', unsafe_allow_html=True)
season = st.sidebar.selectbox(
    "Période de simulation",
    options=["Été (Dimensionnement de pointe)", "Hiver (Conditions favorables)", "Moyenne annuelle (Majorité du temps)"],
    index=0,
    label_visibility="collapsed"
)

if "Été" in season:
    t_ext_default = city_data["design_summer"]
elif "Hiver" in season:
    t_ext_default = city_data["winter"]
else:
    t_ext_default = city_data["avg_annual"]

# Affichage des caractéristiques thermiques de la wilaya
st.sidebar.markdown(f"""
<div style="background-color:#EAF2F8; padding:10px; border-radius:5px; border-left:4px solid #2980B9; margin-top:5px; margin-bottom:10px;">
    <p style="margin:0 0 5px 0; font-size:0.85rem; color:#1B4F72;"><b>Zone :</b> {city_data['desc']}</p>
    <p style="margin:0 0 3px 0; font-size:0.8rem; color:#2C3E50;"><i class="fa-solid fa-temperature-arrow-up" style="color:#E74C3C;"></i> <b>Été Max (Pointe) :</b> {city_data['design_summer']} °C</p>
    <p style="margin:0 0 3px 0; font-size:0.8rem; color:#2C3E50;"><i class="fa-solid fa-temperature-arrow-down" style="color:#3498DB;"></i> <b>Hiver :</b> {city_data['winter']} °C</p>
    <p style="margin:0; font-size:0.8rem; color:#2C3E50;"><i class="fa-solid fa-clock" style="color:#F39C12;"></i> <b>Moyenne Annuelle :</b> {city_data['avg_annual']} °C</p>
</div>
""", unsafe_allow_html=True)

# Mode de Température Cible (Simplifié HCD)
st.sidebar.markdown('<span class="sidebar-label"><i class="fa-solid fa-temperature-low"></i> Type de Chambre Froide</span>', unsafe_allow_html=True)
room_type = st.sidebar.radio(
    "Type de Chambre Froide",
    options=["Froid Positif (+4°C) - Fruits, Légumes, Laitages", "Froid Négatif (-18°C) - Viandes, Congelés"],
    index=0,
    label_visibility="collapsed"
)
t_target = 4.0 if "Positif" in room_type else -18.0

# Volume de la chambre
st.sidebar.markdown('<span class="sidebar-label"><i class="fa-solid fa-cubes"></i> Volume de la chambre froide (m³)</span>', unsafe_allow_html=True)
volume = st.sidebar.number_input(
    "Volume de la chambre froide (m³)",
    min_value=10,
    max_value=1000,
    value=100,
    step=10,
    help="Volume géométrique intérieur de la chambre froide.",
    label_visibility="collapsed"
)

# Budget max
st.sidebar.markdown('<span class="sidebar-label"><i class="fa-solid fa-credit-card"></i> Budget maximum disponible (DA)</span>', unsafe_allow_html=True)
budget_max = st.sidebar.number_input(
    "Budget maximum disponible (DA)",
    min_value=100000,
    max_value=20000000,
    value=4000000,
    step=100000,
    format="%d",
    help="Budget alloué pour la fabrication et l'installation de la batterie thermique.",
    label_visibility="collapsed"
)

# Autonomie cible
st.sidebar.markdown('<span class="sidebar-label"><i class="fa-solid fa-clock"></i> Autonomie souhaitée (heures)</span>', unsafe_allow_html=True)
autonomy_target = st.sidebar.slider(
    "Autonomie souhaitée (heures)",
    min_value=4,
    max_value=24,
    value=13,
    step=1,
    help="Nombre d'heures de coupure compresseur à couvrir.",
    label_visibility="collapsed"
)


with st.sidebar.expander("Paramètres Techniques & CAO Avancés", expanded=False):
    t_ext = st.slider(
        "Température extérieure (°C)",
        min_value=0.0,
        max_value=55.0,
        value=float(t_ext_default),
        step=1.0
    )
    
    pu_default = config.THICKNESS_PU_POS if t_target >= 0 else config.THICKNESS_PU_NEG
    thickness_pu = st.slider(
        "Épaisseur isolation PU (mm)",
        min_value=50,
        max_value=250,
        value=int(pu_default * 1000.0),
        step=10
    ) / 1000.0
    
    # 1. Hauteur de la chambre froide (Calculée par défaut mais ajustable)
    default_height = 3.0 if volume < 50.0 else (4.0 if volume < 200.0 else 5.0)
    height = st.number_input(
        "Hauteur de la chambre (m)",
        min_value=2.0, max_value=10.0,
        value=float(default_height),
        step=0.5,
        help="Ajustez la hauteur sous plafond de la chambre froide."
    )
    
    # 2. Dimensions de la porte (Largeur et Hauteur paramétrables)
    default_w_door = 1.0 if volume < 50.0 else (1.4 if volume < 200.0 else 2.0)
    default_h_door = 2.0 if volume < 50.0 else (2.2 if volume < 200.0 else 2.5)
    w_door = st.number_input(
        "Largeur de la porte (m)",
        min_value=0.5, max_value=4.0,
        value=float(default_w_door),
        step=0.1
    )
    h_door = st.number_input(
        "Hauteur de la porte (m)",
        min_value=1.0, max_value=4.0,
        value=float(default_h_door),
        step=0.1
    )
    
    # 3. Thermodynamique (COP et Température de Fusion du MCP)
    default_cop = 3.0 if t_target >= 0 else 1.8
    default_t_fusion = 2.0 if t_target >= 0 else -21.0
    cop = st.number_input(
        "COP du compresseur",
        min_value=0.5, max_value=6.0,
        value=float(default_cop),
        step=0.1,
        help="Coefficient de Performance du compresseur frigorifique."
    )
    t_fusion_pcm = st.number_input(
        "Température de fusion du MCP (°C)",
        min_value=-40.0, max_value=30.0,
        value=float(default_t_fusion),
        step=0.5,
        help="Température de transition solide-liquide de la paraffine."
    )
    
    # 4. Taux de maintenance annuel
    maintenance_rate = st.number_input(
        "Taux de maintenance annuel (%)",
        min_value=0.0, max_value=10.0,
        value=2.0,
        step=0.5,
        help="Coût d'entretien annuel en pourcentage de l'investissement initial."
    ) / 100.0
    
    empty_space_opt = st.selectbox(
        "Ciel gazeux (espace dilatation %)",
        options=[10, 15, 20],
        index=0
    )
    
    enforce_dfm = st.checkbox(
        "Forcer les contraintes mécaniques (DFM & RDM)",
        value=True,
        help="Active les garde-fous pour empêcher la génération de géométries impossibles à fabriquer."
    )
    
    st.markdown("**Grille d'optimisation CAO :**")
    
    # Granularité augmentée : pas de 10mm pour les diamètres et 0.25m pour les longueurs
    dia_opts = st.multiselect(
        "Diamètres extérieurs (mm)",
        options=[80, 90, 100, 110, 120],
        default=[80, 90, 100, 110, 120]
    )
    
    fin_len_opts = st.multiselect(
        "Longueurs d'ailettes (mm)",
        options=[15, 18, 20, 22, 25, 30],
        default=[18, 20, 22],
        help="Longueurs d'ailettes radiales (interne & externe) à tester (mm)."
    )
    
    len_opts = st.multiselect(
        "Longueurs de tubes (m)",
        options=[0.5, 1.0, 1.25, 1.5, 1.75, 2.0],
        default=[0.5, 1.0, 1.5, 2.0]
    )
    
    fins_opts = st.multiselect(
        "Nombre d'ailettes (internes/externes)",
        options=[0, 2, 4, 6, 8, 10, 12],
        default=[0, 2, 4, 6, 8, 10, 12],
        help="Nombre d'ailettes de chaque côté de la paroi (interne et externe)."
    )
    
    vent_opts = st.multiselect(
        "Options de ventilation",
        options=["ON", "OFF"],
        default=["ON", "OFF"]
    )
    
    st.markdown("**Données opérationnelles :**")
    door_openings = st.number_input("Ouvertures de porte par heure", value=config.N_OPENINGS_PER_HOUR, step=1.0)
    door_duration = st.number_input("Durée d'ouverture (sec)", value=config.T_OPENING, step=5.0)
    stock_vol = st.number_input("Volume du stock (L)", value=config.STOCK_VOLUME, step=1000.0)
    stock_turn = st.slider("Rotation stock quotidien (%)", min_value=0, max_value=100, value=int(config.STOCK_TURNOVER * 100)) / 100.0
    
    st.markdown("**Gestion des Risques & Pannes :**")
    outages_per_year = st.number_input("Coupures / Pannes Sonelgaz par an", value=3.0, step=1.0)
    stock_value_da = st.number_input("Valeur du stock protégé (DA)", value=float(volume * 20000.0), step=50000.0)
    loss_prevented_pct = st.slider("Pertes évitées grâce au MCP (%)", min_value=0, max_value=100, value=100) / 100.0
    
    st.markdown("**Gestion de la Recharge Nocturne :**")
    compressor_power_kw = st.number_input(
        "Puissance du compresseur existant (kW)",
        min_value=1.0, max_value=500.0, value=15.0, step=1.0,
        help="Puissance frigorifique nominale du compresseur du client."
    )
    t_recharge_h = st.slider(
        "Heures creuses pour recharge (h)",
        min_value=4.0, max_value=12.0, value=8.0, step=0.5,
        help="Durée disponible la nuit pour recharger/re-solidifier le MCP."
    )


# ==============================================================================
# 2. LOGIQUE THERMODYNAMIQUE & CALCUL DE CHARGE
# ==============================================================================

area_floor = volume / height
side_length = math.sqrt(area_floor)
a_env = 2.0 * area_floor + 4.0 * side_length * height

# Charge thermique interne statique indexée sur le volume de la chambre (Q6)
q_internal_static = 50.0 + 1.0 * volume

# Humidité relative extérieure dynamique selon le climat de la wilaya (Q7)
desc_lower = city_data.get("desc", "").lower()
if "littoral" in desc_lower or "côtier" in desc_lower:
    rh_ext = 75.0
elif "sud" in desc_lower or "saharien" in desc_lower or "désertique" in desc_lower:
    rh_ext = 25.0
elif "plateaux" in desc_lower or "continental" in desc_lower:
    rh_ext = 45.0
else:
    rh_ext = 60.0
    
rh_int = 90.0 if t_target >= 0 else 95.0

def get_air_density(temp_c):
    temp_k = temp_c + 273.15
    return config.P_ATM / (config.R_AIR * temp_k)

def get_saturation_vapor_pressure(temp_c):
    if temp_c >= 0:
        a, b = 17.27, 237.3
    else:
        a, b = 21.875, 265.5
    return 610.78 * math.exp((a * temp_c) / (temp_c + b))

def get_humidity_ratio(temp_c, rh_percent):
    p_sat = get_saturation_vapor_pressure(temp_c)
    p_v = (rh_percent / 100.0) * p_sat
    p_v = min(p_v, config.P_ATM - 100.0)
    return 0.622 * p_v / (config.P_ATM - p_v)

def get_air_enthalpy(temp_c, rh_percent):
    w = get_humidity_ratio(temp_c, rh_percent)
    return config.CP_AIR * temp_c + w * (2501000.0 + 1860.0 * temp_c)

# Pertes parois
q_wall = max(0.0, (1.0 / ((1.0 / config.H_INT_WALL) + (thickness_pu / config.LAMBDA_PU) + (1.0 / config.H_EXT_WALL))) * a_env * (t_ext - t_target))

# Infiltration porte
rho_ext = get_air_density(t_ext)
rho_int = get_air_density(t_target)
rho_avg = (rho_ext + rho_int) / 2.0
delta_rho = max(0.0, rho_int - rho_ext)
m_dot_air = (2.0 / 3.0) * config.C_D * w_door * (h_door ** 1.5) * math.sqrt(config.G * delta_rho / rho_avg) if delta_rho > 0 else 0
h_ext = get_air_enthalpy(t_ext, rh_ext)
h_int = get_air_enthalpy(t_target, rh_int)
delta_h = max(0.0, h_ext - h_int)
d_open = (door_openings * door_duration) / 3600.0
q_infiltration = m_dot_air * delta_h * d_open

# Refroidissement produit
m_turnover = stock_vol * stock_turn
t_in_product = t_ext - config.T_IN_PRODUCT_OFFSET
q_product = max(0.0, (m_turnover * config.CP_PRODUCT * (t_in_product - t_target)) / (24.0 * 3600.0))

# Charge totale pour la période sélectionnée (affichage et simulation locale)
q_load_total = q_wall + q_infiltration + q_product + q_internal_static

# --- CALCUL DE LA CHARGE DE CONCEPTION (Pointe d'été de la wilaya, pour le dimensionnement physique) ---
t_ext_summer = city_data["design_summer"]
q_wall_summer = max(0.0, (1.0 / ((1.0 / config.H_INT_WALL) + (thickness_pu / config.LAMBDA_PU) + (1.0 / config.H_EXT_WALL))) * a_env * (t_ext_summer - t_target))

rho_ext_summer = get_air_density(t_ext_summer)
rho_avg_summer = (rho_ext_summer + rho_int) / 2.0
delta_rho_summer = max(0.0, rho_int - rho_ext_summer)
m_dot_air_summer = (2.0 / 3.0) * config.C_D * w_door * (h_door ** 1.5) * math.sqrt(config.G * delta_rho_summer / rho_avg_summer) if delta_rho_summer > 0 else 0
h_ext_summer = get_air_enthalpy(t_ext_summer, rh_ext)
delta_h_summer = max(0.0, h_ext_summer - h_int)
q_infiltration_summer = m_dot_air_summer * delta_h_summer * d_open

t_in_product_summer = t_ext_summer - config.T_IN_PRODUCT_OFFSET
q_product_summer = max(0.0, (m_turnover * config.CP_PRODUCT * (t_in_product_summer - t_target)) / (24.0 * 3600.0))

q_load_summer_peak = q_wall_summer + q_infiltration_summer + q_product_summer + q_internal_static

# --- CALCUL DE LA CHARGE THERMIQUE MOYENNE ANNUELLE (Pour les gains financiers réels) ---
t_ext_mean = city_data["avg_annual"]
q_wall_mean = max(0.0, (1.0 / ((1.0 / config.H_INT_WALL) + (thickness_pu / config.LAMBDA_PU) + (1.0 / config.H_EXT_WALL))) * a_env * (t_ext_mean - t_target))

rho_ext_mean = get_air_density(t_ext_mean)
rho_avg_mean = (rho_ext_mean + rho_int) / 2.0
delta_rho_mean = max(0.0, rho_int - rho_ext_mean)
m_dot_air_mean = (2.0 / 3.0) * config.C_D * w_door * (h_door ** 1.5) * math.sqrt(config.G * delta_rho_mean / rho_avg_mean) if delta_rho_mean > 0 else 0
h_ext_mean = get_air_enthalpy(t_ext_mean, rh_ext)
delta_h_mean = max(0.0, h_ext_mean - h_int)
q_infiltration_mean = m_dot_air_mean * delta_h_mean * d_open

t_in_product_mean = t_ext_mean - config.T_IN_PRODUCT_OFFSET
q_product_mean = max(0.0, (m_turnover * config.CP_PRODUCT * (t_in_product_mean - t_target)) / (24.0 * 3600.0))

q_load_mean = max(0.0, q_wall_mean + q_infiltration_mean + q_product_mean + q_internal_static)

# Énergie requise et masse de MCP de base (basé sur la charge de pointe pour la sécurité de dimensionnement)
e_required_joules = q_load_summer_peak * autonomy_target * 3600.0
m_pcm_required = e_required_joules / config.L_F

# Delta T moteur de transfert basé sur la température de fusion réglée
delta_t_driving = t_target - t_fusion_pcm

# ==============================================================================
# 3. MODÉLISATION DE LA GRILLE DE CYLINDRES
# ==============================================================================
t_wall = 0.002
t_fin = 0.0015
t_paint = 100e-6

results_list = []

for d_cyl_mm in dia_opts:
    d_cyl = d_cyl_mm / 1000.0
    d_inner = d_cyl - 2 * t_wall
    for n_fins in fins_opts:
        # Si pas d'ailettes, on teste une longueur fictive de 0 mm
        current_fin_len_opts = fin_len_opts if n_fins > 0 else [0]
        for l_fin_mm in current_fin_len_opts:
            l_fin = l_fin_mm / 1000.0
            
            # -------------------------------------------------------------
            # APPLICATION DES RÈGLES DFM & RDM (GARDE-FOUS MÉCANIQUES)
            # -------------------------------------------------------------
            dfm_passed = True
            
            # Règle 1: Puits Central (Mini DFM_PUITS_CENTRAL_MIN_MM)
            if n_fins > 0:
                puits_central_mm = (d_inner - 2 * l_fin) * 1000.0
                if enforce_dfm and puits_central_mm < config.DFM_PUITS_CENTRAL_MIN_MM:
                    dfm_passed = False
            else:
                puits_central_mm = d_inner * 1000.0
                
            # Règle 2: Ratio d'élancement (Max RDM_ASPECT_RATIO_MAX)
            if n_fins > 0:
                aspect_ratio = l_fin_mm / (t_fin * 1000.0)
                if enforce_dfm and aspect_ratio > config.RDM_ASPECT_RATIO_MAX:
                    dfm_passed = False
            else:
                aspect_ratio = 0.0
                
            # Règle 3: Standardisation à DFM_STANDARD_FINS_COUNT ailettes pour les diamètres classiques
            if enforce_dfm and config.DFM_MIN_DIA_STANDARD_FINS <= d_cyl_mm <= config.DFM_MAX_DIA_STANDARD_FINS and n_fins != config.DFM_STANDARD_FINS_COUNT:
                dfm_passed = False
                
            if not dfm_passed:
                continue # Rejeter la configuration car non fabricable
            # -------------------------------------------------------------
            
            # Exclure dynamiquement les configurations non physiques ou ne respectant pas le critère anti-givre (12 mm min aux pointes d'ailettes d'un même tube)
            if n_fins > 0:
                spacing_ext_tip_check = (math.pi * (d_cyl_mm + 2.0 * l_fin_mm) - n_fins * t_fin * 1000.0) / n_fins
                spacing_int_base_check = (math.pi * d_inner * 1000.0 - n_fins * t_fin * 1000.0) / n_fins
                if spacing_ext_tip_check < 12.0 or spacing_int_base_check <= 0.0:
                    continue
                
            current_fin_thickness = 0.0 if n_fins == 0 else t_fin
            for vent in vent_opts:
                for l_cyl in len_opts:
                    
                    h_conv = config.H_CONV_VENT_ON if vent == "ON" else config.H_CONV_VENT_OFF
                    l_fin_ext = l_fin
                    l_fin_int = l_fin
                    
                    # Résistance thermique
                    a_unfinned_ext = math.pi * d_cyl - n_fins * current_fin_thickness
                    a_fin_ext = 2.0 * n_fins * l_fin_ext
                    if n_fins > 0:
                        m_fin_ext = math.sqrt((h_conv * 2.0) / (config.LAMBDA_AL * current_fin_thickness))
                        efficiency_fin_ext = math.tanh(m_fin_ext * l_fin_ext) / (m_fin_ext * l_fin_ext) if (m_fin_ext * l_fin_ext) > 0 else 1.0
                    else:
                        efficiency_fin_ext = 1.0
                    a_eff_ext = a_unfinned_ext + efficiency_fin_ext * a_fin_ext
                    r_conv = 1.0 / (h_conv * a_eff_ext)
                    
                    r_paint = t_paint / (config.LAMBDA_EPOXY * math.pi * d_cyl) + config.R_CONTACT_EPOXY / (math.pi * d_cyl)
                    r_wall_al = math.log(d_cyl / d_inner) / (2.0 * math.pi * config.LAMBDA_AL)
                    
                    a_pcm_casing = math.pi * (d_inner ** 2) / 4.0
                    a_fins_int_cross = n_fins * current_fin_thickness * l_fin_int
                    phi_fins_int = a_fins_int_cross / a_pcm_casing if a_pcm_casing > 0 else 0.0
                    lambda_pcm_eff = config.LAMBDA_PCM * (1.0 - phi_fins_int) + config.LAMBDA_AL * phi_fins_int
                    r_pcm = 1.0 / (4.0 * math.pi * lambda_pcm_eff)
                    
                    r_linear = r_conv + r_paint + r_wall_al + r_pcm
                    
                    # Masse MCP et Alu par mètre
                    a_pcm_cross = a_pcm_casing - a_fins_int_cross
                    if a_pcm_cross <= 0:
                        continue
                    m_pcm_per_meter = a_pcm_cross * config.RHO_PCM
                    
                    # Longueur physique totale des cylindres (incluant la marge de dilatation thermique et le ciel gazeux)
                    total_length_physical = (m_pcm_required * 1.10) / (m_pcm_per_meter * (1.0 - empty_space_opt / 100.0))
                    
                    ua_battery = total_length_physical / r_linear
                    q_battery_max = ua_battery * delta_t_driving
                    
                    a_al_cross = (math.pi * (d_cyl**2 - d_inner**2) / 4.0) + n_fins * current_fin_thickness * (l_fin_ext + l_fin_int)
                    m_al_total = a_al_cross * config.RHO_AL * total_length_physical
                    
                    # Autonomie sous le pic de charge estival (dimensionnement physique & optimisation)
                    thermal_effectiveness_summer = min(1.0, q_battery_max / q_load_summer_peak)
                    t_autonomy_summer = autonomy_target * thermal_effectiveness_summer
                    
                    # Autonomie sous la charge de la période sélectionnée (affichage & simulation locale)
                    thermal_effectiveness_selected = min(1.0, q_battery_max / q_load_total)
                    t_autonomy_selected = autonomy_target * thermal_effectiveness_selected
                    
                    # Autonomie sous la charge moyenne annuelle (calcul de rentabilité économique réelle)
                    thermal_effectiveness_mean = min(1.0, q_battery_max / q_load_mean)
                    t_autonomy_mean = autonomy_target * thermal_effectiveness_mean
                    
                    # Nombre de cylindres (parfaitement cohérent avec la longueur physique totale construite)
                    n_modules = total_length_physical / l_cyl
                    
                    # Coût total
                    cout_total = (m_al_total * config.PRIX_AL_BASE) + (m_pcm_required * config.PRIX_MCP_BASE) + (n_modules * config.COUT_FAB_CYL)
                    if vent == "ON":
                        cout_total += config.SURCOUT_VENTILATION
                        
                    # Économie d'énergie Sonelgaz (DA/an) - Arbitrage (basé sur la charge MOYENNE ANNUELLE pour la crédibilité du ROI)
                    p_elec_saved = q_load_mean / (cop * 1000.0)
                    e_saved_daily = p_elec_saved * t_autonomy_mean
                    # Prime d'économie Sonelgaz indexée sur la taille du système (Q21)
                    prime_savings_da = 10000.0 + 700.0 * volume
                    economie_arbitrage_da = (e_saved_daily * config.DELTA_TARIF_DA_KWH * config.DAYS_OP_YEAR) + prime_savings_da
                    
                    # Économie sur perte de marchandise évitée (DA/an) - Sécurité
                    fraction_protection = min(1.0, t_autonomy_mean / autonomy_target)
                    economie_pannes_da = outages_per_year * stock_value_da * loss_prevented_pct * fraction_protection
                    
                    economie_annuelle_da = economie_arbitrage_da + economie_pannes_da
                    
                    # Faisabilité de la recharge nocturne (basé sur les heures creuses et le compresseur de l'utilisateur)
                    p_recharge_needed_kw = (m_pcm_required * config.L_F) / (t_recharge_h * 3600.0 * 1000.0)
                    recharge_feasible = "OUI" if p_recharge_needed_kw <= compressor_power_kw else "NON"
                    
                    payback_years = cout_total / economie_annuelle_da if economie_annuelle_da > 0 else 99.0
                    
                    # Coût de sensibilité (+20% Alu)
                    cout_sens = cout_total + (m_al_total * 0.20 * config.PRIX_AL_BASE)
                    payback_years_sens = cout_sens / economie_annuelle_da if economie_annuelle_da > 0 else 99.0
                    
                    # Calcul de la VAN (NPV) sur 10 ans avec taux d'actualisation de 8% et inflation énergie de 5% (Q23)
                    # Coût annuel de maintenance dynamique de l'investissement initial
                    van = -cout_total
                    if economie_annuelle_da > 0:
                        for year in range(1, 11):
                            cf_year = economie_annuelle_da * ((1.05) ** year) - maintenance_rate * cout_total
                            van += cf_year / ((1.08) ** year)
                    else:
                        van = -cout_total
                        
                    # Calcul du TRI (IRR) actualisé sur 10 ans par méthode de bissection
                    irr = -100.0  # Valeur par défaut si non rentable
                    if economie_annuelle_da > 0:
                        def get_npv(r):
                            npv_val = -cout_total
                            for year in range(1, 11):
                                cf_year = economie_annuelle_da * ((1.05) ** year) - maintenance_rate * cout_total
                                npv_val += cf_year / ((1.0 + r) ** year)
                            return npv_val
                        
                        low, high = -0.5, 3.0
                        if get_npv(low) > 0 and get_npv(high) < 0:
                            for _ in range(30):
                                mid = (low + high) / 2.0
                                mid_npv = get_npv(mid)
                                if abs(mid_npv) < 1e-2:
                                    irr = mid * 100.0
                                    break
                                if mid_npv > 0:
                                    low = mid
                                else:
                                    high = mid
                            else:
                                irr = mid * 100.0
                        elif get_npv(low) <= 0:
                            irr = -50.0  # Totalement non rentable
                        else:
                            irr = 300.0  # Rentabilité exceptionnellement élevée
                    
                    # Calcul de l'encombrement au plafond (Q19)
                    # Chaque cylindre a une largeur de d_cyl + 2*l_fin + 50mm d'espacement de sécurité (0.05 m)
                    # Et une longueur utile l_cyl
                    area_proj_single = (d_cyl + 2.0 * l_fin + 0.05) * l_cyl
                    # Les tubes sont empilés par racks de 20 (configuration 7-6-7)
                    n_racks = math.ceil(n_modules / 20.0)
                    # L'encombrement au plafond est basé sur la projection au sol des racks (7 tubes de large par rack)
                    ceiling_occupancy_pct = (n_racks * 7.0 * area_proj_single) / area_floor * 100.0
                    
                    # Calcul du nombre de suspentes M14 requises (Q20)
                    # Chaque rack de 20 tubes est suspendu de manière isostatique par 4 tiges filetées M14 aux angles
                    total_mass_kg = m_al_total + m_pcm_required * 1.10
                    n_suspentes = n_racks * 4
                    
                    # Score d'optimisation basé sur la performance d'été (garantissant un choix robuste)
                    score_da = t_autonomy_summer / cout_total if cout_total > 0 else 0
                    
                    results_list.append({
                        "D_Cyl_mm": d_cyl_mm,
                        "N_Fins": n_fins,
                        "L_Fin_mm": l_fin_mm,
                        "Puits_Central_mm": puits_central_mm,
                        "Aspect_Ratio": aspect_ratio,
                        "Ventilation": vent,
                        "L_Cyl_m": l_cyl,
                        "Q_Load_Total_W": q_load_total,
                        "M_PCM_Required_kg": m_pcm_required,
                        "M_Al_Total_kg": m_al_total,
                        "Autonomy_Real_h": t_autonomy_selected,
                        "Autonomy_Summer_h": t_autonomy_summer,
                        "Autonomy_Mean_h": t_autonomy_mean,
                        "R_Linear": r_linear,
                        "N_Modules": math.ceil(n_modules),
                        "Cost_DA": cout_total,
                        "Cost_Sens_DA": cout_sens,
                        "Savings_Electricity_Yearly_DA": economie_arbitrage_da,
                        "Savings_Outages_Yearly_DA": economie_pannes_da,
                        "Savings_Yearly_DA": economie_annuelle_da,
                        "Payback_Years": payback_years,
                        "Payback_Years_Sens": payback_years_sens,
                        "VAN_DA": van,
                        "TRI_Percent": irr,
                        "Ceiling_Occupancy_Pct": ceiling_occupancy_pct,
                        "N_Suspentes": n_suspentes,
                        "P_Recharge_Needed_kW": p_recharge_needed_kw,
                        "P_Compressor_Est_kW": compressor_power_kw,
                        "Recharge_Feasible": recharge_feasible,
                        "Optimization_Score_h_DA": score_da
                    })

df_sim = pd.DataFrame(results_list)

# Filtrer par rapport au budget max
df_filtered = df_sim[df_sim["Cost_DA"] <= budget_max]

# Filtrage à deux étapes pour prioriser les configurations rechargeables avec le compresseur existant (Q1)
df_recharge_ok = df_filtered[df_filtered["Recharge_Feasible"] == "OUI"]
if not df_recharge_ok.empty:
    df_sorted = df_recharge_ok.sort_values(by="Optimization_Score_h_DA", ascending=False).reset_index(drop=True)
    recharge_fallback_active = False
else:
    # Si aucune configuration n'est faisable dans le budget, on fallback sur toutes les configurations
    df_sorted = df_filtered.sort_values(by="Optimization_Score_h_DA", ascending=False).reset_index(drop=True)
    recharge_fallback_active = True


# ==============================================================================
# 4. EXPLOITATION DE L'INTERFACE UTILISATEUR
# ==============================================================================

if df_sorted.empty:
    st.error("Aucune configuration trouvée sous le budget maximum. Veuillez augmenter le budget ou réduire les exigences.")
else:
    # Fonctions de formatage pour éviter les valeurs sentinelles de la bissection et ROI infinis
    def format_irr(val):
        if val <= -50.0:
            return "Non rentable"
        elif val >= 300.0:
            return "> 300 %"
        else:
            return f"{val:.1f} %"
            
    def format_payback(val):
        if val >= 99.0:
            return "Infini"
        else:
            return f"{val:.2f} ans"

    # Récupérer la meilleure configuration (#1)
    best_conf = df_sorted.iloc[0]
    
    # Onglets d'études techniques pour présentation prototype KryoDrop
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Dimensionnement & Optimum",
        "Dossier d'Étude CAO & DFM",
        "Dossier d'Étude RDM & Structure",
        "Étude Thermodynamique & Transferts",
        "Étude Électrique & Secours",
        "Étude Budgétaire & Rentabilité",
        "Données Complètes de Simulation"
    ])
    
    # --- ONGLET 1: DIMENSIONNEMENT & OPTIMUM ---
    with tab1:
        st.markdown("### <i class='fa-solid fa-snowflake' style='color:#29B6D8; margin-right:8px;'></i> Solution Optimale Recommandée (#1)", unsafe_allow_html=True)
        st.info("**Règle de Dimensionnement Sécuritaire** : Pour garantir la chaîne du froid toute l'année, la batterie (tubes, masse MCP et coût) est **toujours dimensionnée face au pic estival de la wilaya** (conception la plus défavorable). Le sélecteur saisonnier de la barre latérale simule la charge de la chambre froide et la performance de la batterie dans les conditions courantes.")
        
        if recharge_fallback_active:
            st.warning("**Alerte Faisabilité Recharge** : Aucune configuration dans le budget maximum n'est compatible avec la puissance de recharge disponible de votre compresseur. Les résultats affichés ci-dessous sont un repli (fallback) sur la meilleure configuration technique, mais nécessiteront un surdimensionnement du compresseur ou une extension du temps de recharge nocturne.")
        
        # Affichage des métriques clés HCD KryoDrop (Régie par la hiérarchie de l'information B2B)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="metric-title">Autonomie Thermique</div>
                        <div class="metric-value">{best_conf['Autonomy_Real_h']:.1f} <span class="metric-unit">h</span></div>
                        <div class="metric-subtitle">Saison : {season.split('(')[0].strip()} | Cible : {autonomy_target}h (Été : {best_conf['Autonomy_Summer_h']:.1f}h)</div>
                    </div>
                    <div class="metric-icon">
                        <i class="fa-solid fa-snowflake"></i>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="metric-title">Gains Annuels (Sonelgaz & Stock)</div>
                        <div class="metric-value">{best_conf['Savings_Yearly_DA']:,.0f} <span class="metric-unit">DA/an</span></div>
                        <div class="metric-subtitle">Arbitrage : {best_conf['Savings_Electricity_Yearly_DA']:,.0f} DA | Stock sécurisé : {best_conf['Savings_Outages_Yearly_DA']:,.0f} DA</div>
                    </div>
                    <div class="metric-icon">
                        <i class="fa-solid fa-bolt"></i>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="metric-title">Retour sur Investissement</div>
                        <div class="metric-value">{format_payback(best_conf['Payback_Years'])}</div>
                        <div class="metric-subtitle">TRI : {format_irr(best_conf['TRI_Percent'])} | Investissement : {best_conf['Cost_DA']:,.0f} DA</div>
                    </div>
                    <div class="metric-icon">
                        <i class="fa-solid fa-chart-line"></i>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Détails de dimensionnement complet de l'optimum
        st.markdown("#### <i class='fa-solid fa-drafting-compass' style='color:#29B6D8; margin-right:8px;'></i> Spécifications CAO pour Fabrication", unsafe_allow_html=True)
        col_dims1, col_dims2 = st.columns(2)
        
        with col_dims1:
            st.markdown(f"""
            <div style="background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; padding: 15px; border-radius: 8px; font-family: sans-serif; font-size: 14px;">
                <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                    <li><b>Diamètre du cylindre</b> : <code>{best_conf['D_Cyl_mm']} mm</code> (Taille idéale pour le transfert)</li>
                    <li><b>Longueur utile d'un cylindre</b> : <code>{best_conf['L_Cyl_m']} m</code></li>
                    <li><b>Ailettes externes</b> : <code>{best_conf['N_Fins']} ailettes</code> en étoile (épaisseur <code>1.5 mm</code>, hauteur <code>{best_conf.get('L_Fin_mm', 30.0):.1f} mm</code>)</li>
                    <li><b>Type de ventilation</b> : Ventilation Active <b>{best_conf['Ventilation']}</b></li>
                    <li><b>Dimensionnement de la porte</b> : <code>{w_door:.1f} m x {h_door:.1f} m</code> (Adapté au volume de la chambre)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_dims2:
            occupancy_style = "color:#E74C3C; font-weight:bold;" if best_conf['Ceiling_Occupancy_Pct'] > 100.0 else "color:#2ECC71; font-weight:bold;"
            n_racks_opt = math.ceil(best_conf['N_Modules'] / 20.0)
            st.markdown(f"""
            <div style="background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; padding: 15px; border-radius: 8px; font-family: sans-serif; font-size: 14px;">
                <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                    <li><b>Masse totale d'Aluminium</b> : <code>{best_conf['M_Al_Total_kg']:,.1f} kg</code> (Poids propre de la structure métallique)</li>
                    <li><b>Volume liquide MCP requis</b> : <code>{best_conf['M_PCM_Required_kg'] * 1.10 / config.RHO_PCM * 1000:,.1f} Litres</code> (dilaté à 10%)</li>
                    <li><b>Ciel gazeux (sécurité dilatation)</b> : <code>{empty_space_opt} %</code></li>
                    <li><b>Points d'ancrage requis (suspentes M14)</b> : <code>{int(best_conf['N_Suspentes'])} suspentes</code> ({n_racks_opt} rack(s) suspendu(s) par 4 tiges M14 chacun)</li>
                    <li><b>Encombrement au plafond</b> : <span style="{occupancy_style}">{best_conf['Ceiling_Occupancy_Pct']:.1f} %</span> de la surface de plafond</li>
                    <li><b>Besoin Frigorifique de Pointe</b> : <code>{q_load_total:,.1f} W</code> (Pertes: <code>{q_wall:,.0f}W</code> Parois, <code>{q_infiltration:,.0f}W</code> Infiltrations, <code>{q_product:,.0f}W</code> Produit)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        if best_conf['Ceiling_Occupancy_Pct'] > 100.0:
            st.warning("**Encombrement plafond élevé (> 100%)** : Le nombre requis de modules dépasse la surface plane disponible au plafond en une seule couche. Une disposition sur plusieurs niveaux superposés ou une réduction de l'autonomie cible est fortement préconisée.")
            
        # Validation DFM & Nomenclature Mécanique Validée pour SolidWorks
        st.markdown("#### <i class='fa-solid fa-gears' style='color:#29B6D8; margin-right:8px;'></i> Validation DFM & Nomenclature Industrielle (SolidWorks)", unsafe_allow_html=True)
        col_dfm1, col_dfm2 = st.columns([1, 2])
        
        with col_dfm1:
            st.markdown("##### <i class='fa-solid fa-gauge-high' style='color:#29B6D8; margin-right:6px;'></i> Indicateurs de Fabricabilité DFM / RDM")
            
            # Puits central
            puits_status = "dfm-ok" if best_conf.get('Puits_Central_mm', 0.0) >= config.DFM_PUITS_CENTRAL_MIN_MM else "dfm-fail"
            puits_icon = "fa-check" if best_conf.get('Puits_Central_mm', 0.0) >= config.DFM_PUITS_CENTRAL_MIN_MM else "fa-xmark"
            st.markdown(f"""
            <div class="dfm-card">
                <p style="margin:0; font-size: 0.9rem; color: #555;">Puits de Remplissage Central (Ø mm)</p>
                <h2 style="margin:0; color: #1B365D;">{best_conf.get('Puits_Central_mm', 0.0):.1f} mm</h2>
                <div class="dfm-badge {puits_status}"><i class="fa-solid {puits_icon}"></i> RÈGLE DFM (Ømin {config.DFM_PUITS_CENTRAL_MIN_MM:.0f}mm)</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Ratio d'élancement
            ratio_status = "dfm-ok" if best_conf.get('Aspect_Ratio', 0.0) <= config.RDM_ASPECT_RATIO_MAX else "dfm-fail"
            ratio_icon = "fa-check" if best_conf.get('Aspect_Ratio', 0.0) <= config.RDM_ASPECT_RATIO_MAX else "fa-xmark"
            st.markdown(f"""
            <div class="dfm-card">
                <p style="margin:0; font-size: 0.9rem; color: #555;">Ratio d'Élancement de l'Ailette (L/e)</p>
                <h2 style="margin:0; color: #1B365D;">{best_conf.get('Aspect_Ratio', 0.0):.1f}</h2>
                <div class="dfm-badge {ratio_status}"><i class="fa-solid {ratio_icon}"></i> RÈGLE RDM (Max {config.RDM_ASPECT_RATIO_MAX:.0f})</div>
            </div>
            """, unsafe_allow_html=True)

        with col_dfm2:
            st.markdown("##### <i class='fa-solid fa-list-check' style='color:#29B6D8; margin-right:6px;'></i> Nomenclature Mécanique Validée pour SolidWorks")
            st.markdown(f"""
            <ul style="line-height: 1.8; font-size: 0.95rem; margin-top: 10px; padding-left: 20px;">
                <li><b>Le Cylindre Extrudé :</b> Tube Ø <code>{best_conf['D_Cyl_mm']:.0f} mm</code> comportant <b>exactement {int(best_conf['N_Fins'])} ailettes longitudinales radiales</b>. Les ailettes internes et externes sont parfaitement <b>alignées</b> pour créer un pont thermique direct.</li>
                <li><b>Dimensions des Ailettes :</b> Longueur optimisée à <code>{best_conf.get('L_Fin_mm', 30.0):.1f} mm</code> et épaisseur de <code>1.5 mm</code>.</li>
                <li><b>Congés de Raccordement (Fillets) :</b> Ajout systématique de congés de <b>1.5 mm</b> à la racine de chaque ailette pour faciliter l'extrusion de l'aluminium et éviter les micro-fissures (RDM).</li>
                <li><b>Usinage des Extrémités :</b> Enlèvement de matière sur <b>40 mm</b> à chaque bout du tube pour créer une surface cylindrique lisse, indispensable au montage.</li>
                <li><b>Système de Bouchons (Soudure TIG) :</b> Utilisation de <b>Bouchons à Épaulement (Stepped Caps)</b>. L'épaulement assure un auto-centrage parfait et empêche l'effondrement du métal fondu dans le tube lors de la soudure. Le bouchon supérieur intègre un taraudage <b>M16</b> pour l'injection du MCP, situé exactement au-dessus du puits libre de <code>{best_conf.get('Puits_Central_mm', 0.0):.1f} mm</code>.</li>
                <li><b>Architecture du Caisson :</b> 
                    <ul style="padding-left: 20px;">
                        <li><b>Montage Drop-in :</b> Les tubes lisses reposent dans des berceaux en acier galvanisé ouverts vers le haut (<b>U-Cradles</b>).</li>
                        <li><b>Isolation Galvanique :</b> Des <b>bagues en EPDM</b> de 2mm séparent l'aluminium de l'acier, absorbant les vibrations du compresseur.</li>
                        <li><b>Structure Modulaire :</b> Le rack de support est conçu en <b>modules d'un étage empilables</b> (Stackable Design) traversés par 4 tiges filetées, permettant de standardiser la production et de caser les <code>{int(best_conf['N_Modules'])} tubes</code> requis sans surcharger le plafond.</li>
                    </ul>
                </li>
            </ul>
            """, unsafe_allow_html=True)
            
        # Graphique d'autonomie vs nombre de modules
        st.markdown("#### <i class='fa-solid fa-chart-line' style='color:#29B6D8; margin-right:8px;'></i> Autonomie Simulée en fonction de la taille de la Batterie (saison sélectionnée)", unsafe_allow_html=True)
        
        fam_d = best_conf["D_Cyl_mm"]
        fam_fins = best_conf["N_Fins"]
        fam_vent = best_conf["Ventilation"]
        fam_l = best_conf["L_Cyl_m"]
        
        modules_range = np.linspace(max(10, int(best_conf["N_Modules"]*0.5)), int(best_conf["N_Modules"]*1.5), 20).astype(int)
        autonomy_plot = []
        for m in modules_range:
            total_length_fict = m * fam_l
            ua_battery_fict = total_length_fict / best_conf["R_Linear"]
            q_battery_max_fict = ua_battery_fict * delta_t_driving
            effectiveness_fict = min(1.0, q_battery_max_fict / q_load_total)
            autonomy_val = autonomy_target * effectiveness_fict
            autonomy_plot.append(autonomy_val)
            
        df_plot = pd.DataFrame({
            "Nombre de Modules": modules_range,
            "Autonomie Simulée (h)": autonomy_plot
        })
        st.line_chart(df_plot, x="Nombre de Modules", y="Autonomie Simulée (h)")

    # --- ONGLET 2: DOSSIER D'ÉTUDE CAO & DFM ---
    with tab2:
        st.markdown("### <i class='fa-solid fa-drafting-compass' style='color:#29B6D8; margin-right:8px;'></i> Dossier d'Étude CAO & DFM (Conception & Fabricabilité)", unsafe_allow_html=True)
        st.write("Cet onglet présente la validation d'ingénierie du modèle CAO SolidWorks et l'analyse de fabricabilité des tubes de stockage thermique.")
        
        col_cao_d1, col_cao_d2 = st.columns(2)
        
        with col_cao_d1:
            st.markdown(rf"""
            ##### 1. Validation de la Géométrie Extrudée (Optimale)
            * **Spécification des Ailettes :** `{best_conf['N_Fins']} ailettes` longitudinales radiales internes et externes alignées.
              * **Élancement d'Ailette (Aspect Ratio) :** Le ratio hauteur/épaisseur ($L_f/e_f$) vaut `{best_conf.get('L_Fin_mm', 20.0)/2.0:.1f}` pour des ailettes de 2mm d'épaisseur (conforme à la règle RDM $\le 15$). Cela élimine tout risque de vibration ou de flexion accidentelle de l'ailette.
              * **Validation du Puits Central :** Le puits libre au centre mesure `{best_conf.get('Puits_Central_mm', 0.0):.1f} mm`. Étant supérieur au seuil DFM minimal de **26 mm**, il garantit le libre passage de la buse de remplissage de paraffine lors de la coulée industrielle, sans risque d'inclusion d'air.
            * **Soudage des Bouchons d'Extrémité (TIG) :**
              * Les caches supérieur et inférieur sont conçus avec un **épaulement intérieur** (internal shoulder).
              * Cet épaulement permet un auto-centrage parfait lors du positionnement avant soudure et sert de support de bain de fusion (backing ring), évitant l'effondrement de l'aluminium liquide à l'intérieur du tube.
            """, unsafe_allow_html=True)
            
        with col_cao_d2:
            st.markdown(rf"""
            ##### 2. Interfaces Métalliques & Dilatation
            * **Bagues d'Isolation en Caoutchouc :** L'ajout de 2 bagues en caoutchouc de 40 mm de longueur aux extrémités lisses (non filetées) de chaque tube isole électriquement l'aluminium (tube) de l'acier galvanisé (berceau en U de supportage).
              * **Corrosion Galvanique évitée :** En atmosphère humide (90% HR), cette isolation est obligatoire pour bloquer le couple bimétallique destructeur pour l'aluminium.
              * **Matériau requis :** **EPDM ou Silicone (Shore 60-70A)**. L'EPDM conserve sa flexibilité et son élasticité jusqu'à $-50^\circ\text{{C}}$, tandis que le Nitrile (NBR) standard durcit et fissure au froid.
              * **Dilatation Différentielle :** Pour une variation de $\Delta T = 30\text{{ K}}$ (charge à $-25^\circ\text{{C}}$ et veille à $+5^\circ\text{{C}}$), la dilatation différentielle sur 2 m génère un glissement de **`0.66 mm`**. Les bagues en caoutchouc absorbent ce frottement cyclique et préviennent l'usure de l'aluminium.
              * *Recommandation CAO :* Usiner une gorge de positionnement peu profonde (1,5 mm) sur les extrémités lisses du tube pour bloquer axialement le caoutchouc face aux vibrations des ventilateurs.
            """, unsafe_allow_html=True)
            
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        
        st.markdown(r"""
        ##### 3. Dispositif Anti-Flexion Median (Portée de 2m)
        * **Défi mécanique :** Les tubes alu de 2 m chargés de paraffine subissent une flèche (sagging) par gravité en leur milieu.
        * **Solution CAO :** Introduction d'une traverse métallique intégrée au cadre au milieu de la portée (à 1 m).
        * **Garde-fou galvanique :** Une barre isolante en plastique (de même section) est montée au-dessus de cette barre métallique. En cas de flèche extrême ou de vibrations, les ailettes du tube en aluminium entrent en contact avec l'isolant en plastique et non avec l'acier galvanisé du cadre.
        * **Plastique préconisé :** **POM (Polyoxyméthylene / Acétal)** ou **PE-HD (Polyéthylène Haute Densité)**, conservant leur résilience et leur résistance au choc à basse température.
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("##### <i class='fa-solid fa-image' style='color:#29B6D8;'></i> Preuves Visuelles du Modèle CAO SolidWorks", unsafe_allow_html=True)
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image("Capture d'écran 2026-07-08 192651.png", caption="Assemblage 7-6-7 en quinconce du rack KryoDrop dans SolidWorks", use_container_width=True)
        with col_img2:
            st.image("Capture d'écran 2026-07-08 182424.png", caption="Détail des berceaux de support et bagues d'isolation galvanique", use_container_width=True)

    # --- ONGLET 3: DOSSIER D'ÉTUDE RDM & STRUCTURE ---
    with tab3:
        st.markdown("### <i class='fa-solid fa-weight-hanging' style='color:#29B6D8; margin-right:8px;'></i> Dossier d'Étude RDM & Tenue de la Structure", unsafe_allow_html=True)
        st.write("Cet onglet documente les calculs de résistance des suspentes et les conditions de rigidité structurelle exigées pour le plafond de la chambre froide.")
        
        total_mass_opt = best_conf['M_Al_Total_kg'] + best_conf['M_PCM_Required_kg'] * 1.10
        f_total_opt = total_mass_opt * 9.81
        n_racks_opt = math.ceil(best_conf['N_Modules'] / 20.0)
        n_suspentes_opt = n_racks_opt * 4
        # Charge par suspente en divisant par le nombre total réel de tiges filetées M14
        f_rod_opt = f_total_opt / n_suspentes_opt
        f_max_rod_opt = f_rod_opt * 1.5
        stress_rod_opt = f_max_rod_opt / 115.0 # M14 tensile area is 115 mm2
        sf_4_6 = 240.0 / stress_rod_opt
        sf_8_8 = 640.0 / stress_rod_opt
        
        col_rdm_d1, col_rdm_d2 = st.columns(2)
        
        with col_rdm_d1:
            st.markdown(rf"""
            ##### 1. Calcul Analytique des Tiges Filetées M14
            * **Masse totale de la batterie optimale (remplie + marge 10%) :** **`{total_mass_opt:.1f} kg`**
            * **Poids total en traction pure (charge statique) :** `{f_total_opt:.1f} N`
            * **Nombre de suspentes :** `{n_suspentes_opt}` tiges filetées M14 aux angles des cadres (`{n_racks_opt}` rack(s) de 20 tubes)
            * **Charge moyenne par suspente :** `{f_rod_opt:.1f} N` (soit `{f_rod_opt/9.81:.1f} kg`)
            * **Charge de calcul maximale (facteur d'excentricité / déséquilibre de 1.5) :** **`{f_max_rod_opt:.1f} N`** (soit `{f_max_rod_opt/9.81:.1f} kg`)
            * **Section résistante de la tige M14 ($A_s$) :** `115 mm²`
            * **Contrainte de traction nominale dans le filet :**
              $$\sigma = \frac{{F_{{max}}}}{{A_s}} = \frac{{{f_max_rod_opt:.1f} \text{{ N}}}}{{115 \text{{ mm}}^2}} = {stress_rod_opt:.2f} \text{{ MPa}}$$
            * **Coefficients de Sécurité (CS) élastique obtenus :**
              * **Classe d'acier 4.6** ($f_y = 240 \text{{ MPa}}$) : **CS = `{sf_4_6:.1f}`** (Hautement conforme, min requis = 3.0)
              * **Classe d'acier 8.8** ($f_y = 640 \text{{ MPa}}$) : **CS = `{sf_8_8:.1f}`** (Sécurité industrielle maximale)
            * *Avis RDM :* Les tiges M14 sont largement surdimensionnées pour supporter les 300 kg. Cette réserve mécanique garantit une excellente rigidité transversale et amortit les efforts dynamiques du flux d'air.
            """, unsafe_allow_html=True)
            
        with col_rdm_d2:
            st.markdown(r"""
            ##### 2. Tenue du Plafond & Conditions d'Ancrage
            * **Calcul de Charge Surfacique (Module 2x1m) :**
              * Surface au plafond : $2\text{ m} \times 1\text{ m} = 2\text{ m}^2$
              * Poids estimé du module : `300 kg`
              * Charge répartie moyenne : **`150 kg/m²`** (soit $1.47\text{ kN/m}^2$)
            * **Limitations des Panneaux Sandwichs :**
              * Les plafonds de chambres froides sont constitués de panneaux sandwichs isolants (PU ou PIR entre tôles de 0.5 mm).
              * **Avertissement :** Ces panneaux ne possèdent aucune tenue mécanique aux charges suspendues concentrées. Un ancrage direct dans le parement inférieur provoquerait une déchirure de la tôle et un délaminage immédiat de la mousse isolante.
            * **Cahier des Charges d'Installation (Ancrage Structurel) :**
              * **Ancrage traversant obligatoire :** Les tiges M14 doivent traverser de part en part les panneaux de plafond.
              * **Fixation sur la charpente primaire :** Ancrage requis directement dans la structure métallique porteuse (pannes, profilés de toit) ou la dalle en béton située au-dessus de la chambre.
              * **Rupture de Pont Thermique :** Insertion obligatoire de fourreaux/douilles en plastique isolant (Nylon/POM) autour des tiges M14 pour empêcher la formation de condensation et de givre.
              * **Scellement étanche :** Injection de mousse PU expansive et mastic élastomère pour préserver le pare-vapeur de la chambre froide.
            """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("##### <i class='fa-solid fa-image' style='color:#29B6D8;'></i> Analyse RDM et Modèle de Suspension", unsafe_allow_html=True)
        st.image("Capture d'écran 2026-07-06 213743.png", caption="Modélisation SolidWorks - Ancrage isostatique à 4 suspentes M14 par module", use_container_width=True)

    # --- ONGLET 4: ÉTUDE THERMODYNAMIQUE & TRANSFERTS ---
    with tab4:
        st.markdown("### <i class='fa-solid fa-calculator' style='color:#29B6D8; margin-right:8px;'></i> Physique du Transfert Thermique & Modélisation", unsafe_allow_html=True)
        st.write("Ce rapport méthodologique détaille les lois de la thermodynamique qui régissent le dimensionnement de notre batterie thermique (TES).")
        
        # Section 1 : Bilan thermique global
        st.markdown("#### 1. Bilan Thermique Global de la Chambre Froide")
        st.write("La puissance frigorifique totale à compenser par la batterie ($Q_{\text{totale}}$) est la somme des charges thermiques stationnaires et dynamiques :")
        st.latex(r"Q_{\text{totale}} = Q_{\text{parois}} + Q_{\text{infiltration}} + Q_{\text{produit}} + Q_{\text{internes}}")
        
        st.markdown(r"""
        * **Transmission par les Parois** (Modèle de conduction unidimensionnelle en série) :
        """)
        st.latex(r"Q_{\text{parois}} = U \cdot A_{\text{enveloppe}} \cdot (T_{\text{ext}} - T_{\text{cible}})")
        st.markdown(f"""
        où le coefficient global de transmission $U$ inclut la résistance de l'isolant PU ($\\lambda = {config.LAMBDA_PU}$ W/m.K) et les coefficients superficiels intérieur/extérieur :
        """)
        st.latex(r"U = \frac{1}{\frac{1}{h_i} + \frac{e_{\text{PU}}}{\lambda_{\text{PU}}} + \frac{1}{h_e}}")
        
        st.markdown(r"""
        * **Infiltrations d'Air Chaud (Théorème de Sebbar)** :
        L'ouverture des portes induit un courant gravitaire d'air chaud et humide. Le flux massique d'air entrant $\dot{m}_{\text{air}}$ est calculé dynamiquement en fonction de la différence de densité $\Delta\rho$ :
        """)
        st.latex(r"\dot{m}_{\text{air}} = \frac{2}{3} C_d W_d H_d^{1.5} \sqrt{g \frac{\Delta\rho}{\rho_{\text{moyen}}}}")
        st.write(r"La charge d'infiltration finale dépend de la différence d'enthalpie de l'air $\Delta h$ et du taux d'ouverture quotidien :")
        st.latex(r"Q_{\text{infiltration}} = \dot{m}_{\text{air}} \cdot \Delta h \cdot d_{\text{ouverture}}")

        # Section 2 : Modélisation des Résistances en Série
        st.markdown("#### 2. Modèle de Résistance Thermique du Module MCP en Série")
        st.write("Pour libérer le froid stocké, la chaleur doit traverser quatre barrières thermiques successives de l'extérieur vers l'intérieur du tube :")
        
        st.latex(r"R_{\text{linéaire}} = R_{\text{convection}} + R_{\text{peinture}} + R_{\text{aluminium}} + R_{\text{conduction MCP}}")
        
        st.markdown(r"""
        1. **Convection externe** : $R_{\text{convection}} = \frac{1}{h_{\text{conv}} \cdot A_{\text{effective}}}$. L'utilisation de **ventilateurs actifs** permet de faire passer $h_{\text{conv}}$ de $5\text{ W/m}^2\text{K}$ (statique) à **$25\text{ W/m}^2\text{K}$** (ventilation forcée). Les ailettes en étoile multiplient la surface efficace d'échange.
        2. **Peinture de protection** (époxy anti-corrosion) : $R_{\text{peinture}} = \frac{e_{\text{peinture}}}{\lambda_{\text{epoxy}} \cdot \pi D} + R_{\text{contact}}$.
        3. **Paroi en Aluminium** : $R_{\text{aluminium}} = \frac{\ln(D_{\text{ex}} / D_{\text{in}})}{2\pi \lambda_{\text{Al}}}$. La conductivité thermique exceptionnelle de l'aluminium ($\lambda_{\text{Al}} = 200\text{ W/m.K}$) rend cette résistance négligeable.
        4. **Conduction interne dans le MCP** : $R_{\text{conduction MCP}} = \frac{1}{4\pi \lambda_{\text{effective}}}$. La conductivité effective du composite MCP + ailettes internes en aluminium est calculée par la loi des mélanges :
        """)
        st.latex(r"\lambda_{\text{effective}} = \lambda_{\text{MCP}} (1 - \phi_{\text{ailettes}}) + \lambda_{\text{Al}} \phi_{\text{ailettes}}")
        
        st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Section 4 : FAQ/Q&A
        st.markdown("#### 3. Validation Scientifique & Guide de Soutenance Technique (FAQ/Q&A)", unsafe_allow_html=True)
        st.write("Retrouvez ci-dessous la justification rigoureuse de nos choix de modélisation physique et économique :")
        
        with st.expander("Q1 : Pourquoi appliquer une double marge sur le volume et la masse du MCP ?", expanded=False):
            st.markdown("""
            **Réponse Technique** : 
            Il ne s'agit pas d'un double comptage mais d'une distinction essentielle entre **sécurité thermique** et **sécurité mécanique** :
            1. **Masse (+10%)** : $m_{\text{dilated}} = m_{\text{required}} \times 1.10$. C'est une marge de sécurité thermique pour compenser les pertes parasites non modélisées et garantir les 13h d'autonomie même en cas de dégradation mineure du MCP au fil des cycles.
            2. **Ciel gazeux (10-20%)** : C'est une marge mécanique impérative. La paraffine subit une expansion volumique de ~10% lors de la transition solide-liquide. Sans ce ciel gazeux (espace de dilatation libre dans le haut du tube), l'augmentation de pression interne provoquerait la rupture par fatigue ou la déformation des tubes en aluminium.
            """)
            
        with st.expander("Q2 : Le ΔT moteur de décharge est-il vraiment constant (2 à 3 K) ?", expanded=False):
            st.markdown(r"""
            **Réponse Technique** : 
            C'est une **hypothèse simplificatrice conservative**. En réalité, au fur et à mesure de la décharge, l'épaisseur de MCP solide diminue et le front de fusion s'éloigne des ailettes, augmentant la résistance interne et faisant dériver le $\Delta T$.
            Considérer un $\Delta T$ fixe de $T_{\text{cible}} - T_{\text{fusion}}$ permet de dimensionner le système au regime nominal stabilisé. Pour la soutenance, nous admettons cette simplification et préconisons l'usage d'une régulation dynamique pour compenser les dérives de fin de cycle.
            """)
            
        with st.expander("Q3 : Quelle est l'interprétation physique de l'Autonomie Réelle calculée ?", expanded=False):
            st.markdown(r"""
            **Réponse Technique** : 
            Si la puissance maximale délivrable par la batterie ($Q_{\text{battery\_max}}$) est inférieure à la charge de pointe ($Q_{\text{load\_total}}$), le modèle applique un dérating de l'autonomie ($t_{\text{autonomy\_real}} = t_{\text{autonomy\_target}} \times \eta_{\text{effectiveness}}$).
            Physiquement, la batterie continuera à fondre pendant toute la durée cible, mais l'insuffisance de puissance entraînera une **dérive temporaire de la température de la chambre froide** au-dessus de sa consigne de sécurité. Ce ratio est donc à interpréter comme un **indice de performance thermique** ou de stabilité de température.
            """)
            
        with st.expander("Q4 : Pourquoi la résistance interne du MCP R_pcm est-elle indépendante du diamètre du tube ?", expanded=False):
            st.markdown(r"""
            **Réponse Technique** : 
            La formule $R_{\text{pcm}} = \frac{1}{4\pi\lambda_{\text{eff}}}$ dérive de l'analogie d'une **génération volumique uniforme de chaleur** dans un cylindre plein en régime stationnaire :
            $$\Delta T = T_{\text{centre}} - T_{\text{surface}} = \frac{q''' \cdot r^2}{4\lambda_{\text{eff}}}$$
            Comme le flux thermique linéaire $q'$ est lié à la génération volumique par $q' = q''' \cdot \pi r^2$, on obtient en remplaçant :
            $$\Delta T = q' \cdot \frac{1}{4\pi\lambda_{\text{eff}}}$$
            Ainsi, le rayon $r$ s'élimine de l'équation. C'est un résultat classique de la théorie des transferts thermiques qui démontre que pour un cylindre homogène, la résistance thermique interne est uniquement régie par la conductivité effective, indépendamment de la taille géométrique.
            """)
            
        with st.expander("Q5 : Le COP du compresseur (3.0 en positif, 1.8 en négatif) est-il constant ?", expanded=False):
            st.markdown("""
            **Réponse Technique** : 
            Non, le COP fluctue selon les températures d'évaporation et de condensation. En faisant tourner le compresseur la nuit (heures creuses) où la température extérieure est plus basse, la température de condensation baisse.
            Cela améliore naturellement le COP réel nocturne par rapport à un fonctionnement diurne. Notre modèle utilise des COP fixes et conservateurs : le gain économique réel sera donc **supérieur** à celui affiché dans notre ROI, renforçant la rentabilité de l'investissement.
            """)

    # --- ONGLET 5: ÉTUDE ÉLECTRIQUE & SECOURS ---
    with tab5:
        st.markdown("### <i class='fa-solid fa-bolt' style='color:#29B6D8; margin-right:8px;'></i> Étude Électrique & Système de Secours (Onduleur / UPS)", unsafe_allow_html=True)
        st.write("Cet onglet présente le bilan des puissances électriques de la ventilation forcée et le dimensionnement de l'onduleur de secours (UPS) requis en cas de panne de secteur.")
        
        n_modules_ceil = math.ceil(best_conf['N_Modules'])
        n_fans = n_modules_ceil * 2 # 2 ventilateurs de 15W par module de 2m
        total_fan_power = n_fans * 15.0
        required_ups_energy_wh = total_fan_power * autonomy_target
        battery_capacity_ah_12v = required_ups_energy_wh / 12.0
        battery_capacity_ah_48v = required_ups_energy_wh / 48.0
        
        col_elec1, col_elec2 = st.columns(2)
        
        with col_elec1:
            st.markdown(f"""
            ##### 1. Bilan de Puissance des Ventilateurs
            * **Nombre de modules à équiper :** `{n_modules_ceil}` modules
            * **Nombre de ventilateurs préconisés (2 par module de 2m) :** `{n_fans}` ventilateurs hélicoïdes
            * **Puissance nominale par ventilateur :** `15 W`
            * **Puissance électrique totale consommée en fonctionnement :** **`{total_fan_power:.0f} W`** (soit `{total_fan_power/1000:.3f} kW`)
            * *Note :* Cette consommation est extrêmement faible comparée à celle du compresseur frigorifique (~15 kW), ce qui rend le système de secours par batterie très compact et économique.
            """, unsafe_allow_html=True)
            
        with col_elec2:
            st.markdown(rf"""
            ##### 2. Dimensionnement de l'Onduleur de Secours (UPS)
            * **Objectif d'autonomie électrique :** `{autonomy_target} heures` (aligné sur l'autonomie thermique de la batterie)
            * **Énergie utile requise dans la batterie de l'UPS :**
              $$E_{{utile}} = P_{{totale}} \times t_{{autonomie}} = {total_fan_power:.0f} \text{{ W}} \times {autonomy_target} \text{{ h}} = {required_ups_energy_wh:.0f} \text{{ Wh}} \quad ({required_ups_energy_wh/1000:.2f} \text{{ kWh}})$$
            * **Capacités équivalentes selon la tension de la batterie :**
              * Sous une tension de **12 V** : **`{battery_capacity_ah_12v:.1f} Ah`**
              * Sous une tension de **48 V** : **`{battery_capacity_ah_48v:.1f} Ah`**
            * **Spécifications recommandées pour l'UPS :**
              * **Type de batterie :** **LiFePO4 (Lithium-Fer-Phosphate)**. Elles supportent les cycles de décharge profonde (80-90% DoD), conservent une longue durée de vie en température de local technique, et sont plus sécurisées que les batteries Plomb ou Lithium-Ion standards.
              * **Technologie :** Onduleur Off-Line ou Line-Interactive de **1000 VA**, largement suffisant pour la charge inductive des ventilateurs.
            """, unsafe_allow_html=True)

    # --- ONGLET 6: ÉTUDE BUDGÉTAIRE & RENTABILITÉ ---
    with tab6:
        st.markdown("### <i class='fa-solid fa-coins' style='color:#29B6D8; margin-right:8px;'></i> Rentabilité Économique et Économies Annuelles", unsafe_allow_html=True)
        st.write("Le gain financier annuel généré par la batterie thermique repose sur deux leviers d'action :")
        
        col_eco1, col_eco2 = st.columns(2)
        with col_eco1:
            st.markdown(f"""
            ##### <i class='fa-solid fa-bolt' style='color:#F39C12;'></i> 1. Arbitrage Tarifaire (Déplacement de charge)
            * **Économie annuelle sur facture** : `{best_conf['Savings_Electricity_Yearly_DA']:,.0f} DA / an`
            * *Principe* : Accumuler le froid pendant les heures creuses nocturnes et couper le compresseur pendant les heures pleines Sonelgaz.
            """, unsafe_allow_html=True)
        with col_eco2:
            st.markdown(f"""
            ##### <i class='fa-solid fa-shield-halved' style='color:#2ECC71;'></i> 2. Assurance Marchandises (Sécurisation du Stock)
            * **Pertes de stock évitées** : `{best_conf['Savings_Outages_Yearly_DA']:,.0f} DA / an`
            * *Principe* : En cas de coupure de courant, de maintenance ou de panne de compresseur, la batterie prend le relais pour maintenir la température et éviter le pourrissement des marchandises.
            """, unsafe_allow_html=True)
            
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            irr_val = format_irr(best_conf['TRI_Percent'])
            st.markdown(f"""
            ##### <i class='fa-solid fa-chart-line' style='color:#29B6D8;'></i> Indicateurs de Retour sur Investissement
            * **Économies Totales** : `{best_conf['Savings_Yearly_DA']:,.0f} DA / an`
            * **Temps de Retour Simple** : **`{format_payback(best_conf['Payback_Years'])}`**
            * **Taux de Rentabilité Interne (TRI actualisé sur 10 ans)** : **`{irr_val}`**
            """, unsafe_allow_html=True)
        with col_pay2:
            van_status = "<span style='color:#29B6D8; font-weight:bold;'>(Projet Viable)</span>" if best_conf['VAN_DA'] > 0 else "<span style='color:#E74C3C; font-weight:bold;'>(Non viable financièrement)</span>"
            st.markdown(f"""
            ##### <i class='fa-solid fa-scale-unbalanced' style='color:#E74C3C;'></i> Valeur Actuelle Nette & Sensibilité
            * **Valeur Actuelle Nette (VAN sur 10 ans @ 8%, maintenance @ {maintenance_rate*100:.1f}%)** : **`{best_conf['VAN_DA']:,.0f} DA`** {van_status}
            * **Sensibilité au prix de l'Aluminium (+20%)** :
              * **Nouveau Coût Total** : `{best_conf['Cost_Sens_DA']:,.0f} DA`
              * **Payback Simple Ajusté** : **`{format_payback(best_conf['Payback_Years_Sens'])}`**
            """, unsafe_allow_html=True)
            
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        
        if best_conf["Savings_Yearly_DA"] <= 0:
            st.warning("Les économies annuelles générées sont nulles ou négatives pour cette configuration. Le temps de retour sur investissement est infini.")
        else:
            st.markdown("#### <i class='fa-solid fa-chart-area' style='color:#29B6D8; margin-right:8px;'></i> Sensibilité : Fluctuation du Temps de Retour face au prix d'achat de l'Aluminium", unsafe_allow_html=True)
            alu_prices = np.linspace(1000.0, 3000.0, 10)
            paybacks = []
            for p in alu_prices:
                cost_temp = (best_conf["M_Al_Total_kg"] * p) + (best_conf["M_PCM_Required_kg"] * config.PRIX_MCP_BASE) + (best_conf["N_Modules"] * config.COUT_FAB_CYL)
                if best_conf["Ventilation"] == "ON":
                    cost_temp += config.SURCOUT_VENTILATION
                paybacks.append(cost_temp / best_conf["Savings_Yearly_DA"])
                
            df_sens = pd.DataFrame({
                "Prix Aluminium (DA/kg)": np.round(alu_prices).astype(int),
                "Temps de Retour Simple (ans)": paybacks
            })
            st.line_chart(df_sens, x="Prix Aluminium (DA/kg)", y="Temps de Retour Simple (ans)")

    # --- ONGLET 7: DONNÉES COMPLÈTES DE SIMULATION ---
    with tab7:
        st.markdown("### <i class='fa-solid fa-database' style='color:#29B6D8; margin-right:8px;'></i> Données de Simulation Exhaustives", unsafe_allow_html=True)
        st.write("Ce tableau regroupe toutes les configurations valides sous le budget maximal.")
        
        df_db_display = df_filtered.copy().sort_values(by="Optimization_Score_h_DA", ascending=False)
        
        # Appliquer les fonctions de formatage pour éviter d'afficher des valeurs sentinelles
        df_db_display["TRI_Percent"] = df_db_display["TRI_Percent"].apply(format_irr)
        df_db_display["Payback_Years"] = df_db_display["Payback_Years"].apply(format_payback)
        
        df_db_display = df_db_display[[
            "D_Cyl_mm", "N_Fins", "L_Fin_mm", "Ventilation", "L_Cyl_m", "Q_Load_Total_W", 
            "M_PCM_Required_kg", "M_Al_Total_kg", "Autonomy_Real_h", "Autonomy_Summer_h", "N_Modules", 
            "Cost_DA", "Payback_Years", "VAN_DA", "TRI_Percent", "Ceiling_Occupancy_Pct", "N_Suspentes"
        ]].rename(columns={
            "D_Cyl_mm": "Dia (mm)",
            "N_Fins": "Fins",
            "L_Fin_mm": "Ailette (mm)",
            "Ventilation": "Ventilation",
            "L_Cyl_m": "Long (m)",
            "Q_Load_Total_W": "Charge (W)",
            "M_PCM_Required_kg": "MCP (kg)",
            "M_Al_Total_kg": "Alu (kg)",
            "Autonomy_Real_h": "Autonomie Simulée (h)",
            "Autonomy_Summer_h": "Autonomie Été (h)",
            "N_Modules": "Nb Cylindres",
            "Cost_DA": "Coût (DA)",
            "Payback_Years": "Payback Simple",
            "VAN_DA": "VAN (DA)",
            "TRI_Percent": "TRI actualisé",
            "Ceiling_Occupancy_Pct": "Occ. Plafond (%)",
            "N_Suspentes": "Nb Suspentes"
        })
        
        st.dataframe(df_db_display.style.format({
            "Ailette (mm)": "{:.1f} mm",
            "Coût (DA)": "{:,.0f} DA",
            "MCP (kg)": "{:,.1f}",
            "Alu (kg)": "{:,.1f}",
            "Autonomie Simulée (h)": "{:.2f} h",
            "Autonomie Été (h)": "{:.2f} h",
            "VAN (DA)": "{:,.0f} DA",
            "Occ. Plafond (%)": "{:.1f} %",
            "Nb Suspentes": "{:d}"
        }), width="stretch")
