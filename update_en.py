import re

with open(r'c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's adjust KOA_MARIE_GERVAIS_NELLY_CV_EN.tex
# 1. Update sideSecTitle spacing and font
text = re.sub(
    r'\\newcommand\{\\sideSecTitle\}\[1\]\{.*?\n\}',
    r'''\\newcommand{\\sideSecTitle}[1]{%
    \\vspace{5.0pt}%
    {\\fontsize{9.4}{12.0}\\selectfont\\textbf{\\color{sectionNavy}#1}}\\\\[1.8pt]%
    {\\color{sectionNavy}\\hrule height 0.65pt}\\vspace{4.5pt}%
}''',
    text,
    flags=re.DOTALL
)

# 2. Adjust sidebar itemsep and inter-section vspaces
text = text.replace('itemsep=4.8pt', 'itemsep=5.8pt')
text = text.replace('itemsep=4.5pt', 'itemsep=5.5pt')
text = text.replace('\\vspace{10.0pt}', '\\vspace{13.5pt}')

# 3. Ensure ASU title is complete:
text = text.replace(
    'ASU (Airport Security Unit) Audit-Ready --- Inspection Simulator',
    'ASU (Airport Security Unit) Audit-Ready --- Compliance \\& Inspection Simulator'
)

# 4. Enlarge titles on right column slightly
text = text.replace(
    r'{\fontsize{9.5}{11.8}\selectfont\textbf{\color{primaryDark}Operational Security Supervisor (Shift Lead AVSEC)}} \hfill {\fontsize{8.0}{9.8}\selectfont\color{mutedSlate}Jan. 2025 -- Present}\\[1.0pt]',
    r'{\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}Operational Security Supervisor (Shift Lead AVSEC)}} \hfill {\fontsize{8.2}{10.0}\selectfont\color{mutedSlate}Jan. 2025 -- Present}\\[1.2pt]'
)
text = text.replace(
    r'{\fontsize{8.5}{10.4}\selectfont\textit{\color{sectionNavy}Cameroon Civil Aviation Authority (CCAA) $|$ Ngaoundéré Airport (DOS)}}\\[1.2pt]',
    r'{\fontsize{8.6}{10.8}\selectfont\textit{\color{sectionNavy}Cameroon Civil Aviation Authority (CCAA) $|$ Ngaoundéré Airport (DOS)}}\\[1.5pt]'
)
text = text.replace(
    r'{\fontsize{9.5}{11.8}\selectfont\textbf{\color{primaryDark}Aviation Security Agent \& Shift Supervisor}} \hfill {\fontsize{8.0}{9.8}\selectfont\color{mutedSlate}2018 -- Jan. 2025}\\[1.0pt]',
    r'{\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}Aviation Security Agent \& Shift Supervisor}} \hfill {\fontsize{8.2}{10.0}\selectfont\color{mutedSlate}2018 -- Jan. 2025}\\[1.2pt]'
)
text = text.replace(
    r'{\fontsize{8.5}{10.4}\selectfont\textit{\color{sectionNavy}Cameroon Civil Aviation Authority (CCAA) $|$ Yaoundé-Nsimalen Int. Airport}}\\[1.2pt]',
    r'{\fontsize{8.6}{10.8}\selectfont\textit{\color{sectionNavy}Cameroon Civil Aviation Authority (CCAA) $|$ Yaoundé-Nsimalen Int. Airport}}\\[1.5pt]'
)

# For project titles
text = text.replace(
    r'{\fontsize{9.5}{11.8}\selectfont\textbf{\color{primaryDark}ASU (Airport Security Unit) Audit-Ready --- Compliance \& Inspection Simulator}}\\[1.0pt]',
    r'{\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}ASU (Airport Security Unit) Audit-Ready --- Compliance \& Inspection Simulator}}\\[1.2pt]'
)
text = text.replace(
    r'{\fontsize{9.5}{11.8}\selectfont\textbf{\color{primaryDark}Dataset Automator --- Agentic Pipeline with Deterministic Rules}}\\[1.0pt]',
    r'{\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}Dataset Automator --- Agentic Pipeline with Deterministic Rules}}\\[1.2pt]'
)
text = text.replace(
    r'{\fontsize{9.5}{11.8}\selectfont\textbf{\color{primaryDark}K1-MathInfo --- Hybrid Retrieval Engine with Epistemic Abstention}}\\[1.0pt]',
    r'{\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}K1-MathInfo --- Hybrid Retrieval Engine with Epistemic Abstention}}\\[1.2pt]'
)
text = text.replace(
    r'{\fontsize{9.5}{11.8}\selectfont\textbf{\color{primaryDark}Archi Cam AI --- Computational Intelligence for Construction}}\\[1.0pt]',
    r'{\fontsize{9.6}{12.0}\selectfont\textbf{\color{primaryDark}Archi Cam AI --- Computational Intelligence for Construction}}\\[1.2pt]'
)

with open(r'c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated KOA_MARIE_GERVAIS_NELLY_CV_EN.tex successfully.")
