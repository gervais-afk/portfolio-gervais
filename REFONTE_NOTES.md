# Portfolio et CV — livraison locale du 16 novembre 2026

## Périmètre

Modifications limitées à `C:\Users\HP\Desktop\portfolio-gervais`. Aucun commit, push ou déploiement. Les projets K1-MathInfo et Dataset Automator n’ont pas été modifiés. Aucun fichier de secrets ou d’identifiants consulté.

Sauvegarde initiale des sources et CV : `scratch/portfolio_before_refresh_20261116_100831.zip`. Les images, podcasts et lettres de motivation d’origine sont préservés. Les anciennes bannières restent sur disque, mais ne sont plus utilisées dans le parcours principal.

## Illustrations à partir des cinq images fournies (16 novembre 2026)

État actuel des cartes : les trois SVG conceptuels de l’itération précédente sont remplacés par des compositions basées sur les images de l’utilisateur. Les SVG restent sur disque. Sauvegarde : `scratch/portfolio_before_project_photos_20261116_135307.zip`.

- **K1** : capture principale complète et détail du graphe dans un montage ; zone des noms/libellés du graphe floutée dans les dérivés publics. La copie principale n’est pas modifiée, ni aucun chiffre ajouté. Les noms du graphe ne sont pas nécessaires pour expliquer la structure.
- **Archi Cam AI** : extrait du triptyque structure/BIM/rendu du bâtiment associé à la capture du site. Recadrage de l’infographie à 29–87 % de sa hauteur pour exclure les bandeaux et anciennes coordonnées. Le bâtiment reste explicitement une illustration conceptuelle, jamais un chantier réalisé. La capture du site conserve ses textes d’origine ; la légende précise que ses promesses commerciales ne sont pas une validation des fonctionnalités.
- **Dataset Automator** : capture du prototype mise en cadre ; statut prototype et vues/métriques partiellement simulées indiqués sur la carte et dans la galerie.
- `scripts/build_project_media.py` produit uniquement des dérivés dans `assets/images/projects/` : compositions 800/1 440 px en WebP, cinq vues séparées et `media-sources.json` avec traitements et SHA-256 des originaux. Les cinq fichiers source à la racine sont préservés octet pour octet. Les compositions 800 px pèsent environ 22–65 Ko ; variantes 1 440 px environ 48–159 Ko.
- Chaque carte permet d’agrandir sa composition dans un nouvel onglet. Les fiches comprennent une galerie (2 vues K1, 2 Archi, 1 Dataset) ; chaque image s’ouvre aussi séparément. Légendes FR/EN, interfaces conservées dans leur langue d’origine, alternatives textuelles dans les galeries. Aucun nouveau contenu fonctionnel ou résultat inventé.
- Vérifications relancées : 22 combinaisons langue/largeur, galeries FR/EN à 320/768/1 440 px, ouverture du lien d’agrandissement, décodage de chaque image, empreintes des cinq originaux, clavier et six modales par langue, CV et téléchargements inchangés. Zéro violation automatique axe dans les 18 états contrôlés après relance (premier démarrage de l’audit : connexion locale refusée transitoire). Pas de certification d’accessibilité revendiquée.
- Aperçu : `scratch/qa/refresh_fr_projects.png`. Aucun commit, push ou déploiement. Serveur local d’aperçu relancé sur `127.0.0.1:4173` après son arrêt par le redémarrage du serveur de l’outil.

## Sublimation visuelle — atelier IA & Data (16 novembre 2026, itération initiale)

Direction approuvée et appliquée localement, sans commit, push ou déploiement. Sauvegarde avant cette passe : `scratch/portfolio_before_sublimation_20261116_131958.zip`.

