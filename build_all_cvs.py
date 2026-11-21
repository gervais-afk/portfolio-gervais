import os
import subprocess
import re

# 1. Update files
import write_all_cvs
import update_surete_cv

def compile_latex(workdir, tex_name, output_pdf=None):
    os.chdir(workdir)
    cmd = [
        r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe',
        '-interaction=nonstopmode',
        tex_name
    ]
    # Run twice for TikZ remember picture coordinate settling
    subprocess.run(cmd, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    res = subprocess.run(cmd, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    
    # If output_pdf requested and differs from default
    default_pdf = tex_name.replace('.tex', '.pdf')
    if output_pdf and output_pdf != default_pdf and os.path.exists(default_pdf):
        if os.path.exists(output_pdf):
            os.remove(output_pdf)
        os.rename(default_pdf, output_pdf)
        actual_pdf = output_pdf
    else:
        actual_pdf = default_pdf
        
    with open(actual_pdf, 'rb') as f:
        pages = len(re.findall(rb'/Type\s*/Page\b', f.read()))
    print(f"[{workdir}] {actual_pdf}: {pages} page(s).")
    return actual_pdf

def render_pdf(workdir, pdf_name, prefix):
    os.chdir(workdir)
    cmd = [
        r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdftoppm.exe',
        '-png',
        '-r', '150',
        pdf_name,
        prefix
    ]
    subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    print(f"[{workdir}] Rendered {pdf_name} to {prefix}-1.png")

# Portfolio Gervais EN & FR
compile_latex(r'c:\Users\HP\Desktop\portfolio-gervais', 'KOA_MARIE_GERVAIS_NELLY_CV_EN.tex')
render_pdf(r'c:\Users\HP\Desktop\portfolio-gervais', 'KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf', 'cv_en_preview')

compile_latex(r'c:\Users\HP\Desktop\portfolio-gervais', 'KOA_MARIE_GERVAIS_NELLY_CV_FR.tex')
render_pdf(r'c:\Users\HP\Desktop\portfolio-gervais', 'KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf', 'cv_fr_preview')

# Candidature GovAI (English with photo)
compile_latex(
    r'C:\Users\HP\Desktop\candidature-govai',
    'KOA_MARIE_GERVAIS_NELLY_CV_LATEX.tex',
    'KOA_MARIE_GERVAIS_NELLY_CV_GOVAI_1PAGE_LATEX.pdf'
)
render_pdf(
    r'C:\Users\HP\Desktop\candidature-govai',
    'KOA_MARIE_GERVAIS_NELLY_CV_GOVAI_1PAGE_LATEX.pdf',
    'cv_govai_preview'
)

# CV Agent de Sûreté Aéroportuaire
compile_latex(
    r'C:\Users\HP\Desktop\cv agent de surete aeroportuaire',
    'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE.tex',
    'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_1PAGE_LATEX.pdf'
)
render_pdf(
    r'C:\Users\HP\Desktop\cv agent de surete aeroportuaire',
    'KOA_MARIE_GERVAIS_NELLY_CV_SURETE_AEROPORTUAIRE_1PAGE_LATEX.pdf',
    'cv_surete_preview'
)

print("All builds completed.")
