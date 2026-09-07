/* ==========================================
   PORTFOLIO INTERACTIVE LOGIC & ANIMATIONS
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {

    // 1. Typewriter Effect
    const words = [
        "Consultant IA & Data",
        "Spécialiste MLOps & RAG",
        "Ingénieur Graphes de Connaissances"
    ];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typewriterElement = document.getElementById('typewriter');
    const typingSpeed = 100;
    const deletingSpeed = 50;
    const delayBetweenWords = 2000;

    function type() {
        const currentWord = words[wordIndex];
        
        if (isDeleting) {
            typewriterElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typewriterElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
        }

        let currentSpeed = isDeleting ? deletingSpeed : typingSpeed;

        if (!isDeleting && charIndex === currentWord.length) {
            currentSpeed = delayBetweenWords;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            currentSpeed = 500;
        }

        setTimeout(type, currentSpeed);
    }
    
    if (typewriterElement) {
        type();
    }

    // 2. 3D Tilt Effect on Project Cards
    const cards = document.querySelectorAll('.project-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // Mouse position inside card
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate tilt degrees (max 10 degrees)
            const rotateX = ((centerY - y) / centerY) * 10;
            const rotateY = ((x - centerX) / centerX) * 10;
            
            card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });

    // 3. Scroll Entrance Animations (Intersection Observer)
    const animatableElements = document.querySelectorAll('.animate-on-scroll, .timeline-item, .project-card, .about-card, .contact-info, .contact-form, .section-title, .stat-item, .techstack-category, .cert-card');
    
    animatableElements.forEach(el => {
        el.classList.add('animate-on-scroll');
    });

    const observerOptions = {
        threshold: 0.05,
        rootMargin: '0px 0px 20px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('appear');
                observer.unobserve(entry.target); // Trigger only once
            }
        });
    }, observerOptions);

    animatableElements.forEach(el => observer.observe(el));

    // 4. Skills Interactive Filtering
    const filterButtons = document.querySelectorAll('.filter-btn');
    const skillTags = document.querySelectorAll('.skill-tag');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            filterButtons.forEach(b => b.classList.remove('active'));
            // Add active to current
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            skillTags.forEach(tag => {
                const category = tag.getAttribute('data-category');
                
                if (filterValue === 'all' || category === filterValue) {
                    tag.classList.remove('fade-out');
                } else {
                    tag.classList.add('fade-out');
                }
            });
        });
    });

    // 5. Active Navbar Link on Scroll
    const sections = document.querySelectorAll('section');
    const navItems = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', () => {
        let currentSectionId = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - 250)) {
                currentSectionId = section.getAttribute('id');
            }
        });

        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === `#${currentSectionId}`) {
                item.classList.add('active');
            }
        });
    });    // 6. Interactive Architecture Modals System
    const projectsData = {
        fr: {
            'archi-cam-ai': {
                badge: "Plateforme Souveraine BIM 5D & Multi-Agents BTP",
                title: "Archi Cam AI 🏛️",
                subtitle: "Plateforme IA souveraine de modélisation BIM 5D, calcul de structures & devis estimatifs normés pour le BTP africain (7 microservices découplés).",
                pipeline: [
                    { num: "Étape 01", title: "Entrée Multimodale & YOLO FastAPI (port 8000)", desc: "Scan 2D/3D, plans DWG/PDF, maquettes IFC et requêtes vocales. Segmentation sémantique par YOLO pour détecter murs, ouvertures et pièces." },
                    { num: "Étape 02", title: "VIM TopologyBuilder (port 8001) & CAD Annotator (port 8002)", desc: "Reconstruction géométrique polygonale via Shapely (snapping 15cm tolérance, calcul des surfaces exactes en m²), cotations architecturales CAD et cartouche automatisé sous Pillow/PIL." },
                    { num: "Étape 03", title: "ADK SCoT Orchestrator (port 8080) & Neo4j 5.20 GraphRAG", desc: "Chain-of-Thought spatial appliquant les normes réglementaires POS et ONAC. RAG de connaissances sur les mercuriales MINMAP 2026 et prix des matériaux." },
                    { num: "Étape 04", title: "Sandbox Déterministe BAEL 91 & BIM 5D", desc: "Calculs d'ingénierie BAEL 91 (armatures, charges), déductions d'ouvertures >0.50m² et exports IFC C++ via IfcOpenShell sans risque d'hallucination." },
                    { num: "Étape 05", title: "Génération Visuelle 3D & Livrables Conformes EU AI Act", desc: "Rendus photoréalistes Fal.ai (SDXL/ControlNet), teasers vidéo drone Veo 3, DQE Excel 6 onglets en <45s, et horodatage cryptographique EXIF SHA-256." }
                ],
                impacts: [
                    "Accélération de +99,2% : génération complète des devis estimatifs (DQE 6 onglets) en <45 secondes (contre 3 à 7 jours manuellement).",
                    "Zéro Hallucination & Conformité Légale : isolation neuro-symbolique stricte (LLM orchestrateur, calculs déterministes Python BAEL 91 + mercuriales MINMAP 2026).",
                    "Reconstruction Topologique Robuste : snapping Shapely à tolérance 15cm fermant automatiquement les lignes brisées et calculant les surfaces en m².",
                    "Haute Précision MLOps (R² = 0,9872) : modèles d'estimation entraînés et surveillés sous MLflow sur plus de 400 projets réels de construction."
                ],
                techs: ["Next.js 14", "FastAPI (ports 8000/8001/8002/8080)", "IfcOpenShell C++", "Shapely (Geometry)", "YOLO Vision", "Neo4j 5.20 GraphRAG", "Python BAEL 91", "Fal.ai / Veo 3", "DuckDB & Prisma", "MLflow MLOps", "EU AI Act SHA-256"],
                github: "https://github.com/gervais-afk/archi-cam-ai"
            },
            'sovereign-bi': {
                badge: "Business Intelligence Agentique & Gouvernance Souveraine",
                title: "Sovereign.BI Agentic 📊",
                subtitle: "Moteur décisionnel d'IA Agentique souveraine permettant d'interroger un Data Warehouse d'entreprise en langage naturel sans aucune fuite de données.",
                pipeline: [
                    { num: "Étape 01", title: "Requête NL, FastMCP Gateway & Garde-fous Zod", desc: "Interface React 18 + Vite transmettant les requêtes exécutives au Gateway FastMCP (Model Context Protocol). Validation stricte des schémas via Zod et contrôle d'accès multi-tenant ABAC." },
                    { num: "Étape 02", title: "Moteur Hybride Dual RAG (Neo4j N10S + pgvector)", desc: "Graphe de connaissances Neo4j 5.20 enrichi d'ontologies RDF (neosemantics n10s) et requêtes hybrides couplées à Apache AGE et PostgreSQL 16 pgvector HNSW (<5s)." },
                    { num: "Étape 03", title: "Moteur Analytique Python FastAPI & CrewAI", desc: "Sandbox REPL isolée exécutant le code d'agrégation statistique, assainissement et masquage automatique des données à caractère personnel (PII)." },
                    { num: "Étape 04", title: "Auditeur de Risque SHAP Sentinel (Théorie des Jeux)", desc: "Attribution d'importance des variables selon les valeurs de Shapley (sentinel_rules.yaml), détection proactive des anomalies de calcul et des injections." },
                    { num: "Étape 05", title: "Inférence Locale Google Gemma 12B QAT (Air-Gapped)", desc: "Exécution 100% hors-ligne via LM Studio / Ollama (port 1234), zéro fuite de données vers des tiers, et synchronisation contextuelle OKF." }
                ],
                impacts: [
                    "Interrogation instantanée (<5s) de Data Warehouses massifs sans exiger de compétences en programmation SQL ou Cypher.",
                    "Étanchéité Souveraine Absolue : données confidentielles traitées en mémoire locale sans transit vers des serveurs externes.",
                    "Auditabilité et Transparence Totale : chaque chiffre et KPI est retracé mathématiquement par l'auditeur d'explicabilité SHAP Sentinel.",
                    "Architecture Découplée & Modulaire : passerelle FastMCP et règles ABAC garantissant l'étanchéité multi-tenant pour les grandes organisations."
                ],
                techs: ["React 18 + Vite", "FastAPI Python", "TypeScript Genkit", "FastMCP Gateway", "Neo4j 5.20 N10S", "Apache AGE", "PostgreSQL pgvector", "CrewAI", "Google Gemma 12B QAT", "SHAP Sentinel", "Zod & ABAC"],
                github: "https://github.com/gervais-afk/-sovereign-bi-agentic"
            },
            'dataset-automator': {
                badge: "Usine MLOps Autonome & Dataset Engineering Factory (Google Cloud Hackathon)",
                title: "Dataset Automator ⚙️",
                subtitle: "Plateforme MLOps d'ingestion Zero-ETL, modélisation tabulaire de fondation, audits d'équité et gouvernance EU AI Act.",
                pipeline: [
                    { num: "Étape 01", title: "Ingestion Serverless & Zero-ETL Profiling (<48ms)", desc: "BigQuery DataFrames (bigframes) pour le profiling statistique haute vitesse, typage réel automatisé, détection d'asymétrie et de valeurs manquantes." },
                    { num: "Étape 02", title: "Google TabFM & Adaptive Cascade Router", desc: "Modèle de fondation tabulaire TabFM (inférence zero-shot in-context learning) couplé à un routeur cascade (arbitrage de tokens 125x : TabFM -> SLM local 152ms -> Gemini 3.5 Flash)." },
                    { num: "Étape 03", title: "Audit d'Équité Google PAIR What-If Tool (WIT)", desc: "Exploration contre-factuelle multidimensionnelle, analyse de sensibilité et contrôle de la parité démographique entre sous-populations." },
                    { num: "Étape 04", title: "Observabilité MLOps & Détection de Dérive (KS/PSI)", desc: "Tests statistiques continus de Kolmogorov-Smirnov et Population Stability Index (PSI > 30%), alertes automatisées et versionnage complet sous MLflow UI." },
                    { num: "Étape 05", title: "Gouvernance Model Card Toolkit (MCT) & Signatures RSASSA-PSS", desc: "Génération de fiches modèles Material Design, export de notebooks forensiques CRISP-ML(Q) de 55 cellules (score 100/100) et signature cryptographique EU AI Act Art. 12 & 26." }
                ],
                impacts: [
                    "Automatisation de bout en bout du cycle de vie des données : de l'ingestion brute à la production de notebooks de qualité certifiée.",
                    "Arbitrage de Coûts Énergétiques et Tokens (125x) grâce au routage adaptatif et à l'exploitation du modèle tabulaire TabFM.",
                    "Conformité Légale Garantie pour l'EU AI Act : fiches de gouvernance MCT et empreintes cryptographiques RSASSA-PSS-SHA256 infalsifiables.",
                    "Visualiseur Spatial DAG GPU SVG 60 FPS permettant de suivre visuellement en temps réel chaque nœud d'exécution de la pipeline."
                ],
                techs: ["Google TabFM", "PAIR What-If Tool (WIT)", "Model Card Toolkit (MCT)", "BigQuery DataFrames", "TypeScript Genkit", "Neo4j GraphRAG", "MLflow", "RSASSA-PSS-SHA256", "CRISP-ML(Q)", "Streamlit", "Pytest"],
                github: "https://github.com/gervais-afk/dataset-automator"
            },
            'asu-audit-ready': {
                badge: "Système Souverain d'Aide au Commandement, Conformité OACI & Ingénierie Documentaire V4 (CCAA)",
                title: "ASU-Audit-Ready 🛡️",
                subtitle: "Plateforme d'intelligence normative pour la Division Opérationnelle de Sûreté (DOS) : génération Word V4 en <2s, auditabilité Zéro Défaut et simulateur d'inspection 100 points.",
                pipeline: [
                    { num: "Pilier 01", title: "Ingestion & Diagnostic Zéro Défaut (PIF & ZSAR)", desc: "Ingestion et monitoring continu des indicateurs d'exploitation terrain : taux de détection aux Points d'Inspection Filtrage, contrôles d'accès ZSAR, patrouilles de clôture et calibrations rayons X." },
                    { num: "Pilier 02", title: "Moteur d'Ingénierie Documentaire Word V4 (python-docx)", desc: "Compilation automatisée du rapport officiel d'activités mensuel en <2 secondes au format normé .docx paginé et scellé, réduisant la charge administrative de 40h/mois à 2 secondes (-95%)." },
                    { num: "Pilier 03", title: "Analyse Numérique des Défaillances (Pareto & Spider Radar)", desc: "Modélisation des compétences en Spider Radar multidimensionnel et diagrammes de Pareto des défaillances de fouille pour identifier pro-activement les vulnérabilités avant le passage des inspecteurs de l'OACI." },
                    { num: "Pilier 04", title: "Scanner d'Audit & Contrôle de Complétude Règlementaire", desc: "Vérification déterministe de 100 points de contrôle, garantissant qu'aucune pièce justificative ou registre n'est omis dans le dossier d'audit international." },
                    { num: "Pilier 05", title: "Simulateur d'Audition Interactive AVSEC (Scoring 100 Pts)", desc: "Moteur d'entraînement confrontant les superviseurs aux questions pièges des auditeurs de l'OACI avec notation temps réel et plan d'action correctif immédiat." }
                ],
                impacts: [
                    "Réduction prouvée de 95% du temps de reporting (de 40 heures de saisie manuelle à moins de 2 secondes en un clic).",
                    "Architecture Souveraine 100% On-Premise / Edge (zéro appel cloud distant, étanchéité mémoire totale pour la sûreté de défense aéroportuaire).",
                    "Auditabilité Zéro Défaut certifiée OACI Annexe 17 & Programme National de Sûreté de l'Aviation Civile (PNSAC).",
                    "Moteur de templating Word dynamique V4 (docxtpl) permettant l'apposition manuelle de visas hiérarchiques avant scellement officiel."
                ],
                techs: ["Streamlit 1.45+", "Python 3.11", "python-docx V4", "docxtpl", "Spider Radar (Matplotlib)", "Diagrammes Pareto", "Simulateur AVSEC 100 Pts", "OACI Annexe 17", "Sovereign Air-Gapped", "openpyxl"],
                github: "https://github.com/gervais-afk/ASU-Audit-Ready"
            },
            'vigie-sahel': {
                badge: "Plateforme MLOps Décisionnelle, Résilience Climat-Santé & Optimisation Agricole au Sahel",
                title: "VigieSahel 🌾",
                subtitle: "Système prédictif ensembliste (R² > 94%) réduisant de 35% les échecs de semis et anticipant les épidémies de méningite à J-14 via le suivi des poussières d'Harmattan (PM2.5).",
                pipeline: [
                    { num: "Pilier 01", title: "Ingestion Spatio-Temporelle Multi-Sources & IoT MQTT", desc: "Streaming continu des flux satellites agrométéorologiques (humidité des sols, pluviométrie) et capteurs de qualité de l'air (concentration minérale PM2.5 d'Harmattan) sur 12 régions sahélo-sahariennes." },
                    { num: "Pilier 02", title: "Moteur Prédictif Ensembliste Climat-Santé (R² > 94%)", desc: "Modélisation couplant XGBoost, CatBoost et Random Forest, reliant mathématiquement les pics d'inhalation minérale et la réactivation de la ceinture de méningite pour déclencher des alertes sanitaires 2 semaines en avance." },
                    { num: "Pilier 03", title: "Optimiseur Déterministe de Calendrier Agricole", desc: "Calcul algorithmique de la fenêtre de semis idéale au jour près pour le coton et les cultures vivrières, réduisant de 35% à 40% les pertes par desséchement précoce des plantules." },
                    { num: "Pilier 04", title: "Observabilité MLOps Active sous MLflow & Supabase", desc: "Lineage complet des données, registre de modèles versionnés, détection continue de dérive de données (Concept Drift via KS-Test & PSI) et base relationnelle PostgreSQL / Supabase Realtime avec contrôle ABAC." },
                    { num: "Pilier 05", title: "Déploiement Conteneurisé Docker Edge & PWA Offline-First", desc: "Architecture ultra-légère et résiliente, conçue pour opérer directement sur le terrain en zone rurale sahélienne sous connectivité réseau intermittente." }
                ],
                impacts: [
                    "Réduction prouvée de 35% des pertes agricoles de semis de coton et de mil face au dérèglement pluviométrique.",
                    "Anticipation épidémiologique précoce à J-14 permettant le pré-positionnement stratégique des stocks de vaccins méningite.",
                    "Explicabilité totale (0% hallucination) : modèles tabulaires déterministes validés pour les politiques publiques de santé et d'agriculture.",
                    "Souveraineté des données africaines : conteneurisation Docker Edge et persistance PostgreSQL / Supabase sécurisée."
                ],
                techs: ["Streamlit Core", "Python 3.11", "XGBoost", "CatBoost", "Scikit-Learn (R² > 94%)", "Supabase PostgreSQL", "MLflow Registry", "Docker Edge", "MQTT & WebSockets", "Harmattan PM2.5"],
                github: "https://github.com/gervais-afk/VigieSahel"
            },
            'k1-mathinfo': {
                badge: "Système Souverain d'IA Multi-Agents, GraphRAG, Advisor Matcher & Certification OKF (DMI - Univ. Ngaoundéré)",
                title: "K1-MATHINFO (v3.2.0) 🏛️",
                subtitle: "Infrastructure souveraine académique : 4 Piliers, 8 agents LangGraph, graphe Neo4j (1 366 nœuds), recommandation de directeurs et auto-apprentissage continu WikiSkill.",
                infographic: "assets/images/k1_mathinfo_infographie_pro.png",
                pipeline: [
                    { num: "Pilier 01", title: "Ingestion Streaming SSE & Deep Research", desc: "Visualiseur d'ingestion en temps réel (Stepper 5 étapes, logs console) et découpage normatif de 470 thèses & 19 projets M1. Deep Research matriciel compact limitant la bande passante à <450 tokens." },
                    { num: "Pilier 02", title: "Graphe Topologique Neo4j & Explorateur 3D", desc: "1 366 nœuds et 3 833 relations (encadrements, jurys, algorithmes, théorèmes). Dispose de 3 modes physiques (Barnes-Hut, Hiérarchique Top-Down, Radial) et d'un Copilot autonome générant du Cypher sans code." },
                    { num: "Pilier 03", title: "Advisor Matcher (Directeur de Thèse Idéal)", desc: "Moteur de recommandation neuro-symbolique couplant similarité cosinus dense du sujet et co-occurrence ontologique Neo4j. Fiches directeurs enrichies parmi les 4 labos DMI (LARI, LAMAP, LAMEX, LASE) avec score d'affinité IA % et actions 1-clic." },
                    { num: "Pilier 04", title: "Certification OKF v0.2 & Auditeur Bibliographique", desc: "Attesteur Cypher SHA-256 No-LLM (Tiers 1/2/3 inviolables) et audit bibliographique Waterfall (DMI -> Semantic Scholar -> Crossref, DOI/arXiv O(1)). Interopérabilité FAIR OAI-PMH v2.0 (Dublin Core, ETD-MS) et exports BibTeX/Zotero." },
                    { num: "Pilier 05", title: "LangGraph 8 Agents, K1-WikiSkill & Quorum 4 Yeux", desc: "Réseau de 8 agents (Superviseur, GraphRAG, Advisor, Math SEIR/Caputo, Biblio, OKF, Critic Q17, WikiSkill). Auto-amélioration continue par méta-compétences (Google Research 2026) et Quorum symétrique (KOA + AZIZ) sous supervision du Pr. DAYANG PAUL." }
                ],
                impacts: [
                    "Élimination absolue des hallucinations académiques par empreinte cryptographique déterministe SHA-256 (OKF v0.2 No-LLM Tiers 1/2/3).",
                    "Advisor Matcher Intelligent : orientation optimale des étudiants vers les directeurs et laboratoires (LARI, LAMAP, LAMEX, LASE) avec justification explicable.",
                    "Explorateur 3D/2D Barnes-Hut & Requêtes Cypher en langage naturel pour naviguer dans 28 ans de patrimoine scientifique (470 thèses, 19 projets M1).",
                    "Auto-Amélioration Continue K1-WikiSkill & Gouvernance Symétrique : 77 tests automatisés (100% succès), cache Redis 7 (<20ms) et Quorum de sécurité 4 Yeux."
                ],
                techs: ["FastAPI 0.115", "LangGraph 8 Agents", "Neo4j 5.26 GraphRAG", "Advisor Matcher", "Barnes-Hut 3D", "OKF v0.2 SHA-256", "K1-WikiSkill", "Redis 7 Lua (<20ms)", "PostgreSQL pgvector", "OAI-PMH Dublin Core"],
                github: "https://github.com/gervais-afk/k1-mathinfo"
            }
        },
        en: {
            'archi-cam-ai': {
                badge: "Sovereign 5D BIM & Agentic AI SaaS",
                title: "Archi Cam AI 🏛️",
                subtitle: "Sovereign 5D BIM & Agentic AI platform for automated structural engineering & quantity surveying in African construction (7 decoupled microservices).",
                pipeline: [
                    { num: "Step 01", title: "Multimodal Input & YOLO FastAPI (port 8000)", desc: "2D/3D scans, DWG/PDF drawings, IFC models & vocal prompts. Semantic segmentation via YOLO to detect walls, openings, and spaces." },
                    { num: "Step 02", title: "VIM TopologyBuilder (port 8001) & CAD Annotator (port 8002)", desc: "Geometric polygon reconstruction via Shapely (snapping with 15cm tolerance, computing exact room areas in m²), automated CAD dimensioning and title block via Pillow/PIL." },
                    { num: "Step 03", title: "ADK SCoT Orchestrator (port 8080) & Neo4j 5.20 GraphRAG", desc: "Spatial Chain-of-Thought agent enforcing POS and ONAC regulations. Knowledge graph for MINMAP 2026 pricing mercurials and construction materials." },
                    { num: "Step 04", title: "Deterministic Python Sandbox BAEL 91 & 5D BIM", desc: "Deterministic BAEL 91 structural calculations (rebar, load bearing), >0.50m² opening deductions, and IFC C++ exports via IfcOpenShell with zero hallucination." },
                    { num: "Step 05", title: "3D Visual Synthesis & EU AI Act Compliance", desc: "Photorealistic Fal.ai renders (SDXL/ControlNet), Veo 3 3D drone teaser videos, 6-sheet Excel BOQs in <45s, and SHA-256 EXIF cryptographic watermarking." }
                ],
                impacts: [
                    "99.2% speedup: Complete Bill of Quantities (6-sheet BOQs) generated in <45 seconds (down from 3 to 7 days manually).",
                    "Zero Hallucination & Regulatory Compliance: strict neuro-symbolic isolation (LLM orchestrator + deterministic BAEL 91 Python engine + MINMAP 2026).",
                    "Robust Topological Reconstruction: Shapely snapping with 15cm tolerance automatically closing broken lines and computing exact room areas.",
                    "MLOps Production Precision (R² = 0.9872): estimating model trained and evaluated under MLflow across 400 African construction projects."
                ],
                techs: ["Next.js 14", "FastAPI (ports 8000/8001/8002/8080)", "IfcOpenShell C++", "Shapely (Geometry)", "YOLO Vision", "Neo4j 5.20 GraphRAG", "Python BAEL 91", "Fal.ai / Veo 3", "DuckDB & Prisma", "MLflow MLOps", "EU AI Act SHA-256"],
                github: "https://github.com/gervais-afk/archi-cam-ai"
            },
            'sovereign-bi': {
                badge: "Agentic Business Intelligence & Security",
                title: "Sovereign.BI Agentic 📊",
                subtitle: "Sovereign agentic enterprise BI engine empowering executives to query massive Data Warehouses in natural language with zero data leakage.",
                pipeline: [
                    { num: "Step 01", title: "NL Query, FastMCP Gateway & Zod Guardrails", desc: "React 18 + Vite interface routing executive queries through FastMCP Gateway (Model Context Protocol). Strict schema validation via Zod and multi-tenant ABAC permissions." },
                    { num: "Step 02", title: "Hybrid Dual RAG Engine (Neo4j N10S + pgvector)", desc: "Neo4j 5.20 knowledge graph enriched with RDF ontologies (neosemantics n10s) and hybrid queries coupled with Apache AGE and PostgreSQL 16 pgvector HNSW (<5s)." },
                    { num: "Step 03", title: "Python FastAPI Analytics Engine & CrewAI", desc: "Sandboxed REPL environment executing analytical statistical aggregations, automated PII sanitization, and data masking." },
                    { num: "Step 04", title: "SHAP Sentinel Risk Auditor (Game Theory)", desc: "Feature importance attribution via Shapley values (sentinel_rules.yaml), proactive detection of query anomalies, and injection defense." },
                    { num: "Step 05", title: "Local Sovereign Google Gemma 12B QAT (Air-Gapped)", desc: "100% offline local inference via LM Studio / Ollama (port 1234), zero third-party data leakage, and OKF contextual synchrony." }
                ],
                impacts: [
                    "Instant querying (<5s) of massive Data Warehouses without requiring SQL or Cypher programming expertise.",
                    "Absolute Sovereign Security: confidential enterprise data processed in local memory with zero external transmission.",
                    "Complete Auditability & Transparency: every number and KPI mathematically verified by the SHAP Sentinel explainability auditor.",
                    "Decoupled & Modular Architecture: FastMCP gateway and ABAC policies enforcing strict multi-tenant data isolation."
                ],
                techs: ["React 18 + Vite", "FastAPI Python", "TypeScript Genkit", "FastMCP Gateway", "Neo4j 5.20 N10S", "Apache AGE", "PostgreSQL pgvector", "CrewAI", "Google Gemma 12B QAT", "SHAP Sentinel", "Zod & ABAC"],
                github: "https://github.com/gervais-afk/-sovereign-bi-agentic"
            },
            'dataset-automator': {
                badge: "Agentic MLOps Platform & Dataset Engineering Factory (Google Cloud Hackathon)",
                title: "Dataset Automator ⚙️",
                subtitle: "Autonomous MLOps factory for Zero-ETL data ingestion, foundation tabular modeling, fairness auditing, and EU AI Act governance.",
                pipeline: [
                    { num: "Step 01", title: "Serverless Ingestion & Zero-ETL Profiling (<48ms)", desc: "BigQuery DataFrames (bigframes) for high-speed statistical profiling, automated real-data typing, skewness detection, and missing-value analysis." },
                    { num: "Step 02", title: "Google TabFM & Adaptive Cascade Router", desc: "Tabular foundation model TabFM (zero-shot in-context learning) paired with an adaptive cascade router (125x token arbitrage: TabFM -> local SLM @ 152ms -> Gemini 3.5 Flash)." },
                    { num: "Step 03", title: "Fairness Audit via Google PAIR What-If Tool (WIT)", desc: "Multidimensional counterfactual exploration, sensitivity analysis, and demographic parity verification across sub-populations." },
                    { num: "Step 04", title: "MLOps Observability & Drift Tracking (KS/PSI)", desc: "Continuous statistical Kolmogorov-Smirnov and Population Stability Index (PSI > 30%) drift tests, automated alerts, and MLflow tracking." },
                    { num: "Step 05", title: "Model Card Toolkit (MCT) Governance & RSASSA-PSS", desc: "Automated Material Design governance cards, 55-cell forensic CRISP-ML(Q) notebook generator (100/100 score), and EU AI Act Art. 12 & 26 signatures." }
                ],
                impacts: [
                    "End-to-end automation of data preparation cycles, quality audits, and certified MLOps notebook generation.",
                    "125x Token & Energy Cost Arbitrage leveraging adaptive routing and Google's TabFM foundation tabular model.",
                    "Guaranteed Regulatory Compliance for EU AI Act: MCT governance cards and tamper-proof RSASSA-PSS-SHA256 signatures.",
                    "60 FPS GPU SVG DAG Spatial Visualizer enabling real-time animated tracking of every execution step across the pipeline."
                ],
                techs: ["Google TabFM", "PAIR What-If Tool (WIT)", "Model Card Toolkit (MCT)", "BigQuery DataFrames", "TypeScript Genkit", "Neo4j GraphRAG", "MLflow", "RSASSA-PSS-SHA256", "CRISP-ML(Q)", "Streamlit", "Pytest"],
                github: "https://github.com/gervais-afk/dataset-automator"
            },
            'asu-audit-ready': {
                badge: "Sovereign Command System, ICAO Compliance & Normative V4 Document Engine (CCAA)",
                title: "ASU-Audit-Ready 🛡️",
                subtitle: "Normative compliance platform for the Operational Security Division (DOS): <2s automated Word V4 generation, Zero-Defect auditability, and 100-point inspection exam simulator.",
                pipeline: [
                    { num: "Pillar 01", title: "Ingestion & Zero-Defect Diagnostics (PIF & ZSAR)", desc: "Continuous ingestion and monitoring of field operational metrics: detection rates at Passenger Screening Checkpoints (PIF), Airside Security Restricted Area (ZSAR) access controls, perimeter patrols, and X-ray calibration logs." },
                    { num: "Pillar 02", title: "Normative Word V4 Document Engine (python-docx)", desc: "Automated compilation of official monthly activity reports in <2 seconds in standardized .docx format, dynamically paginated and sealed, reducing administrative workload from 40h/month to 2 seconds (-95%)." },
                    { num: "Pillar 03", title: "Numerical Failure Analytics (Pareto & Spider Radar)", desc: "Multidimensional Spider Radar competency modeling and Pareto failure distribution charts to proactively identify operational vulnerabilities before ICAO international inspection audits." },
                    { num: "Pillar 04", title: "Regulatory Compliance Scanner & Evidence Auditor", desc: "Deterministic audit across 100 verification checkpoints, ensuring zero omission of evidentiary dossiers, interception logs, or equipment calibration records." },
                    { num: "Pillar 05", title: "Interactive AVSEC Oral Exam Simulator (100-Point Scoring)", desc: "Interactive training engine confronting supervisors with unannounced ICAO inspection scenarios featuring real-time scoring and instant corrective remediation plans." }
                ],
                impacts: [
                    "Proven 95% reduction in audit reporting time (from 40 hours of manual paperwork down to <2 seconds in a single click).",
                    "100% On-Premise / Sovereign Edge Architecture (zero cloud leakage, total in-memory isolation for national aviation defense security).",
                    "Zero-Defect Auditability certified compliant with ICAO Annex 17 and Cameroon National Civil Aviation Security Program (PNSAC).",
                    "Dynamic Word V4 templating engine (docxtpl) enabling manual executive sign-off visas prior to official sealing."
                ],
                techs: ["Streamlit 1.45+", "Python 3.11", "python-docx V4", "docxtpl", "Spider Radar (Matplotlib)", "Pareto Charts", "AVSEC 100-Pt Simulator", "ICAO Annex 17", "Sovereign Air-Gapped", "openpyxl"],
                github: "https://github.com/gervais-afk/ASU-Audit-Ready"
            },
            'vigie-sahel': {
                badge: "Predictive MLOps Platform, Climate-Health Resilience & Agricultural Optimization in the Sahel",
                title: "VigieSahel 🌾",
                subtitle: "Ensemble predictive system (R² > 94%) cutting crop sowing losses by 35% and forecasting meningitis outbreaks 14 days in advance by tracking Harmattan dust (PM2.5).",
                pipeline: [
                    { num: "Pillar 01", title: "Multi-Source Spatio-Temporal Ingestion & IoT MQTT", desc: "Continuous streaming of agrometeorological satellite telemetry (soil moisture, rainfall, drought index) and air quality sensors (PM2.5 mineral dust / Harmattan winds) across 12 strategic Sahelian regions." },
                    { num: "Pillar 02", title: "Ensemble Climate-Health Predictive Engine (R² > 94%)", desc: "XGBoost, CatBoost, and Random Forest ensemble models mathematically linking desert dust inhalation to meningitis belt reactivation for proactive red alerts 2 weeks in advance." },
                    { num: "Pillar 03", title: "Deterministic Agricultural Sowing Optimizer", desc: "Algorithmic daily prescription of the optimal sowing window for cotton and staple food crops, preventing 35% to 40% seedling loss from premature desiccation." },
                    { num: "Pillar 04", title: "Active MLOps Observability under MLflow & Supabase", desc: "End-to-end data lineage, versioned model registry, continuous concept drift detection (KS-Test & PSI), and sovereign PostgreSQL / Supabase Realtime backend with ABAC access controls." },
                    { num: "Pillar 05", title: "Docker Edge Containerization & Offline-First PWA", desc: "Ultra-lightweight, resilient edge deployment engineered to operate locally in remote rural Sahelian environments with intermittent or zero internet connectivity." }
                ],
                impacts: [
                    "Proven 35% reduction in crop failure for cotton and millet facing violent rainfall variability.",
                    "14-day early epidemiological warning enabling strategic pre-positioning of meningitis vaccine reserves.",
                    "100% Explainability (0% Hallucination): deterministic tabular ensemble models approved for public health and agricultural policies.",
                    "African Data Sovereignty: Docker Edge containerization and secure PostgreSQL / Supabase persistence."
                ],
                techs: ["Streamlit Core", "Python 3.11", "XGBoost", "CatBoost", "Scikit-Learn (R² > 94%)", "Supabase PostgreSQL", "MLflow Registry", "Docker Edge", "MQTT & WebSockets", "Harmattan PM2.5"],
                github: "https://github.com/gervais-afk/VigieSahel"
            },
            'k1-mathinfo': {
                badge: "Sovereign Multi-Agent AI System, GraphRAG, Advisor Matcher & Academic Certification (DMI - Univ. of Ngaoundéré)",
                title: "K1-MATHINFO (v3.2.0) 🏛️",
                subtitle: "Sovereign academic AI infrastructure: 4 Engineering Pillars, 8 LangGraph agents, Neo4j graph (1,366 nodes), advisor recommendation, and continuous self-evolution via WikiSkill.",
                infographic: "assets/images/k1_mathinfo_infographie_pro.png",
                pipeline: [
                    { num: "Pillar 01", title: "5-Stage SSE Streaming Ingestion & Deep Research", desc: "Real-time ingestion visualizer (5-stage animated stepper, live terminal console) and normative chunking of 470 theses & 19 M1 projects. Compact matrix Deep Research keeping bandwidth <450 tokens." },
                    { num: "Pillar 02", title: "Topological Neo4j Graph & 3D Explorer", desc: "1,366 nodes and 3,833 relationships (supervision genealogy, juries, algorithms, theorems). Features 3 physical rendering modes (Barnes-Hut, Hierarchical Top-Down, Radial) and autonomous no-code Cypher Copilot." },
                    { num: "Pillar 03", title: "Advisor Matcher (Ideal Thesis Supervisor)", desc: "Neuro-symbolic recommendation engine combining dense cosine topic similarity and Neo4j ontological co-occurrence. Rich advisor profiles across DMI's 4 laboratories (LARI, LAMAP, LAMEX, LASE) with AI affinity score % and 1-click actions." },
                    { num: "Pillar 04", title: "OKF v0.2 Certification & Waterfall Citation Audit", desc: "No-LLM Cypher SHA-256 certifier (tamper-proof Tiers 1/2/3) and Waterfall anti-hallucination auditor (DMI -> Semantic Scholar -> Crossref, DOI/arXiv O(1)). FAIR OAI-PMH v2.0 (Dublin Core, ETD-MS) and BibTeX/Zotero exports." },
                    { num: "Pillar 05", title: "8-Agent LangGraph Network, K1-WikiSkill & Quorum", desc: "8 specialized agents (Supervisor, GraphRAG, Advisor, Math SEIR/Caputo, Biblio, OKF, Critic Q17, WikiSkill). Continuous self-evolution via procedural meta-skills (Google Research 2026) and 4-Eyes symmetric quorum under supervision of Prof. DAYANG PAUL." }
                ],
                impacts: [
                    "Absolute elimination of academic hallucinations via deterministic OKF v0.2 SHA-256 No-LLM cryptographic verification.",
                    "Intelligent Advisor Matcher: optimal guidance matching students with supervisors and laboratories (LARI, LAMAP, LAMEX, LASE) with explainable rationale.",
                    "Interactive 3D/2D Barnes-Hut Visualizer & Natural Language Cypher queries to navigate 28 years of scientific assets (470 theses, 19 M1 projects).",
                    "Continuous Self-Evolution via K1-WikiSkill & High Reliability: 77 automated unit tests (100% pass rate), Redis 7 fast cache (<20ms), and 4-Eyes security quorum."
                ],
                techs: ["FastAPI 0.115", "LangGraph 8 Agents", "Neo4j 5.26 GraphRAG", "Advisor Matcher", "Barnes-Hut 3D", "OKF v0.2 SHA-256", "K1-WikiSkill", "Redis 7 Lua (<20ms)", "PostgreSQL pgvector", "OAI-PMH Dublin Core"],
                github: "https://github.com/gervais-afk/k1-mathinfo"
            }
        }
    };

    const modalOverlay = document.getElementById('projectModal');
    const modalCloseBtn = document.getElementById('modalClose');
    const modalBadge = document.getElementById('modalBadge');
    const modalTitle = document.getElementById('modalTitle');
    const modalSubtitle = document.getElementById('modalSubtitle');
    const modalContent = document.getElementById('modalContent');
    const openModalBtns = document.querySelectorAll('.open-modal-btn');

    function openModal(projectId) {
        const lang = localStorage.getItem('preferredLang') || 'fr';
        const project = projectsData[lang] ? projectsData[lang][projectId] : null;
        if (!project) return;

        modalBadge.textContent = project.badge;
        modalTitle.textContent = project.title;
        modalSubtitle.textContent = project.subtitle;

        // Build Pipeline Steps HTML
        const pipelineHTML = project.pipeline.map(step => `
            <div class="pipeline-step">
                <span class="pipeline-step-num">${step.num}</span>
                <h5 class="pipeline-step-title">${step.title}</h5>
                <p class="pipeline-step-desc">${step.desc}</p>
            </div>
        `).join('');

        // Build Impacts List HTML
        const impactsHTML = project.impacts.map(imp => `
            <li><i class="fa-solid fa-circle-check"></i> <span>${imp}</span></li>
        `).join('');

        // Build Tech Pills HTML
        const techsHTML = project.techs.map(tech => `
            <span>${tech}</span>
        `).join('');

        const headers = {
            fr: {
                arch: "Architecture System &amp; Flux de Données",
                impact: "Valeur Ajoutée &amp; Impacts Clés",
                tech: "Technologies &amp; Frameworks",
                github: "Accéder au Dépôt GitHub"
            },
            en: {
                arch: "System Architecture &amp; Data Flow",
                impact: "Value Added &amp; Key Impacts",
                tech: "Technologies &amp; Frameworks",
                github: "Access GitHub Repository"
            }
        };

        const activeHeader = headers[lang] || headers.fr;

        const infographicHTML = project.infographic ? `
            <div class="arch-section" style="grid-column: 1 / -1; margin-bottom: 0.8rem;">
                <h4><i class="fa-solid fa-image"></i> ${lang === 'fr' ? 'Infographie Officielle — Vue Globale du Système' : 'Official Infographic — Global System Overview'}</h4>
                <div style="border-radius: 12px; overflow: hidden; border: 1px solid rgba(0, 242, 254, 0.35); background: rgba(0,0,0,0.5); text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.4);">
                    <a href="${project.infographic}" target="_blank" title="${lang === 'fr' ? 'Cliquer pour agrandir' : 'Click to enlarge'}">
                        <img src="${project.infographic}" alt="Infographie ${project.title}" style="width: 100%; max-height: 480px; object-fit: contain; display: block; margin: 0 auto; transition: transform 0.3s ease;">
                    </a>
                    <div style="padding: 0.5rem; font-size: 0.8rem; color: var(--text-muted); background: rgba(10, 15, 30, 0.7);">
                        <i class="fa-solid fa-magnifying-glass-plus text-neon"></i> ${lang === 'fr' ? 'Cliquer sur l\'image pour afficher en pleine résolution HD' : 'Click image to open high-resolution HD view'}
                    </div>
                </div>
            </div>
        ` : '';

        modalContent.innerHTML = `
            <div class="modal-grid">
                ${infographicHTML}
                <div class="arch-section">
                    <h4><i class="fa-solid fa-diagram-project"></i> ${activeHeader.arch}</h4>
                    <div class="pipeline-flow">
                        ${pipelineHTML}
                    </div>
                </div>

                <div class="arch-section">
                    <h4><i class="fa-solid fa-bullseye"></i> ${activeHeader.impact}</h4>
                    <ul class="impact-list">
                        ${impactsHTML}
                    </ul>
                </div>

                <div class="arch-section">
                    <h4><i class="fa-solid fa-code"></i> ${activeHeader.tech}</h4>
                    <div class="tech-pills">
                        ${techsHTML}
                    </div>
                </div>

                <div class="project-links-row">
                    <a href="${project.github}" target="_blank" class="btn btn-primary w-100">
                        ${activeHeader.github} <i class="fa-brands fa-github"></i>
                    </a>
                </div>
            </div>
        `;

        modalOverlay.classList.add('active');
        modalOverlay.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modalOverlay.classList.remove('active');
        modalOverlay.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = 'auto';
    }

    openModalBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const projectId = btn.getAttribute('data-project');
            openModal(projectId);
        });
    });

    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', closeModal);
    }

    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            closeModal();
        }
    });
});

/* ==========================================
   PODCAST HUB PLAYER LOGIC
   ========================================== */
