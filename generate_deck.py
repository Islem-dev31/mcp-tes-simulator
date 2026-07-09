import os
import sys
import subprocess

# --- AUTO-INSTALL DEPENDENCY ---
try:
    import pptx
except ImportError:
    print("python-pptx is not installed. Installing it now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
        import pptx
        print("python-pptx installed successfully.")
    except Exception as e:
        print(f"Error installing python-pptx: {e}")
        print("Please install it manually using: pip install python-pptx")
        sys.exit(1)

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# --- DESIGN & COLOR PALETTE CONFIGURATION ---
# Curated expert designer palette for KryoDrop (ThermaShift concept)
COLOR_NAVY = RGBColor(27, 54, 93)       # #1B365D - Primary brand color (trust, stability)
COLOR_CYAN = RGBColor(41, 182, 216)     # #29B6D8 - Brand accent color (energy, cooling)
COLOR_LIGHT_BG = RGBColor(244, 250, 252) # #F4FAFC - Light ice-blue canvas background
COLOR_WHITE = RGBColor(255, 255, 255)   # #FFFFFF - Clean card containers
COLOR_DARK_TEXT = RGBColor(17, 24, 39)  # #111827 - High-contrast body text
COLOR_MUTED_TEXT = RGBColor(107, 114, 128) # #6B7280 - Secondary descriptive text
COLOR_RED = RGBColor(220, 38, 38)       # #DC2626 - Highlight for problems/risks
COLOR_GREEN = RGBColor(22, 163, 74)     # #16A34A - Highlight for viability/ROI

FONT_TITLE = "Segoe UI"
FONT_BODY = "Segoe UI"

def set_slide_background(slide, color):
    """Sets a solid background color for the slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_slide_header(slide, title, category="KRYODROP | DECISION PITCH"):
    """Adds a standard header anchor to regular slides (excludes Title/Transition slides)."""
    # Tracker / Category (Small caps style)
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = FONT_TITLE
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN
    
    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

def draw_card_shape(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=None):
    """Draws a rounded card shape with optional border, hiding default borders cleanly."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        # A robust way to hide border is to color it same as fill
        card.line.fill.solid()
        card.line.fill.fore_color.rgb = bg_color
    return card

def add_content_card(slide, left, top, width, height, title, paragraphs, title_color=COLOR_NAVY, bg_color=COLOR_WHITE, border_color=None):
    """Creates a beautiful content card with a title and multi-paragraph body text."""
    # Draw card background
    draw_card_shape(slide, left, top, width, height, bg_color, border_color)
    
    # Overlay a text box inset inside the card boundaries
    inset = Inches(0.3)
    txBox = slide.shapes.add_textbox(left + inset, top + inset, width - (inset * 2), height - (inset * 2))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    # Card Title
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(16)
    p_title.font.bold = True
    p_title.font.color.rgb = title_color
    p_title.space_after = Pt(12)
    
    # Card Body Paragraphs
    for p_text in paragraphs:
        p = tf.add_paragraph()
        p.text = p_text
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT if bg_color == COLOR_WHITE else COLOR_WHITE
        p.space_after = Pt(8)

def add_stat_card(slide, left, top, width, height, value, label, value_color=COLOR_CYAN, bg_color=COLOR_WHITE):
    """Creates a statistics callout card with a large number and label below it."""
    draw_card_shape(slide, left, top, width, height, bg_color)
    
    inset = Inches(0.2)
    txBox = slide.shapes.add_textbox(left + inset, top + inset, width - (inset * 2), height - (inset * 2))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    # Stat Value (Large bold number)
    p_val = tf.paragraphs[0]
    p_val.text = value
    p_val.font.name = FONT_TITLE
    p_val.font.size = Pt(44)
    p_val.font.bold = True
    p_val.font.color.rgb = value_color
    p_val.alignment = PP_ALIGN.CENTER
    
    # Label Description
    p_lbl = tf.add_paragraph()
    p_lbl.text = label
    p_lbl.font.name = FONT_BODY
    p_lbl.font.size = Pt(10)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_MUTED_TEXT if bg_color == COLOR_WHITE else COLOR_WHITE
    p_lbl.alignment = PP_ALIGN.CENTER
    p_lbl.space_before = Pt(4)

def add_image_if_exists(slide, file_name, left, top, width, height):
    """Tries to find and add an image from local paths, returning True if successful."""
    paths_to_try = [
        file_name,
        os.path.join(r"c:\Users\AURES\Desktop\MCP", file_name)
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            try:
                slide.shapes.add_picture(p, left, top, width, height)
                return True
            except Exception as e:
                print(f"Error adding image {p}: {e}")
    return False

def style_table_cell(cell, text, font_size=10, bold=False, text_color=COLOR_DARK_TEXT, bg_color=None, align=PP_ALIGN.LEFT):
    """Styles a table cell with font, color, alignment and background fill."""
    cell.text = text
    p = cell.text_frame.paragraphs[0]
    p.font.name = "Segoe UI"
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    p.alignment = align
    if bg_color:
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color

def create_textbox_tf(slide, left, top, width, height):
    """Helper to create a text box and return its text frame with zero margins."""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    return tf

def build_pitch_deck():
    prs = Presentation()
    
    # Widescreen 16:9 format
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6] # Blank slide layout

    # =========================================================================
    # SLIDE 1: COVER SLIDE (ThermaShift / KryoDrop)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, COLOR_NAVY)
    
    # Left vertical accent line
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.0), Inches(0.12), Inches(3.5))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = COLOR_CYAN
    accent_bar.line.fill.solid()
    accent_bar.line.fill.fore_color.rgb = COLOR_CYAN
    
    # Title Text Frame
    tf1 = create_textbox_tf(slide1, Inches(1.4), Inches(1.9), Inches(7.2), Inches(4.0))
    p_main = tf1.paragraphs[0]
    p_main.text = "KryoDrop"
    p_main.font.name = FONT_TITLE
    p_main.font.size = Pt(64)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_WHITE
    
    p_sub = tf1.add_paragraph()
    p_sub.text = "ThermaShift : Le stockage thermique intelligent pour l'agro-industrie"
    p_sub.font.name = FONT_TITLE
    p_sub.font.size = Pt(20)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_CYAN
    p_sub.space_before = Pt(8)
    p_sub.space_after = Pt(20)
    
    p_desc = tf1.add_paragraph()
    p_desc.text = "Solution brevetée de stockage thermique par matériau à changement de phase (MCP-TES) pour optimiser et décarboner les chambres froides industrielles."
    p_desc.font.name = FONT_BODY
    p_desc.font.size = Pt(14)
    p_desc.font.color.rgb = COLOR_LIGHT_BG
    
    # Logo insertion on the right if available
    add_image_if_exists(slide1, "logo_icon.png", left=Inches(9.2), top=Inches(2.0), width=Inches(3.2), height=Inches(3.2))
    
    # Footer Details
    tf_foot = create_textbox_tf(slide1, Inches(1.4), Inches(6.1), Inches(10.0), Inches(0.5))
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "Greentech Challenge 2026  |  Pitch de Validation Industrielle"
    p_foot.font.name = FONT_BODY
    p_foot.font.size = Pt(11)
    p_foot.font.color.rgb = COLOR_CYAN

    # =========================================================================
    # SLIDE 2: THE PROBLEM (Factures Sonelgaz & Pertes)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, COLOR_LIGHT_BG)
    add_slide_header(slide2, "L'Explosion des Coûts & la Vulnérabilité des Stocks", "LE CONTEXTE ET LE PROBLÈME")
    
    # Left Card: Electrical Tariffs
    add_content_card(
        slide2,
        left=Inches(0.8), top=Inches(1.6), width=Inches(5.6), height=Inches(3.4),
        title="1. Factures d'Électricité en Heures Pleines (Sonelgaz)",
        paragraphs=[
            "Les compresseurs frigorifiques tournent à plein régime en journée, subissant les tarifs électriques les plus élevés (Heures Pleines).",
            "La prime fixe annuelle de puissance souscrite est gonflée par ces appels de courant de pointe diurnes.",
            "Aucune flexibilité d'exploitation sans barrière de stockage d'énergie."
        ],
        title_color=COLOR_NAVY
    )
    
    # Right Card: Stock Protection
    add_content_card(
        slide2,
        left=Inches(6.9), top=Inches(1.6), width=Inches(5.6), height=Inches(3.4),
        title="2. Ruptures & Vulnérabilité (Coupures Réseau)",
        paragraphs=[
            "Les coupures de courant d'été (délestages récurrents) et les pannes du groupe compresseur provoquent la rupture immédiate de la chaîne du froid.",
            "Coût direct : perte sèche de marchandises et risques sanitaires majeurs.",
            "Une seule coupure sévère peut détruire la rentabilité annuelle d'un site."
        ],
        title_color=COLOR_NAVY
    )
    
    # Bottom Stats
    add_stat_card(slide2, left=Inches(0.8), top=Inches(5.3), width=Inches(5.6), height=Inches(1.6), value="+30 %", label="Surcoût lié aux Heures Pleines diurnes (Sonelgaz)", value_color=COLOR_RED)
    add_stat_card(slide2, left=Inches(6.9), top=Inches(5.3), width=Inches(5.6), height=Inches(1.6), value="1.5M DA", label="Valeur moyenne d'un stock de denrées exposé en chambre froide", value_color=COLOR_RED)

    # =========================================================================
    # SLIDE 3: THE SOLUTION (Batterie PCM-TES)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, COLOR_LIGHT_BG)
    add_slide_header(slide3, "KryoDrop : Charger la Nuit, Libérer le Jour", "NOTRE PROPOSITION DE VALEUR")
    
    # Left Hero Box
    add_content_card(
        slide3,
        left=Inches(0.8), top=Inches(1.6), width=Inches(6.5), height=Inches(5.3),
        title="Le Cycle de Fonctionnement Intelligent",
        paragraphs=[
            "• Stockage de Froid (Nuit) : Le compresseur fonctionne de nuit pendant les Heures Creuses (tarif réduit). Le COP nocturne est supérieur de 20% grâce à la fraîcheur de l'air extérieur, permettant une solidification du MCP (paraffine) à haute efficacité énergétique.",
            "• Restitution Passive (Jour) : Le compresseur est éteint durant les Heures Pleines (8 à 12 heures). KryoDrop maintient la consigne thermique (+4°C / -18°C) par fusion contrôlée du MCP sans solliciter le compresseur.",
            "• Effacement Actif de la pointe de consommation sur le réseau électrique Sonelgaz."
        ],
        title_color=COLOR_CYAN,
        bg_color=COLOR_NAVY
    )
    
    # Right Stacked Cards
    add_content_card(
        slide3,
        left=Inches(7.7), top=Inches(1.6), width=Inches(4.8), height=Inches(2.4),
        title="Arbitrage Énergétique Direct",
        paragraphs=[
            "Déplacement de 100% de la consommation de pointe vers les heures creuses nocturnes, permettant d'économiser sur les coûts variables et de réduire la prime de puissance souscrite."
        ],
        title_color=COLOR_NAVY
    )
    
    add_content_card(
        slide3,
        left=Inches(7.7), top=Inches(4.5), width=Inches(4.8), height=Inches(2.4),
        title="Sécurisation Active (13h)",
        paragraphs=[
            "En cas de délestage ou de panne, la batterie thermique prend le relais automatiquement pour maintenir le froid pendant plus de 13 heures, éliminant les pertes de marchandises."
        ],
        title_color=COLOR_NAVY
    )
    
    # Visual left indicators for right cards
    ind1 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.7), Inches(1.6), Inches(0.08), Inches(2.4))
    ind1.fill.solid()
    ind1.fill.fore_color.rgb = COLOR_CYAN
    ind1.line.fill.solid()
    ind1.line.fill.fore_color.rgb = COLOR_CYAN
    
    ind2 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.7), Inches(4.5), Inches(0.08), Inches(2.4))
    ind2.fill.solid()
    ind2.fill.fore_color.rgb = COLOR_CYAN
    ind2.line.fill.solid()
    ind2.line.fill.fore_color.rgb = COLOR_CYAN

    # =========================================================================
    # SLIDE 4: LE JUMEAU NUMÉRIQUE (Digital Twin & Algorithm)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, COLOR_LIGHT_BG)
    add_slide_header(slide4, "Le Jumeau Numérique de Co-Dimensionnement", "NOTRE FORCE TECHNOLOGIQUE")
    
    # Left Card: Value of Simulator
    add_content_card(
        slide4,
        left=Inches(0.8), top=Inches(1.6), width=Inches(5.2), height=Inches(5.2),
        title="Dimensionnement Sur-Mesure par Algorithme",
        paragraphs=[
            "• Modélisation Physique Rigoureuse : Notre simulateur Streamlit intègre les équations de transfert thermique transitoire à changement de phase (Stefan) et calcule la masse de MCP requise.",
            "• Base Climatique Algérienne : Intégration des données réelles des 58 wilayas d'Algérie pour évaluer les charges d'infiltration d'air lors des ouvertures de porte.",
            "• Sécurité Compresseur : Vérification de la faisabilité de la recharge nocturne par le compresseur existant.",
            "• Nomenclature instantanée (BOM) et Ratios Financiers (VAN, TRI, Payback) calculés sur-mesure pour chaque client."
        ]
    )
    
    # Right Image Card Container
    draw_card_shape(slide4, left=Inches(6.4), top=Inches(1.6), width=Inches(6.1), height=Inches(5.2))
    has_img4 = add_image_if_exists(slide4, "Capture d'écran 2026-07-08 182424.png", left=Inches(6.6), top=Inches(2.1), width=Inches(5.7), height=Inches(4.2))
    if not has_img4:
        # Fallback to other screenshot
        has_img4_fb = add_image_if_exists(slide4, "Capture d'écran 2026-07-06 213743.png", left=Inches(6.6), top=Inches(2.1), width=Inches(5.7), height=Inches(4.2))
        if not has_img4_fb:
            # Placeholder text if no image
            tf_p4 = create_textbox_tf(slide4, Inches(6.6), Inches(3.0), Inches(5.7), Inches(2.0))
            p_p4 = tf_p4.paragraphs[0]
            p_p4.text = "[ Capture d'écran du Simulateur Streamlit ]\n(Simulateur d'aide à la décision technique et financière)"
            p_p4.font.name = FONT_TITLE
            p_p4.font.size = Pt(14)
            p_p4.alignment = PP_ALIGN.CENTER
            p_p4.font.color.rgb = COLOR_MUTED_TEXT

    # =========================================================================
    # SLIDE 5: INGÉNIERIE MÉCANIQUE (SolidWorks & DFM/RDM)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, COLOR_LIGHT_BG)
    add_slide_header(slide5, "Conception CAO & Robustesse Mécanique", "INGÉNIERIE MATÉRIELLE & DFM")
    
    # Left Card
    add_content_card(
        slide5,
        left=Inches(0.8), top=Inches(1.6), width=Inches(5.2), height=Inches(5.2),
        title="Un Design Optimisé pour la Fabrication (DFM)",
        paragraphs=[
            "• Caisson Modulaire & Système Drop-In : Conçu pour s'installer rapidement au plafond des chambres froides industrielles, sans perturber la disposition du stock.",
            "• Dégagement des Ailettes : Profil d'ailettes en étoile (8 externes, 8 internes, L=20mm, e=2mm) avec un entraxe de 50mm anti-givre pour maintenir le flux d'air.",
            "• Puits Central de 46 mm : Passage libre sécurisé pour la buse de remplissage de paraffine.",
            "• Isolation Galvanique EPDM : Manchons isolants placés aux points de contact pour éliminer la corrosion galvanique entre l'aluminium et le châssis en acier."
        ]
    )
    
    # Right Image Card Container for SolidWorks Renders
    draw_card_shape(slide5, left=Inches(6.4), top=Inches(1.6), width=Inches(6.1), height=Inches(5.2))
    has_img5 = add_image_if_exists(slide5, "Capture d'écran 2026-07-08 192651.png", left=Inches(6.6), top=Inches(2.1), width=Inches(5.7), height=Inches(4.2))
    if not has_img5:
        # Fallback to other screenshot
        has_img5_fb = add_image_if_exists(slide5, "Capture d'écran 2026-07-08 182424.png", left=Inches(6.6), top=Inches(2.1), width=Inches(5.7), height=Inches(4.2))
        if not has_img5_fb:
            tf_p5 = create_textbox_tf(slide5, Inches(6.6), Inches(3.0), Inches(5.7), Inches(2.0))
            p_p5 = tf_p5.paragraphs[0]
            p_p5.text = "[ Rendus SolidWorks & CAO ]\n(Batterie thermique, caisson modulaire et suspentes)"
            p_p5.font.name = FONT_TITLE
            p_p5.font.size = Pt(14)
            p_p5.alignment = PP_ALIGN.CENTER
            p_p5.font.color.rgb = COLOR_MUTED_TEXT

    # =========================================================================
    # SLIDE 6: INTELLIGENCE ÉLECTRIQUE (PLC / IHM / Automation)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, COLOR_LIGHT_BG)
    add_slide_header(slide6, "Contrôle-Commande & Automatisation", "INTELLIGENCE ÉLECTRIQUE")
    
    # Left Card
    add_content_card(
        slide6,
        left=Inches(0.8), top=Inches(1.6), width=Inches(5.6), height=Inches(5.2),
        title="Le Cerveau Électrique et Régulation",
        paragraphs=[
            "• Automate Industriel (PLC) : Régulation intelligente PID des flux thermiques. Basculement automatique entre les phases de charge nocturne et de décharge diurne.",
            "• Interface IHM (Écran Tactile) : Supervision locale et affichage en temps réel de l'état de charge (SOC) de la batterie thermique et des températures MCP.",
            "• Gestion de Secours Intégrée : En cas de coupure réseau, l'automate pilote le passage instantané de la ventilation sur l'onduleur de secours (UPS) pour continuer à diffuser le froid stocké.",
            "• Protection Électrique : Coffret câblé selon les normes industrielles avec sectionneurs, relais thermiques et contacteurs de puissance."
        ]
    )
    
    # Right Card: Schematic blocks representations
    draw_card_shape(slide6, left=Inches(6.8), top=Inches(1.6), width=Inches(5.7), height=Inches(5.2))
    
    # Block 1: Sensors
    card_sens = draw_card_shape(slide6, left=Inches(7.3), top=Inches(2.0), width=Inches(4.7), height=Inches(1.15), bg_color=COLOR_LIGHT_BG)
    tf_sens = create_textbox_tf(slide6, Inches(7.5), Inches(2.1), Inches(4.3), Inches(0.9))
    p_sens_title = tf_sens.paragraphs[0]
    p_sens_title.text = "1. Capteurs Thermiques (MCP & Air)"
    p_sens_title.font.name = "Segoe UI"
    p_sens_title.font.size = Pt(12)
    p_sens_title.font.bold = True
    p_sens_title.font.color.rgb = COLOR_NAVY
    p_sens = tf_sens.add_paragraph()
    p_sens.text = "Mesure en continu des températures du MCP et de l'air pour calculer l'état de charge (SOC)."
    p_sens.font.name = "Segoe UI"
    p_sens.font.size = Pt(10)
    p_sens.font.color.rgb = COLOR_DARK_TEXT
    
    # Block 2: PLC
    card_plc = draw_card_shape(slide6, left=Inches(7.3), top=Inches(3.5), width=Inches(4.7), height=Inches(1.15), bg_color=COLOR_NAVY)
    tf_plc = create_textbox_tf(slide6, Inches(7.5), Inches(3.6), Inches(4.3), Inches(0.9))
    p_plc_title = tf_plc.paragraphs[0]
    p_plc_title.text = "2. Automate PLC & Écran IHM"
    p_plc_title.font.name = "Segoe UI"
    p_plc_title.font.size = Pt(12)
    p_plc_title.font.bold = True
    p_plc_title.font.color.rgb = COLOR_CYAN
    p_plc = tf_plc.add_paragraph()
    p_plc.text = "Traitement des données, régulation PID, gestion des vannes et interface de contrôle opérateur."
    p_plc.font.name = "Segoe UI"
    p_plc.font.size = Pt(10)
    p_plc.font.color.rgb = COLOR_WHITE
    
    # Block 3: Actuators / UPS
    card_act = draw_card_shape(slide6, left=Inches(7.3), top=Inches(5.0), width=Inches(4.7), height=Inches(1.15), bg_color=COLOR_LIGHT_BG)
    tf_act = create_textbox_tf(slide6, Inches(7.5), Inches(5.1), Inches(4.3), Inches(0.9))
    p_act_title = tf_act.paragraphs[0]
    p_act_title.text = "3. Ventilation & Onduleur UPS"
    p_act_title.font.name = "Segoe UI"
    p_act_title.font.size = Pt(12)
    p_act_title.font.bold = True
    p_act_title.font.color.rgb = COLOR_NAVY
    p_act = tf_act.add_paragraph()
    p_act.text = "Activation de la soufflerie (60W-120W) secourue par UPS (LiFePO4 1.6 kWh) pendant 13 heures de délestage."
    p_act.font.name = "Segoe UI"
    p_act.font.size = Pt(10)
    p_act.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 7: BUSINESS MODEL & ROI (Tableau de Rentabilité)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, COLOR_LIGHT_BG)
    add_slide_header(slide7, "Une Solution Rentable aux Amortissements Rapides", "BUSINESS MODEL & ROI")
    
    # Left Stats Column
    add_stat_card(slide7, left=Inches(0.8), top=Inches(1.6), width=Inches(4.0), height=Inches(1.6), value="< 3 Ans", label="Temps de Retour Simple (Payback)", value_color=COLOR_GREEN)
    add_stat_card(slide7, left=Inches(0.8), top=Inches(3.4), width=Inches(4.0), height=Inches(1.6), value="> 25 %", label="Taux de Rentabilité Interne (TRI)", value_color=COLOR_GREEN)
    add_stat_card(slide7, left=Inches(0.8), top=Inches(5.2), width=Inches(4.0), height=Inches(1.6), value="VAN > 0", label="Valeur Actuelle Nette (Projet Rentable)", value_color=COLOR_GREEN)
    
    # Right Table Card
    draw_card_shape(slide7, left=Inches(5.2), top=Inches(1.6), width=Inches(7.3), height=Inches(5.2))
    
    # Add PowerPoint Table
    rows, cols = 5, 3
    table_shape = slide7.shapes.add_table(rows, cols, Inches(5.4), Inches(2.0), Inches(6.9), Inches(4.4))
    table = table_shape.table
    
    # Set columns width
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(3.4)
    table.columns[2].width = Inches(1.7)
    
    # Header Row
    style_table_cell(table.cell(0, 0), "Poste Économique", font_size=11, bold=True, text_color=COLOR_WHITE, bg_color=COLOR_NAVY, align=PP_ALIGN.CENTER)
    style_table_cell(table.cell(0, 1), "Détails Énergétiques & Fonctionnels", font_size=11, bold=True, text_color=COLOR_WHITE, bg_color=COLOR_NAVY, align=PP_ALIGN.CENTER)
    style_table_cell(table.cell(0, 2), "Impact Budgétaire", font_size=11, bold=True, text_color=COLOR_WHITE, bg_color=COLOR_NAVY, align=PP_ALIGN.CENTER)
    
    # Row 1
    style_table_cell(table.cell(1, 0), "Arbitrage Tarifaire", font_size=10, bold=True, text_color=COLOR_DARK_TEXT, bg_color=COLOR_WHITE)
    style_table_cell(table.cell(1, 1), "Consommation déplacée Heures Pleines → Heures Creuses (Sonelgaz)", font_size=9, text_color=COLOR_DARK_TEXT, bg_color=COLOR_WHITE)
    style_table_cell(table.cell(1, 2), "Économie de 30% sur le kWh variable", font_size=9, text_color=COLOR_GREEN, bg_color=COLOR_WHITE, align=PP_ALIGN.CENTER)
    
    # Row 2
    style_table_cell(table.cell(2, 0), "Prime de Puissance", font_size=10, bold=True, text_color=COLOR_DARK_TEXT, bg_color=COLOR_LIGHT_BG)
    style_table_cell(table.cell(2, 1), "Réduction de la prime fixe de puissance souscrite indexée sur le volume de la chambre", font_size=9, text_color=COLOR_DARK_TEXT, bg_color=COLOR_LIGHT_BG)
    style_table_cell(table.cell(2, 2), "Gain annuel fixe (Sonelgaz)", font_size=9, text_color=COLOR_GREEN, bg_color=COLOR_LIGHT_BG, align=PP_ALIGN.CENTER)
    
    # Row 3
    style_table_cell(table.cell(3, 0), "Protection Anti-Panne", font_size=10, bold=True, text_color=COLOR_DARK_TEXT, bg_color=COLOR_WHITE)
    style_table_cell(table.cell(3, 1), "Sauvegarde statistique du stock de marchandises face aux délestages et coupures d'électricité", font_size=9, text_color=COLOR_DARK_TEXT, bg_color=COLOR_WHITE)
    style_table_cell(table.cell(3, 2), "Risques de pertes éliminés", font_size=9, text_color=COLOR_GREEN, bg_color=COLOR_WHITE, align=PP_ALIGN.CENTER)
    
    # Row 4
    style_table_cell(table.cell(4, 0), "Payback & Viabilité", font_size=10, bold=True, text_color=COLOR_DARK_TEXT, bg_color=COLOR_LIGHT_BG)
    style_table_cell(table.cell(4, 1), "Investissement remboursé par les économies opérationnelles nettes cumulées", font_size=9, text_color=COLOR_DARK_TEXT, bg_color=COLOR_LIGHT_BG)
    style_table_cell(table.cell(4, 2), "Amortissement < 3 ans", font_size=9, bold=True, text_color=COLOR_NAVY, bg_color=COLOR_LIGHT_BG, align=PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 8: L'ÉQUIPE (ENPO-MA & ENPA Synergy)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, COLOR_LIGHT_BG)
    add_slide_header(slide8, "Une Équipe Pluridisciplinaire Complète", "SYNERGIE & FORCE HUMAINE")
    
    # Left Card: ENPO-MA
    add_content_card(
        slide8,
        left=Inches(0.8), top=Inches(1.6), width=Inches(5.6), height=Inches(5.2),
        title="Synergie ENPO-MA (Mécanique & Énergétique)",
        paragraphs=[
            "• Modélisation Physique & Thermique : Analyse transitoire du changement de phase solide-liquide (MCP), résolution des équations de conduction et convection forcée.",
            "• Conception Mécanique CAO : Conception complète de l'échangeur, des profilés d'ailettes en étoile SolidWorks et de la structure de supportage suspendue.",
            "• Résistance des Matériaux (RDM) : Validation de la tenue mécanique des suspentes M14, calculs de flexion (flèche médiane) des tubes de 2m, et analyses DFM de fabrication locale."
        ]
    )
    
    # Right Card: ENPA
    add_content_card(
        slide8,
        left=Inches(6.9), top=Inches(1.6), width=Inches(5.6), height=Inches(5.2),
        title="Synergie ENPA (Électrotechnique & Automatisme)",
        paragraphs=[
            "• Conception de l'Armoire Électrique : Câblage de puissance, schémas de protection et intégration des contacteurs compresseurs et de la soufflerie.",
            "• Programmation Automate (PLC) : Écriture de la logique de régulation, gestion PID des vannes, et détection automatique des coupures de courant.",
            "• Interface IHM & Supervision : Conception de l'écran tactile pour le suivi des températures, de l'état de charge (SOC) et des historiques d'exploitation.",
            "• Secours Électrique : Dimensionnement de l'UPS et du pack de batteries LiFePO4 de secours."
        ]
    )

    # --- SAVE PRESENTATION ---
    output_filename = "kryodrop_pitch_deck.pptx"
    prs.save(output_filename)
    print(f"\n[SUCCESS] Pitch deck generated successfully: '{output_filename}'")
    print(f"Absolute path: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    build_pitch_deck()
