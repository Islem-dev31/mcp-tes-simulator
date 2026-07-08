# Rapport d'Ingénierie — Compatibilité CAO/Simulateur, DFM & Refonte KryoDrop

**Auteur :** Analyse technique (ingénierie froid & conception système)
**Date :** Juillet 2026
**Portée :** Comparaison du modèle CAO SolidWorks réel (assemblage batterie MCP) avec le simulateur Streamlit (`app.py` / `config.py`), analyse DFM/RDM, et cahier des charges de refonte graphique pour l'identité **KryoDrop**.

---

## 1. Résumé exécutif

Le simulateur a beaucoup progressé (règles DFM/RDM, puits central, ratio d'élancement, standardisation des ailettes). C'est un bon socle. Mais la comparaison avec l'assemblage CAO réel (captures SolidWorks) révèle **un écart structurel majeur** entre ce que l'app décrit textuellement (suspentes M10 individuelles par tube) et ce que le modèle CAO construit réellement (rack/cadre suspendu portant plusieurs tubes via des brides caoutchoutées). Le modèle de coût ne reflète pas non plus la nomenclature réelle visible dans l'arbre de construction SolidWorks (bouchons, caoutchoucs, brides, boulonnerie, cadre). Enfin, l'app n'a **aucune identité visuelle KryoDrop** à ce stade — elle utilise encore un thème générique "Batterie Thermique MCP".

Ce rapport liste, par ordre de priorité, tout ce qui doit être corrigé ou ajouté.

---

## 2. Analyse de compatibilité CAO ↔ Simulateur

### 2.1 Ce qui est cohérent (bon travail déjà fait)

| Élément CAO observé | Élément app.py correspondant | Statut |
|---|---|---|
| `bouchon<8>`, `bouchon<9>` (embouts soudés en bout de tube) | Section "Système de Bouchons (Soudure TIG)" avec bouchons à épaulement + taraudage M16 pour injection MCP (ligne ~880) | ✅ Cohérent, bien décrit |
| Ailettes en étoile visibles sur les tubes | Modèle de résistance thermique avec ailettes internes/externes, efficacité de type tanh(mL) | ✅ Cohérent |
| Répétitions linéaires (`Répétition linéaire locale1/2/3`) pour dupliquer les tubes | Boucle d'optimisation générant `N_Modules` cylindres identiques | ✅ Cohérent dans le principe |

### 2.2 Écart majeur n°1 — Le système de suspension réel n'est PAS celui décrit dans l'app

**Ce que montre la CAO (Image 2, capture 19:26) :** les cylindres ne sont pas suspendus individuellement. Ils sont **clampés par paires de brides supérieure/inférieure (`cache-sup`, `cache-inf`)** sur des rails, eux-mêmes portés par un **cadre rigide (`cadre2`)** suspendu au plafond par seulement quelques tiges filetées d'angle (`long vice`) — une conception de type "cassette" ou "rack", pas une grille de suspentes individuelles.

**Ce que dit l'app aujourd'hui (tab1 + tab3) :** *"Suspension de ces rails au plafond à l'aide de suspentes en tiges filetées M10 (quantité requise : N suspentes pour une charge sécurisée)"*, avec `n_suspentes = ceil(masse_totale / 300kg)` — un calcul qui suppose implicitement une distribution de charge fine et continue, comme si chaque tige reprenait une fraction égale et indépendante du poids total.

**Pourquoi c'est un problème :** ce ne sont pas seulement deux façons de décrire la même chose — ce sont **deux architectures mécaniques différentes** avec des charges concentrées différentes :
- Dans la conception CAO réelle, les 3-4 tiges d'angle du cadre reprennent chacune une fraction *beaucoup plus grande* de la charge totale (charge concentrée aux coins, pas répartie uniformément).
- Le calcul `n_suspentes = ceil(masse/300kg)` sous-estime donc la charge réelle par point d'ancrage si le nombre de tiges réellement utilisées (visible en CAO : 4 par cadre) est inférieur au nombre "théorique" calculé par la formule.

**Recommandation :** remplacer le modèle de suspentes par un modèle **cadre + rack** cohérent avec la CAO :
```
n_cadres = ceil(N_Modules / capacité_cadre)  # ex: 8-12 tubes par cadre selon la CAO
masse_par_cadre = masse_totale / n_cadres
n_tiges_par_cadre = 4  # coins, fixe (visible en CAO)
charge_par_tige_kg = masse_par_cadre / n_tiges_par_cadre
```
Puis vérifier `charge_par_tige_kg` contre la limite structurelle réelle d'une tige filetée (M10 classe 8.8 ≈ 800-900 kg en traction pure, avec coefficient de sécurité 3 → limite d'usage ≈ 270-300 kg/tige, ce qui reste cohérent avec le seuil actuel de 300kg, mais appliqué au **bon dénominateur**, pas au nombre total abstrait).

