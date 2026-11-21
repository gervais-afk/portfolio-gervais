import os
import subprocess
import pypdf

os.chdir(r'c:\Users\HP\Desktop\portfolio-gervais')

def compile_latex(tex_name):
    cmd = [
        r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe',
        '-interaction=nonstopmode',
        tex_name
    ]
    # Run twice for TikZ remember picture coordinate settling
    subprocess.run(cmd, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    res = subprocess.run(cmd, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    out_lines = [l for l in res.stdout.splitlines() if 'Output written on' in l or 'Fatal error' in l]
    print(f"Compile {tex_name}:", out_lines)
    return res.returncode == 0

def render_pdf(pdf_name, prefix):
    reader = pypdf.PdfReader(pdf_name)
    num_pages = len(reader.pages)
    print(f"{pdf_name} has {num_pages} page(s).")
    cmd = [
        r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe',
        '-png',
        '-r', '150',
        pdf_name,
        prefix
    ]
    subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    print(f"Rendered {pdf_name} to {prefix}-1.png")

compile_latex('KOA_MARIE_GERVAIS_NELLY_CV_EN.tex')
render_pdf('KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf', 'cv_en_preview')

compile_latex('KOA_MARIE_GERVAIS_NELLY_CV_FR.tex')
render_pdf('KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf', 'cv_fr_preview')
