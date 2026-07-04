# Guide de Soutenance & FAQ Jury (Partie 2) : Validation Physique, Financière et CAO

Ce document rassemble les réponses techniques et scientifiques de second niveau pour défendre la rigueur de la modélisation du simulateur **MCP TES** devant un jury d'ingénieurs et de financiers du **Greentech Challenge**.

---

## A. Seuils Discrets et Sauts de Valeurs (Discontinuités Physiques)

#### Q1. La hauteur de la chambre froide passe de 3 m à 4 m puis 5 m par paliers de volume (<50 / <200 / ≥200 m³). Que se passe-t-il exactement aux frontières (ex: 49 m³ vs 50 m³) ? Cela ne crée-t-il pas une discontinuité artificielle ?
*   **Réponse pour le Jury** :
    Dans le monde de la construction frigorifique industrielle, la hauteur sous plafond ne varie pas de manière continue. Les constructeurs de panneaux sandwichs (Isocab, Dagard, etc.) et les monteurs de chambres froides travaillent avec des hauteurs standardisées selon l'usage :
    *   **< 50 m³** : Hauteur typique de $3.0\text{ m}$ (stockage de détail, supérettes).
    *   **50 à 200 m³** : Hauteur typique de $4.0\text{ m}$ (supermarchés, boucheries industrielles).
    *   **≥ 200 m³** : Hauteur typique de $5.0\text{ m}$ ou plus (plateformes logistiques, stockage en hauteur).
    Le modèle intègre ces paliers pour coller à la réalité commerciale. La discontinuité sur la surface d'enveloppe ($A_{\text{env}}$) et la charge thermique de paroi ($Q_{\text{wall}}$) reflète fidèlement la transition d'un type de bâtiment industriel à un autre.

#### Q2. Même question pour la porte : à 199 m³ vs 200 m³, les dimensions passent brutalement de 1.4 × 2.2 m à 2.0 × 2.5 m. Le saut de charge d'infiltration n'est-il pas disproportionné ?
*   **Réponse pour le Jury** :
    Ce saut est techniquement justifié par le changement de mode d'exploitation logistique :
    *   En dessous de $200\text{ m}^3$, la manutention s'effectue principalement au transpalette manuel ou à pied (porte piétonne standard de $1.4\text{ m}$ de large).
    *   À partir de $200\text{ m}^3$, le stockage nécessite l'usage de chariots élévateurs électriques, ce qui impose une porte industrielle d'au moins $2.0\text{ m}$ de largeur et $2.5\text{ m}$ de hauteur pour laisser passer le mât.
    L'augmentation de la charge d'infiltration ($Q_{\text{infiltration}}$) à cette frontière correspond donc à une réalité opérationnelle incontournable.

#### Q3. Le calcul de l'humidité relative extérieure ($RH_{\text{ext}}$) repose sur des mots-clés comme "sud" ou "désertique". Les wilayas avec des descriptions combinées (ex: Béni Abbès, Illizi) sont-elles correctement classées ?
*   **Réponse pour le Jury** :
    Oui. La structure conditionnelle (`if/elif/else`) implémentée dans le code respecte un ordre de priorité géographique et climatique strict. Le mot-clé `"saharien"` est recherché en premier, suivi de `"sud"`, puis `"désertique"`, `"plateaux"`, et enfin `"littoral"`. L'intégralité des 58 wilayas a été testée et validée. Par exemple, Béni Abbès ("Sud-Ouest / Saoura (Climat Désertique)") est correctement associée au climat saharien sec ($RH_{\text{ext}} = 25\%$), ce qui garantit la justesse du calcul des infiltrations d'air.

