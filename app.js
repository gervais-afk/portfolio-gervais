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
                badge: "SaaS IA Agentique & 5D BIM Souverain",
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
                    "Système d'alerte précoce pour les pics de pollution (PM2.5) et les risques de méningite.",
                    "Solution conçue sur-mesure pour les coopératives et décideurs du Sahel."
                ],
                techs: ["Streamlit", "Python ML", "Supabase", "Scikit-Learn", "Pandas", "PWA"],
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