window.playPodcastTrack = function(index, audioSrc, titleKey, tagKey, descKey) {
    const player = document.getElementById('podcastAudioPlayer');
    const source = document.getElementById('podcastAudioSource');
    const titleEl = document.getElementById('mainTrackTitle');
    const tagEl = document.getElementById('mainTrackTag');
    const descEl = document.getElementById('mainTrackDesc');

    if (!player || !source) return;

    // Update active card style
    const cards = document.querySelectorAll('.podcast-track-card');
    cards.forEach((c, idx) => c.classList.toggle('active', idx === index));

    // Update audio source & play
    source.src = audioSrc;
    player.load();
    player.play().catch(e => console.log('Playback started:', e));

    // Update data-i18n attributes
    if (titleEl) titleEl.setAttribute('data-i18n', titleKey);
    if (tagEl) tagEl.setAttribute('data-i18n', tagKey);
    if (descEl) descEl.setAttribute('data-i18n', descKey);

    // Refresh active language translation for main player
    const lang = localStorage.getItem('preferredLang') || 'fr';
    if (typeof translations !== 'undefined' && translations[lang]) {
        if (titleEl && translations[lang][titleKey]) titleEl.innerHTML = translations[lang][titleKey];
        if (tagEl && translations[lang][tagKey]) tagEl.innerHTML = translations[lang][tagKey];
        if (descEl && translations[lang][descKey]) descEl.innerHTML = translations[lang][descKey];
    }
};

/* ==========================================
   i18n LANGUAGE SWITCHER ENGINE
   ========================================== */
window.currentAppLang = localStorage.getItem('preferredLang') || 'fr';

window.switchLanguage = function(lang) {
    window.currentAppLang = lang;
    localStorage.setItem('preferredLang', lang);

    const btnNavFr = document.getElementById('btnNavFr');
    const btnNavEn = document.getElementById('btnNavEn');
    if (btnNavFr && btnNavEn) {
        btnNavFr.classList.toggle('active', lang === 'fr');
        btnNavEn.classList.toggle('active', lang === 'en');
    }

    if (typeof translations === 'undefined') return;
    const t = translations[lang];
    if (!t) return;

    // Translate elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            el.innerHTML = t[key];
        }
    });

    // Update dynamic CV download link if present
    const heroDownloadCv = document.getElementById('heroDownloadCv');
    if (heroDownloadCv) {
        if (lang === 'fr') {
            heroDownloadCv.setAttribute('href', 'KOA_MARIE_GERVAIS_NELLY_CV%20FR.pdf');
        } else {
            heroDownloadCv.setAttribute('href', 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf');
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferredLang') || 'fr';
    window.switchLanguage(savedLang);
});