- `style.css` réorganisé : ivoire `#F8F6F0`, navy `#142E3C`, teal `#126B63`, grille technique discrète, portrait architectural conservant l’image originale, cartes et section contact retravaillées. Texte courant au moins 14 px dans les zones testées, légendes 11 px.
- Manrope variable 200–800 et Newsreader italique 400 auto-hébergées en WOFF2 ; environ 57 Ko au total. Sources, conversion et licences SIL OFL dans `assets/fonts/`. Aucun CDN ou service de polices pendant la visite. CV inchangés par cette passe.
- Trois SVG originaux dans `assets/images/editorial/` : documents/graphe K1, maquette architecturale Archi Cam AI et données/notebook Dataset Automator. Créations vectorielles avec profondeur et gradients, **pas des images générées photoréalistes, captures de logiciel ou preuves de résultats**. Moins de 9 Ko chacun. Légende conceptuelle sur chaque carte, aucune ressource externe embarquée.
- Positionnement du hero aligné sur le CV (« Ingénieur IA & Architecte Data » / « AI Engineer & Data Architect »), sans modification de diplôme. Le bouton « Consulter mon CV » ouvre les versions Web et leurs téléchargements. Contextes de projets affichés sur les cartes ; limites, statuts de prototype et avertissements éditoriaux préservés.
- Entrées courtes du hero, illustrations et étapes ; aucune animation permanente ni défilement forcé. Réduction des mouvements respectée au chargement et si la préférence change pendant la visite. Contenu visible sans JavaScript.
- Contrôles : `scripts/check_visual_refresh.py` passe sur 22 combinaisons langue/largeur (FR/EN, 320 à 1 920 px), mode fichier et mobile sans JS. `scripts/check_portfolio.py` passe : six fiches par langue, clavier/focus, menus, absence de requête audio initiale, téléchargements CV et absence d’erreurs JS/HTTP locales.
- Audit axe-core 4.10.3 : contraste des numéros de projet corrigé, puis zéro violation automatique dans les 18 états testés (pages FR/EN, six modales dans chaque langue sur desktop, page et modale Dataset sur mobile FR/EN). Rapport `scratch/qa/axe_visual_refresh.json`. Ce contrôle automatisé n’est pas une certification WCAG et conserve des éléments nécessitant une revue humaine. La dépendance axe n’est utilisée que pour l’audit local dans `scratch/qa/`, jamais chargée par le portfolio.
- Aperçus : `scratch/qa/refresh_fr_hero.png`, `refresh_fr_projects.png`, `refresh_fr_contact.png`, variantes EN et captures mobiles du contrôle principal. Aucun score de performance réseau réel revendiqué pour cette passe.

## Livraison

- Portfolio statique HTML/CSS/JS, thème atelier ivoire/navy/teal, polices WOFF2 locales, portrait WebP optimisé et illustrations SVG originales, sans framework ni CDN.
- Français/anglais : titres, navigation, sections, fiches projet, coordonnées et téléchargements. La langue passe au CV par `?lang=fr` ou `?lang=en`.
- Trois projets principaux : K1-MathInfo, Archi Cam AI et Dataset Automator. Les trois autres réalisations restent consultables.
- Schémas éditoriaux identifiés comme tels, sans les faire passer pour des captures de logiciel.
- Fiches projet : contexte, contribution, approche, technologies, limites et liens disponibles.
- Navigation mobile, accès clavier, focus de modale, fermeture par Échap/bouton/fond, lien d’évitement et préférence de mouvement réduit.
- Animations d’apparition ponctuelles. Pas de tilt, néons, boucles de pulsation ou bibliothèque d’animation.
- Articles historiques accompagnés d’un avertissement ; podcasts dans une archive explicitement générée par IA, après les projets. Aucun fichier audio demandé au chargement initial, aucun démarrage automatique.

## CV

Source éditoriale commune : `profile.json`.

Contextes précisés par l’utilisateur et ajoutés aux CV FR/EN : K1 réalisé pour le département de mathématiques et informatique de l’Université de Ngaoundéré, Archi Cam AI développé dans le cadre de Google Applied Africa AI Lab, Dataset Automator développé pour le Google Cloud #AllThingsAgentic Hackathon. Les fiches du portfolio sont alignées. Ces mentions décrivent le cadre de réalisation, sans revendiquer de prix, certification ou validation par Google. Après ces ajouts : PDF, impressions Web et DOCX Word toujours sur une page par langue, contenu intégral contrôlé.

