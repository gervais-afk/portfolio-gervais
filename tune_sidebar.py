with open(r'c:\Users\HP\Desktop\portfolio-gervais\write_all_cvs.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add \raggedright to sidebar sections where needed
code = code.replace(
    r'''    % ── LANGUAGES ──
    \sideSecTitle{LANGUAGES}
    {\fontsize{8.5}{11.4}\selectfont''',
    r'''    % ── LANGUAGES ──
    \sideSecTitle{LANGUAGES}
    {\fontsize{8.5}{11.4}\selectfont\raggedright'''
)

code = code.replace(
    r'''    % ── LANGUES ──
    \sideSecTitle{LANGUES}
    {\fontsize{8.5}{11.4}\selectfont''',
    r'''    % ── LANGUES ──
    \sideSecTitle{LANGUES}
    {\fontsize{8.5}{11.4}\selectfont\raggedright'''
)

with open(r'c:\Users\HP\Desktop\portfolio-gervais\write_all_cvs.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open(r'c:\Users\HP\Desktop\portfolio-gervais\update_surete_cv.py', 'r', encoding='utf-8') as f:
    scode = f.read()

scode = scode.replace(
    r'''    % ── LANGUES ──
    \sideSecTitle{LANGUES}
    {\fontsize{8.5}{11.4}\selectfont''',
    r'''    % ── LANGUES ──
    \sideSecTitle{LANGUES}
    {\fontsize{8.5}{11.4}\selectfont\raggedright'''
)

with open(r'c:\Users\HP\Desktop\portfolio-gervais\update_surete_cv.py', 'w', encoding='utf-8') as f:
    f.write(scode)

print("Updated write_all_cvs.py and update_surete_cv.py")
