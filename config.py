# -*- coding: utf-8 -*-
"""
Configuration des constantes physiques et économiques pour le simulateur MCP TES.
Ce fichier centralise les paramètres pour faciliter leur modification future.
"""

# ------------------------------------------------------------------------------
# 1. CONSTANTES CLIMATIQUES DE L'ALGÉRIE (Températures annuelles et de pointe d'été)
# ------------------------------------------------------------------------------
CITIES_CLIMATE = {
    "01 - Adrar": {"avg_annual": 28.0, "design_summer": 48.0, "winter": 10.0, "desc": "Sud (Climat Saharien hyper-aride)"},
    "02 - Chlef": {"avg_annual": 20.0, "design_summer": 42.0, "winter": 8.0, "desc": "Nord-Ouest (Climat Semi-aride chaud)"},
    "03 - Laghouat": {"avg_annual": 18.0, "design_summer": 40.0, "winter": 4.0, "desc": "Hauts-Plateaux Centre (Climat Semi-aride)"},
    "04 - Oum El Bouaghi": {"avg_annual": 15.0, "design_summer": 39.0, "winter": 2.0, "desc": "Hauts-Plateaux Est (Climat Semi-aride continental)"},
    "05 - Batna": {"avg_annual": 15.0, "design_summer": 39.0, "winter": 1.0, "desc": "Est / Aurès (Climat Continental / Montagneux)"},
    "06 - Béjaïa": {"avg_annual": 18.0, "design_summer": 34.0, "winter": 9.0, "desc": "Nord-Est / Littoral (Climat Méditerranéen humide)"},
    "07 - Biskra": {"avg_annual": 23.0, "design_summer": 45.0, "winter": 11.0, "desc": "Sud-Est / Portes du Désert (Climat Saharien)"},
    "08 - Béchar": {"avg_annual": 21.0, "design_summer": 43.0, "winter": 8.0, "desc": "Sud-Ouest / Saoura (Climat Désertique)"},
    "09 - Blida": {"avg_annual": 18.0, "design_summer": 36.0, "winter": 8.0, "desc": "Nord / Centre (Climat Méditerranéen sub-humide)"},
    "10 - Bouira": {"avg_annual": 17.0, "design_summer": 39.0, "winter": 5.0, "desc": "Centre / Continental (Climat Méditerranéen)"},
    "11 - Tamanrasset": {"avg_annual": 22.0, "design_summer": 36.0, "winter": 9.0, "desc": "Sud / Hoggar (Climat Désertique d'altitude)"},
    "12 - Tébessa": {"avg_annual": 16.0, "design_summer": 39.0, "winter": 2.0, "desc": "Extrême Est / Frontière (Climat Continental)"},
    "13 - Tlemcen": {"avg_annual": 16.0, "design_summer": 37.0, "winter": 6.0, "desc": "Extrême Ouest / Altitude (Climat Méditerranéen)"},
    "14 - Tiaret": {"avg_annual": 15.0, "design_summer": 38.0, "winter": 3.0, "desc": "Hauts-Plateaux Ouest (Climat Continental sec)"},
    "15 - Tizi Ouzou": {"avg_annual": 18.0, "design_summer": 39.0, "winter": 7.0, "desc": "Centre / Kabylie (Climat Méditerranéen continental)"},
    "16 - Alger": {"avg_annual": 19.0, "design_summer": 35.0, "winter": 9.0, "desc": "Nord / Littoral Centre (Climat Méditerranéen)"},
    "17 - Djelfa": {"avg_annual": 14.0, "design_summer": 38.0, "winter": 1.0, "desc": "Hauts-Plateaux Centre (Climat Continental semi-aride)"},
    "18 - Jijel": {"avg_annual": 18.0, "design_summer": 33.0, "winter": 10.0, "desc": "Nord-Est / Littoral (Climat Méditerranéen très humide)"},
    "19 - Sétif": {"avg_annual": 14.0, "design_summer": 38.0, "winter": 1.0, "desc": "Hauts-Plateaux Est (Climat Continental froid)"},
    "20 - Saïda": {"avg_annual": 16.0, "design_summer": 38.0, "winter": 5.0, "desc": "Hauts-Plateaux Ouest (Climat Semi-aride)"},
    "21 - Skikda": {"avg_annual": 18.0, "design_summer": 33.0, "winter": 9.0, "desc": "Nord-Est / Littoral (Climat Méditerranéen humide)"},
    "22 - Sidi Bel Abbès": {"avg_annual": 17.0, "design_summer": 39.0, "winter": 6.0, "desc": "Ouest (Climat Semi-aride)"},
    "23 - Annaba": {"avg_annual": 18.0, "design_summer": 34.0, "winter": 9.0, "desc": "Nord-Est / Littoral (Climat Méditerranéen)"},
    "24 - Guelma": {"avg_annual": 17.0, "design_summer": 40.0, "winter": 7.0, "desc": "Est / Sublittoral (Climat Méditerranéen chaud)"},
    "25 - Constantine": {"avg_annual": 16.0, "design_summer": 39.0, "winter": 4.0, "desc": "Est / Altitude (Climat Continental)"},
    "26 - Médéa": {"avg_annual": 15.0, "design_summer": 38.0, "winter": 4.0, "desc": "Centre / Atlas Blidéen (Climat Continental d'altitude)"},
    "27 - Mostaganem": {"avg_annual": 18.0, "design_summer": 33.0, "winter": 10.0, "desc": "Nord-Ouest / Littoral (Climat Méditerranéen)"},
    "28 - M'Sila": {"avg_annual": 19.0, "design_summer": 41.0, "winter": 6.0, "desc": "Hauts-Plateaux / Hodna (Climat Semi-aride steppique)"},
    "29 - Mascara": {"avg_annual": 18.0, "design_summer": 40.0, "winter": 6.0, "desc": "Ouest (Climat Méditerranéen chaud)"},
    "30 - Ouargla": {"avg_annual": 24.0, "design_summer": 46.0, "winter": 9.0, "desc": "Sud / Basse-Saharienne (Climat Saharien chaud)"},
    "31 - Oran": {"avg_annual": 18.5, "design_summer": 34.0, "winter": 9.0, "desc": "Nord-Ouest / Littoral (Climat Semi-aride)"},
    "32 - El Bayadh": {"avg_annual": 13.0, "design_summer": 37.0, "winter": 0.0, "desc": "Hauts-Plateaux Ouest / Djebel Amour (Continental froid)"},
    "33 - Illizi": {"avg_annual": 25.0, "design_summer": 44.0, "winter": 10.0, "desc": "Sud-Est / Frontière (Climat Saharien désertique)"},
    "34 - Bordj Bou Arréridj": {"avg_annual": 15.0, "design_summer": 38.0, "winter": 2.0, "desc": "Hauts-Plateaux Est (Climat Continental froid)"},
    "35 - Boumerdès": {"avg_annual": 18.0, "design_summer": 34.0, "winter": 9.0, "desc": "Nord / Littoral (Climat Méditerranéen)"},
    "36 - El Tarf": {"avg_annual": 18.0, "design_summer": 33.0, "winter": 9.0, "desc": "Nord-Est / Frontière littoral (Méditerranéen)"},
    "37 - Tindouf": {"avg_annual": 24.0, "design_summer": 46.0, "winter": 10.0, "desc": "Sud-Ouest / Frontière (Climat Désertique hyper-aride)"},
    "38 - Tissemsilt": {"avg_annual": 15.0, "design_summer": 39.0, "winter": 4.0, "desc": "Hauts-Plateaux / Ouarsenis (Climat Continental)"},
    "39 - El Oued": {"avg_annual": 23.0, "design_summer": 45.0, "winter": 10.0, "desc": "Sud-Est / Souf (Climat Saharien ergs)"},
    "40 - Khenchela": {"avg_annual": 14.0, "design_summer": 38.0, "winter": 1.0, "desc": "Est / Aurès (Climat Continental montagnard)"},
    "41 - Souk Ahras": {"avg_annual": 16.0, "design_summer": 39.0, "winter": 4.0, "desc": "Extrême Est / Frontière (Climat Continental)"},
    "42 - Tipaza": {"avg_annual": 18.0, "design_summer": 34.0, "winter": 9.0, "desc": "Nord / Littoral Centre (Climat Méditerranéen)"},
    "43 - Mila": {"avg_annual": 16.0, "design_summer": 39.0, "winter": 4.0, "desc": "Est / Continental (Climat Méditerranéen continental)"},
    "44 - Aïn Defla": {"avg_annual": 19.0, "design_summer": 42.0, "winter": 7.0, "desc": "Centre / Plaine du Chelif (Continental chaud)"},
    "45 - Naâma": {"avg_annual": 14.0, "design_summer": 37.0, "winter": 1.0, "desc": "Hauts-Plateaux Ouest / Altitude (Continental froid)"},
    "46 - Aïn Témouchent": {"avg_annual": 18.0, "design_summer": 33.0, "winter": 9.0, "desc": "Nord-Ouest / Littoral (Climat Méditerranéen)"},
    "47 - Ghardaïa": {"avg_annual": 22.0, "design_summer": 43.0, "winter": 9.0, "desc": "Sud-Est / Vallée du M'zab (Climat Saharien)"},
    "48 - Relizane": {"avg_annual": 20.0, "design_summer": 43.0, "winter": 8.0, "desc": "Ouest / Plaine de la Mina (Climat Semi-aride chaud)"},
    "49 - El M'Ghair": {"avg_annual": 23.0, "design_summer": 45.0, "winter": 10.0, "desc": "Sud-Est (Climat Saharien bas)"},
    "50 - Ouled Djellal": {"avg_annual": 23.0, "design_summer": 45.0, "winter": 11.0, "desc": "Sud-Est / Ziban (Climat Saharien)"},
    "51 - Bordj Baji Mokhtar": {"avg_annual": 29.0, "design_summer": 48.0, "winter": 12.0, "desc": "Extrême Sud / Tanezrouft (Climat Désertique hyper-aride)"},
    "52 - Béni Abbès": {"avg_annual": 22.0, "design_summer": 44.0, "winter": 9.0, "desc": "Sud-Ouest / Saoura (Climat Désertique)"},
    "53 - In Salah": {"avg_annual": 29.0, "design_summer": 48.0, "winter": 11.0, "desc": "Sud central / Gourara (Climat Désertique hyper-aride)"},
    "54 - In Guezzam": {"avg_annual": 29.0, "design_summer": 46.0, "winter": 14.0, "desc": "Extrême Sud / Sahel algérien (Climat Désertique chaud)"},
    "55 - Touggourt": {"avg_annual": 24.0, "design_summer": 45.0, "winter": 10.0, "desc": "Sud-Est / Oued Righ (Climat Saharien)"},
    "56 - Djanet": {"avg_annual": 23.0, "design_summer": 40.0, "winter": 8.0, "desc": "Extrême Sud-Est / Tassili (Climat Désertique d'altitude)"},
    "57 - El Meniaa": {"avg_annual": 23.0, "design_summer": 44.0, "winter": 8.0, "desc": "Sud central (Climat Désertique)"},
    "58 - Timimoun": {"avg_annual": 27.0, "design_summer": 47.0, "winter": 10.0, "desc": "Sud-Ouest / Gourara (Climat Désertique hyper-aride)"}
}

