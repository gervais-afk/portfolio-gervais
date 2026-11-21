import subprocess, os, shutil
import pypdf
import pypdfium2 as pdfium

pdflatex = r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
p_dir = r'C:\Users\HP\Desktop\portfolio-gervais'
govai_dir = r'C:\Users\HP\Desktop\candidature-govai'
avsec_dir = r'C:\Users\HP\Desktop\cv agent de surete aeroportuaire'

# 1. COMPILE PORTFOLIO EN
print('1. Compiling Portfolio EN...')
for i in range(2):
    subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_EN.tex'], cwd=p_dir, capture_output=True, text=True)

shutil.copy(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf'), os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_ATS_EN.pdf'))
reader_en = pypdf.PdfReader(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf'))
print('Portfolio EN page count:', len(reader_en.pages))

pdf_en = pdfium.PdfDocument(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf'))
pdf_en[0].render(scale=2).to_pil().save(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN_p1.png'))


# 2. COMPILE PORTFOLIO FR
print('2. Compiling Portfolio FR...')
for i in range(2):
    subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_FR.tex'], cwd=p_dir, capture_output=True, text=True)

shutil.copy(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf'), os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_ATS_FR.pdf'))
reader_fr = pypdf.PdfReader(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf'))
print('Portfolio FR page count:', len(reader_fr.pages))

pdf_fr = pdfium.PdfDocument(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf'))
pdf_fr[0].render(scale=2).to_pil().save(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_FR_p1.png'))


# 3. COMPILE GOVAI (EN)
print('3. Compiling GovAI CV...')
shutil.copy(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.tex'), os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_LATEX.tex'))
for i in range(2):
    subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_LATEX.tex'], cwd=govai_dir, capture_output=True, text=True)

shutil.copy(os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_LATEX.pdf'), os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_GOVAI_1PAGE_LATEX.pdf'))
reader_govai = pypdf.PdfReader(os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_GOVAI_1PAGE_LATEX.pdf'))
print('GovAI page count:', len(reader_govai.pages))

pdf_govai = pdfium.PdfDocument(os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_GOVAI_1PAGE_LATEX.pdf'))
pdf_govai[0].render(scale=2).to_pil().save(os.path.join(govai_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_LATEX_p1.png'))


# 4. UPDATE & COMPILE AVSEC CV
print('4. Compiling AVSEC CV...')
avsec_tex = os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.tex')
with open(avsec_tex, 'r', encoding='utf-8') as f:
    av_c = f.read()

# Update education in AVSEC
av_c = av_c.replace(r'{\color{sectionNavy}\textit{Univ. de Ngaoundéré (DMI)}} \hfill {\color{mutedSlate}2025--2027}\\', r'{\color{sectionNavy}\textit{Univ. de Ngaoundéré (DMI)}} \hfill {\fontsize{7.4}{8.8}\selectfont\color{mutedSlate}2025--2027}\\[0.8pt]\n    {\fontsize{7.3}{8.7}\selectfont\textbf{\color{accentGold}En cours} \ -- \ \color{bodyText}Dept. de Mathématiques et Informatique. Modélisation des risques et audits OACI.}\\[2.5pt]%')
av_c = av_c.replace(r'ISTDI / IUC Douala', r'IUC Douala (Institut Univ. de la Côte)')

with open(avsec_tex, 'w', encoding='utf-8') as f:
    f.write(av_c)

for i in range(2):
    subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.tex'], cwd=avsec_dir, capture_output=True, text=True)

shutil.copy(os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.pdf'), os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_1PAGE_LATEX.pdf'))
reader_avsec = pypdf.PdfReader(os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_1PAGE_LATEX.pdf'))
print('AVSEC page count:', len(reader_avsec.pages))

pdf_avsec = pdfium.PdfDocument(os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_1PAGE_LATEX.pdf'))
pdf_avsec[0].render(scale=2).to_pil().save(os.path.join(avsec_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_p1.png'))

print('=== ALL 4 TUNED CVS PROCESSED SUCCESSFULLY ===')
