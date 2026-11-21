import subprocess, os, shutil
import pypdf
import pypdfium2 as pdfium

pdflatex = r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
p_dir = r'C:\Users\HP\Desktop\portfolio-gervais'
govai_dir = r'C:\Users\HP\Desktop\candidature-govai'
avsec_dir = r'C:\Users\HP\Desktop\cv agent de surete aeroportuaire'

# ══════════════════════════════════════════════════════════════════════
# 1. TEMPLATE GENERATOR FOR ENGLISH CV (portfolio-gervais & govai)
# ══════════════════════════════════════════════════════════════════════
def build_en_cv(font_scale=1.0, itemsep=1.2, sec_vspace=3.0):
    tex = rf'''\documentclass[10pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{lmodern}}
\renewcommand{{\familydefault}}{{\sfdefault}}
\usepackage[margin=0.34in,top=0.30in,bottom=0.30in]{{geometry}}
\usepackage{{xcolor}}
\usepackage{{amssymb}}
\usepackage{{graphicx}}
\usepackage{{tikz}}
\usepackage{{hyperref}}
\usepackage{{tabularx}}
\usepackage{{enumitem}}

% ── Palette Harmonieuse & Élégante ──
\definecolor{{primaryDark}}{{HTML}}{{0F172A}}    % Slate 900
\definecolor{{sectionNavy}}{{HTML}}{{1E3A5F}}    % Oxford Navy
\definecolor{{subheading}}{{HTML}}{{334155}}     % Slate 700
\definecolor{{bodyText}}{{HTML}}{{1E293B}}       % Slate 800
\definecolor{{mutedSlate}}{{HTML}}{{64748B}}     % Slate 500
\definecolor{{accentGold}}{{HTML}}{{92400E}}     % Ambre doré
\definecolor{{subtleRule}}{{HTML}}{{CBD5E1}}     % Filet discret
\definecolor{{sidebarBg}}{{HTML}}{{F0F4F8}}      % Fond ardoise bleutée colonne gauche

% ── Couleurs d'En-tête & Marges ──
\definecolor{{headerBg}}{{HTML}}{{E8EFF7}}       % Fond bleu cassé doux
\definecolor{{headerBorder}}{{HTML}}{{CBDCEB}}   % Liseré discret
\definecolor{{marginBlue}}{{HTML}}{{E2EDF8}}     % Bleu clair dilué 4 marges
\definecolor{{marginBorder}}{{HTML}}{{BFD5EC}}   % Filet intérieur

\hypersetup{{
    colorlinks=true,
    linkcolor=sectionNavy,
    urlcolor=sectionNavy,
    pdfauthor={{KOA Marie Gervais Nelly}},
    pdftitle={{Curriculum Vitae - KOA Marie Gervais Nelly}}
}}

\pagestyle{{empty}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{0pt}}
\linespread{{1.06}}

\newcommand{{\secTitle}}[1]{{%
    \vspace{{{sec_vspace}pt}}%
    {{\fontsize{{9.3}}{{11.5}}\selectfont\textbf{{\color{{sectionNavy}}#1}}}}\\[1.2pt]%
    {{\color{{sectionNavy}}\hrule height 0.65pt}}\vspace{{2.5pt}}%
}}

\newcommand{{\sideSecTitle}}[1]{{%
    \vspace{{{sec_vspace}pt}}%
    {{\fontsize{{8.7}}{{10.8}}\selectfont\textbf{{\color{{sectionNavy}}#1}}}}\\[1.2pt]%
    {{\color{{sectionNavy}}\hrule height 0.60pt}}\vspace{{2.2pt}}%
}}

\setlist[itemize]{{leftmargin=*,labelsep=3.5pt,itemsep={itemsep}pt,topsep=0.8pt,parsep=0pt}}
\newcommand{{\bulletItem}}[2]{{%
    \item \textbf{{\color{{primaryDark}}#1}} {{\fontsize{{8.25}}{{10.2}}\selectfont\color{{bodyText}}#2}}%
}}

\begin{document}

% ══════════════════════════════════════════════════════════════════
% CADRE 4 MARGES & BANDE LATÉRALE GAUCHE PLEINE HAUTEUR (TIKZ)
% ══════════════════════════════════════════════════════════════════
\begin{tikzpicture}[remember picture, overlay]
    % 1. Teinte des 4 marges extérieures :
    \fill[marginBlue] (current page.south west) rectangle (current page.north east);
    % 2. Conteneur blanc intérieur :
    \fill[white] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
    
    % 3. BANDE ARDOISE BLEUTÉE QUI DESCEND JUSQU'AU TOUT BAS DE LA PAGE :
    \fill[sidebarBg] ([xshift=4.5mm, yshift=4.5mm]current page.south west) rectangle ([xshift=72.2mm, yshift=-33.8mm]current page.north west);
    
    % 4. Filet intérieur de finition :
    \draw[marginBorder, line width=0.75pt] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
\end{tikzpicture}

% ══════════════════════════════════════════════════════════════════
% EN-TÊTE ÉLÉGANT : FOND BLEU CASSÉ, PHOTO AGRANDIE & VRAIES ICÔNES
% ══════════════════════════════════════════════════════════════════
\setlength{{\fboxsep}}{{4.0pt}}%
\noindent\fcolorbox{{headerBorder}}{{headerBg}}{{%
\begin{minipage}{{\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax}}
    % Photo officielle agrandie (2.20cm) dans un médaillon circulaire
    \begin{minipage}[c]{{0.150\textwidth}}
        \centering
        \begin{tikzpicture}
            \clip (0,0) circle (1.10cm);
            \node at (0,0) {{\includegraphics[width=2.20cm]{{profile_headshot_clean.png}}}};
            \draw[headerBorder, line width=1.1pt] (0,0) circle (1.10cm);
        \end{tikzpicture}
    \end{minipage}%
    \hspace{{0.015\textwidth}}%
    % Nom, Titre & Coordonnées
    \begin{minipage}[c]{{0.535\textwidth}}
        {{\fontsize{{17.2}}{{19.8}}\selectfont\textbf{{\color{{primaryDark}} KOA MARIE GERVAIS NELLY}}}}\\[2.0pt]
        {{\fontsize{{9.4}}{{11.5}}\selectfont\textbf{{\color{{sectionNavy}} AI Systems Engineer \& Operational Risk Specialist (AVSEC)}}}}\\[3.2pt]
        {{\fontsize{{7.8}}{{9.8}}\selectfont
        \raisebox{{-0.8pt}}{{\includegraphics[height=7.0pt]{{icons/icon_location.png}}}}\hspace{{2.0pt}}{{\color{{bodyText}}Ngaound\'er\'e / Douala, CM}}
        \quad{{\color{{mutedSlate}}$|$}}\quad
        \raisebox{{-0.8pt}}{{\includegraphics[height=6.6pt]{{icons/icon_phone.png}}}}\hspace{{2.0pt}}{{\color{{bodyText}}+237 695 35 34 02}}\\[1.8pt]
        \raisebox{{-0.8pt}}{{\includegraphics[height=6.6pt]{{icons/icon_email.png}}}}\hspace{{2.0pt}}\href{{mailto:contact@archicam-ai.com}}{{\color{{primaryDark}}\textbf{{contact@archicam-ai.com}}}}
        }}
    \end{minipage}%
    \hfill
    % Liens professionnels
    \begin{minipage}[c]{{0.29\textwidth}}
        \raggedleft
        {{\fontsize{{7.8}}{{9.8}}\selectfont
        \raisebox{{-0.8pt}}{{\includegraphics[height=6.8pt]{{icons/icon_globe.png}}}}\hspace{{2.0pt}}\href{{https://portfolio-gervais.vercel.app}}{{\textbf{{\color{{primaryDark}}portfolio-gervais.vercel.app}}}}\\[2.0pt]
        \raisebox{{-0.8pt}}{{\includegraphics[height=6.8pt]{{icons/icon_github.png}}}}\hspace{{2.0pt}}\href{{https://github.com/gervais-afk}}{{\color{{bodyText}}github.com/gervais-afk}}\\[2.0pt]
        \raisebox{{-0.8pt}}{{\includegraphics[height=6.8pt]{{icons/icon_linkedin.png}}}}\hspace{{2.0pt}}\href{{https://linkedin.com/in/marie-gervais-koa}}{{\color{{bodyText}}linkedin.com/in/marie-gervais-koa}}
        }}
    \end{minipage}
\end{minipage}%
}}

\vspace{{2.8pt}}

% ══════════════════════════════════════════════════════════════════
% DEUX COLONNES VERTICALES (POLICE AGRANDIE DES DEUX CÔTÉS)
% ══════════════════════════════════════════════════════════════════
\begin{minipage}[t]{{0.32\textwidth}}
\vspace{{1.5pt}}%

    % ── AI GOVERNANCE & RISK ──
    \sideSecTitle{{AI GOVERNANCE \& SAFETY}}
    {{\fontsize{{8.0}}{{10.2}}\selectfont
    \begin{itemize}[leftmargin=7pt,label={{\color{{sectionNavy}}\scriptsize$\blacktriangleright$}},itemsep=1.3pt]
        \item \textbf{{Operational Risk Modeling:}} ICAO Annex 17 \& Doc 8973 multilateral safety standards.
        \item \textbf{{Incident Forensics:}} Root-cause analysis, anomaly reporting, zero-failure mitigation.
        \item \textbf{{Epistemic Abstention:}} Thresholds to prevent hallucinations under low confidence.
        \item \textbf{{Verifiable Workflows:}} Deterministic schema verification \& graph rule compliance.
        \item \textbf{{Red-Teaming \& Inspection:}} Crisis protocols, drill design, vulnerability screening.
    \end{itemize}
    }}

    % ── EDUCATION ──
    \sideSecTitle{{EDUCATION}}
    {{\fontsize{{8.0}}{{10.1}}\selectfont
    \textbf{{\color{{primaryDark}}Professional Master's in Applied AI}}\\[0.8pt]
    {{\color{{sectionNavy}}\textit{{University of Ngaoundéré (DMI)}}}} \hfill {{\fontsize{{7.4}}{{8.8}}\selectfont\color{{mutedSlate}}2025--2027}}\\[0.8pt]
    {{\fontsize{{7.4}}{{8.8}}\selectfont\textbf{{\color{{accentGold}}In progress}} \ -- \ \color{{bodyText}}Advanced curriculum in production AI architectures, knowledge graphs, and verifiable pipelines.}}\\[3.0pt]
    \textbf{{\color{{primaryDark}}B.Sc. \& HND in Civil Engineering}}\\[0.8pt]
    {{\color{{sectionNavy}}\textit{{IUC Douala (Institut Univ. de la Côte)}}}} \hfill {{\fontsize{{7.4}}{{8.8}}\selectfont\color{{mutedSlate}}2015--2016}}\\[0.8pt]
    {{\fontsize{{7.4}}{{8.8}}\selectfont\color{{bodyText}}Building specialization. Grounding in structural mechanics, physical risk modeling, and metrology.}}
    }}

    % ── TECHNICAL TOOLING ──
    \sideSecTitle{{TECHNICAL TOOLING}}
    {{\fontsize{{7.8}}{{9.8}}\selectfont
    \textbf{{\color{{sectionNavy}}Languages \& Back-End:}}\\[0.5pt]
    Python, TypeScript, FastAPI, Docker, pytest, Git.\\[2.5pt]
    \textbf{{\color{{sectionNavy}}AI, Data \& Verification:}}\\[0.5pt]
    FastMCP, Genkit, Neo4j (Cypher), MLflow, Optuna, Zod, PostgreSQL, pgvector, SQLite, OLAP.
    }}

    % ── CERTIFICATIONS ──
    \sideSecTitle{{CERTIFICATIONS \& CLEARANCES}}
    {{\fontsize{{7.8}}{{9.8}}\selectfont
    \begin{itemize}[leftmargin=7pt,label={{\color{{sectionNavy}}\scriptsize$\blacktriangleright$}},itemsep=1.3pt]
        \item \textbf{{Certified AVSEC Supervisor \& Agent}} (CCAA / ICAO Annex 17 compliant).
        \item \textbf{{Active Airside Security Clearance (ZSAR)}}.
        \item \textbf{{X-ray Radioscopy Threat Specialist}}.
    \end{itemize}
    }}

    % ── LANGUAGES ──
    \sideSecTitle{{LANGUAGES}}
    {{\fontsize{{7.9}}{{10.0}}\selectfont
    \textbf{{French:}} Native / Bilingual operational.\\[1.5pt]
    \textbf{{English:}} Technical, Aviation \& Academic.
    }}

\end{minipage}%
\hfill
\begin{minipage}[t]{{0.655\textwidth}}

    % ── EXECUTIVE PROFILE ──
    \secTitle{{EXECUTIVE PROFILE}}
    {{\fontsize{{8.4}}{{10.6}}\selectfont\color{{bodyText}}
    Applied AI Systems Engineer and Certified Aviation Security (AVSEC) Supervisor combining 8+ years of frontline risk governance in high-stakes infrastructure with hands-on machine learning architecture. Developer of \textit{{ASU (Airport Security Unit) Audit-Ready}} and verifiable agentic pipelines. Bridges zero-tolerance operational defense protocols, multi-stakeholder auditability, and epistemic abstention with frontier AI safety governance.
    }}

    % ── OPERATIONAL RISK EXPERIENCE ──
    \secTitle{{HIGH-CONSEQUENCE OPERATIONAL RISK LEADERSHIP}}

    {{\fontsize{8.6}{10.8}\selectfont\textbf{{\color{{primaryDark}}Operational Security Supervisor (Shift Lead AVSEC)}}} \hfill {{\fontsize{{7.8}}{{9.6}}\selectfont\color{{mutedSlate}}Jan. 2025 -- Present}}\\[0.8pt]
    {{\fontsize{{7.9}}{{9.6}}\selectfont\textit{{\color{{sectionNavy}}Cameroon Civil Aviation Authority (CCAA) $|$ Ngaoundéré Airport (DOS)}}}\\[1.2pt]
    \begin{itemize}
        \bulletItem{{Command of Shift: }}{Lead frontline security personnel across passenger checkpoints (PIF), access portals, and airside zones (ZSAR); enforced 100\% compliance with ICAO Annex 17 standards.}
        \bulletItem{{Safety-Critical Diagnostics: }}{Supervise daily calibration of metal detectors, trace detectors, and dual-view X-ray imaging systems with zero operational downtime.}
        \bulletItem{{Airside Threat Defense: }}{Enforce perimeter security, access control, and anti-intrusion protocols with unbroken compliance across external ICAO and national oversight inspections.}
    \end{itemize}
    \vspace{{2.0pt}}
    {{\fontsize{8.6}{10.8}\selectfont\textbf{{\color{{primaryDark}}Aviation Security Agent \& Shift Supervisor}}} \hfill {{\fontsize{{7.8}}{{9.6}}\selectfont\color{{mutedSlate}}2018 -- Jan. 2025}}\\[0.8pt]
    {{\fontsize{{7.9}}{{9.6}}\selectfont\textit{{\color{{sectionNavy}}Cameroon Civil Aviation Authority (CCAA) $|$ Yaoundé-Nsimalen Int. Airport}}}\\[1.2pt]
    \begin{itemize}
        \bulletItem{{Lead Radioscopy Analyst: }}{Screened 100,000+ passengers and hold baggage, detecting concealed prohibited threats and resolving high-consequence security anomalies.}
        \bulletItem{{Incident Forensics \& Audit Trails: }}{Authored statutory 24h incident briefs, risk evaluations, and chain-of-custody dossiers for official international audit panels.}
    \end{itemize}

    % ── APPLIED AI & VERIFICATION PROJECTS ──
    \secTitle{{APPLIED AI, VERIFICATION \& AUDITING PROJECTS}}

    {{\fontsize{8.6}{10.8}\selectfont\textbf{{\color{{primaryDark}}ASU (Airport Security Unit) Audit-Ready --- Compliance \& Inspection Simulator}}}}\\[0.5pt]
    {{\fontsize{{7.9}}{{9.6}}\selectfont\textit{{\color{{sectionNavy}}Conceived for CCAA Operational Security Division (DOS)}} \hfill {{\color{{mutedSlate}}2025 -- Present}}}\\[1.2pt]
    \begin{itemize}
        \bulletItem{{95\% Reporting Automation: }}{Eliminated 40 hours of monthly paperwork down to 2 seconds, generating signed audit-compliant documentation ready for multilateral ICAO inspectors.}
        \bulletItem{{Pre-Audit Vulnerability Tracker: }}{Built analytics dashboards mapping screening failures and real-time operational competencies across active airport security personnel.}
        \bulletItem{{Audition Drill Simulator: }}{Engineered an interactive module drilling officers on multilateral ICAO inspection interviews and emergency crisis procedures.}
    \end{itemize}
    \vspace{{2.0pt}}
    {{\fontsize{8.6}{10.8}\selectfont\textbf{{\color{{primaryDark}}Dataset Automator --- Agentic Pipeline with Deterministic Rules}}}}\\[0.5pt]
    {{\fontsize{{7.9}}{{9.6}}\selectfont\textit{{\color{{sectionNavy}}Google Cloud \#AllThingsAgentic Hackathon Prototype}} \hfill {{\color{{mutedSlate}}2026}}}\\[1.2pt]
    \begin{itemize}
        \bulletItem{{Deterministic Schema Verification: }}{Architected autonomous data profiling and model validation agents enforcing sanity checks via Zod schemas and Neo4j graph rules.}
        \bulletItem{{Model Auditing: }}{Integrated Optuna optimization with MLflow tracking for tamper-proof reproducibility of model training runs and data transformations.}
    \end{itemize}
    \vspace{{2.0pt}}
    {{\fontsize{8.6}{10.8}\selectfont\textbf{{\color{{primaryDark}}K1-MathInfo --- Hybrid Retrieval Engine with Epistemic Abstention}}}}\\[0.5pt]
    {{\fontsize{{7.9}}{{9.6}}\selectfont\textit{{\color{{sectionNavy}}Academic Repository System $|$ Dept. of Mathematics \& Computer Science (Univ. of Ngaoundéré)}} \hfill {{\color{{mutedSlate}}2026}}}\\[1.2pt]
    \begin{itemize}
        \bulletItem{{Hallucination Defense: }}{Engineered hybrid search with explicit abstention thresholds and weighted Jaccard explainability across 525 works---refusing to generate speculative claims.}
    \end{itemize}
    \vspace{{2.0pt}}
    {{\fontsize{8.6}{10.8}\selectfont\textbf{{\color{{primaryDark}}Archi Cam AI --- Computational Intelligence for Construction}}}}\\[0.5pt]
    {{\fontsize{{7.9}}{{9.6}}\selectfont\textit{{\color{{sectionNavy}}Google Applied Africa AI Lab $|$ Applied AI Project}} \hfill {{\color{{mutedSlate}}2026}}}\\[1.2pt]
    \begin{itemize}
        \bulletItem{{Domain Calculation Integrity: }}{Developed automated cost estimation (DQE) and quantity takeoff algorithms, preventing budgetary misestimations.}
    \end{itemize}

    % ── HONOURS & DISTINCTIONS ──
    \secTitle{{HONOURS \& DISTINCTIONS}}
    {{\fontsize{{8.5}}{{10.6}}\selectfont
    \textbf{{\color{{accentGold}} $\bigstar$ CCAA Excellence \& Integrity Award (April 2023)}} \ -- \ \textbf{{\color{{sectionNavy}}Cameroon Civil Aviation Authority (CCAA)}}\\[1.2pt]
    {{\fontsize{{7.9}}{{9.7}}\selectfont\color{{bodyText}}
    Solemnly awarded by Director General Mme Paule Assoumou Koki for exceptional operational integrity, incident reporting rigor, and 100\% compliance in civil aviation security operations.
    }}
    }}

\end{minipage}

\end{document}
'''
    return tex

# Test compiling the English CV with increased fonts
tex_content = build_en_cv()
with open(os.path.join(p_dir, 'test_tuned_en.tex'), 'w', encoding='utf-8') as f:
    f.write(tex_content)

for i in range(2):
    res = subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'test_tuned_en.tex'], cwd=p_dir, capture_output=True, text=True)

reader = pypdf.PdfReader(os.path.join(p_dir, 'test_tuned_en.pdf'))
print('Tuned EN CV page count:', len(reader.pages))

pdf = pdfium.PdfDocument(os.path.join(p_dir, 'test_tuned_en.pdf'))
img = pdf[0].render(scale=2).to_pil()
img.save(os.path.join(p_dir, 'test_tuned_en.png'))
print('Saved test_tuned_en.png')