# ------------------------------------------------------------------------------
# 2. CARACTÉRISTIQUES PHYSIQUES DE LA CHAMBRE FROIDE ET PAROIS
# ------------------------------------------------------------------------------
LAMBDA_PU = 0.022          # Conductivité thermique du Polyuréthane (W/m.K)
THICKNESS_PU_POS = 0.100   # Épaisseur isolant pour +4°C (m)
THICKNESS_PU_NEG = 0.200   # Épaisseur isolant pour -18°C (m)

H_INT_WALL = 8.3           # Convection intérieure de paroi (W/m².K)
H_EXT_WALL = 25.0          # Convection extérieure de paroi (W/m².K)

# ------------------------------------------------------------------------------
# 3. LOIS D'INFILTRATION DE LA PORTE (Théorème de Sebbar / Tamm)
# ------------------------------------------------------------------------------
C_D = 0.6                  # Coefficient de décharge
G = 9.81                   # Accélération de la pesanteur (m/s²)
P_ATM = 101325.0           # Pression atmosphérique standard (Pa)
R_AIR = 287.05             # Constante spécifique de l'air (J/kg.K)
CP_AIR = 1005.0            # Capacité thermique de l'air (J/kg)
W_DOOR = 1.2               # Largeur de la porte (m)
H_DOOR = 2.0               # Hauteur de la porte (m)
N_OPENINGS_PER_HOUR = 4.0  # Nombre d'ouvertures de porte par heure
T_OPENING = 30.0           # Durée moyenne d'une ouverture (secondes)

