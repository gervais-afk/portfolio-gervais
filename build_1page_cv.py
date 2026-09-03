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

def generate_exact_user_1page_cv():
    doc = Document()

    # FULL-BLEED A4 SETUP
    for s in doc.sections:
        s.page_width = Inches(8.27)    # A4 width (210 mm)
        s.page_height = Inches(11.69)  # A4 height (297 mm)
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
    CYAN_HDR           = RGBColor(0x38, 0xBD, 0xF8)   # Electric Sky Blue
    ICE_WHITE          = RGBColor(0xF8, 0xFA, 0xFC)   # Ice White
    SLATE_MID          = RGBColor(0x94, 0xA3, 0xB8)   # Mid Slate (for subtle sidebar text)
    NAVY               = RGBColor(0x0A, 0x11, 0x28)   # Deep Navy
    OCEAN              = RGBColor(0x02, 0x84, 0xC7)   # Ocean Blue Accent
    BODY               = RGBColor(0x33, 0x41, 0x55)   # Body Slate
    MUTED              = RGBColor(0x64, 0x74, 0x8B)   # Muted Slate

    # STRICT SINGLE ROW TABLE (1 x 2)
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    set_table_zero_indent(table)
    remove_table_borders(table)

    # EXACT A4 height in dxa: 297mm × (1440/25.4) ≈ 16837 dxa
    # Using 'exact' forces the row to fill the full page — blue column reaches the bottom
    row = table.rows[0]
    trPr = row._tr.get_or_add_trPr()
    trHeight = parse_xml(f'<w:trHeight {nsdecls("w")} w:val="16837" w:hRule="exact"/>')
    trPr.append(trHeight)

    col_widths = [Inches(2.60), Inches(5.67)]

    # ========================= SIDEBAR (LEFT — DARK NAVY) =========================
    c0 = table.cell(0, 0)
    c0.width = col_widths[0]
    set_cell_background(c0, SIDEBAR_FILL)
    # left=600 (~10.6mm), right=500 (~8.8mm) — proper breathing room on both sides
    set_cell_margins(c0, top=280, bottom=280, left=600, right=500)

    # --- Photo ---
    photo_path = r"c:\Users\HP\Desktop\portfolio-gervais\assets\images\profile_headshot_circular.jpeg"
    photo_box = c0.add_table(rows=1, cols=1)
    photo_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_cell = photo_box.cell(0, 0)
    p_cell.width = Inches(1.55)
    set_cell_background(p_cell, "1E3A5F")   # richer blue-navy frame
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
        """Section header with decorative underline bar"""
        # Spacer before section
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

        # Thin underline separator
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
    add_sb_section(c0, "Contact & Profils")
    add_sb_item(c0, "✉  magenel85@gmail.com")
    add_sb_item(c0, "✆  +237 695 35 34 02")
    add_sb_item(c0, "⌂  Douala / Ngaoundéré, CM")
    add_sb_item(c0, "⚡  devpost.com/magenel85")
    add_sb_item(c0, "🌐  github.com/gervais-afk")
    add_sb_item(c0, "💼  linkedin.com/in/marie-gervais-koa")
    add_sb_item(c0, "🏅  Google Developer Program")

    # --- IA & LLM Stack ---
    add_sb_section(c0, "IA & LLM Stack")
    add_sb_item(c0, "Google Antigravity IDE  ■ ■ ■ ■ ■")
    add_sb_item(c0, "Google Gemma 4 (12B)    ■ ■ ■ ■ ■")
    add_sb_item(c0, "Gemini 2.5 / 1.5 Pro    ■ ■ ■ ■ ■")
    add_sb_item(c0, "Google TabFM (Tabular)  ■ ■ ■ ■ ■")
    add_sb_item(c0, "LangGraph Multi-Agents  ■ ■ ■ ■ ■")
    add_sb_item(c0, "Firebase Genkit         ■ ■ ■ ■ ■")
    add_sb_item(c0, "Neo4j GraphRAG — Agent K1  ■ ■ ■ ■ ■")

    # --- Data & Graphes ---
    add_sb_section(c0, "Data & Graphes")
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

    # --- Sécurité & Audit ---
    add_sb_section(c0, "Sécurité & Audit")
    add_sb_item(c0, "◈ Gouvernance Quorum 4 Yeux")
    add_sb_item(c0, "◈ OKF v0.2 SHA-256 No-LLM")
    add_sb_item(c0, "◈ EU AI Act (RSASSA-PSS)")
    add_sb_item(c0, "◈ Cadre AVSEC (Annexe 17 OACI)")

    # --- Langues ---
    add_sb_section(c0, "Langues")
    add_sb_item(c0, "Français  —  Courant / Natif")
    add_sb_item(c0, "Anglais   —  Technique & Pro")

    # --- Atouts Clés ---
    add_sb_section(c0, "Atouts Clés")
    add_sb_item(c0, "◈ Double compétence IA & BTP")
    add_sb_item(c0, "◈ Gestion de crise & Sûreté (CCAA)")
    add_sb_item(c0, "◈ Rigueur mathématique & Guardrails")

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
    r_sub = p_sub.add_run("Lead AI Engineer & Consultant IA / Data   │   Fondateur @ Archi Cam AI")
    r_sub.font.size = Pt(9.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = OCEAN

    # Decorative full-width rule
    p_rule = c1.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(0)
    p_rule.paragraph_format.space_after = Pt(5)
    r_rule = p_rule.add_run("─" * 72)
    r_rule.font.size = Pt(6)
    r_rule.font.color.rgb = OCEAN

    # --- Main section helper ---
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
        # Underline rule
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

    # ── Résumé Professionnel ──
    add_section_title(c1, "Résumé Professionnel")
    add_body_text(c1,
        "Consultant IA & Lead AI Engineer (Google Developer Program Member), j'utilise Google Antigravity "
        "pour concevoir et orchestrer des systèmes d'agents autonomes neuro-symboliques, du GraphRAG (Neo4j) "
        "et des plateformes MLOps souveraines. Spécialiste des architectures déterministes et explicables, "
        "je déploie des solutions étanches sans hallucination. Fondateur d'Archi Cam AI (candidat Google "
        "Africa Applied AI Lab), j'allie méthodologie d'ingénieur BTP, rigueur mathématique et vision produit."
    )

    # ── Projets IA Majeurs ──
    add_section_title(c1, "Projets IA Majeurs")

    add_entry_header(c1, "Archi Cam AI", "SaaS IA Agentique & 5D BIM")
    add_bullet(c1, "Candidat officiel Google Africa Applied AI Lab. Développé sous Google Antigravity (Gemma 4 12B, Gemini, BAEL 91).")
    add_bullet(c1, "Génération DQE Excel en <45s (–99,2% temps, R²=0,9872 sous MLflow) et rendus 3D Imagen 3 + ControlNet.")

    add_entry_header(c1, "K1-MATHINFO (v3.0.0)", "IA Souveraine Multi-Agents & Certification OKF")
    add_bullet(c1, "Système souverain DMI (Univ. Ngaoundéré) sous Google Antigravity : 470 thèses, 19 projets M1, graphe Neo4j 1 366 nœuds.")
    add_bullet(c1, "6 agents LangGraph, recherche hybride RRF k=60 + Cross-Encoder, attesteur SHA-256 No-LLM, 77/77 tests (100%).")

    add_entry_header(c1, "Sovereign.BI Agentic", "Business Intelligence & NL-to-SQL/Cypher")
    add_bullet(c1, "Moteur d'interrogation SQL/Graph en langage naturel (PostgreSQL pgvector, Neo4j N10S, latence <5s).")
    add_bullet(c1, "Garde-fous dynamiques anti-injection ABAC et explicabilité certifiée par auditeur SHAP Sentinel.")

    add_entry_header(c1, "Dataset Automator & VigieSahel", "MLOps & IA Impact Agro-Climatique")
    add_bullet(c1, "Dataset Automator : Usine MLOps sous Google Antigravity (TabFM, BigQuery DataFrames, Data Drift KS/PSI, EU AI Act).")
    add_bullet(c1, "VigieSahel : Prédiction épidémies et optimisation semis (–35% pertes, XGBoost R²>94%, Supabase, MLflow).")

    # ── Parcours Professionnel ──
    add_section_title(c1, "Parcours Professionnel")

    add_entry_header(c1, "Consultant IA & Data Science", "2025 – Présent")
    add_company_line(c1, "Projets Indépendants & Entreprises  │  Douala")
    add_bullet(c1, "Accompagnement d'entreprises dans l'adoption d'IA souveraines, pipelines RAG/GraphRAG Neo4j et bases SQL.")
    add_bullet(c1, "Analyse exploratoire de jeux de données massifs, modélisation prédictive et reporting décisionnel exécutif.")

    add_entry_header(c1, "Agent de Sûreté Aéroportuaire (AVSEC)", "2018 – Présent")
    add_company_line(c1, "CCAA (Autorité Aéronautique du Cameroun)")
    add_bullet(c1, "Analyse des risques opérationnels, contrôle d'accès sécurisé et audits de conformité (Annexe 17 OACI).")
    add_bullet(c1, "Rédaction de rapports de sûreté critiques et coordination d'interventions opérationnelles d'urgence.")

    # ── Formation Académique ──
    add_section_title(c1, "Formation Académique")

    add_entry_header(c1, "Master Professionnel en Intelligence Artificielle Appliquée", "2025 – 2027  [En cours]")
    add_company_line(c1, "Université de Ngaoundéré")
    add_bullet(c1, "Programme d'Excellence (5 Blocs) : ML & Statistique Bayésienne, Data Engineering & Neo4j, Vision & Robotique, Cybersécurité & Blockchain, MLOps Souverains.")

    add_entry_header(c1, "Licence & BTS Génie Civil (Option Bâtiment)", "2015 – 2016")
    add_company_line(c1, "ISTDI / IUC Douala")
    add_bullet(c1, "Dimensionnement de structures (BAEL 91), métrés & gestion de projets de construction BTP.")

    # ── Reconnaissances & Candidatures ──
    add_section_title(c1, "Reconnaissances & Candidatures")

    p_rec = c1.add_paragraph()
    p_rec.paragraph_format.space_before = Pt(0)
    p_rec.paragraph_format.space_after = Pt(2)
    p_rec.paragraph_format.line_spacing = 1.2
    r1 = p_rec.add_run("◈ Google Africa Applied AI Lab (Accra, 2026) : ")
    r1.font.bold = True
    r1.font.size = Pt(8.5)
    r1.font.color.rgb = NAVY
    r2 = p_rec.add_run("Candidature officielle portée par la plateforme Archi Cam AI.")
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = BODY

    p_rec2 = c1.add_paragraph()
    p_rec2.paragraph_format.space_before = Pt(0)
    p_rec2.paragraph_format.space_after = Pt(0)
    p_rec2.paragraph_format.line_spacing = 1.2
    r3 = p_rec2.add_run("◈ Hackathon Google Cloud #AllThingsAgentic : ")
    r3.font.bold = True
    r3.font.size = Pt(8.5)
    r3.font.color.rgb = NAVY
    r4 = p_rec2.add_run("Dataset Automator v4.0 conçu sous Google Antigravity (TabFM, WIT, bigframes, MCT).")
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
    f_fr_docx = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV_FR.docx"
    try:
        doc.save(f_fr_docx)
        print(f"Saved: {f_fr_docx}")
    except Exception as e:
        print(f"Error saving {f_fr_docx}: {e}")

    # Export PDF via Word COM
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        pdf_fr = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_CV FR.pdf"

        if os.path.exists(f_fr_docx):
            doc_com = word.Documents.Open(os.path.abspath(f_fr_docx))
            doc_com.SaveAs(os.path.abspath(pdf_fr), FileFormat=17)
            doc_com.Close()
            print(f"Exported PDF: {pdf_fr}")

        word.Quit()
        print("Generated French PDF successfully via Word COM!")
    except Exception as ex:
        print(f"Word COM PDF export note: {ex}")

if __name__ == "__main__":
    generate_exact_user_1page_cv()
