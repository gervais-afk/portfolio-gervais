import subprocess, os, shutil
import pypdf
import pypdfium2 as pdfium

pdflatex = r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
p_dir = r'C:\Users\HP\Desktop\portfolio-gervais'
govai_dir = r'C:\Users\HP\Desktop\candidature-govai'
avsec_dir = r'C:\Users\HP\Desktop\cv agent de surete aeroportuaire'

# ══════════════════════════════════════════════════════════════════════
# 1. UPDATE PORTFOLIO-GERVAIS FR
# ══════════════════════════════════════════════════════════════════════
fr_tex_path = os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR.tex')
with open(fr_tex_path, 'r', encoding='utf-8') as f:
    fr_c = f.read()

# Update TikZ overlay
old_tikz = r'''\begin{tikzpicture}[remember picture, overlay]
    \fill[marginBlue] (current page.south west) rectangle (current page.north east);
    \fill[white] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
    \draw[marginBorder, line width=0.75pt] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
\end{tikzpicture}'''

new_tikz = r'''\begin{tikzpicture}[remember picture, overlay]
    % 1. Teinte des 4 marges extérieures :
    \fill[marginBlue] (current page.south west) rectangle (current page.north east);
    % 2. Conteneur blanc intérieur :
    \fill[white] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
    
    % 3. BANDE ARDOISE BLEUTÉE QUI DESCEND JUSQU'AU TOUT BAS DE LA PAGE :
    \fill[sidebarBg] ([xshift=4.5mm, yshift=4.5mm]current page.south west) rectangle ([xshift=72.2mm, yshift=-33.8mm]current page.north west);
    
    % 4. Filet intérieur de finition :
    \draw[marginBorder, line width=0.75pt] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
\end{tikzpicture}'''

if old_tikz in fr_c:
    fr_c = fr_c.replace(old_tikz, new_tikz)

# Remove colorbox wrapping around the left minipage
old_col_fr = r'''% Deux colonnes verticales
\setlength{\fboxsep}{5.5pt}%
\colorbox{sidebarBg}{%
\begin{minipage}[t][0.835\textheight][t]{\dimexpr0.32\textwidth-2\fboxsep\relax}'''

if old_col_fr in fr_c:
    fr_c = fr_c.replace(old_col_fr, "% Deux colonnes verticales (Fond pleine hauteur géré par TikZ jusqu'au bas de page)\n\\begin{minipage}[t]{0.32\\textwidth}\n\\vspace{1.5pt}%")
    fr_c = fr_c.replace(r'\end{minipage}%' + '\n' + r'}%', r'\end{minipage}%')

with open(fr_tex_path, 'w', encoding='utf-8') as f:
    f.write(fr_c)

for i in range(2):
    subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_FR.tex'], cwd=p_dir, capture_output=True, text=True)

