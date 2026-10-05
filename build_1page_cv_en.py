import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def generate_exact_user_1page_cv_en():
    doc = Document()
    for s in doc.sections:
        s.page_width  = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = 0
        s.header_distance = 0
        s.footer_distance = 0

    doc.styles['Normal'].font.name = 'Segoe UI'
    doc.styles['Normal'].font.size = Pt(8.2)

    SIDEBAR_FILL = "0F172A"
    CYAN   = RGBColor(0x38, 0xBD, 0xF8)
    ICE    = RGBColor(0xF8, 0xFA, 0xFC)
    NAVY   = RGBColor(0x0A, 0x11, 0x28)
    OCEAN  = RGBColor(0x02, 0x84, 0xC7)
    BODY   = RGBColor(0x33, 0x41, 0x55)
    MUTED  = RGBColor(0x64, 0x74, 0x8B)

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    
    # helper functions
    def set_cell_background(cell, fill_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=140, left=400, bottom=0, right=160):
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

    tblPr = table._tbl.tblPr
    tblInd = parse_xml(f'<w:tblInd {nsdecls("w")} w:w="0" w:type="dxa"/>')
    tblPr.append(tblInd)
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/><w:left w:val="none"/>'
        f'<w:bottom w:val="none"/><w:right w:val="none"/>'
        f'<w:insideH w:val="none"/><w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    row = table.rows[0]
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:trHeight {nsdecls("w")} w:val="16550" w:hRule="atLeast"/>'))

    col_widths = [Inches(2.62), Inches(5.65)]

    # ── SIDEBAR ──
    c0 = table.cell(0, 0)
    c0.width = col_widths[0]
    set_cell_background(c0, SIDEBAR_FILL)
    set_cell_margins(c0, top=140, left=400, bottom=0, right=160)

    photo_path = r"c:\Users\HP\Desktop\portfolio-gervais\assets\images\profile_headshot_circular.jpeg"
    p_ph = c0.paragraphs[0]
    p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ph.paragraph_format.space_before = Pt(0)
    p_ph.paragraph_format.space_after  = Pt(0)
    if os.path.exists(photo_path):
        p_ph.add_run().add_picture(photo_path, width=Inches(1.48))

    p_badge = c0.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_before = Pt(3.0)
    p_badge.paragraph_format.space_after  = Pt(1.5)
    rb = p_badge.add_run("Founder  ·  Archi Cam AI")
    rb.font.name = 'Segoe UI'; rb.font.bold = True
    rb.font.size = Pt(7.4); rb.font.color.rgb = CYAN

    def sb_h(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(9.2)
        p.paragraph_format.space_after  = Pt(0)
        p.paragraph_format.left_indent  = Pt(5)
        r = p.add_run(text.upper())
        r.font.name = 'Segoe UI'; r.font.bold = True
        r.font.size = Pt(9.2); r.font.color.rgb = CYAN
        sep = cell.add_paragraph()
        sep.paragraph_format.space_before = Pt(0.2)
        sep.paragraph_format.space_after  = Pt(1.8)
        sep.paragraph_format.left_indent  = Pt(5)
        rs = sep.add_run("━" * 18)
        rs.font.size = Pt(4.5); rs.font.color.rgb = OCEAN

    def sb_t(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(2.5)
        p.paragraph_format.line_spacing = 1.08
        p.paragraph_format.left_indent  = Pt(5)
        r = p.add_run(text)
        r.font.size = Pt(8.3); r.font.color.rgb = ICE

    sb_h(c0, "Contact & Profiles")
    sb_t(c0, "✉  contact@archicam-ai.com")
    sb_t(c0, "✆  +237 695 35 34 02")
    sb_t(c0, "⌂  Douala / Ngaoundéré, CM")
    sb_t(c0, "🐙  github.com/gervais-afk")
    sb_t(c0, "✍  dev.to/gervais_marie")
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
    sb_t(c0, "English  —  Tech & Written / Spoken Interm.")

    # ── MAIN COLUMN ──
    c1 = table.cell(0, 1)
    c1.width = col_widths[1]
    set_cell_background(c1, "FFFFFF")
    set_cell_margins(c1, top=140, left=180, bottom=0, right=190)

    p_nm = c1.paragraphs[0]
    p_nm.paragraph_format.space_before = Pt(0)
    p_nm.paragraph_format.space_after  = Pt(0.4)
    r = p_nm.add_run("KOA MARIE GERVAIS NELLY")
    r.font.name = 'Segoe UI'; r.font.bold = True
    r.font.size = Pt(20.5); r.font.color.rgb = NAVY

    p_sub = c1.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after  = Pt(0.6)
    rs = p_sub.add_run("AI Systems Architect & Data Engineer   │   Founder @ Archi Cam AI")
    rs.font.size = Pt(9.4); rs.font.bold = True; rs.font.color.rgb = OCEAN

    p_rule = c1.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(0)
    p_rule.paragraph_format.space_after  = Pt(1.5)
    rr = p_rule.add_run("─" * 70)
    rr.font.size = Pt(5.0); rr.font.color.rgb = OCEAN

    def mn_h(cell, title):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after  = Pt(0.1)
        r1 = p.add_run("◈  "); r1.font.bold = True; r1.font.size = Pt(8.0); r1.font.color.rgb = OCEAN
        r2 = p.add_run(title.upper())
        r2.font.name = 'Segoe UI'; r2.font.bold = True
        r2.font.size = Pt(9.8); r2.font.color.rgb = NAVY
        sep = cell.add_paragraph()
        sep.paragraph_format.space_before = Pt(0)
        sep.paragraph_format.space_after  = Pt(0.6)
        rs1 = sep.add_run("━" * 18)
        rs1.font.size = Pt(4.5); rs1.font.color.rgb = OCEAN
        rs2 = sep.add_run("─" * 44)
        rs2.font.size = Pt(4.0); rs2.font.color.rgb = CYAN

    def entry(cell, title, badge):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1.2)
        p.paragraph_format.space_after  = Pt(0.1)
        r1 = p.add_run(title); r1.font.bold = True; r1.font.size = Pt(9.4); r1.font.color.rgb = NAVY
        r2 = p.add_run(f"   —   {badge}")
        r2.font.italic = True; r2.font.size = Pt(8.1); r2.font.color.rgb = OCEAN

    def company(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0.1)
        r = p.add_run(text)
        r.font.italic = True; r.font.size = Pt(8.1); r.font.color.rgb = MUTED

    def bullet(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0.25)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.left_indent  = Pt(10)
        rb = p.add_run("▸  ")
        rb.font.bold = True; rb.font.size = Pt(7.5); rb.font.color.rgb = OCEAN
        rt = p.add_run(text)
        rt.font.size = Pt(8.2); rt.font.color.rgb = BODY

    def body(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0.3)
        p.paragraph_format.space_after  = Pt(0.7)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(text)
        r.font.size = Pt(8.4); r.font.color.rgb = BODY

    def award(cell, title, detail):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0.8)
        p.paragraph_format.space_after  = Pt(0.25)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.left_indent  = Pt(10)
        r1 = p.add_run("◆  ")
        r1.font.bold = True; r1.font.size = Pt(7.5); r1.font.color.rgb = OCEAN
        r2 = p.add_run(f"{title}  —  ")
        r2.font.name = 'Segoe UI'; r2.font.bold = True; r2.font.size = Pt(8.2); r2.font.color.rgb = NAVY
        r3 = p.add_run(detail)
        r3.font.name = 'Segoe UI'; r3.font.size = Pt(8.2); r3.font.color.rgb = BODY

    # ── Executive Summary ──
    mn_h(c1, "Executive Summary")
    body(c1, "AI Systems Architect & Data Engineer designing and deploying mission-critical autonomous multi-agent architectures, Neo4j GraphRAG, and sovereign production MLOps pipelines. Specialized in deterministic zero-hallucination systems, neuro-symbolic reasoning, and verifiable algorithmic trust. Founder of Archi Cam AI (5D BIM), bridging structural engineering rigor with modern systems engineering for high-impact enterprise solutions.")

    # ── Flagship AI Projects ──
    mn_h(c1, "Flagship AI Projects")

    entry(c1, "Archi Cam AI", "Agentic AI & 5D BIM Construction SaaS")
    bullet(c1, "Full automation of construction quantity takeoff and cost estimation: eliminating human error and material waste.")
    bullet(c1, "Instant generation of standardized BOQ estimates in <45s (99.2% time savings) and 3D architectural renders.")
    bullet(c1, "Deterministic zero-hallucination structural concrete validation enforcing strict compliance with urban planning codes.")

    entry(c1, "K1-MATHINFO (v3.2.0)", "Sovereign Academic Research Platform")
    bullet(c1, "GraphRAG over 30 yrs archives (471 theses DMI, 4,494 Neo4j relations), LatentGate (5.2ms) & vCache (0% FP).")
    bullet(c1, "Tri-engine WRRF (P@5=96.4%), S-GRPO, OKF v0.2 SHA-256 No-LLM, 192 tests (100%), and Dev.to deep-dive.")

    entry(c1, "Sovereign.BI Agentic", "Enterprise Business Intelligence & Decisions")
    bullet(c1, "Executive decision enablement: querying complex corporate data warehouses directly in natural language in under 5 seconds.")
    bullet(c1, "Total sovereign enterprise privacy with air-gapped local execution and mathematical explainability for every KPI.")

    entry(c1, "Dataset Automator & VigieSahel", "Climate Resilience & Production MLOps")
    bullet(c1, "Dataset Automator: MLOps data factory (TabFM, PAIR WIT, EU AI Act RSASSA-PSS seals) and Dev.to publication.")
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

    # ── Education & Certifications ──
    mn_h(c1, "Education & Certifications")

    entry(c1, "M.Sc. in Applied Artificial Intelligence", "Dec. 2025 – 2027  [In Progress]")
    company(c1, "University of Ngaoundéré  │  Cameroon")
    bullet(c1, "ML & Bayesian Statistics, Data Engineering & Neo4j, Computer Vision & Robotics, Ethics & Cybersecurity, Production MLOps.")
    bullet(c1, "Research project: K1-MATHINFO v3.2 sovereign system — multi-source agent certified OKF v0.2 (SHA-256 No-LLM, 192 tests).")

    entry(c1, "B.Sc. in Civil Engineering (Building Option)", "2015 – 2016")
    company(c1, "ISTDI / IUC Douala  │  Cameroon")
    bullet(c1, "Structural calculations (BAEL 91), quantity surveying, construction project management — AI-applied estimation base.")

    # ── Honors & Distinctions ──
    mn_h(c1, "Honors & Applied AI Distinctions")

    award(c1, "CCAA Attestation of Excellence & Integrity (2023)", "Awarded by the Director General for outstanding operational performance & ethics.")
    award(c1, "Technical Publications on DEV Community (2026)", "Author of architectural deep-dives: Zero-Hallucination GraphRAG & Dataset Automator MLOps.")
    award(c1, "Google Cloud #AllThingsAgentic Hackathon", "Dataset Automator v4.0 (Google Antigravity, TabFM, BigQuery DataFrames, WIT).")
    award(c1, "AICC Accra & Startup Ecosystem", "Active member · Accra AI Community Centre & Google for Startups Accelerator Network.")

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

    docx_path = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.docx"
    doc.save(docx_path)
    print(f"[OK] DOCX saved: {docx_path}")

    # ── PDF export via Word COM ──
    try:
        import pythoncom
        import win32com.client

        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        pdf_path = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf"

        d = word.Documents.Open(os.path.abspath(docx_path), ReadOnly=True)
        pages = d.ComputeStatistics(2)
        print(f"[EN] Page Count: {pages}")
        d.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        d.Close(False)
        word.Quit()

        if pages == 1:
            print(f"[OK] PDF saved (1 page): {pdf_path}")
        else:
            print(f"[WARN] Multi-page detected ({pages} pages)!")
    except Exception as e:
        print(f"[WARN] Word COM export: {e}")

if __name__ == "__main__":
    generate_exact_user_1page_cv_en()
    print("EN generation completed!")