### 2.3 Écart majeur n°2 — Le coût ne reflète pas la nomenclature CAO réelle

L'arbre SolidWorks montre, par cylindre, une nomenclature bien plus riche que ce que facture `COUT_FAB_CYL = 1000 DA` :

| Pièce visible en CAO | Présente dans le coût actuel ? |
|---|---|
| `cylindre` (corps extrudé) | ✅ Oui — via `m_al_total × PRIX_AL_BASE` |
| `bouchon` × 2 par tube (embouts soudés, usinés avec épaulement + taraudage M16) | ❌ Non — un bouchon usiné avec taraudage n'est pas un simple "coût de fabrication" forfaitaire |
| `caoutchouc` × plusieurs par tube (joints/isolation galvanique) | ❌ Absent du coût **et absent de toute justification technique dans l'app** |
| `cache-sup` / `cache-inf` (brides de clampage) | ❌ Absent |
| `boulon` / `ecroue` (boulonnerie de clampage) | ❌ Absent |
| `plastique` (probablement une cale/entretoise isolante) | ❌ Absent |
| `cadre` + `long vice` (structure de suspension) | ❌ Absent — uniquement les "suspentes M10" sont comptées, pas le cadre lui-même |

**Recommandation concrète pour `config.py` :** ajouter une section 8 avec des coûts unitaires réalistes pour chaque pièce annexe, et les intégrer dans `cout_total` :
```python
COUT_BOUCHON_UNITAIRE_DA = 350.0      # bouchon à épaulement usiné + taraudage M16
COUT_CAOUTCHOUC_UNITAIRE_DA = 80.0    # joint/entretoise isolation galvanique par tube
COUT_BRIDE_CLAMPAGE_DA = 250.0        # paire cache-sup/cache-inf + boulonnerie
COUT_CADRE_PAR_UNITE_DA = 6000.0      # cadre de suspension (capacité ~10 tubes)
```
Sans cela, le "Coût Total Estimé" affiché en tab1 — le chiffre le plus regardé par un investisseur ou un jury — **sous-estime structurellement le vrai prix de revient**, car il ignore une part significative de la nomenclature réelle que vous avez pourtant déjà modélisée en CAO.

### 2.4 Écart n°3 — Le rôle du `caoutchouc` (isolation galvanique) n'est mentionné nulle part

Les pièces `caoutchouc` en contact entre l'aluminium (tube) et l'acier galvanisé (rails/brides) suggèrent que votre propre équipe CAO a déjà anticipé un vrai risque d'ingénierie : **la corrosion galvanique** entre deux métaux différents en présence d'humidité (quasi garantie dans une chambre froide, surtout en positif avec `rh_int = 90%`). C'est un point fort technique que l'app ne valorise pas du tout dans son argumentaire (tab3), alors que c'est exactement le genre de détail qui impressionne un ingénieur senior ou un investisseur industriel. **Recommandation :** ajouter un paragraphe dans tab3 ("Choix Technologiques") expliquant ce choix de conception — c'est un vrai différentiateur qualité qui ne coûte rien à documenter.