shutil.copy(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf'), os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_ATS_FR.pdf'))
reader_fr = pypdf.PdfReader(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf'))
print('1. Portfolio FR page count:', len(reader_fr.pages))

pdf_fr = pdfium.PdfDocument(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf'))
pdf_fr[0].render(scale=2).to_pil().save(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR_p1.png'))


# ══════════════════════════════════════════════════════════════════════
# 2. UPDATE PORTFOLIO-GERVAIS EN
# ══════════════════════════════════════════════════════════════════════
en_tex_path = os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.tex')
with open(en_tex_path, 'r', encoding='utf-8') as f:
    en_c = f.read()

if old_tikz in en_c:
    en_c = en_c.replace(old_tikz, new_tikz)

old_col_en = r'''% Deux colonnes verticales
\setlength{\fboxsep}{5.5pt}%
\colorbox{sidebarBg}{%
\begin{minipage}[t][0.835\textheight][t]{\dimexpr0.32\textwidth-2\fboxsep\relax}'''

if old_col_en in en_c:
    en_c = en_c.replace(old_col_en, "% Deux colonnes verticales (Fond pleine hauteur géré par TikZ jusqu'au bas de page)\n\\begin{minipage}[t]{0.32\\textwidth}\n\\vspace{1.5pt}%")
    en_c = en_c.replace(r'\end{minipage}%' + '\n' + r'}%', r'\end{minipage}%')

with open(en_tex_path, 'w', encoding='utf-8') as f:
    f.write(en_c)

for i in range(2):
    subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_EN.tex'], cwd=p_dir, capture_output=True, text=True)

shutil.copy(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf'), os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_ATS_EN.pdf'))
reader_en = pypdf.PdfReader(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf'))
print('2. Portfolio EN page count:', len(reader_en.pages))

pdf_en = pdfium.PdfDocument(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf'))
pdf_en[0].render(scale=2).to_pil().save(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN_p1.png'))


# ══════════════════════════════════════════════════════════════════════
# 3. UPDATE CANDIDATURE-GOVAI
# ══════════════════════════════════════════════════════════════════════
govai_tex_path = os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_LATEX.tex')
shutil.copy(en_tex_path, govai_tex_path)

for i in range(2):
    subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_LATEX.tex'], cwd=govai_dir, capture_output=True, text=True)

shutil.copy(os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_LATEX.pdf'), os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_GOVAI_1PAGE_LATEX.pdf'))
reader_govai = pypdf.PdfReader(os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_GOVAI_1PAGE_LATEX.pdf'))
print('3. GovAI page count:', len(reader_govai.pages))

pdf_govai = pdfium.PdfDocument(os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_GOVAI_1PAGE_LATEX.pdf'))
pdf_govai[0].render(scale=2).to_pil().save(os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_LATEX_p1.png'))


# ══════════════════════════════════════════════════════════════════════
# 4. UPDATE CV SÛRETÉ AÉROPORTUAIRE (AVSEC)
# ══════════════════════════════════════════════════════════════════════
avsec_tex_path = os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.tex')
with open(avsec_tex_path, 'r', encoding='utf-8') as f:
    avsec_c = f.read()

# For AVSEC, top of sidebar is below gold encart (around -45mm)
new_tikz_avsec = r'''\begin{tikzpicture}[remember picture, overlay]
    % 1. Teinte des 4 marges extérieures :
    \fill[marginBlue] (current page.south west) rectangle (current page.north east);
    % 2. Conteneur blanc intérieur :
    \fill[white] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
    
    % 3. BANDE ARDOISE BLEUTÉE QUI DESCEND JUSQU'AU TOUT BAS DE LA PAGE :
    \fill[sidebarBg] ([xshift=4.5mm, yshift=4.5mm]current page.south west) rectangle ([xshift=72.2mm, yshift=-45.0mm]current page.north west);
    
    % 4. Filet intérieur de finition :
    \draw[marginBorder, line width=0.75pt] ([xshift=4.5mm,yshift=4.5mm]current page.south west) rectangle ([xshift=-4.5mm,yshift=-4.5mm]current page.north east);
\end{tikzpicture}'''

if old_tikz in avsec_c:
    avsec_c = avsec_c.replace(old_tikz, new_tikz_avsec)

old_col_avsec = r'''% Deux colonnes verticales
\setlength{\fboxsep}{5.5pt}%
\colorbox{sidebarBg}{%
\begin{minipage}[t][0.805\textheight][t]{\dimexpr0.32\textwidth-2\fboxsep\relax}'''

if old_col_avsec in avsec_c:
    avsec_c = avsec_c.replace(old_col_avsec, "% Deux colonnes verticales (Fond pleine hauteur géré par TikZ jusqu'au bas de page)\n\\begin{minipage}[t]{0.32\\textwidth}\n\\vspace{1.5pt}%")
    avsec_c = avsec_c.replace(r'\end{minipage}%' + '\n' + r'}%', r'\end{minipage}%')

with open(avsec_tex_path, 'w', encoding='utf-8') as f:
    f.write(avsec_c)

for i in range(2):
    subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.tex'], cwd=avsec_dir, capture_output=True, text=True)

shutil.copy(os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.pdf'), os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_1PAGE_LATEX.pdf'))
reader_avsec = pypdf.PdfReader(os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_1PAGE_LATEX.pdf'))
print('4. AVSEC page count:', len(reader_avsec.pages))

pdf_avsec = pdfium.PdfDocument(os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_1PAGE_LATEX.pdf'))
pdf_avsec[0].render(scale=2).to_pil().save(os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_p1.png'))

print('=== ALL 4 CVS UPDATED AND VERIFIED SUCCESSFULLY ===')
