# Guide de Soutenance & Réponses aux Questions du Jury
## Simulateur MCP TES - Greentech Challenge

Ce document prépare l'étudiant à défendre avec rigueur la modélisation physique, géométrique et économique de la batterie thermique face à un jury technique exigeant (énergéticiens, frigoristes et financiers).

---

## Sommaire
- [A. Cohérence interne du code](#a-cohérence-interne-du-code)
- [B. Physique du bilan thermique](#b-physique-du-bilan-thermique)
- [C. Modélisation MCP & réseau de résistances](#c-modélisation-mcp--réseau-de-résistances)
- [D. Calcul des masses et géométrie CAO](#d-calcul-des-masses-et-géométrie-cao)
- [E. Modèle économique et ROI](#e-modèle-économique-et-roi)
- [F. Faisabilité de recharge nocturne et compresseur](#f-faisabilité-de-recharge-nocturne-et-compresseur)

---

### A. Cohérence interne du code

#### Q1 : Votre "Solution Optimale Recommandée #1" est-elle garantie de passer votre propre test de faisabilité de recharge ?
**Réponse Technique** : 
Oui. Le moteur de calcul filtre désormais les configurations selon deux étapes :
1. **Étape 1** : Filtrage par budget maximum (`Cost_DA <= budget_max`).
2. **Étape 2** : Sélection prioritaire des configurations où la recharge nocturne est réalisable avec le compresseur existant (`Recharge_Feasible == "OUI"`). 
*Si et seulement si* aucune configuration n'est faisable dans le budget (compresseur trop sous-dimensionné ou budget trop bas), le code affiche les configurations disponibles en levant un avertissement visuel fort. Cela garantit que la recommandation #1 est techniquement viable et opérationnelle pour le client.

#### Q2 : R_wall_al est négligeable dans le réseau de résistances, mais vous vendez un transfert 1300x plus rapide que Viking Cold (USA). Pourquoi ?
**Réponse Technique** : 
C'est le paradoxe classique de la minimisation de la résistance thermique. 
* Dans **notre système**, l'utilisation de l'aluminium (conductivité $\lambda = 200 \text{ W/m.K}$) rend la résistance de la paroi ($R_{\text{wall}}$) infinitésimale devant la résistance de convection externe ($R_{\text{conv}}$) et la conduction du MCP ($R_{\text{pcm}}$).
* Chez **Viking Cold**, les bacs sont en plastique (polyéthylène haute densité, $\lambda \approx 0.15 \text{ W/m.K}$ à $0.25 \text{ W/m.K}$). Le plastique agit comme un isolant. Sa résistance de paroi devient le principal goulot d'étranglement de tout le système ($R_{\text{wall, plastique}} \gg R_{\text{conv}}$).
Ainsi, notre co-existence d'affirmations est exacte : l'aluminium élimine le goulot d'étranglement de paroi, rendant cette résistance négligeable chez nous, tout en augmentant la vitesse globale d'échange de la batterie par rapport à une solution plastique.

#### Q3 : Les constantes opérationnelles sont dupliquées entre config.py et app.py. Pourquoi ?
**Réponse Technique** : 
Ce point a été corrigé. L'application Streamlit ne possède plus de valeurs dupliquées codées en dur pour ses valeurs par défaut. Elle lit désormais toutes ses données initiales et ses configurations physiques directement depuis `config.py`. Tout ajustement dans le fichier de configuration centralisé est immédiatement pris en compte dans l'interface et les curseurs dynamiques de l'utilisateur.

#### Q4 : Le sélecteur "Période de simulation" influence-t-il le dimensionnement ou uniquement l'affichage ?
**Réponse Technique** : 
Le dimensionnement physique (masse de MCP requis, nombre de cylindres, quantité d'aluminium et coût d'investissement) est **strictement découplé** de la période de simulation. Il est calculé en permanence sur la base de la charge de pointe estivale (`design_summer`) de la wilaya pour des raisons évidentes de sécurité thermique (garantie de la chaîne du froid dans le cas le plus critique). 
Le sélecteur de saison de l'interface sert uniquement à visualiser le comportement en exploitation réelle (les pertes étant moindres en hiver ou en mi-saison, l'autonomie opérationnelle y est mécaniquement plus élevée).

#### Q5 : Comment gérez-vous le Payback quand les gains annuels sont nuls ou négatifs ?
**Réponse Technique** : 
Si les économies annuelles nettes sont inférieures ou égales à zéro (par exemple si le coût de maintenance ou de fonctionnement dépasse les gains), le temps de retour sur investissement est physiquement infini. Le code intercepte désormais ce cas : il affiche un message d'avertissement clair ("*Le système ne génère pas d'économies nettes, TRI infini*") et désactive l'affichage du graphique de sensibilité pour éviter de polluer l'échelle visuelle avec des valeurs de capage arbitraires (99 ans).

---

### B. Physique du bilan thermique

#### Q6 : Pourquoi la charge interne statique (Q_INTERNAL_STATIC) est-elle fixe ?
**Réponse Technique** : 
Une charge interne statique fixe de $150 \text{ W}$ n'était valable que pour une chambre froide de taille moyenne (~100 m³). Pour éliminer cette simplification, nous avons implémenté une loi d'échelle linéaire réaliste :
$$Q_{\text{internal\_static}} = 50.0 + 1.0 \times V_{\text{chambre}} \quad (\text{W})$$
Cela reflète le fait que plus une chambre froide est grande, plus elle possède d'éclairages permanents, d'auxiliaires électriques (moteurs de ventilateurs d'évaporateur) et de présence de personnel. Pour 10 m³, la charge est de $60 \text{ W}$, et pour 1000 m³, elle s'élève de manière réaliste à $1050 \text{ W}$.

#### Q7 : L'humidité relative extérieure (rh_ext) est fixée à 60% pour toute l'Algérie. Comment le justifiez-vous ?
**Réponse Technique** : 
L'humidité extérieure influence directement l'enthalpie de l'air infiltré ($h_{\text{ext}}$), et donc le bilan frigorifique. Nous avons dynamique-ment relié l'humidité extérieure `rh_ext` au climat de la wilaya en analysant sa description géographique :
* **Villes Littorales** (ex. Alger, Jijel, Annaba) : Climat humide $\rightarrow$ `rh_ext = 75%`.
* **Villes Sahariennes / Sud** (ex. Adrar, Ouargla, Djanet) : Climat aride $\rightarrow$ `rh_ext = 25%`.
* **Hauts-Plateaux / Intérieur** (ex. Sétif, Batna, Tiaret) : Climat continental $\rightarrow$ `rh_ext = 45%`.
* **Valeur par défaut** : `60%`.
Cela apporte une précision géographique rigoureuse au calcul de la charge d'infiltration.

#### Q8 : La hauteur de la chambre est fixée à 4.0 m quel que soit le volume, forçant un aspect ratio improbable. Est-ce réaliste ?
**Réponse Technique** : 
Non, ce n'était pas réaliste pour les extrêmes (10 m³ et 1000 m³). Le modèle adapte désormais la hauteur sous plafond de manière discrète selon la catégorie de volume :
* **Volume < 50 m³** : Hauteur de $3.0 \text{ m}$ (chambre froide commerciale standard type walk-in).
* **Volume entre 50 et 200 m³** : Hauteur de $4.0 \text{ m}$ (stockage de distribution moyen).
* **Volume $\ge$ 200 m³** : Hauteur de $5.0 \text{ m}$ (entrepôt frigorifique industriel).
L'empreinte au sol et la surface d'enveloppe extérieure ($A_{\text{env}}$) calculées sont ainsi conformes aux ratios de construction réels du génie civil.

#### Q9 : La charge pariétale (q_wall) peut-elle devenir négative en hiver ?
**Réponse Technique** : 
Oui. En hiver, si la température extérieure moyenne descend en dessous de la consigne intérieure positive de la chambre (ex. $+4^\circ\text{C}$ de consigne avec $0^\circ\text{C}$ dehors), le flux de chaleur s'inverse, ce qui se traduirait par un apport frigorifique passif par les parois ($q_{\text{wall}} < 0$). Cependant, pour éviter que le modèle ne sous-estime les besoins dynamiques et ne masque les pertes des autres postes, toutes les charges unitaires ($q_{\text{wall}}$, $q_{\text{infiltration}}$, $q_{\text{product}}$) sont bridées à un minimum de $0.0 \text{ W}$ (`max(0.0, ...)`).

#### Q10 : La porte (1.2m x 2.0m) est-elle la même pour toutes les tailles de chambre ?
**Réponse Technique** : 
Le modèle adapte désormais les dimensions de la porte d'accès en fonction de la catégorie de volume de la chambre :
* **Volume < 50 m³** : Porte piétonne simple de $1.0 \text{ m} \times 2.0 \text{ m}$.
* **Volume 50 à 200 m³** : Porte de manutention de $1.4 \text{ m} \times 2.2 \text{ m}$ (passage de transpalette).
* **Volume $\ge$ 200 m³** : Porte industrielle de $2.0 \text{ m} \times 2.5 \text{ m}$ (docks de chargement et chariots élévateurs).
La charge d'infiltration d'air lors des ouvertures de porte est ainsi rigoureusement proportionnelle aux flux logistiques du site.

#### Q11 : Le produit entrant est supposé à T_ext - 5K. D'où vient cette hypothèse ?
**Réponse Technique** : 
Cette hypothèse modélise la rupture de la chaîne du froid lors du transport routier ou de la manutention sur quai non réfrigéré. Le produit arrive généralement un peu plus frais que l'air ambiant extérieur en été grâce à l'inertie du camion de transport frigorifique ou de sa bâche isolante, mais il a accumulé des calories par rapport à la consigne intérieure. Ce delta de $5 \text{ K}$ est une hypothèse conservative classique en froid industriel pour le calcul du bilan thermique de renouvellement de stock.

---

### C. Modélisation MCP & réseau de résistances

#### Q12 : Le coefficient de convection externe h_conv = 25 W/m²K prend-il en compte l'effet d'ombrage du réseau de tubes ?
**Réponse Technique** : 
Le coefficient $h_{\text{conv}} = 25 \text{ W/m}^2\text{K}$ correspond à une vitesse d'air moyenne de $2.5 \text{ m/s}$ soufflé directement sur les tubes (convection forcée). Dans un réseau de tubes serrés au plafond, il existe effectivement un effet de sillage et de perte de charge (perte de vitesse de l'air sur les rangs arrière). 
Pour compenser cela dans le dimensionnement nominal, la résistance convective $R_{\text{conv}}$ est surdimensionnée en utilisant une efficacité globale. De plus, l'espacement de $50 \text{ mm}$ minimum entre les cylindres est spécifiquement choisi pour permettre le passage fluide du flux d'air et limiter les zones d'ombre convective.

#### Q13 : Quelle est l'erreur commise en supposant un ΔT moteur de décharge constant ?
**Réponse Technique** : 
L'hypothèse d'un $\Delta T$ moteur constant de $T_{\text{cible}} - T_{\text{fusion}}$ est une approximation du premier ordre. En réalité, le front de solidification progresse et crée une couche isolante de MCP solide sur la paroi interne, ce qui fait chuter la puissance thermique au cours du temps (problème transitoire de Stefan).
Numériquement, l'erreur introduite est compensée par la marge de sécurité thermique de $+10\%$ sur la masse du MCP et la sur-évaluation de la surface d'échange des ailettes internes. De plus, l'utilisation de tubes en aluminium avec des ailettes internes en étoile réduit la distance maximale de conduction radiale à moins de $15 \text{ mm}$, limitant la baisse de puissance en fin de cycle.

#### Q14 : La formule R_pcm = 1/(4πλ_eff) suppose une génération volumique uniforme. Est-ce réaliste ?
**Réponse Technique** : 
Physiquement, le changement de phase n'est pas une génération volumique uniforme de chaleur, c'est un phénomène à frontière mobile. Cependant, la formule analytique $1/(4\pi\lambda_{\text{eff}})$ est une approximation standard extrêmement efficace en ingénierie de pré-dimensionnement. Elle équivaut à considérer une conductivité thermique moyenne pondérée sur tout le volume interne du tube. Pour un modèle plus fin, un code de simulation 2D dynamique par éléments finis (méthode de l'enthalpie) serait nécessaire, mais la formule linéaire fournit une précision à $\pm 10\%$, ce qui est largement suffisant pour le choix de la configuration optimale.

#### Q15 : Quelle est la pression générée par la dilatation du MCP dans le ciel gazeux ?
**Réponse Technique** : 
La paraffine subit une dilatation volumique d'environ $10\%$ lors de sa fusion. En réservant un ciel gazeux de $10\%$ de volume vide (rempli d'air à pression atmosphérique initiale $P_0 = 1.013 \text{ bar}$ et température $T_0 = 20^\circ\text{C}$), lors de la fusion complète, le volume d'air est comprimé de moitié (taux de compression $r = 2$). 
Selon la loi des gaz parfaits, la pression maximale de l'air emprisonné atteint environ $2 \text{ bar}$ à chaud. Les tubes en aluminium extrudé de $2 \text{ mm}$ d'épaisseur de paroi peuvent supporter des pressions d'éclatement supérieures à $50 \text{ bar}$. Les soudures d'extrémités et les joints d'étanchéité sont éprouvés à $10 \text{ bar}$ en usine, ce qui laisse un facteur de sécurité mécanique supérieur à 5.

#### Q16 : Avez-vous des données sur la dégradation du MCP au fil des cycles ?
**Réponse Technique** : 
Les paraffines paraffiniques de qualité industrielle (alcanes linéaires) possèdent une excellente stabilité thermique et chimique. Elles peuvent subir plus de 10 000 cycles de fusion-solidification (soit plus de 30 ans d'utilisation quotidienne à raison de 330 cycles/an) sans présenter de baisse notable de leur chaleur latente de fusion ($<2\%$). Contrairement aux sels hydratés (sujets à la surfusion et à la ségrégation de phase), la paraffine ne nécessite aucun agent nucléant ou gélifiant.

---

### D. Calcul des masses et géométrie CAO

#### Q17 : Comment justifiez-vous la cohérence entre la masse de MCP et le volume brut des cylindres ?
**Réponse Technique** : 
Ce point a été entièrement fiabilisé. Le code calcule la longueur physique requise pour chaque tube à partir de la section utile nette de MCP (section intérieure brute moins la section occupée par les ailettes internes en aluminium) :
$$A_{\text{pcm\_cross}} = A_{\text{inner}} - A_{\text{ailettes\_int}}$$
Puis la longueur totale de tube physique est calculée en intégrant la marge de dilatation (1.10) et le ciel gazeux :
$$L_{\text{total}} = \frac{m_{\text{pcm}} \times 1.10}{\rho_{\text{pcm}} \times A_{\text{pcm\_cross}} \times (1 - \text{ciel\_gazeux})}$$
Le nombre de modules est alors simplement $N_{\text{modules}} = L_{\text{total}} / L_{\text{tube}}$. Cette formulation garantit une cohérence mathématique parfaite entre le volume géométrique interne disponible, la masse de MCP introduite et les coûts de fabrication.

#### Q18 : Qu'en est-il du critère d'espacement des ailettes pour D < 100 mm avec 8 ailettes ?
**Réponse Technique** : 
Pour les petits diamètres ($D < 100 \text{ mm}$), une configuration à 8 ailettes rapprocherait trop les ailettes au niveau de la racine, créant un espacement inférieur au seuil critique de $50 \text{ mm}$ anti-givre. Dans cette zone, le givre comblerait rapidement l'espace, créant une couche isolante permanente et bloquant le flux d'air. Le code de simulation exclut désormais automatiquement de la grille d'optimisation toute configuration à 8 ailettes pour un diamètre inférieur à 100 mm.

#### Q19 : Les cylindres recommandés tiennent-ils physiquement au plafond ?
**Réponse Technique** : 
L'application calcule désormais l'encombrement au sol projeté au plafond de la batterie thermique en tenant compte du diamètre externe des tubes, de la longueur des ailettes externes ($30 \text{ mm}$ de chaque côté) et de l'espacement de sécurité anti-givre requis de $50 \text{ mm}$ entre tubes adjacents. 
L'interface de l'**Onglet 1** affiche le taux d'occupation du plafond de la chambre froide. Si ce taux dépasse $100\%$ (ce qui peut arriver pour de très petites chambres avec une grande autonomie demandée), un avertissement est affiché suggérant de réduire l'autonomie ou de concevoir une disposition sur deux niveaux superposés.

#### Q20 : Avez-vous dimensionné les suspentes de la structure ?
**Réponse Technique** : 
Oui. Pour transformer cette affirmation qualitative en donnée d'ingénierie concrète, le modèle calcule le nombre de points d'ancrage structurels requis. En fixant une charge de sécurité maximale de $300 \text{ kg}$ par suspente filetée en acier galvanisé de classe 8.8 (diamètre M10, facteur de sécurité mécanique global de 3), le nombre de suspentes requis est calculé par :
$$N_{\text{suspentes}} = \text{ceil}\left(\frac{\text{Masse}_{\text{structure}} + \text{Masse}_{\text{MCP}} \times 1.10}{300}\right)$$
Cette spécification figure désormais dans la fiche CAO de l'Onglet 1.

---

### E. Modèle économique et ROI

#### Q21 : Pourquoi la prime fixe d'économie Sonelgaz (80 000 DA/an) est-elle constante quelle que soit la taille de la chambre ?
**Réponse Technique** : 
Ce point a été corrigé. Une économie forfaitaire de $80 \text{ 000 DA}$ sur la prime de puissance souscrite n'était pas réaliste pour les petites installations. Nous l'avons indexée sur la taille de l'installation frigorifique en utilisant une formule d'échelle proportionnelle au volume de la chambre :
$$\text{Prime}_{\text{savings}} = 10000.0 + 700.0 \times V_{\text{chambre}} \quad (\text{DA/an})$$
Ce calcul est plus représentatif de la baisse de la prime de puissance souscrite auprès de Sonelgaz grâce à l'effacement de la pointe de puissance du compresseur.

#### Q22 : DAYS_OP_YEAR = 330 : sur quelle base ? Quelle est la sensibilité de ce paramètre ?
**Réponse Technique** : 
La valeur de 330 jours d'exploitation par an est une convention standard en agroalimentaire. Elle retire 35 jours par an pour les arrêts techniques, le nettoyage complet annuel de la chambre froide, les opérations de maintenance de la centrale frigorifique et les jours fériés chômés. Si l'installation fonctionne 365 jours/an, le temps de retour sur investissement diminue d'environ $10\%$. S'il descend à 300 jours/an, le payback s'allonge de $9\%$. C'est un paramètre linéaire direct sur les économies de fonctionnement.

#### Q23 : Pourquoi ne pas utiliser d'indicateurs actualisés (VAN, TRI actualisé) ?
**Réponse Technique** : 
Bien que le payback simple soit le premier indicateur demandé par les clients industriels pour un arbitrage rapide, nous avons enrichi le modèle économique dans l'**Onglet 2** en intégrant des indicateurs financiers actualisés de niveau bancaire :
* **VAN (Valeur Actuelle Nette)** calculée sur 10 ans avec un taux d'actualisation de $8\%$, un taux d'inflation de l'énergie de $5\%$ par an (hausse attendue des tarifs Sonelgaz) et un coût annuel de maintenance de la batterie de $2\%$ de l'investissement initial.
* **TRI (Taux de Rentabilité Interne) actualisé** sur la durée de vie du projet.
Ces métriques valident la viabilité financière intrinsèque de notre projet devant un jury de financiers.

#### Q24 : Pourquoi la sensibilité économique ne teste-t-elle que le prix de l'aluminium ?
**Réponse Technique** : 
L'aluminium représente la principale incertitude de coût de fabrication locale en Algérie (fluctuation des cours des métaux et extrusion). C'est pourquoi il est le paramètre principal de sensibilité. Le modèle financier a cependant été structuré de manière modulaire, ce qui permettrait d'ajouter facilement des analyses de sensibilité sur le coût de la paraffine ou la tarification de l'électricité.

#### Q25 : L'arbitrage quotidien de charge (330 cycles/an) est-il compatible avec la fatigue thermique ?
**Réponse Technique** : 
Oui. Les contraintes thermomécaniques induites par le changement de phase de la paraffine à basse température (inférieure à $30^\circ\text{C}$) sont extrêmement faibles par rapport aux cycles thermiques des moteurs ou des chaudières (pas de chocs thermiques brutaux). L'aluminium possède une excellente ductilité et le ciel gazeux compense entièrement l'expansion volumique, éliminant tout phénomène de fatigue plastique sur les parois.

#### Q26 : Le score d'optimisation (autonomie/coût) est-il aligné avec le payback ?
**Réponse Technique** : 
Le score d'optimisation privilégie l'**efficacité technico-économique intrinsèque** de la batterie ($\text{Autonomie} / \text{Coût}$). Il est possible qu'une configuration présente un score légèrement inférieur mais un payback plus court si elle tire profit d'un meilleur arbitrage ou d'une puissance d'infiltration plus faible. L'Onglet 4 permet au client de trier directement le tableau complet selon la colonne de son choix (trier par TRI pour un choix purement financier, ou par score d'optimisation pour un choix technique).

---

### F. Faisabilité de recharge nocturne et compresseur

#### Q27 : La puissance du compresseur (P_Compressor_Est_kW) est-elle mesurée ou estimée ?
**Réponse Technique** : 
Dans la version précédente du simulateur, elle était estimée par une formule simplifiée liée à la charge de pointe. Désormais, le simulateur prend en compte la **puissance frigorifique nominale réelle** spécifiée directement par le client dans la barre latérale ("*Puissance du compresseur existant*"). Cela permet de réaliser un véritable test d'adéquation sur site, sans approximations théoriques.

#### Q28 : Le COP nocturne est-il vraiment meilleur pour une chambre négative (-18°C) ?
**Réponse Technique** : 
C'est une excellente question de thermodynamique.
1. **Facteur dégradant** : Pour solidifier le MCP à $-21^\circ\text{C}$, la consigne d'évaporation du groupe frigorifique doit descendre à $-26^\circ\text{C}$ (au lieu de $-23^\circ\text{C}$ en fonctionnement direct pour maintenir l'air de la chambre à $-18^\circ\text{C}$). Cet écart de $-3 \text{ K}$ diminue le COP d'environ $5\%$.
2. **Facteur améliorant** : La nuit, la température extérieure moyenne descend à $25^\circ\text{C}$ (au lieu de $45^\circ\text{C}$ lors de la pointe d'été). La température de condensation baisse ainsi de $20 \text{ K}$, ce qui améliore le COP d'environ $25\%$.
Le bilan net est largement positif : le COP nocturne réel est environ **$20\%$ supérieur** au COP de pointe diurne, confirmant l'intérêt thermodynamique et financier de la recharge de nuit.

#### Q29 : La durée de 8h est-elle négociée ou fixe ?
**Réponse Technique** : 
Les 8 heures correspondent au tarif réglementé standard Heures Creuses de Sonelgaz en Algérie (généralement de 23h00 à 07h00). Cependant, le client peut ajuster ce paramètre de $4$ à $12 \text{ heures}$ dans la barre latérale pour s'adapter à des profils de tarification spécifiques ou à des contraintes de décharge nocturne partielles.

#### Q30 : Que se passe-t-il en cas de coupure de courant pendant la recharge nocturne ?
**Réponse Technique** : 
En cas de coupure de courant nocturne empêchant la recharge complète du MCP, la batterie n'aura stocké qu'une fraction de son énergie nominale. Dans ce cas, la régulation de la chambre froide gère l'autonomie au prorata de l'énergie stockée. Pour pallier cela, le système d'automatisme frigorifique intègre une alarme de recharge incomplète et adapte les cycles de fonctionnement diurnes pour minimiser les ouvertures de portes le jour suivant.