Le générateur `build_cv.py` produit :

- `profile.js` pour la page `cv.html` ;
- `KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf` et `KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf` ;
- `KOA_MARIE_GERVAIS_NELLY_CV_ATS_FR.pdf` et `KOA_MARIE_GERVAIS_NELLY_CV_ATS_EN.pdf`, versions candidature complémentaires ;
- les deux DOCX correspondants à la présentation, variante linéaire éditable avec photo ;
- l’alias historique français `KOA_MARIE_GERVAIS_NELLY_CV FR.pdf`, identique au PDF français canonique.

Finition actuelle des CV de présentation : bleu nuit `#172B3A`, titres graphite `#30363D`, texte anthracite `#343A40`, contextes/dates ardoise `#52606D`, icônes bleues `#2167A5`, fond latéral gris perle `#F3F5F7`. Le CV Web est aligné sur cette palette ; les couleurs du portfolio lui-même ne sont pas modifiées. Bandeau PDF réduit de 135 à 112 pt, photo dans un cadre clair fin de 0,8 pt avec espace intérieur et angles discrets, sans ombre ni retouche du portrait. Les grands encadrés de projet disparaissent, remplacés par des filets légers et des points de description ; les rubriques LANGUES et DISTINCTION sont séparées. Les réalisations et contextes restent identiques sur le fond.

Le titre partagé par les CV FR/EN est « Ingénieur IA & Architecte Data » / « AI Engineer & Data Architect » : il s’agit du positionnement professionnel demandé, sans ajout de diplôme ni modification de la formation. La photo `assets/images/cv_portrait.jpg` (480 × 600, environ 66 Ko) est dérivée du portrait original, préservé. Elle est intégrée aux PDF de présentation, au CV Web et aux DOCX, jamais aux PDF candidature. Sauvegardes : `scratch/cv_before_portrait_20261116_105250.zip` et, avant la finition et l’ajout candidature, `scratch/cv_before_polish_ats_20261116_124920.zip`.

Nouvelle répartition approuvée, inspirée de la structure du CV sûreté consulté en lecture seule : deux colonnes PDF, environ 31 % pour les compétences/formation/langues/distinction à gauche et 64 % pour les projets/expérience à droite, séparées par une gouttière. Aucun contenu métier du CV sûreté importé. Grands titres sans numéros : « PROJETS IA & DATA » / « EXPÉRIENCE PROFESSIONNELLE », et équivalents anglais. Les numéros des projets sont aussi retirés. Le CV Web reprend les deux colonnes au-dessus de 640 px et une lecture verticale projets/expérience puis informations complémentaires sur mobile. Le DOM conserve cet ordre de lecture ; aucune promesse de compatibilité universelle des logiciels de recrutement n’est faite. Les DOCX restent une variante linéaire éditable, au contenu synchronisé et sans numéros.

Les PDF de présentation conservent du texte sélectionnable, un corps de **10,5 pt** (compétences/langues : **10 pt**), des titres de rubrique de **12 pt** dans la colonne principale et **11 pt** dans la colonne latérale, des coordonnées/contextes de **9,5 pt**, des icônes vectorielles et six liens cliquables. Génération en zone temporaire puis validation de toutes les langues demandées avant remplacement des fichiers publiés. Le générateur échoue en cas de débordement ; il ne réduit pas silencieusement la police.

Les PDF candidature sont en une colonne, sans photo, icône, fond coloré ou tracé décoratif. Même contenu factuel, source `profile.json` commune ; titres standards PROFIL/PROJETS/EXPÉRIENCE PROFESSIONNELLE/COMPÉTENCES TECHNIQUES/FORMATION/LANGUES/DISTINCTION et équivalents anglais. Corps de 10,5 pt, contextes/contacts à 9,5 pt, six contacts cliquables et ordre d’extraction linéaire contrôlé. Aucun ATS commercial n’a été testé et aucun classement ou taux d’acceptation n’est garanti. La barre du CV Web distingue les boutons « PDF présentation » et « PDF candidature » dans les deux langues ; les téléchargements sont vérifiés octet par octet contre les fichiers locaux.