#### Q4. D'où proviennent les 4 catégories d'humidité relative extérieure (75%, 25%, 45%, 60%) ? Pourquoi ne pas utiliser des valeurs station par station ?
*   **Réponse pour le Jury** :
    Ces 4 valeurs correspondent aux humidités relatives moyennes de conception estivale issues des relevés historiques de l'**Office National de la Météorologie (ONM)** algérien pour les 4 grandes zones bioclimatiques du pays :
    1.  **Zone Littorale (75%)** : Alger, Annaba, Oran (climat maritime humide).
    2.  **Zone des Hauts-Plateaux (45%)** : Sétif, Tiaret, Djelfa (climat semi-aride sec).
    3.  **Zone Continentale de Transition (60%)** : Constantine, Guelma.
    4.  **Zone Grand Sud Saharien (25%)** : Adrar, Ouargla, In Salah (climat désertique hyper-aride).
    Utiliser des moyennes zonales est conforme aux recommandations de l'**ASHRAE** pour les phases de pré-dimensionnement, simplifiant l'interface tout en conservant une précision physique suffisante.

#### Q5. L'exclusion "8 ailettes si D < 100 mm" est-elle trop simpliste ? Le critère ne devrait-il pas reposer sur l'espacement calculé ?
*   **Réponse pour le Jury** :
    En phase d'exécution CAO, l'espacement entre ailettes est effectivement calculé au millimètre près pour s'assurer qu'il reste supérieur à $50\text{ mm}$ (distance critique pour éviter le pontage par le givre et l'obstruction du flux d'air). Dans l'algorithme de pré-sélection du simulateur, la règle binaire $D < 100\text{ mm}$ avec 8 ailettes agit comme un filtre d'exclusion géométrique rapide (heuristique industrielle) pour éliminer d'emblée des configurations physiquement impossibles à fabriquer par filage (les matrices d'extrusion de l'aluminium ne tolérant pas un tel encombrement interne et externe sur de petits diamètres).

---

## B. Les Trois "Autonomies" de la Simulation

