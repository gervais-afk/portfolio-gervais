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

def set_cell_margins(cell, top=180, bottom=140, left=320, right=160):
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

    # FULL-BLEED A4 SETUP
    for s in doc.sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(0)
        s.bottom_margin = Inches(0)
        s.left_margin = Inches(0)
        s.right_margin = Inches(0)

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Segoe UI'
    style_normal.font.size = Pt(9)

    # Color palette
    SIDEBAR_FILL       = "0F172A"
    MAIN_FILL          = "FFFFFF"
    CYAN_HDR           = RGBColor(0x38, 0xBD, 0xF8)
    ICE_WHITE          = RGBColor(0xF8, 0xFA, 0xFC)
    SLATE_MID          = RGBColor(0x94, 0xA3, 0xB8)
    NAVY               = RGBColor(0x0A, 0x11, 0x28)
    OCEAN              = RGBColor(0x02, 0x84, 0xC7)
    BODY               = RGBColor(0x33, 0x41, 0x55)
    MUTED              = RGBColor(0x64, 0x74, 0x8B)

    # STRICT SINGLE ROW TABLE
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    set_table_zero_indent(table)
    remove_table_borders(table)

    # EXACT A4 height — forces blue sidebar to fill full page bottom
    row = table.rows[0]
    trPr = row._tr.get_or_add_trPr()
    trHeight = parse_xml(f'<w:trHeight {nsdecls("w")} w:val="16837" w:hRule="exact"/>')
    trPr.append(trHeight)

    col_widths = [Inches(2.60), Inches(5.67)]

    # ========================= SIDEBAR (LEFT — DARK NAVY) =========================
    c0 = table.cell(0, 0)
    c0.width = col_widths[0]
    set_cell_background(c0, SIDEBAR_FILL)
    set_cell_margins(c0, top=280, bottom=280, left=600, right=500)

    # --- Photo ---
    photo_path = r"c:\Users\HP\Desktop\portfolio-gervais\assets\images\profile_headshot_circular.jpeg"
    photo_box = c0.add_table(rows=1, cols=1)
    photo_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_cell = photo_box.cell(0, 0)
    p_cell.width = Inches(1.55)
    set_cell_background(p_cell, "1E3A5F")
    set_cell_margins(p_cell, top=16, bottom=16, left=16, right=16)

    p_ph = p_cell.paragraphs[0]
    p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ph.paragraph_format.space_before = Pt(0)
    p_ph.paragraph_format.space_after = Pt(0)

    if os.path.exists(photo_path):
        try:
            r_ph = p_ph.add_run()
            r_ph.add_picture(photo_path, width=Inches(1.50))
        except Exception:
            r_ph = p_ph.add_run("[ PHOTO ]")
            r_ph.font.size = Pt(8)
            r_ph.font.color.rgb = CYAN_HDR
    else:
        r_ph = p_ph.add_run("[ PHOTO ]")
        r_ph.font.size = Pt(8)
        r_ph.font.color.rgb = CYAN_HDR

    # --- Sidebar helpers ---
    def add_sb_section(cell, title):
        sp = cell.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(0)
        sp.add_run("")

        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(title.upper())
        r.font.name = 'Segoe UI'
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = CYAN_HDR

        sep = cell.add_paragraph()
        sep.paragraph_format.space_before = Pt(1)
        sep.paragraph_format.space_after = Pt(3)
        r_sep = sep.add_run("━" * 22)
        r_sep.font.size = Pt(5)
        r_sep.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    def add_sb_item(cell, text, is_label=False):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.2)
        p.paragraph_format.line_spacing = 1.1
        r = p.add_run(text)
        r.font.size = Pt(7.8) if not is_label else Pt(7.4)
        r.font.color.rgb = ICE_WHITE if not is_label else SLATE_MID

    # --- Contact & Profiles ---
    add_sb_section(c0, "Contact & Profiles")
    add_sb_item(c0, "✉  magenel85@gmail.com")
    add_sb_item(c0, "✆  +237 695 35 34 02")
    add_sb_item(c0, "⌂  Douala / Ngaoundéré, CM")
    add_sb_item(c0, "⚡  devpost.com/magenel85")
    add_sb_item(c0, "🌐  github.com/gervais-afk")
    add_sb_item(c0, "💼  linkedin.com/in/marie-gervais-koa")
    add_sb_item(c0, "🏅  Google Developer Program")

    # --- AI & LLM Stack ---
    add_sb_section(c0, "AI & LLM Stack")
    add_sb_item(c0, "Google Antigravity IDE  ■ ■ ■ ■ ■")
    add_sb_item(c0, "Google Gemma 4 (12B)    ■ ■ ■ ■ ■")
    add_sb_item(c0, "Gemini 2.5 / 1.5 Pro    ■ ■ ■ ■ ■")
    add_sb_item(c0, "Google TabFM (Tabular)  ■ ■ ■ ■ ■")
    add_sb_item(c0, "LangGraph Multi-Agents  ■ ■ ■ ■ ■")
    add_sb_item(c0, "Firebase Genkit         ■ ■ ■ ■ ■")
    add_sb_item(c0, "Neo4j GraphRAG — Agent K1  ■ ■ ■ ■ ■")

    # --- Data & Graphs ---
    add_sb_section(c0, "Data & Graphs")
    add_sb_item(c0, "Neo4j / Cypher Graph    ■ ■ ■ ■ ■")
    add_sb_item(c0, "PostgreSQL / pgvector   ■ ■ ■ ■ ■")
    add_sb_item(c0, "Google BigQuery         ■ ■ ■ ■ □")
    add_sb_item(c0, "Supabase Realtime       ■ ■ ■ ■ □")
    add_sb_item(c0, "Pandas / NumPy ETL      ■ ■ ■ ■ ■")

    # --- Dev & MLOps ---
    add_sb_section(c0, "Dev & MLOps")
    add_sb_item(c0, "Python 3.11+ / MLOps    ■ ■ ■ ■ ■")
    add_sb_item(c0, "FastAPI / Next.js 14    ■ ■ ■ ■ □")
    add_sb_item(c0, "MLflow & Data Drift     ■ ■ ■ ■ □")
    add_sb_item(c0, "SHAP Sentinel Audit     ■ ■ ■ ■ ■")
    add_sb_item(c0, "Docker & Streamlit      ■ ■ ■ ■ ■")
    add_sb_item(c0, "IfcOpenShell (5D BIM)   ■ ■ ■ ■ □")

    # --- Security & Audit ---
    add_sb_section(c0, "Security & Audit")
    add_sb_item(c0, "◈ Quorum 4-Eyes Governance")
    add_sb_item(c0, "◈ OKF v0.2 SHA-256 No-LLM")
    add_sb_item(c0, "◈ EU AI Act (RSASSA-PSS)")
    add_sb_item(c0, "◈ AVSEC Framework (ICAO Annex 17)")

    # --- Languages ---
    add_sb_section(c0, "Languages")
    add_sb_item(c0, "French   —  Native / Fluent")
    add_sb_item(c0, "English  —  Technical / Pro")

    # --- Key Assets ---
    add_sb_section(c0, "Key Assets")
    add_sb_item(c0, "◈ Dual Competence: AI & Civil Eng.")
    add_sb_item(c0, "◈ Aviation Security & Crisis (CCAA)")
    add_sb_item(c0, "◈ Mathematical Rigor & Guardrails")

    # ========================= MAIN COLUMN (RIGHT — WHITE) =========================
    c1 = table.cell(0, 1)
    c1.width = col_widths[1]
    set_cell_background(c1, MAIN_FILL)
    set_cell_margins(c1, top=300, bottom=280, left=300, right=320)

    # --- Name block ---
    p_nm = c1.paragraphs[0]
    p_nm.paragraph_format.space_before = Pt(0)
    p_nm.paragraph_format.space_after = Pt(2)
    r_nm = p_nm.add_run("KOA MARIE GERVAIS NELLY")
    r_nm.font.name = 'Segoe UI'
    r_nm.font.bold = True
    r_nm.font.size = Pt(19)
    r_nm.font.color.rgb = NAVY

    p_sub = c1.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("Lead AI Engineer & Data Architect   │   Founder @ Archi Cam AI")
    r_sub.font.size = Pt(9.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = OCEAN

    p_rule = c1.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(0)
    p_rule.paragraph_format.space_after = Pt(5)
    r_rule = p_rule.add_run("─" * 72)
    r_rule.font.size = Pt(6)
    r_rule.font.color.rgb = OCEAN

    # --- Main section helpers ---
    def add_section_title(cell, title):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(1)
        r_icon = p.add_run("◈  ")
        r_icon.font.bold = True
        r_icon.font.size = Pt(9)
        r_icon.font.color.rgb = OCEAN
        r_title = p.add_run(title.upper())
        r_title.font.name = 'Segoe UI'
        r_title.font.bold = True
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = NAVY
        sep = cell.add_paragraph()
        sep.paragraph_format.space_before = Pt(0)
        sep.paragraph_format.space_after = Pt(4)
        r_sep = sep.add_run("─" * 62)
        r_sep.font.size = Pt(5.5)
        r_sep.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    def add_entry_header(cell, title, badge):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(1)
        r1 = p.add_run(title)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = NAVY
        r2 = p.add_run(f"   —   {badge}")
        r2.font.italic = True
        r2.font.size = Pt(8)
        r2.font.color.rgb = OCEAN

    def add_company_line(cell, company):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(company)
        r.font.size = Pt(8)
        r.font.color.rgb = MUTED
        r.font.bold = True

    def add_bullet(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.12)
        rb = p.add_run("▸  ")
        rb.font.bold = True
        rb.font.size = Pt(8)
        rb.font.color.rgb = OCEAN
        rt = p.add_run(text)
        rt.font.size = Pt(8)
        rt.font.color.rgb = BODY

    def add_body_text(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2
        r = p.add_run(text)
        r.font.size = Pt(8.5)
        r.font.color.rgb = BODY

    # ── Executive Summary ──
    add_section_title(c1, "Executive Summary")
    add_body_text(c1,
        "Lead AI Engineer & Data Architect (Google Developer Program Member), leveraging Google Antigravity "
        "to design and orchestrate neuro-symbolic autonomous multi-agent systems, Neo4j GraphRAG, and sovereign "
        "production MLOps. Specialized in deterministic architectures and verifiable AI trust. Founder of Archi "
        "Cam AI (official applicant for Google Africa Applied AI Lab), bridging civil engineering methodology, "
        "mathematical rigor, and product vision."
    )

    # ── Flagship AI Projects ──
    add_section_title(c1, "Flagship AI Projects")

    add_entry_header(c1, "Archi Cam AI", "Agentic AI SaaS & 5D BIM")
    add_bullet(c1, "Official Applicant Google Africa Applied AI Lab. Built with Google Antigravity (Gemma 4 12B, Gemini, BAEL 91).")
    add_bullet(c1, "Automated Excel BOQs in <45s (–99.2% time, MLflow R²=0.9872) and 3D renders via Imagen 3 + ControlNet.")

    add_entry_header(c1, "K1-MATHINFO (v3.0.0)", "Sovereign Multi-Agent AI & OKF Certification")
    add_bullet(c1, "Sovereign DMI system (Univ. of Ngaoundéré) with Google Antigravity: 470 theses, 19 M1 projects, 1,366 Neo4j nodes.")
    add_bullet(c1, "6-agent LangGraph network, hybrid retrieval (RRF k=60 + Cross-Encoder), SHA-256 No-LLM cert, 77/77 tests (100%).")

    add_entry_header(c1, "Sovereign.BI Agentic", "Enterprise Security & Agentic BI")
    add_bullet(c1, "Sovereign NL-to-SQL/Graph query engine for enterprise databases (PostgreSQL pgvector, Neo4j N10S, <5s latency).")
    add_bullet(c1, "Enforces dynamic ABAC security guardrails and explainability certified via SHAP Sentinel game theory auditor.")

    add_entry_header(c1, "Dataset Automator & VigieSahel", "MLOps Pipeline & Climate AI Impact")
    add_bullet(c1, "Dataset Automator: Built with Google Antigravity (Google Cloud Hackathon) with TabFM, BigQuery DataFrames, EU AI Act.")
    add_bullet(c1, "VigieSahel: Predictive ML for epidemic forecasting & crop sowing optimization (–35% loss, XGBoost R²>94%, Supabase).")

    # ── Professional Experience ──
    add_section_title(c1, "Professional Experience")

    add_entry_header(c1, "AI Lead & Data Science Consultant", "2025 – Present")
    add_company_line(c1, "Independent Projects & Enterprises  │  Douala, CM")
    add_bullet(c1, "Guiding enterprises in deploying sovereign private AI agents, Neo4j GraphRAG pipelines, and PostgreSQL databases.")
    add_bullet(c1, "High-dimensional EDA, predictive modeling, and executive interactive decision dashboards.")

    add_entry_header(c1, "Aviation Security Officer (AVSEC)", "2018 – Present")
    add_company_line(c1, "CCAA (Cameroon Civil Aviation Authority)")
    add_bullet(c1, "Operational threat assessment, secure access control, and regulatory compliance audits (ICAO Annex 17).")
    add_bullet(c1, "Critical aviation security reporting and field emergency operational crisis response coordination.")

    # ── Education ──
    add_section_title(c1, "Education & Certifications")

    add_entry_header(c1, "M.Sc. in Applied Artificial Intelligence", "2025 – 2027  [In Progress]")
    add_company_line(c1, "University of Ngaoundéré")
    add_bullet(c1, "Excellence Curriculum (5 Blocs): ML & Bayesian Statistics, Data Engineering & Neo4j, Computer Vision & Robotics, Cybersecurity & Blockchain, Production Sovereign MLOps.")

    add_entry_header(c1, "B.Sc. in Civil Engineering (Building Option)", "2015 – 2016")
    add_company_line(c1, "ISTDI / IUC Douala")
    add_bullet(c1, "Structural calculations (BAEL 91), quantity surveying, and construction project management.")

    # ── Honors ──
    add_section_title(c1, "Honors & Applied AI Recognitions")

    p_rec = c1.add_paragraph()
    p_rec.paragraph_format.space_before = Pt(0)
    p_rec.paragraph_format.space_after = Pt(2)
    p_rec.paragraph_format.line_spacing = 1.2
    r1 = p_rec.add_run("◈ Google Africa Applied AI Lab (Accra, 2026): ")
    r1.font.bold = True
    r1.font.size = Pt(8.5)
    r1.font.color.rgb = NAVY
    r2 = p_rec.add_run("Official candidacy supported by the Archi Cam AI platform.")
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = BODY

    p_rec2 = c1.add_paragraph()
    p_rec2.paragraph_format.space_before = Pt(0)
    p_rec2.paragraph_format.space_after = Pt(0)
    p_rec2.paragraph_format.line_spacing = 1.2
    r3 = p_rec2.add_run("◈ Google Cloud #AllThingsAgentic Hackathon: ")
    r3.font.bold = True
    r3.font.size = Pt(8.5)
    r3.font.color.rgb = NAVY
    r4 = p_rec2.add_run("Dataset Automator v4.0 built with Google Antigravity (TabFM, WIT, bigframes, MCT).")
    r4.font.size = Pt(8.5)
    r4.font.color.rgb = BODY

    # Minimize trailing paragraph
    if len(doc.paragraphs) > 0:
        p_after = doc.paragraphs[-1]
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(0)
        p_after.paragraph_format.line_spacing = Pt(1)
        r = p_after.add_run("")
        r.font.size = Pt(1)

    # Save DOCX
    f_en_docx = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.docx"
    try:
        doc.save(f_en_docx)
        print(f"Saved: {f_en_docx}")
    except Exception as e:
        print(f"Error saving {f_en_docx}: {e}")

    # Export PDF via Word COM
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        pdf_en = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf"

        if os.path.exists(f_en_docx):
            doc_com = word.Documents.Open(os.path.abspath(f_en_docx))
            doc_com.SaveAs(os.path.abspath(pdf_en), FileFormat=17)
            doc_com.Close()
            print(f"Exported PDF: {pdf_en}")

        word.Quit()
        print("Generated English PDF successfully via Word COM!")
    except Exception as ex:
        print(f"Word COM PDF export note: {ex}")

if __name__ == "__main__":
    generate_exact_user_1page_cv_en()