Niveau d’anglais corrigé selon la déclaration de l’utilisateur : « Anglais intermédiaire : lecture et compréhension orale ; expression orale simple. » Équivalent anglais : « Intermediate English: reading and listening comprehension; basic spoken communication. » Aucun niveau CECRL ni aisance écrite revendiqués.

Les wrappers `build_1page_cv.py`, `build_1page_cv_en.py` et le lanceur `export_cv_pdf.vbs` utilisent désormais cette source commune. Ne pas modifier directement les PDF, `profile.js` ou les DOCX pour changer le contenu : ils seraient remplacés à la prochaine génération.

Le rendu Word des DOCX peut varier selon la version du logiciel et les polices installées. Les deux fichiers ont été repaginés et exportés avec Microsoft Word sur cette machine : une page chacun, contenu intégral vérifié. Les PDF canoniques restent les versions ReportLab.

## Maintenance

Depuis ce dossier, avec Node et le Python disposant de ReportLab, python-docx et pypdf :

```powershell
& 'C:\Users\HP\anaconda3\python.exe' -B -X utf8 build_cv.py
node scripts/sync_static.mjs
```

- `translations.js` : contenu bilingue du portfolio.
- `renderers.js` : fonctions de rendu partagées entre le navigateur et le synchroniseur.
- `scripts/sync_static.mjs` : actualise sept blocs et 76 libellés du HTML français de secours, ainsi que les versions de cache CSS/JS du portfolio et du CV.
- `profile.json` : identité et contenu des CV FR/EN.
- `style.css` / `app.js` : présentation et interactions du portfolio.
- `cv.css` / `cv.js` : présentation et interactions du CV Web.

Le site fonctionne également par ouverture directe de `index.html` ; un serveur HTTP est préférable pour les contrôles et la copie dans le presse-papiers.

Prévisualisation locale :

```powershell
& 'C:\Users\HP\anaconda3\python.exe' -B -m http.server 4173 --bind 127.0.0.1
```

Puis `http://127.0.0.1:4173/` ou `http://127.0.0.1:4173/cv.html`.

## Contrôles réalisés

Commandes de régression, serveur local démarré :

```powershell
& 'C:\Users\HP\anaconda3\python.exe' -B -X utf8 scripts/check_portfolio.py
& 'C:\Users\HP\anaconda3\python.exe' -B -X utf8 scripts/check_cv_variants.py
& 'C:\Users\HP\anaconda3\python.exe' -B -X utf8 scripts/check_cv_word.py
```

La première utilise Playwright et Microsoft Edge installé ; la deuxième contrôle les quatre PDF avec pypdf ; la troisième est un contrôle optionnel nécessitant Microsoft Word et pywin32.

- Quatre PDF canoniques (présentation et candidature FR/EN) : une page A4 chacun ; texte complet et six liens vérifiés avec pypdf. Présence de photo vérifiée dans la présentation, absence de photo/décoration et ordre de lecture linéaire vérifiés dans la candidature.
- Deux impressions du CV Web : une page A4 chacune, portrait embarqué et texte intégral comparé à la source éditoriale ; projets en tête et nouveau niveau d’anglais vérifiés.
- Deux DOCX : une page chacun dans Microsoft Word ; export et texte intégral contrôlés.
- Sept largeurs du portfolio : 320, 375, 390, 768, 1 024, 1 440 et 1 920 px, sans débordement horizontal. CV vérifié à 320, 390, 600, 640, 641, 768, 840 et 1 024 px, avec absence de chevauchement des colonnes.
- Six fiches dans chacune des deux langues, navigation clavier avant/arrière, focus contenu/restitution, fermetures et navigation mobile.
- Aucun message d’erreur JavaScript ni HTTP sur les ressources locales utilisées.
- Rendu français des sections principales disponible sans JavaScript ; téléchargements PDF accessibles.
- Bascule FR/EN du portfolio et du CV testée aussi en `file://`.
- Portrait WebP d’environ 36 Ko ; aucune dépendance réseau tierce au chargement initial ; zéro requête audio initiale.
- Audits Lighthouse antérieurs : accessibilité, bonnes pratiques et SEO à 100/100 pour le portfolio et le CV Web à deux colonnes. Sur la finition actuelle, premier passage à 100/100 dans ces catégories, avec un avertissement sur la correspondance texte visible/nom accessible des nouveaux liens PDF. Les noms ont été corrigés et leur correspondance est désormais couverte par Playwright FR/EN. La relance Lighthouse après correction a expiré avec `ERR_NETWORK_IO_SUSPENDED` dans le navigateur de Review ; aucun résultat final sans avertissement n’est revendiqué pour cette relance. Le site fonctionne dans Edge/Playwright et tous les contrôles locaux passent. Rapports conservés dans `scratch/qa/`, dont `lighthouse_cv_polish_fr_pre_label_fix.*`. Ce n’est ni une certification d’accessibilité ni un benchmark de performances réseau réel.
- Contrôle visuel des versions desktop/mobile et des deux PDF.