# ------------------------------------------------------------------------------
# 4. CAPACITÉ THERMIQUE DU STOCK (PRODUITS) AND CHARGES INTERNES
# ------------------------------------------------------------------------------
CP_PRODUCT = 3800.0        # Capacité thermique massique moyenne (J/kg.K)
T_IN_PRODUCT_OFFSET = 5.0  # Écart de température d'entrée du produit / ambiance (K)
STOCK_VOLUME = 20000.0     # Capacité de stockage (L)
STOCK_TURNOVER = 0.10      # Taux de rotation quotidien du stock (10%)
Q_INTERNAL_STATIC = 150.0  # Charge thermique interne statique constante (W)

# ------------------------------------------------------------------------------
# 5. CARACTÉRISTIQUES DE LA BATTERIE DE STOCKAGE THERMIQUE
# ------------------------------------------------------------------------------
LAMBDA_AL = 200.0          # Conductivité de l'Aluminium (W/m.K)
RHO_AL = 2700.0            # Masse volumique de l'Aluminium (kg/m³)

LAMBDA_PCM = 0.20          # Conductivité thermique de la paraffine standard (W/m.K)
L_F = 200000.0             # Chaleur latente de fusion du MCP (J/kg, soit 200 kJ/kg)
RHO_PCM = 850.0            # Masse volumique de la paraffine (kg/m³)

