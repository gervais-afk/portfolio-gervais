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

def set_cell_margins(cell, top=180, left=440, bottom=140, right=200):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def remove_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/><w:left w:val="none"/>'
        f'<w:bottom w:val="none"/><w:right w:val="none"/>'
        f'<w:insideH w:val="none"/><w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def set_table_zero_indent(table):
    tblPr = table._tbl.tblPr
    tblInd = parse_xml(f'<w:tblInd {nsdecls("w")} w:w="0" w:type="dxa"/>')
    tblPr.append(tblInd)

def generate_exact_user_1page_cv_en():
    doc = Document()
    for s in doc.sections:
        s.page_width  = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = 0

    doc.styles['Normal'].font.name = 'Segoe UI'
    doc.styles['Normal'].font.size = Pt(8.0)

    SIDEBAR_FILL = "0F172A"
    CYAN   = RGBColor(0x38, 0xBD, 0xF8)
    ICE    = RGBColor(0xF8, 0xFA, 0xFC)
    NAVY   = RGBColor(0x0A, 0x11, 0x28)
    OCEAN  = RGBColor(0x02, 0x84, 0xC7)
    BODY   = RGBColor(0x33, 0x41, 0x55)
    MUTED  = RGBColor(0x64, 0x74, 0x8B)
    GOLD   = RGBColor(0xF5, 0xA6, 0x23)
    WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    set_table_zero_indent(table)
    remove_table_borders(table)

    row = table.rows[0]
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:trHeight {nsdecls("w")} w:val="15400" w:hRule="atLeast"/>'))

    col_widths = [Inches(2.58), Inches(5.69)]

    # ══════════════ SIDEBAR (LEFT — DEEP SLATE NAVY) ══════════════
    c0 = table.cell(0, 0)
    c0.width = col_widths[0]
    set_cell_background(c0, SIDEBAR_FILL)
    set_cell_margins(c0, top=180, left=440, bottom=140, right=180)

    photo_path = r"c:\Users\HP\Desktop\portfolio-gervais\assets\images\profile_headshot_circular.jpeg"

    # ── Photo Headshot ──
    p_ph = c0.paragraphs[0]
    p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ph.paragraph_format.space_before = Pt(0)
    p_ph.paragraph_format.space_after  = Pt(0)
    if os.path.exists(photo_path):
        try:
            p_ph.add_run().add_picture(photo_path, width=Inches(1.42))
        except:
            r = p_ph.add_run("K G"); r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = CYAN
    else:
        r = p_ph.add_run("K G"); r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = CYAN

    # Badge label under photo
    p_badge = c0.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_before = Pt(3.0)
    p_badge.paragraph_format.space_after  = Pt(1.5)
    rb = p_badge.add_run("Founder  ·  Archi Cam AI")
    rb.font.name = 'Segoe UI'; rb.font.bold = True
    rb.font.size = Pt(6.8); rb.font.color.rgb = CYAN

    def sb_h(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(4.2)
        p.paragraph_format.space_after  = Pt(0)
        p.paragraph_format.left_indent  = Pt(6)
        r = p.add_run(text.upper())
        r.font.name = 'Segoe UI'; r.font.bold = True
        r.font.size = Pt(8.2); r.font.color.rgb = CYAN
        sep = cell.add_paragraph()
        sep.paragraph_format.space_before = Pt(0.2)
        sep.paragraph_format.space_after  = Pt(1.2)
        sep.paragraph_format.left_indent  = Pt(6)
        rs = sep.add_run("━" * 17)
        rs.font.size = Pt(4.5); rs.font.color.rgb = OCEAN

    def sb_t(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(1.0)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.left_indent  = Pt(6)
        r = p.add_run(text)
        r.font.size = Pt(7.6); r.font.color.rgb = ICE

    sb_h(c0, "Contact & Profiles")
    sb_t(c0, "✉  contact@archicam-ai.com")
    sb_t(c0, "✆  +237 695 35 34 02")
    sb_t(c0, "⌂  Douala / Ngaoundéré, CM")
    sb_t(c0, "🐙  github.com/gervais-afk")
    sb_t(c0, "💼  linkedin.com/in/marie-gervais-koa")

    sb_h(c0, "AI & LLM Stack")
    sb_t(c0, "Google Antigravity IDE  ■ ■ ■ ■ ■")
    sb_t(c0, "LangGraph & CrewAI      ■ ■ ■ ■ ■")
    sb_t(c0, "Google Gemma 4 (12B)    ■ ■ ■ ■ ■")
    sb_t(c0, "Gemini 2.5 / 1.5 Pro    ■ ■ ■ ■ ■")
    sb_t(c0, "Google TabFM (Tabular)  ■ ■ ■ ■ ■")
    sb_t(c0, "FastMCP & Genkit        ■ ■ ■ ■ ■")
    sb_t(c0, "Neo4j GraphRAG — Agent K1")

    sb_h(c0, "Data & Graphs")
    sb_t(c0, "Neo4j / Cypher Graph    ■ ■ ■ ■ ■")
    sb_t(c0, "PostgreSQL / pgvector   ■ ■ ■ ■ ■")
    sb_t(c0, "Apache AGE & DuckDB     ■ ■ ■ ■ □")
    sb_t(c0, "BigQuery DataFrames     ■ ■ ■ ■ □")
    sb_t(c0, "Pandas / NumPy ETL      ■ ■ ■ ■ ■")

    sb_h(c0, "Dev & MLOps")
    sb_t(c0, "Python 3.11+ / MLOps    ■ ■ ■ ■ ■")
    sb_t(c0, "FastAPI / Next.js 14    ■ ■ ■ ■ □")
    sb_t(c0, "MLflow & Data Drift     ■ ■ ■ ■ □")
    sb_t(c0, "SHAP Sentinel Audit     ■ ■ ■ ■ ■")
    sb_t(c0, "IfcOpenShell & Shapely  ■ ■ ■ ■ □")
    sb_t(c0, "Docker & Pytest         ■ ■ ■ ■ ■")

    sb_h(c0, "Ethics, Security & Audit")
    sb_t(c0, "◈ CCAA Excellence Attestation '23")
    sb_t(c0, "◈ AVSEC Officer (ICAO Annex 17)")
    sb_t(c0, "◈ AI Ethics & Anti-Hallucination")
    sb_t(c0, "◈ OKF v0.2 SHA-256 No-LLM")
    sb_t(c0, "◈ EU AI Act Compliance (RSASSA)")

    sb_h(c0, "Languages")
    sb_t(c0, "French   —  Native / Fluent")
    sb_t(c0, "English  —  Professional / Tech.")

    # ══════════════ MAIN COLUMN (RIGHT — WHITE) ══════════════
    c1 = table.cell(0, 1)
    c1.width = col_widths[1]
    set_cell_background(c1, "FFFFFF")
    set_cell_margins(c1, top=180, left=200, bottom=100, right=220)

    # Name block
    p_nm = c1.paragraphs[0]
    p_nm.paragraph_format.space_before = Pt(0)
    p_nm.paragraph_format.space_after  = Pt(0.5)
    r = p_nm.add_run("KOA MARIE GERVAIS NELLY")
    r.font.name = 'Segoe UI'; r.font.bold = True
    r.font.size = Pt(20); r.font.color.rgb = NAVY

    p_sub = c1.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after  = Pt(0.8)
    rs = p_sub.add_run("Lead AI Engineer & Data Architect   │   Founder @ Archi Cam AI")
    rs.font.size = Pt(9.2); rs.font.bold = True; rs.font.color.rgb = OCEAN

    p_rule = c1.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(0)
    p_rule.paragraph_format.space_after  = Pt(2.0)
    rr = p_rule.add_run("─" * 70)
    rr.font.size = Pt(5.0); rr.font.color.rgb = OCEAN

    def mn_h(cell, title):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2.6)
        p.paragraph_format.space_after  = Pt(0.1)
        r1 = p.add_run("◈  "); r1.font.bold = True; r1.font.size = Pt(8.2); r1.font.color.rgb = OCEAN
        r2 = p.add_run(title.upper())
        r2.font.name = 'Segoe UI'; r2.font.bold = True
        r2.font.size = Pt(9.6); r2.font.color.rgb = NAVY
        sep = cell.add_paragraph()
        sep.paragraph_format.space_before = Pt(0)
        sep.paragraph_format.space_after  = Pt(1.0)
        rs1 = sep.add_run("━" * 18)
        rs1.font.size = Pt(4.5); rs1.font.color.rgb = OCEAN
        rs2 = sep.add_run("─" * 44)
        rs2.font.size = Pt(4.0); rs2.font.color.rgb = CYAN

    def entry(cell, title, badge):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1.8)
        p.paragraph_format.space_after  = Pt(0.1)
        r1 = p.add_run(title); r1.font.bold = True; r1.font.size = Pt(9.0); r1.font.color.rgb = NAVY
        r2 = p.add_run(f"   —   {badge}")
        r2.font.italic = True; r2.font.size = Pt(7.8); r2.font.color.rgb = OCEAN

    def company(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0.1)
        r = p.add_run(text); r.font.size = Pt(7.8); r.font.bold = True; r.font.color.rgb = MUTED

    def bullet(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0.4)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.left_indent  = Inches(0.08)
        rb = p.add_run("▸  "); rb.font.bold = True; rb.font.size = Pt(7.8); rb.font.color.rgb = OCEAN
        rt = p.add_run(text); rt.font.size = Pt(7.8); rt.font.color.rgb = BODY

    def body(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(1.0)
        p.paragraph_format.line_spacing = 1.06
        r = p.add_run(text); r.font.size = Pt(8.2); r.font.color.rgb = BODY

    def award(cell, title, detail):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0.6)
        p.paragraph_format.space_after  = Pt(0.3)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.left_indent  = Inches(0.08)
        r1 = p.add_run("◈ "); r1.font.bold = True; r1.font.size = Pt(7.8); r1.font.color.rgb = OCEAN
        r2 = p.add_run(title); r2.font.bold = True; r2.font.size = Pt(7.8); r2.font.color.rgb = NAVY
        r3 = p.add_run(f"  —  {detail}")
        r3.font.size = Pt(7.7); r3.font.color.rgb = BODY

    # ── Executive Summary ──
    mn_h(c1, "Executive Summary")
    body(c1, "Applied AI Engineer & Specialist, I design zero-hallucination autonomous agent systems — sovereign, deterministic, and fully explainable. Member of the Google Developer Program and the AICC Accra community, I transform complex data into reliable decisions by leveraging my dual background in civil engineering and data science to build high-impact operational solutions. Founder of Archi Cam AI (Sovereign AI SaaS & 5D BIM), I embody a rigorous, auditable, and results-driven African AI.")

    # ── Flagship AI Projects ──
    mn_h(c1, "Flagship AI Projects")

    entry(c1, "Archi Cam AI", "Agentic AI & 5D BIM Construction SaaS")
    bullet(c1, "Full automation of construction quantity takeoff and cost estimation: eliminating human error and material waste.")
    bullet(c1, "Instant generation of standardized BOQ estimates in <45s (99.2% time savings) and 3D architectural renders.")
    bullet(c1, "Deterministic zero-hallucination structural concrete validation enforcing strict compliance with urban planning codes.")

    entry(c1, "K1-MATHINFO (v3.0.0)", "Sovereign Academic Research & Asset Platform")
    bullet(c1, "Preservation, indexing, and semantic exploration across 28 years of university scientific research (470 Ph.D. theses).")
    bullet(c1, "Intelligent student-to-advisor recommendation (Advisor Matcher) and cryptographic certification of research integrity.")

    entry(c1, "Sovereign.BI Agentic", "Enterprise Business Intelligence & Strategic Decision Engine")
    bullet(c1, "Executive decision enablement: querying complex corporate data warehouses directly in natural language in under 5 seconds.")
    bullet(c1, "Total sovereign enterprise privacy with air-gapped local execution and mathematical explainability for every KPI.")

    entry(c1, "Dataset Automator & VigieSahel", "Climate Resilience & Production MLOps Systems")
    bullet(c1, "Dataset Automator: Autonomous data engineering factory for reliable dataset preparation, fairness audits, and compliance.")
    bullet(c1, "VigieSahel: Sahelian resilience system cutting crop sowing failures by 35% and forecasting meningitis epidemics 14 days ahead.")

    # ── Professional Experience ──
    mn_h(c1, "Professional Experience")

    entry(c1, "AI Lead & Data Science Consultant", "March 2026 – Present")
    company(c1, "Independent Projects & Enterprises  │  Douala, CM")
    bullet(c1, "Ethical sovereign AI systems: GraphRAG Neo4j pipelines, high-dimensional EDA, multi-source RAG architectures.")
    bullet(c1, "Executive decision reporting, automated KPI dashboards, and SHAP explainability audits for African SMEs.")

    entry(c1, "Aviation Security Officer (AVSEC)", "2018 – Present")
    company(c1, "CCAA — Cameroon Civil Aviation Authority  │  Douala, CM")
    bullet(c1, "Threat assessment, secure access control, and regulatory compliance audits (ICAO Annex 17).")
    bullet(c1, "Operational crisis management: emergency team coordination, anti-intrusion protocols.")

    # ── Education ──
    mn_h(c1, "Education & Certifications")

    entry(c1, "M.Sc. in Applied Artificial Intelligence", "Dec. 2025 – 2027  [In Progress]")
    company(c1, "University of Ngaoundéré  │  Cameroon")
    bullet(c1, "ML & Bayesian Statistics, Data Engineering & Neo4j, Computer Vision & Robotics, Ethics & Cybersecurity, Production MLOps.")
    bullet(c1, "Research project: K1-MATHINFO v3 sovereign system — multi-source agent certified OKF v0.2 (SHA-256 No-LLM).")

    entry(c1, "B.Sc. in Civil Engineering (Building Option)", "2015 – 2016")
    company(c1, "ISTDI / IUC Douala  │  Cameroon")
    bullet(c1, "Structural calculations (BAEL 91), quantity surveying, construction project management — AI-applied estimation base.")

    # ── Honors ──
    mn_h(c1, "Honors & Applied AI Distinctions")

    award(c1, "CCAA Attestation of Excellence & Integrity (2023)", "Awarded by the Director General for outstanding operational performance & ethics.")
    award(c1, "Google Cloud #AllThingsAgentic Hackathon", "Dataset Automator v4.0 (Google Antigravity, TabFM, BigQuery DataFrames, WIT).")
    award(c1, "Google Developer Program · AICC Accra", "Active member · Accra AI Community Centre & Google for Startups Accelerator Network.")

    # ── Trailing 1pt paragraph ──
    p_tail = doc.add_paragraph()
    p_tail.paragraph_format.space_before = Pt(0)
    p_tail.paragraph_format.space_after  = Pt(0)
    p_tail.paragraph_format.line_spacing = Pt(1)
    pPr = p_tail._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:spacing {nsdecls("w")} w:before="0" w:after="0" w:line="20" w:lineRule="exact"/>'))
    pPr.append(parse_xml(f'<w:rPr {nsdecls("w")}><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr>'))
    r_tail = p_tail.add_run()
    r_tail.font.size = Pt(1)

    # ── Save DOCX ──
    f_docx = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.docx"
    try:
        doc.save(f_docx)
        print(f"[OK] DOCX saved: {f_docx}")
    except Exception as e:
        print(f"[ERROR] saving DOCX: {e}")
        return

    # ── PDF export via Word COM ──
    try:
        import pythoncom
        import win32com.client

        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        pdf_path = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf"

        d = word.Documents.Open(os.path.abspath(f_docx), ReadOnly=True)
        pages = d.ComputeStatistics(2)
        print(f"[EN] Page Count: {pages}")
        d.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        d.Close(False)
        word.Quit()

        print(f"[OK] PDF saved ({pages} page): {pdf_path}")
    except Exception as ex:
        print(f"[ERROR] Word COM export: {ex}")

    print("EN generation completed!")

if __name__ == "__main__":
    generate_exact_user_1page_cv_en()