Les captures et sorties de contrôle sont dans `scratch/qa/` et les aperçus PDF dans `scratch/cv_fr_preview.png`, `scratch/cv_en_preview.png`, `scratch/cv_fr_ats_preview.png` et `scratch/cv_en_ats_preview.png`. Le dossier `scratch/` est déjà ignoré par Git.

## Liens publics à rétablir après vérification

Lors du contrôle HTTP sans authentification :

| Adresse | Résultat observé |
| --- | --- |
| `https://k1.archicam-ai.com` | HTTP 200 |
| `https://github.com/gervais-afk/notebooks-factory` | HTTP 200 |
| `https://github.com/gervais-afk/VigieSahel` | HTTP 200 |
| Les deux articles DEV | HTTP 200 |
| `https://github.com/gervais-afk/k1-mathinfo` | HTTP 404 |
| `https://github.com/gervais-afk/archi-cam-ai` | HTTP 404 |
| `https://github.com/gervais-afk/-sovereign-bi-agentic` | HTTP 404 |
| `https://github.com/gervais-afk/ASU-Audit-Ready` | HTTP 404 |
| `https://archicam-ai.com` | Résolution DNS impossible depuis cet environnement |

Une erreur 404 ne permet pas de conclure qu’un dépôt n’existe pas : il peut être privé, déplacé ou temporairement indisponible. Aucun dépôt n’a été rendu public et aucune configuration DNS n’a été modifiée.

Les adresses d’origine sont conservées dans `translations.js`, mais les boutons concernés sont masqués grâce à `githubPublic: false` ou `websiteAvailable: false`. Les projets ne sont pas supprimés ; leurs fiches proposent un échange par email. Pour rétablir un bouton, confirmer l’URL, mettre à jour la propriété dans les deux langues, puis exécuter le synchroniseur.

## Limites éditoriales préservées

- Aucun titre Lead/Senior, client, résultat commercial ou certification ajouté artificiellement.
- Master décembre 2025–2027 explicitement en cours ; Licence & BTS conservés sans équivalence de diplôme inventée.
- K1-MathInfo : 525 travaux, 2010–2026, projet en binôme ; aucune garantie zéro hallucination ou métrique de performance non vérifiée.
- Archi Cam AI : positionnement IA/BTP, sans gains chiffrés ni validation automatique des livrables. Son code n’a pas fait l’objet du même audit.
- Dataset Automator : prototype individuel de hackathon ; simulations et intégrations non confirmées explicitées ; pas de conformité EU AI Act revendiquée.
- Aucun pipeline métier, entraînement ou test des dépôts de référence exécuté pendant cette refonte. Les contrôles décrits ici concernent le portfolio et ses CV.
- Les anciens articles et podcasts peuvent encore contenir des formulations excessives : ils sont signalés comme archives, pas présentés comme preuves indépendantes.
- La délivrabilité de l’email et la réception des appels n’ont pas été testées.
