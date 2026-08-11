import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def remove_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def generate_exact_user_1page_cv_en():
    doc = Document()

    # Ultra-compact 1-page margins (0.2 inch / ~0.5 cm)
    for s in doc.sections:
        s.top_margin = Inches(0.2)
        s.bottom_margin = Inches(0.2)
        s.left_margin = Inches(0.2)
        s.right_margin = Inches(0.2)

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Segoe UI'
    style_normal.font.size = Pt(8)

    SIDEBAR_FILL = "0F172A"       # Deep Slate Navy
    MAIN_FILL = "FFFFFF"          # Pure Crisp White
    
    CYAN_BLUE_HEADER = RGBColor(0x38, 0xBD, 0xF8)   # Electric Sky Blue
    ICE_WHITE_TEXT = RGBColor(0xF8, 0xFA, 0xFC)     # Crisp White
    
    NAVY_TITLE = RGBColor(0x0A, 0x11, 0x28)         # Deep Executive Navy
    OCEAN_BLUE = RGBColor(0x02, 0x84, 0xC7)         # Professional Ocean Blue Accent
    BODY_DARK = RGBColor(0x33, 0x41, 0x55)          # Slate Text Body
    SUBTLE_TEXT = RGBColor(0x64, 0x74, 0x8B)        # Muted Slate

    # STRICT SINGLE ROW (1 ROW x 2 COLUMNS) -> Fits on exactly 1 page
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    remove_table_borders(table)

    col_widths = [Inches(2.3), Inches(5.3)]

    # ==================== CELL 0 (SIDEBAR LEFT) ====================
    c0 = table.cell(0, 0)
    c0.width = col_widths[0]
    set_cell_background(c0, SIDEBAR_FILL)
    set_cell_margins(c0, top=100, bottom=100, left=120, right=120)

    # Photo Box
    photo_path = r"c:\Users\HP\Desktop\portfolio-gervais\assets\images\profile_headshot_circular.jpeg"
    photo_box = c0.add_table(rows=1, cols=1)
    photo_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_cell = photo_box.cell(0, 0)
    p_cell.width = Inches(1.4)
    set_cell_background(p_cell, "1E293B")
    set_cell_margins(p_cell, top=40, bottom=40, left=40, right=40)
    
    p_ph = p_cell.paragraphs[0]
    p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ph.paragraph_format.space_before = Pt(0)
    p_ph.paragraph_format.space_after = Pt(0)

    if os.path.exists(photo_path):
        try:
            r_ph = p_ph.add_run()
            r_ph.add_picture(photo_path, width=Inches(1.3))
        except Exception:
            r_ph = p_ph.add_run("📷 CV PHOTO")
            r_ph.font.size = Pt(7)
            r_ph.font.bold = True
            r_ph.font.color.rgb = CYAN_BLUE_HEADER
    else:
        r_ph = p_ph.add_run("📷 CV PHOTO")
        r_ph.font.size = Pt(7)
        r_ph.font.bold = True
        r_ph.font.color.rgb = CYAN_BLUE_HEADER

    def add_sb_h(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(text.upper())
        r.font.name = 'Segoe UI Semibold'
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = CYAN_BLUE_HEADER

    def add_sb_t(cell, icon_txt):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(icon_txt)
        r.font.size = Pt(7.5)
        r.font.color.rgb = ICE_WHITE_TEXT

    add_sb_h(c0, "CONTACT")
    add_sb_t(c0, "✉  magenel85@gmail.com")
    add_sb_t(c0, "✆  +237 695 35 34 02")
    add_sb_t(c0, "⌂  Douala / Ngaoundéré, CM")
    add_sb_t(c0, "🌐  github.com/gervais-afk")
    add_sb_t(c0, "💼  linkedin.com/in/gervais-koa")

    add_sb_h(c0, "AI & LLM STACK")
    add_sb_t(c0, "Google Gemma 4   ■ ■ ■ ■ ■")
    add_sb_t(c0, "Gemini 1.5 Pro   ■ ■ ■ ■ ■")
    add_sb_t(c0, "CrewAI/LangGraph ■ ■ ■ ■ ■")
    add_sb_t(c0, "Firebase Genkit  ■ ■ ■ ■ ■")
    add_sb_t(c0, "RAG / GraphRAG   ■ ■ ■ ■ ■")

    add_sb_h(c0, "DATA & GRAPHS")
    add_sb_t(c0, "Neo4j / Cypher      ■ ■ ■ ■ ■")
    add_sb_t(c0, "PostgreSQL / SQL    ■ ■ ■ ■ ■")
    add_sb_t(c0, "Supabase           ■ ■ ■ ■ □")
    add_sb_t(c0, "Firebase Emulator  ■ ■ ■ ■ □")
    add_sb_t(c0, "Pandas / NumPy     ■ ■ ■ ■ ■")

    add_sb_h(c0, "DEV & MLOPS")
    add_sb_t(c0, "Python (BAEL 91)   ■ ■ ■ ■ ■")
    add_sb_t(c0, "IfcOpenShell (5D)  ■ ■ ■ ■ □")
    add_sb_t(c0, "FastAPI / Next.js  ■ ■ ■ ■ □")
    add_sb_t(c0, "MLflow (MLOps)     ■ ■ ■ ■ □")
    add_sb_t(c0, "Streamlit / Docker ■ ■ ■ ■ ■")

    add_sb_h(c0, "LANGUAGES")
    add_sb_t(c0, "French (Native)")
    add_sb_t(c0, "English (Professional / Tech)")

    add_sb_h(c0, "KEY ASSETS")
    add_sb_t(c0, "◈ Dual Competence AI & Civil Eng.")
    add_sb_t(c0, "◈ Aviation Security & Risk (AVSEC)")
    add_sb_t(c0, "◈ Strict Math Guardrails & 0 Hallucination")

    # ==================== CELL 1 (MAIN COLUMN RIGHT) ====================
    c1 = table.cell(0, 1)
    c1.width = col_widths[1]
    set_cell_background(c1, MAIN_FILL)
    set_cell_margins(c1, top=100, bottom=100, left=140, right=100)

    p_m01 = c1.paragraphs[0]
    p_m01.paragraph_format.space_before = Pt(0)
    p_m01.paragraph_format.space_after = Pt(1)
    r_nm = p_m01.add_run("KOA MARIE GERVAIS NELLY")
    r_nm.font.name = 'Segoe UI'
    r_nm.font.bold = True
    r_nm.font.size = Pt(15)
    r_nm.font.color.rgb = NAVY_TITLE

    p_sub = c1.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(1)
    r_sb = p_sub.add_run("Lead AI Engineer & Data Architect   │   Founder @ Archi Cam AI")
    r_sb.font.size = Pt(8.5)
    r_sb.font.bold = True
    r_sb.font.color.rgb = OCEAN_BLUE

    p_dec = c1.add_paragraph()
    p_dec.paragraph_format.space_before = Pt(0)
    p_dec.paragraph_format.space_after = Pt(3)
    r_d = p_dec.add_run("─── ◈ ────────────────────────────────────────────────────────── ◈ ───")
    r_d.font.size = Pt(7)
    r_d.font.color.rgb = OCEAN_BLUE

    def add_mn_h(cell, title):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1.5)
        r1 = p.add_run("◈  ")
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = OCEAN_BLUE
        r2 = p.add_run(title.upper())
        r2.font.name = 'Segoe UI'
        r2.font.bold = True
        r2.font.size = Pt(9)
        r2.font.color.rgb = NAVY_TITLE

    add_mn_h(c1, "EXECUTIVE SUMMARY")
    p_pr = c1.add_paragraph()
    p_pr.paragraph_format.space_before = Pt(0)
    p_pr.paragraph_format.space_after = Pt(3)
    p_pr.paragraph_format.line_spacing = 1.05
    r_pr = p_pr.add_run(
        "Lead AI Engineer & Data Architect specializing in sovereign autonomous agents, Neo4j GraphRAG, and deterministic civil engineering software. Founder of Archi Cam AI (official applicant for Google Africa Applied AI Lab), bridging multi-agent orchestration with strict mathematical compliance (BAEL 91, ICAO Annex 17) and production MLOps."
    )
    r_pr.font.size = Pt(8)
    r_pr.font.color.rgb = BODY_DARK

    add_mn_h(c1, "FLAGSHIP AI PROJECTS")

    def add_proj_compact(cell, name, sub_badge, bullets):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2.5)
        p.paragraph_format.space_after = Pt(0.5)
        r1 = p.add_run(name + "  ")
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = NAVY_TITLE
        
        r2 = p.add_run("–  " + sub_badge)
        r2.font.italic = True
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = OCEAN_BLUE

        for b in bullets:
            bp = cell.add_paragraph()
            bp.paragraph_format.space_before = Pt(0)
            bp.paragraph_format.space_after = Pt(0.5)
            bp.paragraph_format.left_indent = Inches(0.1)
            rb_ico = bp.add_run("▸  ")
            rb_ico.font.bold = True
            rb_ico.font.size = Pt(7.5)
            rb_ico.font.color.rgb = OCEAN_BLUE
            rb_txt = bp.add_run(b)
            rb_txt.font.size = Pt(7.5)
            rb_txt.font.color.rgb = BODY_DARK

    add_proj_compact(
        c1,
        "Archi Cam AI",
        "Agentic AI & 5D BIM SaaS",
        [
            "Official candidate for Google Africa Applied AI Lab (Accra, Ghana). Sovereign 5D BIM & BOQ estimation platform.",
            "Combines local Google Gemma 4 12B QAT, Gemini 1.5 Pro, and deterministic Python Sandbox (IfcOpenShell, BAEL 91).",
            "Automates 6-sheet NDA Excel BOQs in <45s (-99.2% time) and synthesizes 3D renders via Imagen 3.0 + ControlNet."
        ]
    )

    add_proj_compact(
        c1,
        "Sovereign.BI Agentic",
        "Enterprise Security & Agentic BI",
        [
            "Sovereign natural language query engine for complex enterprise SQL & Graph databases.",
            "TypeScript Orchestrator architecture, Neo4j N10S (GraphRAG), and FastAPI/PostgreSQL backend.",
            "Enforces dynamic ABAC guardrails and anti-hallucination explainability via SHAP Sentinel."
        ]
    )

    add_proj_compact(
        c1,
        "Dataset Automator & VigieSahel",
        "MLOps Pipeline & Climate AI Impact",
        [
            "Dataset Automator: Time-series evaluation RAG pipeline (Neo4j, MLflow tracking, Firebase Genkit).",
            "VigieSahel: Predictive ML platform for agro-climatic sowing optimization & health outbreak tracking (R² > 0.94)."
        ]
    )

    add_mn_h(c1, "PROFESSIONAL EXPERIENCE")

    def add_job_compact(cell, title, period, company, bullets):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2.5)
        p.paragraph_format.space_after = Pt(0.5)
        r1 = p.add_run(title + "  ")
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = NAVY_TITLE

        r2 = p.add_run(f"({period})")
        r2.font.italic = True
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = OCEAN_BLUE

        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0.5)
        r3 = p2.add_run(company)
        r3.font.bold = True
        r3.font.size = Pt(7.5)
        r3.font.color.rgb = SUBTLE_TEXT

        for b in bullets:
            bp = cell.add_paragraph()
            bp.paragraph_format.space_before = Pt(0)
            bp.paragraph_format.space_after = Pt(0.5)
            bp.paragraph_format.left_indent = Inches(0.1)
            rb_ico = bp.add_run("▸  ")
            rb_ico.font.bold = True
            rb_ico.font.size = Pt(7.5)
            rb_ico.font.color.rgb = OCEAN_BLUE
            rb_txt = bp.add_run(b)
            rb_txt.font.size = Pt(7.5)
            rb_txt.font.color.rgb = BODY_DARK

    add_job_compact(
        c1,
        "AI Lead & Data Science Consultant",
        "2025 – Present",
        "Independent Projects & Enterprises  │  Douala, CM",
        [
            "Guiding enterprises in deploying sovereign local AI agents and private data processing pipelines.",
            "Exploratory data analysis and preprocessing of high-dimensional complex datasets.",
            "Knowledge graph modeling (Neo4j Cypher) and end-to-end GraphRAG pipeline development.",
            "Designing PostgreSQL relational schema and interactive executive reporting dashboards."
        ]
    )

    add_job_compact(
        c1,
        "Aviation Security Officer (AVSEC)",
        "2018 – Present",
        "CCAA (Cameroon Civil Aviation Authority)",
        [
            "Critical threat assessment, security inspections, and access control management (ICAO Annex 17).",
            "Drafting regulatory security compliance reports and coordinating operational field emergency response."
        ]
    )

    add_mn_h(c1, "EDUCATION & CERTIFICATIONS")

    def add_edu_compact(cell, degree, period, school, note=""):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(0.5)
        r1 = p.add_run(degree + "  ")
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = NAVY_TITLE

        r2 = p.add_run(f"({period})")
        r2.font.italic = True
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = OCEAN_BLUE

        if note:
            r_nt = p.add_run(f"   [{note}]")
            r_nt.font.bold = True
            r_nt.font.size = Pt(7.5)
            r_nt.font.color.rgb = OCEAN_BLUE

        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0.5)
        r3 = p2.add_run(school)
        r3.font.size = Pt(7.5)
        r3.font.color.rgb = SUBTLE_TEXT

    add_edu_compact(
        c1,
        "Master of Science in Applied Artificial Intelligence",
        "2025 – 2027",
        "University of Ngaoundéré  │  Graph Modeling (Neo4j), MLOps, Prompt Engineering & LLM Architecture",
        note="In Progress"
    )
    
    add_edu_compact(
        c1,
        "Bachelor of Science in Civil Engineering (Building Option)",
        "2015 – 2016",
        "ISTDI / IUC Douala  │  Structural Calculations (BAEL 91), Quantity Surveying & Construction Project Management"
    )

    # Word output paths
    f_exec_docx = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EXECUTIVE_EN.docx"
    f_main_docx = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.docx"
    
    try:
        doc.save(f_exec_docx)
    except Exception as e:
        print(f"Exec docx save error: {e}")

    try:
        doc.save(f_main_docx)
    except Exception as e:
        print(f"Main docx save error: {e}")

    print(f"Generated English Word CVs successfully.")

    # Export to PDF via Word COM
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        pdf_exec = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EXECUTIVE_EN.pdf"
        pdf_main = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf"

        # Export EXECUTIVE
        if os.path.exists(f_exec_docx):
            doc_com = word.Documents.Open(f_exec_docx)
            doc_com.SaveAs(pdf_exec, FileFormat=17) # 17 = wdFormatPDF
            doc_com.Close()

        # Export MAIN
        if os.path.exists(f_main_docx):
            doc_com = word.Documents.Open(f_main_docx)
            doc_com.SaveAs(pdf_main, FileFormat=17)
            doc_com.Close()

        word.Quit()
        print("Generated English PDF files successfully via Word COM!")
    except Exception as ex:
        print(f"Word COM PDF export note: {ex}")

if __name__ == "__main__":
    generate_exact_user_1page_cv_en()
