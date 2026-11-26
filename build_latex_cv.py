"""Generate and compile premium LaTeX presentation CVs (FR & EN) from profile.json.
Uses pdflatex + lmodern + microtype for vector typography and 100% faithful UTF-8 text extraction.
"""
from pathlib import Path
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
PDFLATEX = Path(r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe')
PDFTOPPM = Path(r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdftoppm.exe')


def tex_escape(text: str) -> str:
    """Escape plain text for pdfLaTeX while preserving UTF-8 accents and typography."""
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
        ('–', r'--'),
        ('—', r'---'),
        ('·', r'\textperiodcentered{}'),
    ]
    out = str(text)
    for src, dst in replacements:
        out = out.replace(src, dst)
    return out


TEMPLATE = r"""\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[a4paper,margin=9.5mm,top=7mm,bottom=7mm]{geometry}
\usepackage{xcolor}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{tcolorbox}
\tcbuselibrary{skins}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}

% ── Palette Premium : Bleu Glacier, Bleu Nuit, Teal & Or Discret ──
\definecolor{marginBlue}{HTML}{DCE9F5}     % Marges extérieures bleu clair
\definecolor{marginBorder}{HTML}{B5CBE0}   % Filet architectural extérieur
\definecolor{headerBg}{HTML}{EDF4FA}       % En-tête bleu glacier doux
\definecolor{headerBorder}{HTML}{C5D7E8}   % Séparateur en-tête
\definecolor{sidebarBg}{HTML}{F2F6FA}      % Colonne latérale ardoise claire
\definecolor{sidebarLine}{HTML}{D4E1ED}    % Ligne séparatrice colonne
\definecolor{primaryDark}{HTML}{0F2438}    % Bleu nuit profond
\definecolor{sectionNavy}{HTML}{1A3F63}    % Bleu Oxford structurant
\definecolor{accentTeal}{HTML}{0F6B63}     % Teal éditorial (cohérent portfolio)
\definecolor{bodyText}{HTML}{1E293B}       % Texte ardoise foncé lisible
\definecolor{mutedSlate}{HTML}{52606D}     % Métadonnées et contextes
\definecolor{subtleRule}{HTML}{CBD8E4}     % Filets fins de projet
\definecolor{goldAccent}{HTML}{9A5B13}     % Ambre doré pour distinction

\newcommand{\editorialfont}{\fontfamily{lmr}\selectfont\itshape}

\hypersetup{
  pdfauthor={<<AUTHOR>>},
  pdftitle={<<PDF_TITLE>>}
}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\hyphenpenalty=10000
\exhyphenpenalty=10000

\newcommand{\mainSecTitle}[1]{%
  \vspace{11pt}%
  {\fontsize{11.0}{13.0}\selectfont\textbf{\color{sectionNavy}\MakeUppercase{#1}}}\\[2.5pt]%
  {\color{accentTeal}\rule{19mm}{1.2pt}\color{subtleRule}\rule{\dimexpr\linewidth-19mm\relax}{0.6pt}}\\[6pt]%
}

\newcommand{\sideSecTitle}[1]{%
  \vspace{11pt}%
  {\fontsize{10.3}{12.4}\selectfont\textbf{\color{sectionNavy}\MakeUppercase{#1}}}\\[2.5pt]%
  {\color{accentTeal}\rule{14mm}{1.1pt}\color{subtleRule}\rule{\dimexpr\linewidth-14mm\relax}{0.55pt}}\\[5.5pt]%
}

\newcommand{\devbadge}{%
  \tikz[baseline=-0.6pt]{\node[draw=accentTeal,fill=white,rounded corners=1.2pt,inner xsep=1.5pt,inner ysep=0.8pt,font=\fontsize{4.9}{5.2}\selectfont\bfseries\color{accentTeal}]{DEV};}%
}

\begin{document}

% ── FOND BLEU CLAIR DANS LES MARGES + FEUILLE BLANCHE + SIDEBAR PLEINE HAUTEUR ──
\begin{tikzpicture}[remember picture, overlay]
  \fill[marginBlue] (current page.south west) rectangle (current page.north east);
  \fill[white] ([xshift=4.8mm,yshift=4.8mm]current page.south west) rectangle ([xshift=-4.8mm,yshift=-4.8mm]current page.north east);
  \fill[sidebarBg] ([xshift=4.8mm,yshift=4.8mm]current page.south west) rectangle ([xshift=72.2mm,yshift=-43.0mm]current page.north west);
  \draw[sidebarLine, line width=0.6pt] ([xshift=72.2mm,yshift=4.8mm]current page.south west) -- ([xshift=72.2mm,yshift=-43.0mm]current page.north west);
  \fill[headerBg] ([xshift=4.8mm,yshift=-43.0mm]current page.north west) rectangle ([xshift=-4.8mm,yshift=-4.8mm]current page.north east);
  \draw[headerBorder, line width=0.7pt] ([xshift=4.8mm,yshift=-43.0mm]current page.north west) -- ([xshift=-4.8mm,yshift=-43.0mm]current page.north east);
  \fill[primaryDark] ([xshift=4.8mm,yshift=-4.8mm]current page.north west) rectangle ([xshift=-65mm,yshift=-6.4mm]current page.north east);
  \fill[accentTeal] ([xshift=-65mm,yshift=-4.8mm]current page.north east) rectangle ([xshift=-4.8mm,yshift=-6.4mm]current page.north east);
  \draw[marginBorder, line width=0.8pt] ([xshift=4.8mm,yshift=4.8mm]current page.south west) rectangle ([xshift=-4.8mm,yshift=-4.8mm]current page.north east);
\end{tikzpicture}

% ── EN-TÊTE STRUCTURÉ : PORTRAIT + IDENTITÉ + COORDONNÉES ALIGNÉES ──
\vspace*{0.8mm}
\noindent\begin{minipage}[c]{0.135\textwidth}
  \centering
  \begin{tikzpicture}
    \clip (0,0) circle (1.16cm);
    \node at (0,0) {\includegraphics[width=2.34cm]{profile_headshot_clean.png}};
    \draw[white, line width=1.8pt] (0,0) circle (1.15cm);
    \draw[headerBorder, line width=0.9pt] (0,0) circle (1.16cm);
  \end{tikzpicture}
\end{minipage}%
\hspace{0.022\textwidth}%
\begin{minipage}[c]{0.843\textwidth}
  \raggedright
  {\fontsize{18.0}{20.2}\selectfont\textbf{\color{primaryDark}<<FAMILY_NAME>>}\hspace{6pt}{\fontsize{16.5}{20.2}\selectfont\color{sectionNavy}<<GIVEN_NAMES>>}}\\[2.5pt]
  {\fontsize{10.9}{13.0}\selectfont\textbf{\color{sectionNavy}<<TITLE>>}}%
  \hspace{5pt}{\color{mutedSlate}\textbar}\hspace{5pt}%
  {\editorialfont\fontsize{10.1}{12.5}\selectfont\color{accentTeal}<<SUBTITLE>>}\\[4.5pt]
  {\fontsize{8.4}{10.5}\selectfont\color{bodyText}
  \raisebox{-1.0pt}{\includegraphics[height=7.0pt]{icons/icon_location.png}}\hspace{3pt}<<LOCATION>>%
  \quad{\color{marginBorder}\textbar}\quad
  \raisebox{-1.0pt}{\includegraphics[height=6.8pt]{icons/icon_phone.png}}\hspace{3pt}\href{<<PHONE_HREF>>}{\color{bodyText}<<PHONE>>}%
  \quad{\color{marginBorder}\textbar}\quad
  \raisebox{-1.0pt}{\includegraphics[height=6.7pt]{icons/icon_email.png}}\hspace{3pt}\href{mailto:<<EMAIL_RAW>>}{\textbf{\color{primaryDark}<<EMAIL>>}}
  }\\[3.2pt]
  {\color{headerBorder}\rule{\linewidth}{0.5pt}}\\[3.5pt]
  {\fontsize{8.3}{10.5}\selectfont
  \begin{tabular}{@{}p{0.50\linewidth}p{0.46\linewidth}@{}}
    \raisebox{-1.0pt}{\includegraphics[height=6.9pt]{icons/icon_globe.png}}\hspace{3pt}\href{<<WEBSITE_URL>>}{\textbf{\color{primaryDark}<<WEBSITE_LABEL>>}} &
    \raisebox{-1.0pt}{\includegraphics[height=6.9pt]{icons/icon_github.png}}\hspace{3pt}\href{<<GITHUB_URL>>}{\color{bodyText}<<GITHUB_LABEL>>} \\[2.2pt]
    \raisebox{-1.0pt}{\includegraphics[height=6.9pt]{icons/icon_linkedin.png}}\hspace{3pt}\href{<<LINKEDIN_URL>>}{\color{bodyText}<<LINKEDIN_LABEL>>} &
    \devbadge\hspace{3pt}\href{<<DEVTO_URL>>}{\color{bodyText}<<DEVTO_LABEL>>}
  \end{tabular}}
\end{minipage}

\vspace{7.5mm}

% ── DEUX COLONNES : SIDEBAR GAUCHE (31%) & CORPS PRINCIPAL DROIT (69%) ──
\noindent\begin{minipage}[t]{0.310\textwidth}
  \raggedright
  \vspace{0pt}
  \sideSecTitle{<<LABEL_SKILLS>>}
<<SKILLS_TEX>>

  \vspace{6pt}
  \sideSecTitle{<<LABEL_EDUCATION>>}
<<EDU_TEX>>

  \vspace{6pt}
  \sideSecTitle{<<LABEL_LANGUAGES>>}
  {\fontsize{9.6}{13.1}\selectfont\color{bodyText}<<LANGUAGES>>}

  \vspace{6pt}
  \sideSecTitle{<<LABEL_AWARD>>}
  {\fontsize{9.6}{13.1}\selectfont\color{bodyText}\textcolor{goldAccent}{$\bigstar$}\ <<AWARD>>}
\end{minipage}%
\hspace{0.042\textwidth}%
\begin{minipage}[t]{0.648\textwidth}
  \raggedright
  \vspace{0pt}
  \mainSecTitle{<<PROFILE_HEADING>>}
  \begin{tcolorbox}[enhanced, frame hidden, colback=sidebarBg,
    borderline west={2.2pt}{0pt}{accentTeal},
    left=8pt, right=7pt, top=7pt, bottom=7pt, boxsep=0pt, arc=1.5pt]
    \raggedright
    {\fontsize{10.0}{13.8}\selectfont\color{bodyText}<<SUMMARY>>}
  \end{tcolorbox}

  \vspace{3pt}
  \mainSecTitle{<<LABEL_PROJECTS>>}
<<PROJECTS_TEX>>

  \vspace{3pt}
  \mainSecTitle{<<LABEL_EXPERIENCE>>}
<<EXP_TEX>>
\end{minipage}

\end{document}
"""


def build_tex(profile: dict, lang: str) -> str:
    """Render a 1-page A4 premium LaTeX document for the given language."""
    identity = profile['identity']
    data = profile['cv'][lang]

    skills_blocks = []
    for item in data['skills']:
        skills_blocks.append(
            "  \\textbf{\\color{sectionNavy}\\fontsize{10.0}{12.2}\\selectfont "
            + tex_escape(item['label'])
            + "}\\\\[2.2pt]\n  {\\fontsize{9.6}{13.0}\\selectfont\\color{bodyText}"
            + tex_escape(item['text'])
            + "}"
        )

    edu_blocks = []
    for entry in data['education']:
        details = ' '.join(tex_escape(d) for d in entry['details'])
        edu_blocks.append(
            "  \\textbf{\\color{primaryDark}\\fontsize{9.9}{12.5}\\selectfont "
            + tex_escape(entry['title'])
            + "}\\\\[1.8pt]\n  {\\fontsize{8.9}{11.2}\\selectfont\\color{mutedSlate}"
            + tex_escape(entry['date'])
            + "}\\\\[2.5pt]\n  {\\fontsize{9.5}{12.9}\\selectfont\\color{bodyText}"
            + details + "}"
        )

    project_blocks = []
    for idx, proj in enumerate(data['projects'], start=1):
        bar_color = 'accentTeal' if idx == 1 else 'subtleRule'
        bar_width = '1.8pt' if idx == 1 else '1.0pt'
        bullets = '\n'.join(
            "    \\item {\\fontsize{9.9}{13.5}\\selectfont\\color{bodyText}" + tex_escape(d) + "}"
            for d in proj['details']
        )
        project_blocks.append(
            f"""  \\begin{{tcolorbox}}[enhanced, frame hidden, interior hidden,
    borderline west={{{bar_width}}}{{0pt}}{{{bar_color}}},
    left=8pt, right=0pt, top=1.5pt, bottom=1.5pt, boxsep=0pt]
    \\raggedright
    {{\\fontsize{{11.2}}{{13.4}}\\selectfont\\textbf{{\\color{{primaryDark}}{tex_escape(proj['title'])}}}}}\\\\[2pt]
    {{\\fontsize{{9.1}}{{12.1}}\\selectfont\\color{{mutedSlate}}{tex_escape(proj['context'])}}}\\\\[3pt]
    \\begin{{itemize}}[leftmargin=10pt,label={{\\color{{accentTeal}}\\tiny$\\blacksquare$}},itemsep=3.2pt,topsep=1.5pt,parsep=0pt]
{bullets}
    \\end{{itemize}}
  \\end{{tcolorbox}}"""
        )

    exp_blocks = []
    for exp in data['experience']:
        details = '\n'.join(
            "  {\\fontsize{9.8}{13.4}\\selectfont\\color{bodyText}" + tex_escape(d) + "}"
            for d in exp['details']
        )
        exp_blocks.append(
            f"""  \\noindent\\begin{{tabular*}}{{\\linewidth}}{{@{{}}p{{0.76\\linewidth}}@{{\\extracolsep{{\\fill}}}}r@{{}}}}
    \\textbf{{\\color{{primaryDark}}\\fontsize{{10.4}}{{12.8}}\\selectfont {tex_escape(exp['title'])}}} &
    {{\\fontsize{{8.9}}{{11.0}}\\selectfont\\color{{mutedSlate}}{tex_escape(exp['date'])}}}
  \\end{{tabular*}}\\\\[2.5pt]
{details}"""
        )

    replacements = {
        '<<AUTHOR>>': tex_escape(identity['name']),
        '<<PDF_TITLE>>': tex_escape(identity['name'] + ' | ' + data['title']),
        '<<FAMILY_NAME>>': tex_escape(identity['familyName']),
        '<<GIVEN_NAMES>>': tex_escape(identity['givenNames']),
        '<<TITLE>>': tex_escape(data['title']),
        '<<SUBTITLE>>': tex_escape(data.get('subtitle', '')),
        '<<LOCATION>>': tex_escape(identity['location'][lang]),
        '<<PHONE_HREF>>': identity['phoneHref'],
        '<<PHONE>>': tex_escape(identity['phone']),
        '<<EMAIL_RAW>>': identity['email'],
        '<<EMAIL>>': tex_escape(identity['email']),
        '<<WEBSITE_URL>>': identity['website'],
        '<<WEBSITE_LABEL>>': tex_escape(identity['website'].removeprefix('https://')),
        '<<GITHUB_URL>>': identity['github'],
        '<<GITHUB_LABEL>>': tex_escape(identity['github'].removeprefix('https://')),
        '<<LINKEDIN_URL>>': identity['linkedin'],
        '<<LINKEDIN_LABEL>>': tex_escape(identity['linkedin'].removeprefix('https://')),
        '<<DEVTO_URL>>': identity['devto'],
        '<<DEVTO_LABEL>>': tex_escape(identity['devto'].removeprefix('https://')),
        '<<LABEL_SKILLS>>': tex_escape(data['labels']['skills']),
        '<<SKILLS_TEX>>': '\n\\vspace{10pt}\n\n'.join(skills_blocks),
        '<<LABEL_EDUCATION>>': tex_escape(data['labels']['education']),
        '<<EDU_TEX>>': '\n\\vspace{11pt}\n\n'.join(edu_blocks),
        '<<LABEL_LANGUAGES>>': tex_escape(data['labels']['additional']),
        '<<LANGUAGES>>': tex_escape(data['languages']),
        '<<LABEL_AWARD>>': tex_escape(data['labels']['award']),
        '<<AWARD>>': tex_escape(data['award']),
        '<<PROFILE_HEADING>>': 'PROFIL' if lang == 'fr' else 'PROFILE',
        '<<SUMMARY>>': tex_escape(data['summary']),
        '<<LABEL_PROJECTS>>': tex_escape(data['labels']['projects']),
        '<<PROJECTS_TEX>>': '\n\\vspace{10pt}\n'.join(project_blocks),
        '<<LABEL_EXPERIENCE>>': tex_escape(data['labels']['experience']),
        '<<EXP_TEX>>': '\n\\vspace{10pt}\n\n'.join(exp_blocks),
    }
    doc = TEMPLATE
    for key, val in replacements.items():
        doc = doc.replace(key, val)
    return doc


def compile_tex(tex_path: Path) -> None:
    cmd = [str(PDFLATEX), '--disable-installer', '-interaction=nonstopmode', '-halt-on-error', tex_path.name]
    for _ in range(2):
        res = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            stdin=subprocess.DEVNULL,
        )
        if res.returncode != 0:
            tail = '\n'.join(res.stdout.splitlines()[-40:])
            raise RuntimeError(f'pdfLaTeX failed for {tex_path.name}:\n{tail}')


def render_preview(pdf_path: Path, prefix: str) -> None:
    subprocess.run(
        [str(PDFTOPPM), '-png', '-r', '150', pdf_path.name, prefix],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def main() -> None:
    profile = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
    for lang in ('fr', 'en'):
        pdf_name = profile['cv'][lang]['files']['pdf']
        tex_path = ROOT / pdf_name.replace('.pdf', '.tex')
        tex_path.write_text(build_tex(profile, lang), encoding='utf-8')
        compile_tex(tex_path)
        pdf_path = ROOT / pdf_name
        render_preview(pdf_path, f'cv_{lang}_preview')
        if lang == 'fr':
            shutil.copyfile(pdf_path, ROOT / 'KOA_MARIE_GERVAIS_NELLY_CV FR.pdf')
        print(f'Built {pdf_name} via pdfLaTeX')


if __name__ == '__main__':
    main()
