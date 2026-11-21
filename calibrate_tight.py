import subprocess, os, shutil
import pypdf
import pypdfium2 as pdfium

pdflatex = r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
p_dir = r'C:\Users\HP\Desktop\portfolio-gervais'
govai_dir = r'C:\Users\HP\Desktop\candidature-govai'
avsec_dir = r'C:\Users\HP\Desktop\cv agent de surete aeroportuaire'

def calibrate_and_compile():
    # Read the EN template
    with open(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.tex'), 'r', encoding='utf-8') as f:
        en_c = f.read()

    # Apply tight calibration:
    en_c = en_c.replace(r'\linespread{1.06}', r'\linespread{1.03}')
    en_c = en_c.replace(r'\vspace{2.8pt}%' + '\n' + r'    {\fontsize{9.2}{11.4}', r'\vspace{1.8pt}%' + '\n' + r'    {\fontsize{9.0}{11.0}')
    en_c = en_c.replace(r'itemsep=1.2pt,topsep=0.8pt', r'itemsep=0.8pt,topsep=0.4pt')
    en_c = en_c.replace(r'{\fontsize{8.25}{10.2}\selectfont\color{bodyText}#2}', r'{\fontsize{8.15}{9.9}\selectfont\color{bodyText}#2}')
    en_c = en_c.replace(r'{\fontsize{8.55}{10.7}\selectfont\textbf{\color{primaryDark}Operational', r'{\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Operational')
    en_c = en_c.replace(r'{\fontsize{8.55}{10.7}\selectfont\textbf{\color{primaryDark}Aviation', r'{\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Aviation')
    en_c = en_c.replace(r'{\fontsize{8.55}{10.7}\selectfont\textbf{\color{primaryDark}ASU', r'{\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}ASU')
    en_c = en_c.replace(r'{\fontsize{8.55}{10.7}\selectfont\textbf{\color{primaryDark}Dataset', r'{\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Dataset')
    en_c = en_c.replace(r'{\fontsize{8.55}{10.7}\selectfont\textbf{\color{primaryDark}K1', r'{\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}K1')
    en_c = en_c.replace(r'{\fontsize{8.55}{10.7}\selectfont\textbf{\color{primaryDark}Archi', r'{\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Archi')
    en_c = en_c.replace(r'\vspace{2.0pt}' + '\n' + r'    {\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Aviation', r'\vspace{1.2pt}' + '\n' + r'    {\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Aviation')
    en_c = en_c.replace(r'\vspace{2.0pt}' + '\n' + r'    {\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Dataset', r'\vspace{1.2pt}' + '\n' + r'    {\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Dataset')
    en_c = en_c.replace(r'\vspace{2.0pt}' + '\n' + r'    {\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}K1', r'\vspace{1.2pt}' + '\n' + r'    {\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}K1')
    en_c = en_c.replace(r'\vspace{2.0pt}' + '\n' + r'    {\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Archi', r'\vspace{1.2pt}' + '\n' + r'    {\fontsize{8.4}{10.4}\selectfont\textbf{\color{primaryDark}Archi')

    with open(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.tex'), 'w', encoding='utf-8') as f:
        f.write(en_c)

    for i in range(2):
        subprocess.run([pdflatex, '--disable-installer', '-interaction=nonstopmode', 'KOA_MARIE_GERVAIS_NELLY_CV_EN.tex'], cwd=p_dir, capture_output=True, text=True)

    reader = pypdf.PdfReader(os.path.join(p_dir, 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf'))
    print('EN page count after calibration:', len(reader.pages))

calibrate_and_compile()
