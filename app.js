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
    });

    // 6. Interactive Architecture Modals System
    const projectsData = {
        fr: {
            'archi-cam-ai': {
                badge: "SaaS IA Agentique & 5D BIM (Candidat Google Africa Applied AI Lab)",
                title: "Archi Cam AI 🏛️",
                subtitle: "Plateforme IA souveraine de modélisation BIM 5D & génération automatisée de métrés normés pour le BTP africain.",
                pipeline: [
                    { num: "Étape 01", title: "Entrée Multimodale", desc: "Scan 2D/3D, fichiers DWG/PDF, maquettes IFC & prompts vocaux/texte de l'ingénieur." },
                    { num: "Étape 02", title: "Agentic RAG & Graph", desc: "Neo4j 5.20 GraphRAG + Gemma 4 12B QAT local & Gemini 2.5/1.5 Flash." },
                    { num: "Étape 03", title: "Python Sandbox BIM", desc: "Calculs déterministes BAEL 91, déductions >0.50m² & IfcOpenShell sans hallucination." },
                    { num: "Étape 04", title: "Livrables BIM 5D", desc: "Fichiers IFC 3D, devis Excel normés (DQE 6 onglets) & rendus Imagen 3.0 + ControlNet." }
                ],
                impacts: [
                    "Accélération de +99,2% : génération des devis estimatifs (DQE) en <45 secondes (contre 3 à 7 jours manuellement).",
                    "Zéro Hallucination & Conformité Légale : moteur déterministe Python BAEL 91 + ontologies Neo4j GraphRAG (MINMAP 2026).",
                    "Résilience Hybride Cloud/Edge : Gemini 2.5/1.5 Flash en cloud avec basculement automatique sur Gemma 4 12B QAT local (LM Studio).",
                    "Précision MLOps (R² = 0.9872) : modèle d'estimation entraîné et évalué sous MLflow sur 400 projets de construction africains."
                ],
                techs: ["Next.js 14", "Firebase Genkit", "Google Gemma 4 12B", "Gemini 2.5/1.5 Flash", "Neo4j GraphRAG", "IfcOpenShell", "Python BAEL 91", "MLflow MLOps", "Imagen 3.0 + ControlNet"],
                github: "https://github.com/gervais-afk/archi-cam-ai"
            },
            'sovereign-bi': {
                badge: "Agentic Business Intelligence & Security",
                title: "Sovereign.BI Agentic 📊",
                subtitle: "Moteur autonome d'analyse de données d'entreprise permettant d’interroger des bases SQL complexes en langage naturel.",
                pipeline: [
                    { num: "Étape 01", title: "NL Query & Guardrail", desc: "Interrogation utilisateur filtrée par des seuils de sécurité dynamiques." },
                    { num: "Étape 02", title: "Orchestrateur TS", desc: "Cartographie du schéma PostgreSQL via Neo4j GraphRAG (N10S)." },
                    { num: "Étape 03", title: "Génération & Audit SQL", desc: "Traduction SQL optimisée + audit SHAP Sentinel contre toute anomalie." },
                    { num: "Étape 04", title: "Visualisation & Insights", desc: "Restitution graphique HTML/React & synthèses exécutives Markdown." }
                ],
                impacts: [
                    "Interrogation instantanée de bases de données volumineuses sans compétences SQL requises.",
                    "Système de guardrails dynamiques évitant toute injection SQL ou altération de données.",
                    "Audits SHAP intégrés pour expliquer en toute transparence le raisonnement des agents."
                ],
                techs: ["React", "FastAPI", "TypeScript Orchestrator", "PostgreSQL", "Neo4j GraphRAG", "Gemini AI", "Docker", "SHAP Auditor"],
                github: "https://github.com/gervais-afk/sovereign-bi-agentic"
            },
            'dataset-automator': {
                badge: "Plateforme MLOps Agentique & Usine d'Ingénierie de Datasets",
                title: "Dataset Automator ⚙️",
                subtitle: "Usine MLOps autonome d'ingestion, d'audit de qualité, de gouvernance sémantique (Neo4j) et d'entraînement automatisé.",
                pipeline: [
                    { num: "Étape 01", title: "Profilage & Data Drift (KS/PSI)", desc: "Analyse Python, détection des types réels et surveillance continue des dérives de distribution (KS-test / PSI > 30%)." },
                    { num: "Étape 02", title: "GraphRAG & Curation Sémantique", desc: "Modélisation dans le Knowledge Graph Neo4j, mappings métiers et auto-correction (Self-Healing) des échecs passés." },
                    { num: "Étape 03", title: "Genkit & MLflow Tracking", desc: "Orchestration TypeScript avec Gemma-4 12B local (LM Studio), validation HITL et tracking complet sur MLflow UI." },
                    { num: "Étape 04", title: "Streamlit Dashboard & Notebook Factory", desc: "Exploration du graphe 2D/3D, audits SHAP et génération automatique de Notebooks Jupyter MLOps (.ipynb) certifiés." }
                ],
                impacts: [
                    "Automatisation complète du cycle de préparation de données et d'entraînement MLOps.",
                    "Détection précoce des dérives de modèles (Data Drift) avec génération automatique d'alertes dans Neo4j.",
                    "Exports instantanés de Notebooks Jupyter documentés et d'interfaces de suivi MLflow / Genkit."
                ],
                techs: ["TypeScript Genkit", "Neo4j GraphRAG", "MLflow", "Google Gemma 4 (LM Studio)", "Streamlit", "Firebase Firestore", "Python MLOps"],
                github: "https://github.com/gervais-afk/dataset-automator"
            },
            'asu-audit-ready': {
                badge: "Conformité Sûreté Aéroportuaire CCAA & Reporting",
                title: "ASU-Audit-Ready 🛡️",
                subtitle: "Tableau de Bord de Conformité Sûreté, Génération de Rapports d'Audit V4 & Simulateur d'Audition pour Agents CCAA.",
                pipeline: [
                    { num: "Étape 01", title: "Tableau de Bord & KPIs Sûreté", desc: "Suivi mensuel des 7 objectifs critiques d'inspection aéronautique (Taux global, PIF, conformité ZSAR)." },
                    { num: "Étape 02", title: "Génération de Rapports Word V4", desc: "Compilation automatique des rapports d'activités mensuels (.docx) selon le Modèle V4 CCAA avec directives et remédiations." },
                    { num: "Étape 03", title: "Vérificateur de Livrables Audit", desc: "Contrôle automatisé de l'exhaustivité et de la conformité des pièces requises pour les audits officiels." },
                    { num: "Étape 04", title: "Simulateur d'Audition AVSEC", desc: "Entraînement interactif et simulation d'audition d'inspection pour la préparation des agents de sûreté." }
                ],
                impacts: [
                    "Digitalisation complète et gain de temps massif dans la rédaction des rapports de sûreté mensuels.",
                    "Garantie de conformité à 100% avec les exigences réglementaires de la CCAA (Autorité Aéronautique du Cameroun).",
                    "Entraînement continu des agents de sûreté aéroportuaire aux scénarios d'inspection d'audit."
                ],
                techs: ["Streamlit", "Python Engine", "python-docx (Modèle V4)", "ChartBuilder", "AuditChecker", "AuditSimulator", "Matplotlib / Seaborn"],
                github: "https://github.com/gervais-afk/ASU-Audit-Ready"
            },
            'vigie-sahel': {
                badge: "IA Impact Climat & Santé Publique",
                title: "VigieSahel 🌾",
                subtitle: "Système prédictif pour l'optimisation agricole et l'anticipation des risques sanitaires dans la région du Sahel.",
                pipeline: [
                    { num: "Étape 01", title: "Collecte Multi-sources", desc: "Ingestion des données météo, satellite & capteurs de qualité de l'air PM2.5." },
                    { num: "Étape 02", title: "Modélisation ML", desc: "Algorithmes de prédiction des dates optimales de semis et propagation épidémique." },
                    { num: "Étape 03", title: "Stockage Supabase", desc: "Base de données cloud synchronisée en temps réel." },
                    { num: "Étape 04", title: "PWA Offline-First", desc: "Interface Streamlit PWA accessible même avec faible connectivité internet." }
                ],
                impacts: [
                    "Optimisation des rendements de la culture du coton face aux variations pluviométriques.",
                    "Système d'alerte précoce pour les pics de pollution (PM2.5) et les risques de méningite.",
                    "Solution conçue sur-mesure pour les coopératives et décideurs du Sahel."
                ],
                techs: ["Streamlit", "Python ML", "Supabase", "Scikit-Learn", "Pandas", "PWA"],
                github: "https://github.com/gervais-afk/VigieSahel"
            },
            'k1-mathinfo': {
                badge: "IA Souveraine, GraphRAG & Certification Scientifique (DMI - Université de Ngaoundéré)",
                title: "K1-MATHINFO (v2.5+) 🏛️",
                subtitle: "Infrastructure souveraine d'IA académique, modélisation de 28 ans de recherche & certification déterministe.",
                pipeline: [
                    { num: "Étape 01", title: "Ingestion & Parseur Normalisé", desc: "Extraction et segmentation automatisée de 451 thèses, métadonnées Dublin Core, formules LaTeX et détection des tables." },
                    { num: "Étape 02", title: "Graphe Topologique Neo4j & pgvector", desc: "Modélisation de 1 366 nœuds et 3 833 relations généalogiques (encadrements, jurys, algorithmes, théorèmes) + index HNSW 384d." },
                    { num: "Étape 03", title: "Recherche Hybride Multi-Stage (RRF k=60)", desc: "Fusion réciproque dense/sparse (BM25 + pgvector), re-ranking Cross-Encoder et boost taxonomique DMI (β=0.35)." },
                    { num: "Étape 04", title: "Certification OKF v0.2 & Auditeur Bibliographique", desc: "Attesteur Cypher SHA-256 No-LLM (Tier 1/2/3), audit anti-hallucination Waterfall (DMI -> Semantic Scholar -> Crossref) et interopérabilité OAI-PMH v2.0." }
                ],
                impacts: [
                    "Élimination totale des hallucinations académiques grâce à la certification déterministe cryptographique OKF v0.2 SHA-256.",
                    "Valorisation de 28 ans de patrimoine scientifique (1997–2025) : 451 thèses et mémoires et 18 projets d'application M1 indexés.",
                    "Auditeur bibliographique en cascade détectant automatiquement les références fictives (« citations fantômes ») avec résolution DOI/arXiv en temps réel.",
                    "Excellence logicielle & gouvernance : 68 tests automatisés (100% passés), cache Redis 7 (<3ms) et gouvernance symétrique (Quorum 4 Yeux KOA + AZIZ)."
                ],
                techs: ["FastAPI 0.115", "Neo4j 5.26 GraphRAG", "Redis 7 Lua", "PostgreSQL pgvector", "OKF v0.2 SHA-256", "LangGraph FSM", "Cross-Encoder", "OAI-PMH Dublin Core"],
                github: "https://github.com/gervais-afk/k1-mathinfo"
            }
        },
        en: {
            'archi-cam-ai': {
                badge: "Agentic AI & 5D BIM SaaS (Google Africa Applied AI Lab Candidate)",
                title: "Archi Cam AI 🏛️",
                subtitle: "Sovereign 5D BIM & Agentic AI platform for automated quantity surveying in African construction.",
                pipeline: [
                    { num: "Step 01", title: "Multimodal Input", desc: "2D/3D scans, DWG/PDF files, IFC models & vocal/text prompts from the engineer." },
                    { num: "Step 02", title: "Agentic RAG & Graph", desc: "Neo4j 5.20 GraphRAG + local Gemma 4 12B QAT & Gemini 2.5/1.5 Flash." },
                    { num: "Step 03", title: "Python Sandbox BIM", desc: "Deterministic BAEL 91 structural calculations, >0.50m² deductions & IfcOpenShell with zero hallucination." },
                    { num: "Step 04", title: "5D BIM Deliverables", desc: "3D IFC files, standardized Excel BOQs (6-tab DQE) & Imagen 3.0 + ControlNet renders." }
                ],
                impacts: [
                    "99.2% speedup: Bill of Quantities (BOQ/DQE) generated in <45 seconds (down from 3 to 7 days manually).",
                    "Zero Hallucination & Regulatory Compliance: deterministic Python BAEL 91 math engine + Neo4j GraphRAG ontologies (MINMAP 2026).",
                    "Hybrid Cloud/Edge Resilience: cloud-based Gemini 2.5/1.5 Flash with automatic failover to local Gemma 4 12B QAT (LM Studio).",
                    "MLOps Accuracy (R² = 0.9872): estimating model trained and evaluated under MLflow on 400 African construction projects."
                ],
                techs: ["Next.js 14", "Firebase Genkit", "Google Gemma 4 12B", "Gemini 2.5/1.5 Flash", "Neo4j GraphRAG", "IfcOpenShell", "Python BAEL 91", "MLflow MLOps", "Imagen 3.0 + ControlNet"],
                github: "https://github.com/gervais-afk/archi-cam-ai"
            },
            'sovereign-bi': {
                badge: "Agentic Business Intelligence & Security",
                title: "Sovereign.BI Agentic 📊",
                subtitle: "Autonomous enterprise data analysis engine allowing users to query complex SQL databases in natural language.",
                pipeline: [
                    { num: "Step 01", title: "NL Query & Guardrail", desc: "User natural language query filtered by dynamic security guardrails." },
                    { num: "Step 02", title: "TS Orchestrator", desc: "PostgreSQL schema mapping via Neo4j GraphRAG (N10S)." },
                    { num: "Step 03", title: "SQL Generation & Audit", desc: "Optimized SQL translation + SHAP Sentinel audit against any query anomaly." },
                    { num: "Step 04", title: "Visualization & Insights", desc: "HTML/React graphic rendering & executive Markdown summaries." }
                ],
                impacts: [
                    "Instant querying of massive datasets without requiring SQL programming expertise.",
                    "Dynamic guardrail system preventing SQL injection attacks or unauthorized data modification.",
                    "Integrated SHAP explainability audits to clarify autonomous agent reasoning with full transparency."
                ],
                techs: ["React", "FastAPI", "TypeScript Orchestrator", "PostgreSQL", "Neo4j GraphRAG", "Gemini AI", "Docker", "SHAP Auditor"],
                github: "https://github.com/gervais-afk/sovereign-bi-agentic"
            },
            'dataset-automator': {
                badge: "Agentic MLOps Platform & Dataset Engineering Factory",
                title: "Dataset Automator ⚙️",
                subtitle: "Autonomous MLOps factory for data ingestion, quality auditing, semantic governance (Neo4j), and automated training.",
                pipeline: [
                    { num: "Step 01", title: "Profiling & Data Drift (KS/PSI)", desc: "Python analysis, real data type detection and continuous monitoring of distribution drift (KS-test / PSI > 30%)." },
                    { num: "Step 02", title: "GraphRAG & Semantic Curation", desc: "Modeling within Neo4j Knowledge Graph, business mappings and self-healing auto-correction of historical failures." },
                    { num: "Step 03", title: "Genkit & MLflow Tracking", desc: "TypeScript orchestration with local Gemma-4 12B (LM Studio), HITL validation and complete tracking on MLflow UI." },
                    { num: "Step 04", title: "Streamlit Dashboard & Notebook Factory", desc: "2D/3D graph visualization, SHAP audits and automated generation of certified Jupyter MLOps notebooks (.ipynb)." }
                ],
                impacts: [
                    "End-to-end automation of data preparation cycles and MLOps training workflows.",
                    "Early detection of model drift (Data Drift) with automatic alert generation inside Neo4j.",
                    "Instant exports of fully documented Jupyter notebooks and MLflow / Genkit tracking interfaces."
                ],
                techs: ["TypeScript Genkit", "Neo4j GraphRAG", "MLflow", "Google Gemma 4 (LM Studio)", "Streamlit", "Firebase Firestore", "Python MLOps"],
                github: "https://github.com/gervais-afk/dataset-automator"
            },
            'asu-audit-ready': {
                badge: "Airport Security Compliance CCAA & Reporting",
                title: "ASU-Audit-Ready 🛡️",
                subtitle: "Security Compliance Dashboard, V4 Audit Report Generator & Aviation Security Interview Simulator for CCAA Officers.",
                pipeline: [
                    { num: "Step 01", title: "Security Dashboard & KPIs", desc: "Monthly monitoring of the 7 critical aviation inspection targets (Global rate, PIF, ZSAR compliance)." },
                    { num: "Step 02", title: "Word V4 Report Generation", desc: "Automatic compilation of monthly activity reports (.docx) matching the CCAA V4 template with corrective directives." },
                    { num: "Step 03", title: "Audit Deliverables Validator", desc: "Automated completeness and compliance checks of all required documents for official audits." },
                    { num: "Step 04", title: "AVSEC Interview Simulator", desc: "Interactive training and simulated inspection interviews for airport security officers preparation." }
                ],
                impacts: [
                    "Complete digitization and massive time savings in drafting monthly security compliance reports.",
                    "100% compliance guarantee with the regulatory standards of the CCAA (Cameroon Civil Aviation Authority).",
                    "Continuous training of airport security officers through realistic simulated audit scenarios."
                ],
                techs: ["Streamlit", "Python Engine", "python-docx (Modèle V4)", "ChartBuilder", "AuditChecker", "AuditSimulator", "Matplotlib / Seaborn"],
                github: "https://github.com/gervais-afk/ASU-Audit-Ready"
            },
            'vigie-sahel': {
                badge: "Climate Impact & Public Health AI",
                title: "VigieSahel 🌾",
                subtitle: "Predictive system for agricultural optimization and public health outbreak forecasting in the Sahel region.",
                pipeline: [
                    { num: "Step 01", title: "Multi-source Data Collection", desc: "Ingestion of weather, satellite imagery & PM2.5 air quality sensor data." },
                    { num: "Step 02", title: "ML Modeling", desc: "Predictive algorithms for optimal crop sowing dates and epidemic disease propagation." },
                    { num: "Step 03", title: "Supabase Realtime Storage", desc: "Cloud database synchronized in real-time." },
                    { num: "Step 04", title: "Offline-First PWA", desc: "Streamlit PWA interface accessible even under low network connectivity." }
                ],
                impacts: [
                    "Cotton crop yield optimization relative to fluctuating rainfall patterns.",
                    "Early warning system for air pollution peaks (PM2.5) and meningitis outbreak risks.",
                    "Tailor-made solution built for agricultural cooperatives and decision-makers in the Sahel."
                ],
                techs: ["Streamlit", "Python ML", "Supabase", "Scikit-Learn", "Pandas", "PWA"],
                github: "https://github.com/gervais-afk/VigieSahel"
            },
            'k1-mathinfo': {
                badge: "Sovereign AI, GraphRAG & Academic Certification (DMI - University of Ngaoundéré)",
                title: "K1-MATHINFO (v2.5+) 🏛️",
                subtitle: "Sovereign academic AI infrastructure, modeling 28 years of research & deterministic knowledge certification.",
                pipeline: [
                    { num: "Step 01", title: "Ingestion & Standardized Parser", desc: "Automated extraction and chunking of 451 theses, Dublin Core metadata, LaTeX formulas, and table detection." },
                    { num: "Step 02", title: "Neo4j Knowledge Graph & pgvector", desc: "Modeling of 1,366 nodes and 3,833 genealogical relationships (advisors, juries, algorithms, theorems) + 384d HNSW index." },
                    { num: "Step 03", title: "Multi-Stage Hybrid Search (RRF k=60)", desc: "Reciprocal Rank Fusion combining dense pgvector and sparse BM25, Cross-Encoder re-ranking, and DMI taxonomy boost (β=0.35)." },
                    { num: "Step 04", title: "OKF v0.2 Certification & Citation Audit", desc: "No-LLM Cypher SHA-256 certifier (Tiers 1/2/3), Waterfall anti-hallucination auditor (DMI -> Semantic Scholar -> Crossref), and OAI-PMH v2.0 export." }
                ],
                impacts: [
                    "Zero academic hallucination guaranteed by deterministic OKF v0.2 SHA-256 cryptographic certification.",
                    "Capitalization of 28 years of scientific heritage (1997–2025): 451 theses and 18 M1 applied projects fully indexed.",
                    "Waterfall bibliographic auditor automatically detecting fake/ghost citations with real-time DOI & arXiv resolution.",
                    "Engineering excellence & governance: 68 automated unit tests (100% passed), Redis 7 fast cache (<3ms), and symmetric 4-eyes quorum security."
                ],
                techs: ["FastAPI 0.115", "Neo4j 5.26 GraphRAG", "Redis 7 Lua", "PostgreSQL pgvector", "OKF v0.2 SHA-256", "LangGraph FSM", "Cross-Encoder", "OAI-PMH Dublin Core"],
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

        modalContent.innerHTML = `
            <div class="modal-grid">
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
    if (savedLang !== 'fr') {
        window.switchLanguage(savedLang);
    }
});