R_CONTACT_EPOXY = 5e-4     # Résistance thermique de contact Époxy (m².K/W)
LAMBDA_EPOXY = 0.20         # Conductivité thermique de la résine Époxy (W/m.K)

H_CONV_VENT_ON = 25.0      # Coefficient convection ventilation ON (W/m².K)
H_CONV_VENT_OFF = 5.0      # Coefficient convection ventilation OFF (W/m².K)

# ------------------------------------------------------------------------------
# 6. INTÉGRATION ÉCONOMIQUE & TARIFICATION SONELGAZ (ALGÉRIE)
# ------------------------------------------------------------------------------
PRIX_AL_BASE = 1500.0      # Prix d'achat de l'Aluminium (DA/kg)
PRIX_MCP_BASE = 400.0      # Prix d'achat de la paraffine MCP (DA/kg)
COUT_FAB_CYL = 1000.0      # Coût de fabrication unitaire par cylindre (DA)
SURCOUT_VENTILATION = 15000.0 # Surcoût ventilation forcée + onduleur de secours (DA)

TARIF_HP_DA_KWH = 11.0     # Tarif Heures Pleines industrielle (DA/kWh)
TARIF_HC_DA_KWH = 3.0      # Tarif Heures Creuses industrielle (DA/kWh)
DAYS_OP_YEAR = 330.0       # Jours de fonctionnement par an
PRIME_FIXE_SAVINGS_DA = 80000.0 # Économie forfaitaire sur prime de puissance (DA/an)
DELTA_TARIF_DA_KWH = TARIF_HP_DA_KWH - TARIF_HC_DA_KWH # Différence tarifaire (8 DA/kWh)
