import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def generate_exact_user_1page_cv_fr():
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
    rb = p_badge.add_run("Fondateur  ·  Archi Cam AI")
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

    sb_h(c0, "Contact & Profils")
    sb_t(c0, "✉  contact@archicam-ai.com")
    sb_t(c0, "✆  +237 695 35 34 02")
    sb_t(c0, "⌂  Douala / Ngaoundéré, CM")
    sb_t(c0, "🐙  github.com/gervais-afk")
    sb_t(c0, "✍  dev.to/gervais_marie")
    sb_t(c0, "💼  linkedin.com/in/marie-gervais-koa")

    sb_h(c0, "IA & LLM Stack")
    sb_t(c0, "Google Antigravity IDE  ■ ■ ■ ■ ■")
    sb_t(c0, "LangGraph & CrewAI      ■ ■ ■ ■ ■")
    sb_t(c0, "Google Gemma 4 (12B)    ■ ■ ■ ■ ■")
    sb_t(c0, "Gemini 2.5 / 1.5 Pro    ■ ■ ■ ■ ■")
    sb_t(c0, "Google TabFM (Tabular)  ■ ■ ■ ■ ■")
    sb_t(c0, "FastMCP & Genkit        ■ ■ ■ ■ ■")
    sb_t(c0, "Neo4j GraphRAG — Agent K1")

    sb_h(c0, "Data & Graphes")
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

    sb_h(c0, "Éthique, Sûreté & Audit")
    sb_t(c0, "◈ Attestation Excellence CCAA '23")
    sb_t(c0, "◈ Agent AVSEC (Annexe 17 OACI)")
    sb_t(c0, "◈ Éthique IA & Anti-Hallucination")
    sb_t(c0, "◈ OKF v0.2 SHA-256 No-LLM")
    sb_t(c0, "◈ Conformité EU AI Act (RSASSA)")

    sb_h(c0, "Langues")
    sb_t(c0, "Français  —  Courant / Natif")
    sb_t(c0, "Anglais   —  Tech. & Écrit / Oral Interm.")

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
    rs = p_sub.add_run("Lead AI Engineer & Spécialiste IA Appliquée   │   Fondateur @ Archi Cam AI")
    rs.font.size = Pt(9.4); rs.font.bold = True; rs.font.color.rgb = OCEAN

    p_rule = c1.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(0)
    p_rule.paragraph_format.space_after  = Pt(1.5)
    rr = p_rule.add_run("─" * 70)
    rr.font.size = Pt(5.0); rr.font.color.rgb = OCEAN

    def mn_h(cell, title):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2.2)
        p.paragraph_format.space_after  = Pt(0.1)
        r1 = p.add_run("◈  "); r1.font.bold = True; r1.font.size = Pt(8.0); r1.font.color.rgb = OCEAN
        r2 = p.add_run(title.upper())
        r2.font.name = 'Segoe UI'; r2.font.bold = True
        r2.font.size = Pt(9.8); r2.font.color.rgb = NAVY
        sep = cell.add_paragraph()
        sep.paragraph_format.space_before = Pt(0)
        sep.paragraph_format.space_after  = Pt(1.0)
        rs1 = sep.add_run("━" * 18)
        rs1.font.size = Pt(4.5); rs1.font.color.rgb = OCEAN
        rs2 = sep.add_run("─" * 44)
        rs2.font.size = Pt(4.0); rs2.font.color.rgb = CYAN

    def entry(cell, title, badge):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1.6)
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
        p.paragraph_format.space_after  = Pt(0.4)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.left_indent  = Pt(10)
        rb = p.add_run("▸  ")
        rb.font.bold = True; rb.font.size = Pt(7.5); rb.font.color.rgb = OCEAN
        rt = p.add_run(text)
        rt.font.size = Pt(8.2); rt.font.color.rgb = BODY

    def body(cell, text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0.4)
        p.paragraph_format.space_after  = Pt(1.0)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(text)
        r.font.size = Pt(8.5); r.font.color.rgb = BODY

    def award(cell, title, detail):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1.2)
        p.paragraph_format.space_after  = Pt(0.4)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.left_indent  = Pt(10)
        r1 = p.add_run("◆  ")
        r1.font.bold = True; r1.font.size = Pt(7.5); r1.font.color.rgb = OCEAN
        r2 = p.add_run(f"{title}  —  ")
        r2.font.name = 'Segoe UI'; r2.font.bold = True; r2.font.size = Pt(8.2); r2.font.color.rgb = NAVY
        r3 = p.add_run(detail)
        r3.font.name = 'Segoe UI'; r3.font.size = Pt(8.2); r3.font.color.rgb = BODY

    # ── Résumé Professionnel ──
    mn_h(c1, "Résumé Professionnel")
    body(c1, "Ingénieur spécialisé en IA appliquée et architectures d'agents autonomes, je conçois des systèmes déterministes, explicables et souverains à zéro hallucination. Membre du Google Developer Program, j'articule la rigueur mathématique du génie civil et la data science avancée pour résoudre des problématiques industrielles complexes. Fondateur d'Archi Cam AI (SaaS BIM 5D & estimation prédictive), je bâtis des solutions auditables, robustes et orientées vers un fort impact opérationnel.")

    # ── Projets IA Majeurs ──
    mn_h(c1, "Projets IA Majeurs")

    entry(c1, "Archi Cam AI", "SaaS IA & Chiffrage BIM 5D pour le BTP")
    bullet(c1, "Automatisation intégrale du chiffrage et métrés gros œuvre : élimine les erreurs d'estimation et le surcoût de matériaux.")
    bullet(c1, "Génération instantanée de devis normés (DQE) en moins de 45s (gain de 99,2% de temps) et projections visuelles 3D.")
    bullet(c1, "Calculs de structures béton armé déterministes zéro-hallucination conformes aux règles d'urbanisme.")

    entry(c1, "K1-MATHINFO (v3.2.0)", "Valorisation & Recherche Académique Souveraine")
    bullet(c1, "GraphRAG sur 30 ans d'archives (471 thèses DMI, 4 494 relations Neo4j), routage LatentGate (5,2 ms) et vCache (0% FP).")
    bullet(c1, "WRRF tri-moteur (P@5=96,4%), inférence S-GRPO, certification OKF v0.2 SHA-256 No-LLM, 192 tests (100%) et article Dev.to.")

    entry(c1, "Sovereign.BI Agentic", "Pilotage Stratégique & Décisionnel d'Entreprise")
    bullet(c1, "Démocratisation de l'aide à la décision : interrogation des entrepôts de données en langage naturel en moins de 5s.")
    bullet(c1, "Étanchéité souveraine absolue en réseau fermé (zéro fuite) et audit mathématique de causalité de chaque KPI.")

    entry(c1, "Dataset Automator & VigieSahel", "IA à Fort Impact & Résilience Agro-Climatique")
    bullet(c1, "Dataset Automator : Usine MLOps autonome (TabFM, PAIR WIT, scellés EU AI Act RSASSA-PSS) et publication Dev.to.")
    bullet(c1, "VigieSahel : Résilience sahélienne réduisant de 35% les échecs de semis et alertant 14 jours avant les flambées.")

    # ── Parcours Professionnel ──
    mn_h(c1, "Parcours Professionnel")

    entry(c1, "Consultant IA & Data Science", "Mars 2026 – Présent")
    company(c1, "Projets Indépendants & Entreprises  │  Douala, CM")
    bullet(c1, "Systèmes IA souverains éthiques : pipelines GraphRAG Neo4j, EDA haute dimension, architectures RAG multi-sources.")
    bullet(c1, "Reporting exécutif, dashboards KPI automatisés et audits d'explicabilité SHAP pour PME.")

    entry(c1, "Agent de Sûreté Aéroportuaire (AVSEC)", "2018 – Présent")
    company(c1, "CCAA — Autorité Aéronautique du Cameroun  │  Douala, CM")
    bullet(c1, "Évaluation des menaces, contrôle strict des accès sécurisés, conformité réglementaire ICAO Annexe 17.")
    bullet(c1, "Gestion de crises opérationnelles : coordination d'équipes en situation d'urgence, protocoles anti-intrusion.")

    # ── Formation Académique ──
    mn_h(c1, "Formation Académique")

    entry(c1, "Master Pro. — Intelligence Artificielle Appliquée", "Déc. 2025 – 2027  [En cours]")
    company(c1, "Université de Ngaoundéré  │  Cameroun")
    bullet(c1, "ML & Stats Bayésienne, Data Engineering Neo4j, Vision & Robotique, Éthique & Cybersécurité, MLOps Souverains.")
    bullet(c1, "Projet de recherche : système K1-MATHINFO v3.2 — agent multi-sources certifié OKF v0.2 (SHA-256 No-LLM, 192 tests).")

    entry(c1, "Licence & BTS Génie Civil (Option Bâtiment)", "2015 – 2016")
    company(c1, "ISTDI / IUC Douala  │  Cameroun")
    bullet(c1, "Dimensionnement structures (BAEL 91), métrés et gestion de projets BTP — base de l'IA appliquée au BTP.")

    # ── Reconnaissances ──
    mn_h(c1, "Reconnaissances & Distinctions")

    award(c1, "Attestation d'Excellence & Intégrité CCAA (2023)", "Décernée par le Directeur Général pour performance et déontologie opérationnelle.")
    award(c1, "Publications Techniques DEV Community (2026)", "Auteur d'articles deep-dive : Zero-Hallucination GraphRAG & Dataset Automator MLOps.")
    award(c1, "Google Cloud #AllThingsAgentic Hackathon", "Dataset Automator v4.0 (Google Antigravity, TabFM, BigQuery DataFrames, WIT).")
    award(c1, "Google Developer Program · AICC Accra", "Membre actif · Accra AI Community Centre & Google for Startups Accelerator Network.")

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

    f_docx = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_FR.docx"
    doc.save(f_docx)
    print(f"[OK] FR DOCX saved to {f_docx}")

    # ── PDF export via Word COM ──
    try:
        import pythoncom
        import win32com.client
        import shutil

        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        pdf_path = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_FR.pdf"
        pdf_space = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV FR.pdf"

        d = word.Documents.Open(os.path.abspath(f_docx), ReadOnly=True)
        pages = d.ComputeStatistics(2)
        print(f"[FR] Page Count: {pages}")
        d.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        d.Close(False)
        word.Quit()

        if pages == 1:
            print(f"[OK] PDF saved (1 page): {pdf_path}")
            shutil.copyfile(pdf_path, pdf_space)
            print(f"[OK] PDF copied to: {pdf_space}")
        else:
            print(f"[WARN] Multi-page detected ({pages} pages)!")
    except Exception as e:
        print(f"[WARN] Word COM export: {e}")

if __name__ == "__main__":
    generate_exact_user_1page_cv_fr()
    print("FR generation completed!")