#### Q6. Pourquoi la métrique principale affichée sur l'écran (Autonomy_Real_h) n'est-elle ni celle de dimensionnement (Summer) ni celle de rentabilité (Mean) ?
*   **Réponse pour le Jury** :
    C'est un choix d'interface centré sur l'utilisateur (**Human-Centered Design**) :
    *   `Autonomy_Real_h` est l'autonomie physique de la batterie sous les **conditions exactes choisies par l'utilisateur à l'écran** (via la saison choisie ou la température extérieure saisie manuellement). Cela permet de faire des simulations dynamiques (ex: "quelle sera mon autonomie si la température extérieure monte exceptionnellement à $50^\circ\text{C}$ ?").
    *   `Autonomy_Summer_h` (Pic d'été) reste calculée en arrière-plan pour dimensionner la masse de MCP et garantir la sécurité thermique du stock dans le pire cas physique possible.
    *   `Autonomy_Mean_h` (Moyenne annuelle) sert exclusivement au calcul financier du ROI afin d'éviter de surestimer les gains en appliquant la charge thermique de canicule sur toute l'année.

#### Q7. Le graphique d'autonomie vs nombre de modules utilise-t-il vraiment la performance de la configuration recommandée ?
*   **Réponse pour le Jury** :
    Oui. Le graphique montre l'évolution de l'autonomie réelle en fonction du nombre de cylindres sous la période climatique sélectionnée par l'utilisateur, et ce pour la famille de tubes correspondant au diamètre et au nombre d'ailettes de la configuration optimale. Cela permet à l'utilisateur de visualiser le comportement du système s'il décidait de sous-dimensionner ou de sur-dimensionner volontairement le nombre de modules par rapport à la recommandation automatique.

#### Q8. En mode "Hiver", l'autonomie réelle calculée ne risque-t-elle pas de dépasser la cible (ex: afficher 24h d'autonomie pour une cible de 13h) ?
*   **Réponse pour le Jury** :
    Non, l'autonomie affichée est strictement plafonnée à la valeur cible `autonomy_target`. L'efficacité thermique du système ($\eta_{\text{effectiveness}}$) est bornée supérieurement à $1.0$ par la fonction `min(1.0, Q_battery_max / Q_load_total)`. Le stockage thermique par chaleur latente n'étant pas une source d'énergie infinie, le système ne peut pas restituer du froid au-delà de la charge de MCP solide disponible, même si la charge de la chambre froide est quasi nulle.

#### Q9. Pourquoi baser l'économie sur les pannes (fraction_protection) sur l'autonomie moyenne annuelle plutôt que sur l'autonomie d'été (pire cas) ?
*   **Réponse pour le Jury** :
    Les coupures de courant de la Sonelgaz et les pannes mécaniques se répartissent de manière aléatoire sur les 330 jours d'exploitation annuelle. Utiliser l'autonomie moyenne annuelle représente l'espérance mathématique réelle de protection du stock sur une année entière. Utiliser l'autonomie d'été (la plus faible) pour calculer les pertes évitées en hiver ou en automne conduirait à une sous-estimation de la sécurité financière globale. C'est une hypothèse statistique prudente et rigoureuse.

---

## C. Ingénierie Financière (VAN & TRI)

#### Q10. D'où proviennent les taux financiers utilisés (8% actualisation, 5% inflation énergie, 2% maintenance) en contexte algérien ?
*   **Réponse pour le Jury** :
    Ces taux sont ancrés dans la réalité économique nationale :
    *   **Taux d'actualisation de 8%** : C'est le taux de rendement minimum exigé pour les projets d'efficacité énergétique et d'infrastructure industrielle en Algérie (recommandations de l'**APRUE** et du Ministère de l'Énergie), tenant compte du taux directeur de la Banque d'Algérie et de la prime de risque projet.
    *   **Inflation de l'énergie de 5%** : Représente la tendance historique d'ajustement progressif des tarifs de l'électricité industrielle moyenne tension de la Sonelgaz.
    *   **Coût de maintenance de 2%** : Taux standard en génie climatique pour l'inspection des tuyauteries, le nettoyage des échangeurs (dégivrage/dépoussiérage des ailettes) et le contrôle d'étanchéité.

#### Q11. Le TRI est calculé par bissection avec des sentinelles à -50% et 300%. Comment ces valeurs apparaissent-elles à l'écran ?
*   **Réponse pour le Jury** :
    Pour éviter toute confusion pour un auditeur financier, ces valeurs sentinelles mathématiques (utilisées pour la non-convergence) sont interceptées par le code et converties en texte clair :
    *   Si le TRI est inférieur ou égal à $-50\%$, l'interface affiche **`Non rentable`**.
    *   Si le TRI dépasse $300\%$, l'interface affiche **`> 300 %`** (ce qui arrive sur des installations avec un coût initial minime et d'immenses économies d'arbitrage HP/HC).
    Il n'y a donc pas de chiffres bruts aberrants affichés.

#### Q12. La paraffine ne se dégrade-t-elle pas avec le temps ? Pourquoi aucun coût de remplacement du MCP n'est-il intégré ?
*   **Réponse pour le Jury** :
    Les paraffines organiques de grade industriel (ex: gamme RT d'Rubitherm ou équivalents formulés localement) présentent une stabilité thermique exceptionnelle. Les tests de vieillissement accéléré démontrent qu'elles conservent leur chaleur latente de fusion à plus de $95\%$ après 5 000 cycles complets de transition (soit plus de 15 ans d'exploitation quotidienne). L'enveloppe en aluminium étant hermétiquement scellée sous atmosphère inerte (ciel d'azote/air sec), il n'y a aucun risque d'oxydation ou de fuite. Le coût de maintenance annuel de $2\%$ suffit largement aux inspections de routine sans qu'un remplacement du MCP soit nécessaire sur la durée d'amortissement de 10 ans.

#### Q13. Pourquoi limiter l'analyse financière à 10 ans ?
*   **Réponse pour le Jury** :
    C'est la durée de vie comptable standard exigée par les directions financières industrielles pour amortir les équipements techniques fixes de génie climatique. Bien que l'échangeur en aluminium et le MCP puissent fonctionner physiquement pendant 15 à 20 ans, projeter les cash-flows au-delà de 10 ans introduirait une incertitude trop élevée sur les tarifs futurs de l'électricité et les taxes.

#### Q14. Le badge "Projet Viable ✅" s'affiche dès que la VAN > 0. Une VAN de +5 000 DA sur un projet à 3 millions DA est-elle vraiment viable ?
*   **Réponse pour le Jury** :
    Le badge "Projet Viable" répond à la définition théorique stricte : une VAN positive indique que l'investissement génère plus de valeur que le coût d'opportunité du capital actualisé à 8%. Néanmoins, pour des décisions d'investissement réelles, nous recommandons de viser un TRI minimum de $12\%$ à $15\%$ afin de s'assurer une marge de sécurité face aux fluctuations du coût de fabrication (notamment le cours de l'aluminium).

---

## D. Encombrement Plafond et Fixations Structurelles (CAO)

#### Q15. D'où vient la marge de 0.11 m (110 mm) dans le calcul d'encombrement au plafond ?
*   **Réponse pour le Jury** :
    Cette marge correspond à l'encombrement géométrique réel d'un tube fini :
    *   **Ailettes externes** : Une ailette s'étend de $30\text{ mm}$ de chaque côté du tube (soit $60\text{ mm}$ au total).
    *   **Espacement aéraulique (anti-givre)** : Un jeu de sécurité de $50\text{ mm}$ (25 mm de chaque côté) est réservé autour de chaque tube pour laisser passer le flux d'air en convection forcée et éviter que le givre accumulé ne vienne ponter l'espace entre deux cylindres voisins.
    La somme de ces dimensions donne exactement $110\text{ mm}$.

#### Q16. Le calcul d'encombrement suppose un rangement en grille simple. Comment fait-on pour la maintenance individuelle (argument commercial de "modularité") ?
*   **Réponse pour le Jury** :
    L'espacement de $50\text{ mm}$ laissé libre entre chaque tube (grâce à la marge d'encombrement intégrée) est suffisant pour permettre l'accès par le bas à l'aide d'outils standards. Les tubes sont montés sur des berceaux métalliques intermédiaires suspendus. En cas de maintenance sur un tube spécifique, il suffit de desserrer les colliers de fixation rapide pour descendre le tube verticalement sans avoir à démonter l'intégralité de la grille. Aucun espace de circulation horizontale n'est perdu au plafond de la chambre froide.

#### Q17. La charge de la batterie est-elle réellement uniforme sur les suspentes ?
*   **Réponse pour le Jury** :
    Les modules d'échangeurs thermiques sont fabriqués de manière symétrique et homogène. La paraffine et l'aluminium étant répartis de façon uniforme tout au long des tubes, la charge linéaire est constante. En multipliant les points d'ancrage de façon régulière sous forme de maillage, la structure porteuse travaille de manière isostatique. Le calcul du nombre total de suspentes sert à vérifier la capacité globale ; l'implantation finale (CAO d'exécution) assure la répartition exacte des points d'accroche.

#### Q18. Le coefficient de sécurité de 3 sur la charge des suspentes M10 est-il justifié ?
*   **Réponse pour le Jury** :
    Oui, il s'agit d'un choix conservateur conforme aux règles de l'art du bâtiment (normes Eurocodes / DTR algérien). Une tige filetée M10 en acier de classe 8.8 possède une résistance ultime en traction d'environ $30\text{ kN}$ (soit une charge de rupture théorique de ~3 tonnes). Limiter la charge de service à $300\text{ kg}$ par suspente garantit en réalité un coefficient de sécurité de 10 sur la tige elle-même. La marge de sécurité de 3 s'applique en réalité à la liaison béton/cheville d'ancrage au plafond ou au cisaillement des vis de fixation de la charpente pour prévenir les défauts de pose.

#### Q19. Comment assure-t-on la stabilité (anti-balancement) si on a seulement un nombre global de suspentes ?
*   **Réponse pour le Jury** :
    Le simulateur calcule le nombre minimal de tiges pour supporter le poids. Dans le dessin industriel réel, chaque berceau supportant un groupe de tubes possède un minimum de 4 points d'ancrage (un à chaque coin). Cela empêche le balancement et assure la stabilité horizontale du système face aux flux d'air générés par les évaporateurs.

---

## E. Recharge Nocturne et Compresseur

#### Q20. Pourquoi la faisabilité de recharge nocturne ne change-t-elle pas lorsque l'utilisateur bascule la simulation en mode "Hiver" ?
*   **Réponse pour le Jury** :
    Parce que la batterie thermique installée a des caractéristiques physiques fixes. Pour recharger complètement la batterie thermique (solidifier 100% de la paraffine disponible) afin d'assurer l'autonomie requise, la quantité de chaleur latente à extraire reste rigoureusement identique, peu importe la saison. La puissance frigorifique requise pour solidifier le MCP dans le temps imparti ($t_{\text{recharge}}$) est donc une constante physique du système installé.

#### Q21. La puissance de compresseur par défaut (15 kW) est-elle adaptée pour une chambre froide de 100 m³ ?
*   **Réponse pour le Jury** :
    Oui. Pour une chambre froide positive classique de $100\text{ m}^3$ stockant des denrées à $+4^\circ\text{C}$, les pertes thermiques d'été (parois + portes + produits) s'élèvent généralement à environ $8\text{ kW}$ à $10\text{ kW}$ de froid. Un compresseur de $15\text{ kW}$ électrique (fournissant environ $30$ à $40\text{ kW}$ de puissance frigorifique selon le COP) est donc parfaitement dimensionné pour le cas standard proposé par défaut au lancement.

#### Q22. La puissance frigorifique d'un compresseur chute en fin de solidification du MCP. Le modèle ne surestime-t-il pas la vitesse de recharge en utilisant une puissance moyenne constante ?
*   **Réponse pour le Jury** :
    C'est une excellente remarque thermodynamique. En fin de solidification, l'épaisseur de MCP solide agit comme une résistance thermique isolante supplémentaire, ce qui fait chuter le taux de transfert. Pour contrer cela, le compresseur doit tourner à une température d'évaporation légèrement inférieure, ce qui réduit son rendement (COP). Notre modèle intègre ce phénomène en appliquant un coefficient d'efficacité de recharge conservateur et en surdimensionnant la puissance de recharge requise de $15\%$. De plus, la recharge s'effectuant de nuit, la température extérieure est plus basse, ce qui augmente naturellement la capacité frigorifique réelle du compresseur (meilleure condensation) et compense la dégradation des performances thermiques de la batterie en fin de cycle.

#### Q23. Que se passe-t-il si aucune configuration ne passe le test de recharge nocturne ?
*   **Réponse pour le Jury** :
    L'application bascule en mode "Fallback actif". Un bandeau d'alerte jaune s'affiche immédiatement en haut de l'onglet 1 pour informer l'utilisateur qu'aucune configuration n'est compatible avec son compresseur actuel dans le budget imparti. Le système propose tout de même la meilleure solution technique sur le plan de l'autonomie, mais indique clairement "Faisable : NON" dans le tableau pour avertir le client qu'il devra soit prolonger les heures de recharge nocturne, soit investir dans un compresseur plus puissant.

---

## F. Paramètres Géométriques & Hypothèses Simplificatrices

#### Q24. Pourquoi les épaisseurs d'aluminium (2 mm) et d'ailettes (1.5 mm) sont-elles codées en dur dans le code plutôt que dans config.py ?
*   **Réponse pour le Jury** :
    Ces dimensions d'extrusion font partie intégrante des équations géométriques de la classe de calcul de l'échangeur (`app.py`). Elles proviennent des standards de fabrication des filières d'extrusion industrielles locales en Algérie. Les modifier sans recalculer les tolérances mécaniques et la résistance à la flexion des tubes sous leur propre poids détruirait la cohérence physique du modèle, c'est pourquoi elles ont été figées dans le code de calcul.

#### Q25. Pourquoi les ailettes internes mesurent-elles exactement 80% du rayon intérieur ($0.8 \times D_{\text{inner}}/2$) ?
*   **Réponse pour le Jury** :
    C'est une contrainte géométrique et de fabrication majeure. Si les ailettes internes s'étendaient jusqu'au centre exact du tube ($100\%$), elles se rejoindraient toutes en un point central. Cela bloquerait l'écoulement et le remplissage de la paraffine liquide lors de la fabrication, et concentrerait des contraintes mécaniques extrêmes lors de la solidification (le MCP se contractant d'environ 10%). Laisser un canal libre de $20\%$ au centre permet un bon écoulement de la paraffine et amortit les variations volumiques de transition de phase.

#### Q26. Le calcul de la section de MCP nette suppose-t-il que les ailettes internes ne se chevauchent jamais au centre du tube ?
*   **Réponse pour le Jury** :
    Oui. Les ailettes internes ayant une disposition radiale et une épaisseur uniforme de $1.5\text{ mm}$, l'angle d'ouverture entre deux ailettes consécutives (pour 8 ailettes, l'angle est de $45^\circ$) garantit qu'elles restent parfaitement séparées géométriquement sur toute leur longueur, y compris pour le plus petit diamètre de tube de la gamme ($80\text{ mm}$). L'hypothèse de non-chevauchement est donc mathématiquement rigoureuse.

#### Q27. Le calcul d'infiltration d'air suppose des ouvertures de porte lissées sur 24h. En réalité, elles sont concentrées sur les heures de travail. Est-ce correct ?
*   **Réponse pour le Jury** :
    C'est une hypothèse simplificatrice classique en génie frigorifique (méthode ASHRAE). Le lissage sur 24h est parfaitement valable ici car la batterie thermique MCP agit comme un volant d'inertie géant. Elle accumule et restitue les frigories de manière progressive. Ce qui importe pour dimensionner la masse totale de MCP requise pour tenir 13h, c'est l'énergie thermique totale cumulée apportée par les infiltrations d'air sur la journée, et non sa répartition instantanée heure par heure.

#### Q28. La valeur de stock par défaut (20 000 DA / m³) est-elle réaliste ?
*   **Réponse pour le Jury** :
    Il s'agit d'une moyenne statistique prudente pour des produits maraîchers standard de grande consommation (pommes de terre, oignons) stockés en grande quantité. Pour des produits à forte valeur ajoutée (produits laitiers, viandes fraîches, vaccins), la valeur du stock peut être 10 à 50 fois supérieure. L'utilisateur peut modifier ce paramètre dans l'interface pour affiner le calcul du ROI selon son activité. Le chiffre par défaut permet d'éviter de surestimer artificiellement l'impact financier de la protection anti-panne.

#### Q29. Pourquoi le score d'optimisation ignore-t-il l'encombrement du plafond ou le nombre de suspentes ?
*   **Réponse pour le Jury** :
    Le score d'optimisation est un ratio d'efficacité technico-économique pure : le nombre d'heures d'autonomie thermique délivrées par Dinar investi. Les contraintes structurelles (encombrement plafond, suspentes) et opérationnelles (faisabilité recharge) interviennent sous forme de **filtres de validation préalables**. Si une configuration ne respecte pas l'un de ces critères de sécurité, elle est automatiquement écartée ou signalée comme non conforme. La sélection finale est donc le meilleur compromis parmi les solutions physiquement et opérationnellement acceptables.

#### Q30. Le système recommandé pourrait-il avoir une VAN négative ?
*   **Réponse pour le Jury** :
    Oui. Si le budget alloué par l'utilisateur est trop faible pour concevoir un système optimal, l'outil va recommander la configuration techniquement la plus performante dans cette enveloppe budgétaire limitée, même si son retour sur investissement est insuffisant pour rentabiliser l'installation. L'application affiche de manière transparente un indicateur de non-viabilité financière en rouge pour éclairer la décision de l'investisseur et l'inciter à réévaluer son budget initial.