### 2.5 Écart n°4 — Risque de configuration vide silencieuse (règle DFM n°3)

La Règle 3 (`enforce_dfm` + diamètre dans [80,120]mm ⟹ `n_fins` doit valoir exactement `DFM_STANDARD_FINS_COUNT` = 8) est activée par défaut (`enforce_dfm = True`). Si l'utilisateur retire "8" de `fins_opts` (par exemple pour tester spécifiquement 4 ailettes) tout en laissant `enforce_dfm` coché, **toutes** les configurations dans la plage 80-120mm seront silencieusement rejetées, sans aucun message d'avertissement. Si en plus l'utilisateur restreint aussi `dia_opts` à cette plage, `df_sim` peut se retrouver vide et l'app affiche juste "Aucune configuration trouvée sous le budget maximum" — un message qui pointe vers la mauvaise cause (budget) alors que le vrai problème est une incompatibilité de règles DFM. **Recommandation :** ajouter une vérification explicite du type *"Aucune configuration ne respecte les règles DFM avec les ailettes sélectionnées — ajoutez 8 ailettes à votre sélection ou désactivez l'application stricte des règles DFM"*.

---

## 3. Analyse DFM/RDM — vérification des nouvelles règles

| Règle | Formule | Vérification |
|---|---|---|
| Puits central minimal | `d_inner - 2×l_fin ≥ 26mm` | Cohérent avec un passage de buse de coulée réaliste (buse standard 8-10mm + jeu). Bonne valeur. |
| Ratio d'élancement ailette | `l_fin / t_fin ≤ 15` | Standard raisonnable pour une ailette extrudée en aluminium sans risque de flambement/vibration excessive. Cohérent avec la pratique d'échangeurs à ailettes. |
| Standardisation 8 ailettes (80-120mm) | Force `n_fins == 8` dans cette plage | Techniquement défendable (réduction du nombre d'outillages d'extrusion = économie réelle en petite série), **mais** contredit partiellement l'ancienne règle "8 ailettes exclues si D<100mm pour l'espacement anti-givre" — ces deux règles doivent être réconciliées (voir §2.5 et point ci-dessous). |

**Point de vigilance supplémentaire :** avec `l_fin_mm` maintenant variable (15 à 30mm) plutôt que fixe à 30mm, le test d'espacement anti-givre (`spacing_ext_tip_check < 50.0`) est réévalué dynamiquement par combinaison — bonne chose. Mais assurez-vous que pour `n_fins=8` forcé par la règle DFM n°3, il existe **au moins une** longueur d'ailette dans `fin_len_opts` qui satisfasse simultanément le puits central (≥26mm) ET l'anti-givre (≥50mm à la pointe) ET le ratio d'élancement (≤15) pour chaque diamètre de 80 à 120mm — sinon la standardisation à 8 ailettes combinée aux autres règles pourrait rendre certains diamètres totalement inaccessibles sans que l'utilisateur comprenne pourquoi.

---

## 4. Analyse d'optimisation — cohérence de la grille

- **Bon point :** la grille croise maintenant diamètre × nombre d'ailettes × longueur d'ailette × longueur de tube × ventilation — un espace de recherche beaucoup plus riche qu'avant, avec les garde-fous DFM qui l'élaguent intelligemment.
- **Point à vérifier :** le score d'optimisation (`t_autonomy_summer / cout_total`) ne prend toujours pas en compte `Recharge_Feasible`, `Ceiling_Occupancy_Pct`, ni le nouveau statut DFM (`Puits_Central_mm`, `Aspect_Ratio`) au moment du tri — ces critères filtrent déjà l'espace de recherche en amont (bien), mais parmi les configurations qui passent tous les filtres, le score final reste un ratio brut autonomie/coût. Envisager un score composite pondéré si vous voulez que la "meilleure" config soit aussi la plus proche des marges DFM (pas juste à la limite).

---

