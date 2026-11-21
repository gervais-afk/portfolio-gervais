surete_cv = r'''\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[margin=0.34in,top=0.20in,bottom=0.20in]{geometry}
\usepackage{xcolor}
\usepackage{amssymb}
\usepackage{tikz}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{tabularx}
\usepackage{enumitem}

% ── Palette Harmonieuse & Sobre (Style Exécutif / Aéronautique) ──
\definecolor{primaryDark}{HTML}{0F172A}    % Ardoise sombre 900
\definecolor{sectionNavy}{HTML}{1E3A5F}    % Bleu marine profond
\definecolor{subheading}{HTML}{334155}     % Ardoise 700
\definecolor{bodyText}{HTML}{1E293B}       % Corps de texte lisible
\definecolor{mutedSlate}{HTML}{64748B}     % Gris moyen (dates / métadonnées)
\definecolor{accentGold}{HTML}{92400E}     % Ambre doré prestigieux
\definecolor{tintGold}{HTML}{FEF3C7}       % Fond or chaud très doux
\definecolor{subtleRule}{HTML}{CBD5E1}     % Filet discret
\definecolor{sidebarBg}{HTML}{F0F4F8}      % Fond colonne gauche ardoise bleutée
\definecolor{marginBlue}{HTML}{E2EDF8}     % Bleu clair dilué pour les 4 marges
\definecolor{marginBorder}{HTML}{BFD5EC}   % Filet intérieur délicat
\definecolor{headerBg}{HTML}{E8EFF7}       % Fond bleu cassé élégant et doux
\definecolor{headerBorder}{HTML}{CBDCEB}   % Liseré discret

\hypersetup{
    colorlinks=true,
    linkcolor=sectionNavy,
    urlcolor=sectionNavy,
    pdfauthor={KOA Marie Gervais Nelly},
    pdftitle={CV Sûreté Aéroportuaire - KOA Marie Gervais Nelly}
}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\linespread{1.01}

% ── Commandes de Titres ──
\newcommand{\secTitle}[1]{%
    \vspace{2.5pt}%
    {\fontsize{9.3}{11.4}\selectfont\textbf{\color{sectionNavy}#1}}\\[1.4pt]%
    {\color{sectionNavy}\hrule height 0.65pt}\vspace{2.6pt}%
}

\newcommand{\sideSecTitle}[1]{%
    \vspace{5.5pt}%
    {\fontsize{9.4}{12.0}\selectfont\textbf{\color{sectionNavy}#1}}\\[1.8pt]%
    {\color{sectionNavy}\hrule height 0.65pt}\vspace{4.5pt}%
}

\setlist[itemize]{leftmargin=*,labelsep=3.5pt,itemsep=1.0pt,topsep=0.4pt,parsep=0pt}
\newcommand{\bulletItem}[2]{%
    \item \textbf{\color{primaryDark}#1} {\fontsize{8.2}{9.9}\selectfont\color{bodyText}#2}%
}

\begin{document}

% ══════════════════════════════════════════════════════════════════
% CADRE 4 MARGES & BANDE LATÉRALE GAUCHE PLEINE HAUTEUR (TIKZ)
% ══════════════════════════════════════════════════════════════════
\begin{tikzpicture}[remember picture, overlay]
    % 1. Teinte des 4 marges extérieures :
    \fill[marginBlue] (current page.south west) rectangle (current page.north east);
    % 2. Conteneur intérieur blanc net :
    \fill[white] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
    % 3. BANDE ARDOISE BLEUTÉE QUI DESCEND JUSQU'AU TOUT BAS DE LA PAGE :
    \fill[sidebarBg] ([xshift=4.5mm, yshift=4.5mm]current page.south west) rectangle ([xshift=73.5mm, yshift=-31.5mm]current page.north west);
    % 4. Filet intérieur de finition :
    \draw[marginBorder, line width=0.75pt] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
\end{tikzpicture}

% ══════════════════════════════════════════════════════════════════
% EN-TÊTE ÉLÉGANT : FOND BLEU CASSÉ, PORTRAIT OFFICIEL & VRAIES ICÔNES
% ══════════════════════════════════════════════════════════════════
\setlength{\fboxsep}{3.2pt}%
\noindent\fcolorbox{headerBorder}{headerBg}{%
\begin{minipage}{\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax}
    % Photo officielle en médaillon circulaire
    \begin{minipage}[c]{0.145\textwidth}
        \centering
        \begin{tikzpicture}
            \clip (0,0) circle (1.08cm);
            \node at (0,0) {\includegraphics[width=2.16cm]{profile_headshot_clean.png}};
            \draw[headerBorder, line width=1.1pt] (0,0) circle (1.08cm);
        \end{tikzpicture}
    \end{minipage}%
    \hspace{0.015\textwidth}%
    % Nom, Titre & Coordonnées
    \begin{minipage}[c]{0.540\textwidth}
        {\fontsize{16.8}{19.2}\selectfont\textbf{\color{primaryDark} KOA MARIE GERVAIS NELLY}}\\[1.8pt]
        {\fontsize{9.1}{11.1}\selectfont\textbf{\color{sectionNavy} Agent Op\'erationnel de S\^uret\'e A\'eroportuaire (AVSEC) $\cdot$ Chef de Groupe}}\\[2.8pt]
        {\fontsize{7.7}{9.6}\selectfont
        \raisebox{-0.8pt}{\includegraphics[height=6.8pt]{icons/icon_location.png}}\hspace{2.0pt}{\color{bodyText}Ngaound\'er\'e / Douala, CM}
        \quad{\color{mutedSlate}$|$}\quad
        \raisebox{-0.8pt}{\includegraphics[height=6.5pt]{icons/icon_phone.png}}\hspace{2.0pt}{\color{bodyText}+237 695 35 34 02}\\[1.5pt]
        \raisebox{-0.8pt}{\includegraphics[height=6.5pt]{icons/icon_email.png}}\hspace{2.0pt}\href{mailto:contact@archicam-ai.com}{\color{primaryDark}\textbf{contact@archicam-ai.com}}
        }
    \end{minipage}%
    \hfill
    % Liens professionnels
    \begin{minipage}[c]{0.29\textwidth}
        \raggedleft
        {\fontsize{7.7}{9.6}\selectfont
        \raisebox{-0.8pt}{\includegraphics[height=6.7pt]{icons/icon_globe.png}}\hspace{2.0pt}\href{https://portfolio-gervais.vercel.app}{\textbf{\color{primaryDark}portfolio-gervais.vercel.app}}\\[1.8pt]
        \raisebox{-0.8pt}{\includegraphics[height=6.7pt]{icons/icon_github.png}}\hspace{2.0pt}\href{https://github.com/gervais-afk}{\color{bodyText}github.com/gervais-afk}\\[1.8pt]
        \raisebox{-0.8pt}{\includegraphics[height=6.7pt]{icons/icon_linkedin.png}}\hspace{2.0pt}\href{https://linkedin.com/in/marie-gervais-koa}{\color{bodyText}linkedin.com/in/marie-gervais-koa}
        }
    \end{minipage}
\end{minipage}%
}

\vspace{1.5pt}

% ══════════════════════════════════════════════════════════════════
% DEUX COLONNES VERTICALES (POLICE AGRANDIE & ÉQUILIBRÉE)
% ══════════════════════════════════════════════════════════════════
\begin{minipage}[t]{0.325\textwidth}
\vspace{0.5pt}%

    % ── CADRE RÉGLEMENTAIRE OACI ──
    \sideSecTitle{CADRE RÉGLEMENTAIRE OACI}
    {\fontsize{8.5}{11.2}\selectfont
    \begin{itemize}[leftmargin=7pt,label={\color{sectionNavy}\scriptsize$\blacktriangleright$},itemsep=5.8pt]
        \item \textbf{OACI Annexe 17 :} Normes internationales de sûreté de l'aviation civile.
        \item \textbf{Manuel OACI Doc 8973 :} Procédures de sûreté aéroportuaire.
        \item \textbf{Programme National (PNSAC) :} Application et conformité CCAA.
        \item \textbf{Habilitation ZSAR Active :} Accès permanent zone réservée.
        \item \textbf{Protocoles d'Urgence :} Plans anti-intrusion et crise aéronautique.
    \end{itemize}
    }

    \vspace{14.5pt}

    % ── COMPÉTENCES SÛRETÉ ──
    \sideSecTitle{COMPÉTENCES SÛRETÉ}
    {\fontsize{8.45}{11.0}\selectfont
    \begin{itemize}[leftmargin=7pt,label={\color{sectionNavy}\scriptsize$\blacktriangleright$},itemsep=4.8pt]
        \item \textbf{Inspection-filtrage (PIF) :} Passagers, cabine, palpations.
        \item \textbf{Imagerie Rayons X :} Détection d'objets prohibés et armes.
        \item \textbf{Contrôle d'accès ZSAR :} Vérification badges et macarons.
        \item \textbf{Tests d'équipements :} Étalonnage portiques et magnétomètres.
        \item \textbf{Commandement de quart :} Relèves, briefings, discipline.
        \item \textbf{Rapports sous 24h :} Traçabilité et comptes rendus d'incidents.
    \end{itemize}
    }

    \vspace{14.5pt}

    % ── FORMATION ACADÉMIQUE ──
    \sideSecTitle{FORMATIONS ACADÉMIQUES}
    {\fontsize{8.45}{11.0}\selectfont
    \textbf{\color{primaryDark}Master Pro en IA Appliquée}\\[1.4pt]
    {\color{sectionNavy}\textit{Univ. de Ngaoundéré (DMI)}} \hfill {\fontsize{8.0}{9.5}\selectfont\color{mutedSlate}2025--2027}\\[2.0pt]
    {\fontsize{7.85}{10.3}\selectfont\textbf{\color{accentGold}En cours} \ -- \ \color{bodyText}Modélisation des risques, imagerie RX assistée et digitalisation des audits OACI.}\\[7.5pt]
    \textbf{\color{primaryDark}Licence \& BTS Génie Civil}\\[1.4pt]
    {\color{sectionNavy}\textit{IUC Douala (Institut Univ. de la Côte)}} \hfill {\fontsize{8.0}{9.5}\selectfont\color{mutedSlate}2015--2016}\\[2.0pt]
    {\fontsize{7.85}{10.3}\selectfont\color{bodyText}Option Bâtiment. Rigueur métrologique et modélisation physique du risque matériel.}
    }

    \vspace{14.5pt}

    % ── HABILITATIONS CCAA ──
    \sideSecTitle{HABILITATIONS CCAA}
    {\fontsize{8.45}{11.2}\selectfont
    \textbf{Certifié AVSEC Agent \& Chef de Groupe}\\[2.0pt]
    {\color{bodyText}Modules : imagerie RX, fouilles, gestion de crise, Annexe 17 OACI.}
    }

    \vspace{14.5pt}

    % ── LANGUES ──
    \sideSecTitle{LANGUES}
    {\fontsize{8.5}{11.4}\selectfont\raggedright
    \textbf{Français :} Langue maternelle / Courant.\par\vspace{5.0pt}
    \textbf{Anglais :} Opérationnel Aéronautique.\par
    }

\end{minipage}%
\hfill
\begin{minipage}[t]{0.650\textwidth}
\vspace{0.5pt}%

    % ── PROFIL PROFESSIONNEL ──
    \secTitle{PROFIL PROFESSIONNEL}
    {\fontsize{8.2}{10.2}\selectfont\color{bodyText}
    Agent Opérationnel de Sûreté Aéroportuaire certifié et Chef de Groupe au sein de l'Autorité Aéronautique du Cameroun (CCAA), cumulant plus de 8 années d'exercice continu sur les plateformes de Yaoundé-Nsimalen et de Ngaoundéré. Spécialiste de l'inspection-filtrage, de l'analyse radioscopique aux rayons X, de la sécurisation des zones réservées (ZSAR) et du commandement de quart. Concepteur de la solution \textit{ASU (Airport Security Unit) Audit-Ready} pour la préparation aux audits internationaux de l'OACI. Lauréat du Prix du Meilleur Agent décerné par la Direction Générale pour rigueur opérationnelle et intégrité.
    }

    % ── PARCOURS OPÉRATIONNEL ──
    \secTitle{PARCOURS OPÉRATIONNEL \& COMMANDEMENT DE QUART}
    
    {\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}Chef de Groupe --- Antenne de Sûreté de l'Unité (ASU)}} \hfill {\fontsize{8.2}{10.0}\selectfont\color{mutedSlate}Janvier 2025 -- Présent}\\[1.2pt]
    {\fontsize{8.6}{10.8}\selectfont\textit{\color{sectionNavy}Aéroport de Ngaoundéré $|$ CCAA --- Division Opérationnelle de Sûreté (DOS)}}\\[1.5pt]
    \begin{itemize}
        \bulletItem{Commandement de Quart \& Relèves :}{Conduite opérationnelle des équipes de sûreté, contrôle des prises de service, respect de la tenue réglementaire et respect à 100\% des normes OACI Annexe 17.}
        \bulletItem{Contrôle des Accès \& Surveillance ZSAR :}{Sécurisation stricte de la zone réservée (vérification badges et macarons véhicules), surveillance tarmac et patrouilles périmétriques anti-intrusion.}
        \bulletItem{Contrôle Quotidien des Équipements :}{Réalisation systématique des tests d'étalonnage des portiques de détection et appareils rayons X double vue avec zéro interruption de service.}
    \end{itemize}
    \vspace{4.0pt}
    {\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}Agent Opérationnel de Sûreté \& Chef de Groupe AVSEC}} \hfill {\fontsize{8.2}{10.0}\selectfont\color{mutedSlate}2018 -- Janvier 2025}\\[1.2pt]
    {\fontsize{8.6}{10.8}\selectfont\textit{\color{sectionNavy}Aéroport International de Yaoundé-Nsimalen $|$ CCAA --- Sûreté Opérationnelle}}\\[1.5pt]
    \begin{itemize}
        \bulletItem{Inspection Filtrage des Passagers \& Bagages :}{Contrôle systématique aux portiques magnétomètres, imagerie rayons X bagages cabine, palpations et détection des articles prohibés.}
        \bulletItem{Sûreté Bagages de Soute \& Tri :}{Inspection radioscopique des bagages de soute, contrôle de concordance passager-bagage et gestion rigoureuse des anomalies selon les procédures OACI.}
        \bulletItem{Gestion des Événements \& Traçabilité :}{Rédaction sous 24h des comptes rendus d'incidents, gestion des fiches de suivi des véhicules de patrouille et tenue des registres officiels.}
    \end{itemize}

    % ── INNOVATION SÛRETÉ : ASU AUDIT-READY (1 TIRET PAR RUBRIQUE) ──
    \secTitle{INNOVATION SÛRETÉ \& PRÉPARATION AUX AUDITS OACI}

    {\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}ASU (Airport Security Unit) Audit-Ready --- Préparation aux Audits}}\\[1.2pt]
    {\fontsize{8.6}{10.8}\selectfont\textit{\color{sectionNavy}Conçue pour la Division Opérationnelle de Sûreté (DOS / CCAA)} \hfill {\fontsize{8.2}{10.0}\selectfont\color{mutedSlate}2025 -- Présent}}\\[1.5pt]
    \begin{itemize}
        \bulletItem{Automatisation des Rapports Mensuels :}{Élimination de 40h de travail mensuel en 2s, générant des dossiers d'audit prêts pour signature des inspecteurs multilatéraux OACI.}
    \end{itemize}

    % ── DISTINCTIONS & MENTIONS D'HONNEUR ──
    \secTitle{DISTINCTIONS \& MENTIONS D'HONNEUR}
    {\fontsize{8.5}{10.6}\selectfont
    \textbf{\color{accentGold}$\bigstar$ Prix de l'Excellence \& de l'Intégrité CCAA (28 Avril 2023)} --- \textbf{\color{sectionNavy}Cameroon Civil Aviation Authority (CCAA)}\\[1.2pt]
    {\fontsize{7.9}{9.6}\selectfont\color{bodyText}
    Solennellement décerné par Mme Paule Assoumou Koki, Directeur Général de la CCAA, pour intégrité opérationnelle exemplaire, rigueur de traçabilité des incidents et 100\% de conformité dans les opérations de sûreté.
    }
    }

\end{minipage}

\end{document}
'''

with open(r'c:\Users\HP\Desktop\cv agent de surete aeroportuaire\KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.tex', 'w', encoding='utf-8') as f:
    f.write(surete_cv)

print("Updated KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.tex")
