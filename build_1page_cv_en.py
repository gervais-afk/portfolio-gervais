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

def set_cell_margins(cell, top=140, bottom=140, left=140, right=140):
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

def set_table_zero_indent(table):
    tblPr = table._tbl.tblPr
    tblInd = parse_xml(f'<w:tblInd {nsdecls("w")} w:w="0" w:type="dxa"/>')
    tblPr.append(tblInd)

def generate_exact_user_1page_cv_en():
    doc = Document()

    # FULL-BLEED A4 SETUP: Margins set to 0 on Left, Top, Right, Bottom
    for s in doc.sections:
        s.page_width = Inches(8.27)    # Standard A4 width (210 mm)
        s.page_height = Inches(11.69)  # Standard A4 height (297 mm)
        s.top_margin = Inches(0)
        s.bottom_margin = Inches(0)
        s.left_margin = Inches(0)
        s.right_margin = Inches(0)

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

    # STRICT SINGLE ROW (1 ROW x 2 COLUMNS)
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    set_table_zero_indent(table)
    remove_table_borders(table)

    # Set row height to 16200 dxa to bleed to the bottom
    row = table.rows[0]
    trPr = row._tr.get_or_add_trPr()
    trHeight = parse_xml(f'<w:trHeight {nsdecls("w")} w:val="16200" w:hRule="atLeast"/>')
    trPr.append(trHeight)

    col_widths = [Inches(2.55), Inches(5.72)]

    # ==================== CELL 0 (SIDEBAR LEFT - FULL BLEED) ====================
    c0 = table.cell(0, 0)
    c0.width = col_widths[0]
    set_cell_background(c0, SIDEBAR_FILL)
    set_cell_margins(c0, top=180, bottom=140, left=180, right=140)

    # Photo Box
    photo_path = r"c:\Users\HP\Desktop\portfolio-gervais\assets\images\profile_headshot_circular.jpeg"
    photo_box = c0.add_table(rows=1, cols=1)
    photo_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_cell = photo_box.cell(0, 0)
    p_cell.width = Inches(1.35)
    set_cell_background(p_cell, "1E293B")
    set_cell_margins(p_cell, top=25, bottom=25, left=25, right=25)
    
    p_ph = p_cell.paragraphs[0]
    p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ph.paragraph_format.space_before = Pt(0)
    p_ph.paragraph_format.space_after = Pt(0)

    if os.path.exists(photo_path):
        try:
            r_ph = p_ph.add_run()
            r_ph.add_picture(photo_path, width=Inches(1.22))
        except Exception:
            r_ph = p_ph.add_run("📷 PHOTO CV")
            r_ph.font.size = Pt(7.5)
            r_ph.font.bold = True
            r_ph.font.color.rgb = CYAN_BLUE_HEADER
    else:
        r_ph = p_ph.add_run("📷 PHOTO CV")
        r_ph.font.size = Pt(7.5)
        r_ph.font.bold = True
        r_ph.font.color.rgb = CYAN_BLUE_HEADER

    def add_sb_h(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1.2)
        r = p.add_run(text.upper())
        r.font.name = 'Segoe UI Semibold'
        r.font.bold = True
        r.font.size = Pt(7.8)
        r.font.color.rgb = CYAN_BLUE_HEADER

    def add_sb_t(cell, icon_txt):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.0)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(icon_txt)
        r.font.size = Pt(7.0)
        r.font.color.rgb = ICE_WHITE_TEXT

    add_sb_h(c0, "CONTACT & PROFILES")
    add_sb_t(c0, "✉  magenel85@gmail.com")
    add_sb_t(c0, "✆  +237 695 35 34 02")
    add_sb_t(c0, "⌂  Douala / Ngaoundéré, CM")
    add_sb_t(c0, "🌐  github.com/gervais-afk")
    add_sb_t(c0, "💼  linkedin.com/in/marie-gervais-koa")
    add_sb_t(c0, "⚡  devpost.com/magenel85")
    add_sb_t(c0, "🏅  Google Developer Program")

    add_sb_h(c0, "AI & LLM STACK")
    add_sb_t(c0, "Google Gemma 4 (12B) ■ ■ ■ ■ ■")
    add_sb_t(c0, "Gemini 2.5 / 1.5 Pro ■ ■ ■ ■ ■")
    add_sb_t(c0, "Google TabFM (Tabular)■ ■ ■ ■ ■")
    add_sb_t(c0, "LangGraph Multi-Agents■ ■ ■ ■ ■")
    add_sb_t(c0, "Firebase Genkit      ■ ■ ■ ■ ■")
    add_sb_t(c0, "Neo4j GraphRAG (N10S)■ ■ ■ ■ ■")

    add_sb_h(c0, "DATA & GRAPHS")
    add_sb_t(c0, "Neo4j / Cypher Graph ■ ■ ■ ■ ■")
    add_sb_t(c0, "PostgreSQL / pgvector■ ■ ■ ■ ■")
    add_sb_t(c0, "Google BigQuery Data ■ ■ ■ ■ □")
    add_sb_t(c0, "Supabase Realtime    ■ ■ ■ ■ □")
    add_sb_t(c0, "Pandas / NumPy ETL   ■ ■ ■ ■ ■")

    add_sb_h(c0, "DEV & MLOPS")
    add_sb_t(c0, "Python (3.11+ MLOps) ■ ■ ■ ■ ■")
    add_sb_t(c0, "FastAPI / Next.js 14 ■ ■ ■ ■ □")
    add_sb_t(c0, "MLflow & Data Drift  ■ ■ ■ ■ □")
    add_sb_t(c0, "SHAP Sentinel Audit  ■ ■ ■ ■ ■")
    add_sb_t(c0, "Docker & Streamlit   ■ ■ ■ ■ ■")
    add_sb_t(c0, "IfcOpenShell (5D BIM)■ ■ ■ ■ □")

    add_sb_h(c0, "SECURITY & AUDIT")
    add_sb_t(c0, "◈ Quorum 4-Eyes (KOA+AZIZ)")
    add_sb_t(c0, "◈ OKF v0.2 SHA-256 No-LLM")
    add_sb_t(c0, "◈ EU AI Act (RSASSA-PSS)")
    add_sb_t(c0, "◈ AVSEC (ICAO Annex 17)")

    add_sb_h(c0, "LANGUAGES")
    add_sb_t(c0, "French (Native / Fluent)")
    add_sb_t(c0, "English (Technical / Pro)")

    add_sb_h(c0, "KEY ASSETS")
    add_sb_t(c0, "◈ Dual Competence AI & Civil Eng.")
    add_sb_t(c0, "◈ Aviation Security & Crisis (CCAA)")
    add_sb_t(c0, "◈ Mathematical Rigor & Guardrails")

    # ==================== CELL 1 (MAIN COLUMN RIGHT - WHITE) ====================
    c1 = table.cell(0, 1)
    c1.width = col_widths[1]
    set_cell_background(c1, MAIN_FILL)
    set_cell_margins(c1, top=180, bottom=140, left=180, right=180)

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
    p_sub.paragraph_format.space_after = Pt(1.5)
    r_sb = p_sub.add_run("Lead AI Engineer & Data Architect   │   Founder @ Archi Cam AI")
    r_sb.font.size = Pt(8.2)
    r_sb.font.bold = True
    r_sb.font.color.rgb = OCEAN_BLUE

    p_dec = c1.add_paragraph()
    p_dec.paragraph_format.space_before = Pt(0)
    p_dec.paragraph_format.space_after = Pt(2.5)
    r_d = p_dec.add_run("─── ◈ ────────────────────────────────────────────────────────── ◈ ───")
    r_d.font.size = Pt(6.5)
    r_d.font.color.rgb = OCEAN_BLUE

    def add_mn_h(cell, title):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(4.5)
        p.paragraph_format.space_after = Pt(1.2)
        r1 = p.add_run("◈  ")
        r1.font.bold = True
        r1.font.size = Pt(7.8)
        r1.font.color.rgb = OCEAN_BLUE
        r2 = p.add_run(title.upper())
        r2.font.name = 'Segoe UI'
        r2.font.bold = True
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = NAVY_TITLE

    add_mn_h(c1, "EXECUTIVE SUMMARY")
    p_pr = c1.add_paragraph()
    p_pr.paragraph_format.space_before = Pt(0)
    p_pr.paragraph_format.space_after = Pt(2.5)
    p_pr.paragraph_format.line_spacing = 1.06
    r_pr = p_pr.add_run(
        "Lead AI Engineer & Data Architect (Google Developer Program Member) specializing in sovereign autonomous multi-agents, Neo4j GraphRAG, and deterministic civil engineering software. Founder of Archi Cam AI (official applicant for Google Africa Applied AI Lab), bridging multi-agent orchestration with strict mathematical compliance (BAEL 91, ICAO Annex 17) and production MLOps."
    )
    r_pr.font.size = Pt(7.4)
    r_pr.font.color.rgb = BODY_DARK

    add_mn_h(c1, "FLAGSHIP AI PROJECTS")

    def add_proj_compact(cell, name, sub_badge, bullets):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2.2)
        p.paragraph_format.space_after = Pt(0.4)
        r1 = p.add_run(name + "  ")
        r1.font.bold = True
        r1.font.size = Pt(8.0)
        r1.font.color.rgb = NAVY_TITLE
        
        r2 = p.add_run("–  " + sub_badge)
        r2.font.italic = True
        r2.font.size = Pt(7.2)
        r2.font.color.rgb = OCEAN_BLUE

        for b in bullets:
            bp = cell.add_paragraph()
            bp.paragraph_format.space_before = Pt(0)
            bp.paragraph_format.space_after = Pt(0.6)
            bp.paragraph_format.line_spacing = 1.04
            bp.paragraph_format.left_indent = Inches(0.08)
            rb_ico = bp.add_run("▸  ")
            rb_ico.font.bold = True
            rb_ico.font.size = Pt(7.0)
            rb_ico.font.color.rgb = OCEAN_BLUE
            rb_txt = bp.add_run(b)
            rb_txt.font.size = Pt(7.0)
            rb_txt.font.color.rgb = BODY_DARK

    add_proj_compact(
        c1,
        "Archi Cam AI",
        "Agentic AI & 5D BIM SaaS",
        [
            "Official Applicant Google Africa Applied AI Lab. 5D BIM & BOQ estimation (local Gemma 4 12B, Gemini, BAEL 91).",
            "Automated Excel BOQs in <45s (-99.2% time, MLflow R²=0.9872) and 3D renders via Imagen 3 + ControlNet."
        ]
    )

    add_proj_compact(
        c1,
        "K1-MATHINFO (v3.0.0)",
        "Sovereign Multi-Agent AI & OKF Certification",
        [
            "Sovereign DMI system (Univ. of Ngaoundéré): 470 theses, 19 M1 projects, Neo4j graph of 1,366 nodes / 3,833 edges.",
            "6-agent LangGraph network, hybrid retrieval (RRF k=60 + Cross-Encoder), SHA-256 No-LLM cert, 77/77 tests (100%)."
        ]
    )

    add_proj_compact(
        c1,
        "Sovereign.BI Agentic",
        "Enterprise Security & Agentic BI",
        [
            "Sovereign natural language query engine for enterprise SQL/Graph databases (PostgreSQL pgvector, Neo4j, <5s latency).",
            "Enforces dynamic ABAC security guardrails and explainability certified via SHAP Sentinel game theory auditor."
        ]
    )

    add_proj_compact(
        c1,
        "Dataset Automator & VigieSahel",
        "MLOps Pipeline & Climate AI Impact",
        [
            "Dataset Automator: TabFM & BigQuery DataFrames MLOps factory with continuous Data Drift tracking (KS/PSI) and EU AI Act.",
            "VigieSahel: Predictive ML for epidemic forecasting & crop sowing optimization (-35% loss, XGBoost R²>94%, Supabase)."
        ]
    )

    add_mn_h(c1, "PROFESSIONAL EXPERIENCE")

    def add_job_compact(cell, title, period, company, bullets):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2.2)
        p.paragraph_format.space_after = Pt(0.4)
        r1 = p.add_run(title + "  ")
        r1.font.bold = True
        r1.font.size = Pt(8.0)
        r1.font.color.rgb = NAVY_TITLE

        r2 = p.add_run(f"({period})")
        r2.font.italic = True
        r2.font.size = Pt(7.2)
        r2.font.color.rgb = OCEAN_BLUE

        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0.6)
        r3 = p2.add_run(company)
        r3.font.bold = True
        r3.font.size = Pt(7.0)
        r3.font.color.rgb = SUBTLE_TEXT

        for b in bullets:
            bp = cell.add_paragraph()
            bp.paragraph_format.space_before = Pt(0)
            bp.paragraph_format.space_after = Pt(0.6)
            bp.paragraph_format.line_spacing = 1.04
            bp.paragraph_format.left_indent = Inches(0.08)
            rb_ico = bp.add_run("▸  ")
            rb_ico.font.bold = True
            rb_ico.font.size = Pt(7.0)
            rb_ico.font.color.rgb = OCEAN_BLUE
            rb_txt = bp.add_run(b)
            rb_txt.font.size = Pt(7.0)
            rb_txt.font.color.rgb = BODY_DARK

    add_job_compact(
        c1,
        "AI Lead & Data Science Consultant",
        "2025 – Present",
        "Independent Projects & Enterprises  │  Douala, CM",
        [
            "Guiding enterprises in deploying sovereign private AI agents, Neo4j GraphRAG pipelines, and PostgreSQL databases.",
            "High-dimensional exploratory data analysis, predictive modeling, and executive interactive decision dashboards."
        ]
    )

    add_job_compact(
        c1,
        "Aviation Security Officer (AVSEC)",
        "2018 – Present",
        "CCAA (Cameroon Civil Aviation Authority)",
        [
            "Operational threat assessment, secure access control, and regulatory compliance audits (ICAO Annex 17).",
            "Critical aviation security reporting and field emergency operational crisis response coordination."
        ]
    )

    add_mn_h(c1, "EDUCATION & CERTIFICATIONS")

    def add_edu_compact(cell, degree, period, school, syllabus_desc, note=None):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2.2)
        p.paragraph_format.space_after = Pt(0.4)
        r1 = p.add_run(degree + "  ")
        r1.font.bold = True
        r1.font.size = Pt(8.0)
        r1.font.color.rgb = NAVY_TITLE

        r2 = p.add_run(f"({period})")
        r2.font.italic = True
        r2.font.size = Pt(7.2)
        r2.font.color.rgb = OCEAN_BLUE

        if note:
            r_nt = p.add_run(f"  [{note}]")
            r_nt.font.bold = True
            r_nt.font.size = Pt(6.6)
            r_nt.font.color.rgb = OCEAN_BLUE

        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0.4)
        r3 = p2.add_run(school)
        r3.font.bold = True
        r3.font.size = Pt(7.0)
        r3.font.color.rgb = SUBTLE_TEXT

        p3 = cell.add_paragraph()
        p3.paragraph_format.space_before = Pt(0)
        p3.paragraph_format.space_after = Pt(0.8)
        p3.paragraph_format.line_spacing = 1.04
        r4 = p3.add_run(syllabus_desc)
        r4.font.size = Pt(6.8)
        r4.font.color.rgb = BODY_DARK

    add_edu_compact(
        c1,
        "Master of Science in Applied Artificial Intelligence",
        "2025 – 2027",
        "University of Ngaoundéré",
        "Excellence Curriculum (5 Blocs): Machine Learning & Bayesian Statistics, Data Engineering & Neo4j Knowledge Graphs, Computer Vision & Robotics/HCI, Cybersecurity & Blockchain, Production Sovereign MLOps Deployment.",
        note="In Progress"
    )
    
    add_edu_compact(
        c1,
        "Bachelor of Science in Civil Engineering (Building Option)",
        "2015 – 2016",
        "ISTDI / IUC Douala",
        "Structural calculations (BAEL 91), quantity surveying, and construction project management."
    )

    add_mn_h(c1, "HONORS & APPLIED AI RECOGNITIONS")
    p_rec = c1.add_paragraph()
    p_rec.paragraph_format.space_before = Pt(0)
    p_rec.paragraph_format.space_after = Pt(0.5)
    p_rec.paragraph_format.line_spacing = 1.04
    r_r1 = p_rec.add_run("◈ Google Africa Applied AI Lab (Accra, 2026): ")
    r_r1.font.bold = True
    r_r1.font.size = Pt(7.0)
    r_r1.font.color.rgb = NAVY_TITLE
    r_r2 = p_rec.add_run("Official candidacy supported by Archi Cam AI platform.\n")
    r_r2.font.size = Pt(7.0)
    r_r2.font.color.rgb = BODY_DARK
    
    r_r3 = p_rec.add_run("◈ Google Cloud #AllThingsAgentic Hackathon: ")
    r_r3.font.bold = True
    r_r3.font.size = Pt(7.0)
    r_r3.font.color.rgb = NAVY_TITLE
    r_r4 = p_rec.add_run("Dataset Automator v4.0 (TabFM, WIT, bigframes, MCT).")
    r_r4.font.size = Pt(7.0)
    r_r4.font.color.rgb = BODY_DARK

    # Minimize trailing paragraph after table
    if len(doc.paragraphs) > 0:
        p_after = doc.paragraphs[-1]
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(0)
        p_after.paragraph_format.line_spacing = Pt(1)
        r = p_after.add_run("")
        r.font.size = Pt(1)

    # Output path
    f_en_docx = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.docx"
    
    try:
        doc.save(f_en_docx)
        print(f"Saved: {f_en_docx}")
    except Exception as e:
        print(f"Error saving {f_en_docx}: {e}")

    # Export to PDF via Word COM
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        pdf_en = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf"

        if os.path.exists(f_en_docx):
            doc_com = word.Documents.Open(os.path.abspath(f_en_docx))
            doc_com.SaveAs(os.path.abspath(pdf_en), FileFormat=17) # 17 = wdFormatPDF
            doc_com.Close()
            print(f"Exported PDF: {pdf_en}")

        word.Quit()
        print("Generated English PDF file successfully via Word COM!")
    except Exception as ex:
        print(f"Word COM PDF export note: {ex}")

if __name__ == "__main__":
    generate_exact_user_1page_cv_en()