## 5. Refonte de l'identité visuelle KryoDrop

### 5.1 Éléments de marque à extraire du logo

- **Nom :** KryoDrop — "Modern Cooling Solutions"
- **Symbole :** un "K" anguleux en bleu marine foncé, avec une goutte d'eau en dégradé cyan/bleu clair intégrée dans la diagonale du K
- **Palette à adopter :**
  - Bleu marine principal : proche de l'actuel `#1B365D` déjà utilisé dans l'app *(heureuse coïncidence — à conserver comme couleur de texte/headers)*
  - **Cyan accent (absent de l'app actuelle)** : à extraire du logo, approximativement `#29B6D8` à `#3FC1E0` — doit devenir la couleur d'action principale (boutons, valeurs clés, barres de progression), remplaçant l'usage actuel dispersé de bleu Bootstrap générique (`#2980B9`, `#3498DB`) qui n'a aucun lien avec la marque.
  - Garder le blanc dominant en fond (cohérent avec le logo sur fond blanc).

### 5.2 Modifications concrètes à apporter à `app.py`

1. **En-tête principal (ligne ~133)** : remplacer `"BATTERIE THERMIQUE MCP - CHAMBRE FROIDE"` par le branding KryoDrop, insérer le logo (`logo5.png`) via `st.image()` ou en CSS background dans le bandeau, et ajouter le sous-titre officiel *"Modern Cooling Solutions"*.
2. **`st.set_page_config`** : changer `page_icon` pour utiliser une version favicon du logo KryoDrop plutôt que l'icône générique Icons8.
3. **Palette CSS globale** : introduire des variables de couleur cohérentes :
   ```css
   :root {
       --kryo-navy: #1B365D;
       --kryo-cyan: #29B6D8;
       --kryo-cyan-light: #E5F7FB;
   }
   ```
   Remplacer systématiquement les couleurs d'accent actuelles (`#2980B9`, `#3498DB`, `#F39C12`, `#2ECC71` pour les éléments *positifs*) par `--kryo-cyan` là où la marque doit apparaître (boutons, indicateurs de succès liés au produit), en gardant le rouge/vert sémantique uniquement pour les alertes (OK/NON faisable), qui doivent rester universellement reconnaissables et ne pas être "brandés".
4. **Sidebar** : remplacer l'icône `icons8 cold.png` générique par le logo KryoDrop en haut de la barre latérale.
5. **Nom des onglets et du titre de page** : `st.set_page_config(page_title="KryoDrop | Simulateur TES")`.
6. **Pied de page / mentions** : ajouter un bandeau de bas de page discret avec le nom KryoDrop et éventuellement un slogan court, pour renforcer l'image "produit fini" plutôt que "prototype de simulation".

### 5.3 Cohérence de ton

Le nom "KryoDrop" et le sous-titre "Modern Cooling Solutions" suggèrent un positionnement **produit fini, professionnel, orienté B2B international** — plus proche d'un outil de configuration commercial que d'un simulateur académique. Cela renforce l'intérêt de :
- Réduire la verbosité de certains blocs Q&A techniques (actuellement très détaillés, utiles pour un jury mais un peu lourds pour un futur client B2B) — envisager un mode "Vue Simplifiée / Vue Technique Complète" togglable.
- Remplacer certains textes très "soutenance académique" (ex. "Q1 : Pourquoi appliquer une double marge...") par un ton produit plus affirmatif pour un usage commercial futur, tout en gardant la version académique disponible (utile pour vous en attendant la compétition).

---

## 6. Plan d'action priorisé

| Priorité | Action | Effort estimé |
|---|---|---|
| 1 (critique) | Aligner le modèle de suspension (cadre + tiges d'angle) avec la CAO réelle | Moyen — refonte du calcul `N_Suspentes` |
| 2 (critique) | Intégrer les coûts BOM manquants (bouchons, caoutchoucs, brides, cadre) dans `cout_total` | Moyen — ajout config + formule |
| 3 (important) | Message d'avertissement explicite si la grille DFM élimine toutes les configs | Faible |
| 4 (important) | Vérifier la compatibilité mutuelle des 3 règles DFM sur toute la plage 80-120mm | Faible (test/QA) |
| 5 (valorisant) | Documenter le rôle anti-corrosion galvanique du caoutchouc dans tab3 | Très faible |
| 6 (image de marque) | Refonte visuelle complète KryoDrop (logo, palette, page_config) | Moyen-élevé |

---

## 7. Note méthodologique

Cette analyse s'appuie sur (a) l'arbre de construction SolidWorks visible dans les deux captures d'écran fournies (noms de pièces et structure d'assemblage), (b) le code source actuel de `app.py` et `config.py`, et (c) le logo KryoDrop fourni. Elle ne remplace pas une revue de plans côtés ni un calcul de résistance des matériaux formel sur les tiges de suspension — ces vérifications restent à faire par un bureau d'études mécanique avant fabrication finale.

---

## 8. Dossier d'Études Techniques Détaillées (Prototype de Présentation)

Ce dossier rassemble l'ensemble des études d'ingénierie nécessaires pour la soutenance et la validation industrielle de la batterie thermique KryoDrop. Ces analyses sont prêtes à être intégrées sous forme d'onglets documentaires interactifs dans l'application Streamlit pour en faire un prototype complet d'aide à la décision.

### 8.1 Étude CAO (Conception Assistée par Ordinateur)

**Avis sur le modèle CAO actuel :** Le modèle CAO est **remarquablement bien conçu et prêt pour la fabrication**, démontrant une excellente anticipation des contraintes d'assemblage et de maintenance. Les choix suivants valident la maturité du design :
1. **Épaulement intérieur des caches (soudure TIG) :** L'épaulement intérieur sur `cache-sup` et `cache-inf` est une excellente pratique de fabrication. Il assure le centrage automatique des pièces lors du pointage, évite l'utilisation de gabarits complexes, et sert de support de soudure (backing ring) empêchant l'aluminium en fusion de s'effondrer à l'intérieur du tube lors de la soudure TIG.
2. **Géométrie des ailettes (8 internes / 8 externes, L=20mm, e=2mm) :**
   * **Aspect Ratio :** $L/e = 20/2 = 10$, ce qui est inférieur à la limite critique de flambement/vibration ($L/e \le 15$). Les ailettes sont très rigides, faciles à extruder sans défaut géométrique, et offrent un excellent rendement thermique.
   * **Puits central :** Pour un tube de diamètre extérieur de 90 mm avec une paroi de 2 mm ($D_{int} = 86$ mm), l'ailette de 20 mm laisse un puits libre central de $86 - 2 \times 20 = 46$ mm. Ce puits est largement supérieur à la contrainte DFM de 26 mm requise pour le passage de la buse de remplissage de paraffine, garantissant une coulée sans poches d'air.
3. **Barre de support médiane et isolant plastique :** L'ajout d'une traverse métallique à mi-portée (à 1 m sur les 2 m de long) est indispensable pour limiter la flèche (déformation en flexion sous le poids propre). L'intégration d'une bande de plastique isolant sur le dessus de cette barre est une solution brillante pour éviter tout frottement direct aluminium-acier, éliminant ainsi le risque de corrosion galvanique au point de flexion.

---

### 8.2 Étude DFM & RDM (Conception pour la Fabricabilité & Résistance des Matériaux)

#### A. Calcul de Résistance des Tiges Filetées de Suspension (M14)
* **Hypothèses de charge :**
  * Masse totale du module (20 tubes + cadre + paraffine) : $M = 300 \text{ kg}$.
  * Nombre de points de suspension (tiges filetées) : $N = 4$ (tiges d'angle).
  * Accélération de la pesanteur : $g = 9,81 \text{ m/s}^2$.
  * Force totale en traction pure : $F = M \cdot g = 300 \cdot 9,81 = 2943 \text{ N}$.
  * Répartition des charges : On suppose une charge uniformément répartie, soit $F_1 = F / 4 = 736 \text{ N}$ par tige. Pour tenir compte des imperfections de montage et d'un éventuel désalignement, nous appliquons un facteur de déséquilibre de 1,5, soit une charge maximale sur la tige la plus sollicitée de :
    $$F_{max} = 736 \text{ N} \times 1,5 = 1104 \text{ N} \approx 1,1 \text{ kN}$$
* **Calcul de la contrainte de traction :**
  * Pour une tige filetée M14 standard (pas gros de 2 mm), la section résistante à la traction (tensile stress area) est de :
    $$A_s \approx 115 \text{ mm}^2$$
  * La contrainte de traction nominale $\sigma$ dans la tige vaut :
    $$\sigma = \frac{F_{max}}{A_s} = \frac{1104 \text{ N}}{115 \text{ mm}^2} \approx 9,6 \text{ MPa}$$
* **Vérification de la limite élastique (Coefficient de Sécurité) :**
  * Si l'on utilise une tige filetée standard de classe de qualité **4.6** (acier à bas carbone très courant) :
    * Limite d'élasticité : $f_y = 240 \text{ MPa}$.
    * Coefficient de sécurité par rapport à la limite élastique :
      $$CS = \frac{f_y}{\sigma} = \frac{240 \text{ MPa}}{9,6 \text{ MPa}} = 25$$
  * Si l'on utilise une classe structurelle **8.8** (acier haute résistance standard en industrie) :
    * Limite d'élasticité : $f_y = 640 \text{ MPa}$.
    * Coefficient de sécurité :
      $$CS = \frac{640}{9,6} \approx 66,7$$
* **Conclusion :** Les 4 tiges filetées M14 sont **extrêmement surdimensionnées** pour supporter la charge statique de 300 kg (le système pourrait supporter plus de 7 tonnes en traction pure avant déformation). Ce surdimensionnement est toutefois recommandé pour :
  * Garantir une rigidité transversale et éviter le balancement (pendulaire) sous l'effet du flux d'air des ventilateurs.
  * Résister au couple de serrage lors de l'installation.
  * Prévenir la fatigue liée aux vibrations induites par les équipements frigorifiques de la chambre.

---

### 8.3 Étude de Dimensionnement & Calcul de Charge du Plafond

* **Charge surfacique moyenne du module :**
  * Surface occupée au sol/plafond : $A = 2 \text{ m} \times 1 \text{ m} = 2 \text{ m}^2$.
  * Charge surfacique brute du système rempli :
    $$q = \frac{300 \text{ kg}}{2 \text{ m}^2} = 150 \text{ kg/m}^2 \quad (1,47 \text{ kN/m}^2)$$
* **Condition de tenue du plafond (Panneaux Sandwichs) :**
  * Les plafonds de chambres froides sont constitués de panneaux sandwichs isolants en mousse rigide de polyuréthane (PU) ou polyisocyanurate (PIR) pris en sandwich entre deux parements en tôle d'acier galvanisé laqué (épaisseur habituelle $0,5 - 0,6$ mm).
  * **Comportement mécanique des panneaux sandwichs :** Ces panneaux ont une excellente résistance en flexion sur de grandes portées pour leur propre poids et des charges climatiques légères, mais leur résistance aux **charges suspendues localisées est extrêmement faible**. Fixer directement une charge de 300 kg sur la tôle inférieure provoquerait :
    * L'arrachement localisé des fixations (déchirure de la tôle fine).
    * Le délaminage de l'interface mousse-métal sous l'effet de la traction, entraînant l'effondrement à court terme du panneau.
  * **La Condition d'État de Plafond Demandée (Règle d'Or d'Installation) :**
    * **Ancrage traversant obligatoire :** Les tiges filetées M14 ne doivent **en aucun cas** s'ancrer dans le panneau sandwich. Elles doivent traverser de part en part le panneau de plafond.
    * **Ancrage structurel supérieur :** Les tiges doivent être solidement fixées à la charpente primaire du bâtiment (pannes métalliques, poutres béton ou dalles supérieures) située au-dessus de la chambre froide.
    * **Étanchéité et isolation thermique du perçage :** Pour chaque point de perçage traversant, il faut :
      1. Insérer un manchon isolant en plastique (type Nylon ou POM) autour de la tige M14 au passage du panneau pour éviter le contact métal-tôle et casser le pont thermique (qui générerait du givre à l'extérieur et de la condensation).
      2. Utiliser des rondelles d'étanchéité néoprène/acier (type rondelles cavaliers) de grand diamètre.
      3. Injecter de la mousse polyuréthane expansive dans le perçage et sceller les extrémités avec un mastic élastomère silicone ou polyuréthane de qualité frigorifique pour maintenir l'étanchéité à la vapeur d'eau.

---

### 8.4 Étude CAO & DFM : Analyse des Interfaces Métalliques & Dilatation

* **Risque de corrosion galvanique :**
  * L'assemblage met en présence deux métaux à potentiels galvaniques très différents : l'aluminium (tube, caches soudés) et l'acier galvanisé (berceaux en U de supportage).
  * En environnement humide (chambre froide positive à 90% d'humidité), la formation d'un film d'eau de condensation sert d'électrolyte. Sans isolation, l'aluminium (le plus anodique, -0,75 V) subira une corrosion galvanique rapide au profit de l'acier (plus cathodique).
* **Rôle protecteur des bagues en caoutchouc :**
  * L'ajout de 2 bagues en caoutchouc de 40 mm de longueur aux extrémités lisses de chaque tube isole électriquement l'aluminium de l'acier du berceau en U, **éliminant totalement le risque de couple galvanique**.
* **Comportement thermique et dilatation différentielle :**
  * Coefficient de dilatation linéaire de l'aluminium : $\alpha_{Al} \approx 23 \times 10^{-6} \text{ K}^{-1}$.
  * Coefficient de dilatation linéaire de l'acier : $\alpha_{Acier} \approx 12 \times 10^{-6} \text{ K}^{-1}$.
  * Pour un cycle de température de $\Delta T = 30 \text{ K}$ (entre la charge nocturne à $-25^\circ\text{C}$ et le repos à $+5^\circ\text{C}$), la différence de dilatation sur un tube de 2 m est de :
    $$\Delta L_{diff} = L \cdot (\alpha_{Al} - \alpha_{Acier}) \cdot \Delta T = 2000 \cdot (23 - 12) \times 10^{-6} \cdot 30 \approx 0,66 \text{ mm}$$
  * Le caoutchouc joue ici un second rôle crucial : sa souplesse absorbe ce déplacement micrométrique cyclique sans frottement métal-sur-métal, évitant l'usure de la couche d'oxyde protectrice de l'aluminium (phénomène de grippage ou *galling*).
* **Choix du matériau élastomère :**
  * Il est impératif d'utiliser du caoutchouc **EPDM (Éthylène-Propylène-Diène Monomère)** ou du **Silicone** de dureté **60 à 70 Shore A**.
  * L'EPDM conserve d'excellentes propriétés élastiques et ne fissure pas jusqu'à $-50^\circ\text{C}$, contrairement au caoutchouc Nitrile (NBR) standard qui durcit, se fragilise au froid, et perdrait sa fonction d'amortissement et de serrage.
  * **Fixation axiale :** Étant donné que le caoutchouc est monté serré sans gorge sur les parties lisses, les cycles thermiques réguliers risquent de faire migrer axialement le manchon. Il est fortement conseillé d'usiner une gorge de positionnement de 1,5 mm de profondeur sur le tube alu, ou d'utiliser un épaulement mécanique pour le bloquer axialement.

---

### 8.5 Étude Thermodynamique (Physique du Transfert)

* **Calcul des puissances de transfert :**
  La batterie thermique fonctionne selon un modèle de transfert thermique transitoire à changement de phase. La résistance thermique totale par unité de longueur $R'_{tot}$ régit le flux thermique linéique $q'$ transmissible :
  $$q' = \frac{T_{amb} - T_{fusion}}{R'_{tot}}$$
  Avec :
  $$R'_{tot} = \frac{1}{h_{conv} \cdot \pi D_{eff}} + R'_{paroi\_alu} + R'_{mcp\_eff}$$
* **Influence de la ventilation :**
  * **Mode Statique (Ventilateur OFF) :** Convective $h = 5 \text{ W/m}^2\text{K}$. La résistance convective externe est dominante, bridant le transfert.
  * **Mode Dynamique (Ventilateur ON) :** Convective $h = 25 \text{ W/m}^2\text{K}$. La résistance externe chute de 80%, permettant de valoriser pleinement la haute conductivité interne des ailettes alu et du MCP.

---

### 8.6 Étude Électrique & Secours (UPS)

* **Puissance consommée par la ventilation :**
  * Chaque module de $2 \times 1$ m nécessite une rampe de petits ventilateurs hélicoïdes pour assurer un flux d'air uniforme entre les ailettes.
  * Puissance unitaire d'un ventilateur de gaine : $\approx 15 \text{ W}$.
  * Pour un module de 20 tubes, un agencement de 4 ventilateurs est requis, soit $4 \times 15 = 60 \text{ W}$ par module.
  * Pour l'ensemble du système de 300 kg (consistant par exemple en 2 modules de $2 \times 1$ m, soit 40 tubes au total), la puissance électrique nécessaire est de $120 \text{ W}$.
* **Sécurisation par Onduleur (UPS) :**
  * En cas de panne générale de secteur (coupure Sonelgaz), le compresseur s'arrête, mais la batterie thermique KryoDrop doit continuer à souffler le froid.
  * La faible consommation des ventilateurs ($\approx 120 \text{ W}$) permet de les raccorder sur un onduleur de secours (UPS) de taille standard.
  * Pour garantir une autonomie de ventilation égale à l'autonomie thermique cible (13 heures) :
    $$E_{batterie\_UPS} = 120 \text{ W} \times 13 \text{ h} = 1560 \text{ Wh} \approx 1,6 \text{ kWh}$$
  * Un onduleur de $2 \text{ kVA}$ avec pack de batteries de $1,6 \text{ kWh}$ (type batteries Lithium-Fer-Phosphate LiFePO4, performantes dans la durée) est préconisé pour alimenter la ventilation de secours.

---

### 8.7 Étude Budgétaire & Rentabilité

L'étude financière s'appuie sur le modèle de coûts algérien et l'arbitrage tarifaire Sonelgaz.
* **Coûts de la Nomenclature Réelle (BOM) :**
  * Aluminium extrudé calibré : $1500 \text{ DA/kg}$
  * Paraffine technique (MCP) : $400 \text{ DA/kg}$
  * Paire de caches (soudage inclus) : $500 \text{ DA}$
  * Usinage + taraudage M16 bouchon : $350 \text{ DA}$
  * Bagues EPDM + vis de serrage : $150 \text{ DA / tube}$
  * Châssis métallique en acier galvanisé de supportage (cadre) : $8000 \text{ DA / module}$
* **Indicateurs Financiers Projets :**
  * **VAN (Valeur Actuelle Nette) :** Calculée sur 10 ans avec un taux d'actualisation de 8% et une inflation de l'électricité de 5%. Un projet est déclaré viable si sa VAN est largement positive.
  * **TRI (Taux de Rentabilité Interne) :** Représente le taux de rendement annuel du capital investi. Un TRI supérieur à 25% démontre un projet industriel hautement attractif.
  * **Temps de retour sur investissement (Payback) :** Délai nécessaire pour que les économies cumulées sur les heures pleines Sonelgaz remboursent l'investissement initial.
