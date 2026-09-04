import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_undp_cover_letter():
    doc = docx.Document()

    # A4 dimensions
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.65)
        section.bottom_margin = Inches(0.65)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    NAVY  = RGBColor(0x0A, 0x11, 0x28)
    OCEAN = RGBColor(0x02, 0x84, 0xC7)
    BODY  = RGBColor(0x27, 0x37, 0x4D)
    MUTED = RGBColor(0x52, 0x6D, 0x82)

    # ── Header / Letterhead ──
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after  = Pt(1)
    r_nm = p_name.add_run("KOA MARIE GERVAIS NELLY")
    r_nm.font.name = 'Segoe UI'
    r_nm.font.bold = True
    r_nm.font.size = Pt(17)
    r_nm.font.color.rgb = NAVY

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after  = Pt(3)
    r_ti = p_title.add_run("Lead AI Engineer & Data Architect   │   M.Sc. Candidate in Applied AI")
    r_ti.font.name = 'Segoe UI'
    r_ti.font.bold = True
    r_ti.font.size = Pt(9.2)
    r_ti.font.color.rgb = OCEAN

    p_contact = doc.add_paragraph()
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after  = Pt(4)
    r_co = p_contact.add_run("Douala / Ngaoundéré, Cameroon   •   magenel85@gmail.com   •   +237 695 35 34 02   •   linkedin.com/in/marie-gervais-koa")
    r_co.font.name = 'Segoe UI'
    r_co.font.size = Pt(8.2)
    r_co.font.color.rgb = MUTED

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after  = Pt(7)
    r_d = p_div.add_run("━" * 65)
    r_d.font.size = Pt(4.5)
    r_d.font.color.rgb = OCEAN

    # Date
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(0)
    p_date.paragraph_format.space_after  = Pt(4)
    r_dt = p_date.add_run("September 4, 2026")
    r_dt.font.name = 'Segoe UI'
    r_dt.font.bold = True
    r_dt.font.size = Pt(8.8)
    r_dt.font.color.rgb = NAVY

    # Recipient
    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.space_before = Pt(0)
    p_rec.paragraph_format.space_after  = Pt(5)
    p_rec.paragraph_format.line_spacing = 1.12
    r_r1 = p_rec.add_run("To: Selection Committee\n")
    r_r1.font.bold = True
    r_r2 = p_rec.add_run("Digital, AI and Innovation (DAI) Hub  │  Bureau for Policy and Programme Support (BPPS)\n")
    r_r3 = p_rec.add_run("United Nations Development Programme (UNDP)\n")
    r_r4 = p_rec.add_run("Job Identification: 33001 — Digital, AI and Innovation Internship: Global Call for 2026")
    r_r4.font.italic = True
    for r in [r_r1, r_r2, r_r3, r_r4]:
        r.font.name = 'Segoe UI'
        r.font.size = Pt(8.6)
        r.font.color.rgb = NAVY

    # Subject line
    p_subj = doc.add_paragraph()
    p_subj.paragraph_format.space_before = Pt(2)
    p_subj.paragraph_format.space_after  = Pt(5)
    r_sb = p_subj.add_run("SUBJECT: Application for Digital, AI and Innovation Internship (Home-Based)")
    r_sb.font.name = 'Segoe UI'
    r_sb.font.bold = True
    r_sb.font.size = Pt(9.2)
    r_sb.font.color.rgb = OCEAN

    # Salutation
    p_sal = doc.add_paragraph()
    p_sal.paragraph_format.space_before = Pt(0)
    p_sal.paragraph_format.space_after  = Pt(3)
    r_sl = p_sal.add_run("Dear Members of the Selection Committee,")
    r_sl.font.name = 'Segoe UI'
    r_sl.font.size = Pt(8.8)
    r_sl.font.color.rgb = NAVY

    def add_p(text, before=0, after=3.5, space=1.12):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after  = Pt(after)
        p.paragraph_format.line_spacing = space
        r = p.add_run(text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(8.6)
        r.font.color.rgb = BODY
        return p

    def add_bullet(bold_head, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(2.5)
        p.paragraph_format.line_spacing = 1.10
        p.paragraph_format.left_indent  = Inches(0.15)
        rb = p.add_run("▪  ")
        rb.font.bold = True
        rb.font.size = Pt(8.6)
        rb.font.color.rgb = OCEAN

        rh = p.add_run(bold_head + ": ")
        rh.font.bold = True
        rh.font.size = Pt(8.6)
        rh.font.color.rgb = NAVY

        rt = p.add_run(text)
        rt.font.size = Pt(8.6)
        rt.font.color.rgb = BODY

    # Intro
    add_p(
        "I am writing to express my enthusiastic application for the Digital, AI and Innovation Internship within UNDP's "
        "Bureau for Policy and Programme Support (BPPS). Currently enrolled in a Master's degree in Applied Artificial "
        "Intelligence at the University of Ngaoundéré (Cameroon) following a Civil Engineering degree (B.Sc.), I design "
        "sovereign, ethical, and high-impact AI systems. I am eager to contribute my technical acumen, product development "
        "experience, and commitment to digital public goods to UNDP's mission of accelerating the Sustainable Development Goals (SDGs)."
    )

    # Bullets
    add_bullet(
        "AI Product Build & Systems Innovation",
        "As founder of Archi Cam AI (official applicant to the Google Africa Applied AI Lab 2026), I developed an agentic platform combining Gemma and Gemini LLMs with 5D BIM standards to automate construction cost estimation and planning (<45s, R²=0.9872). Furthermore, I engineered K1-MATHINFO v3, a sovereign multi-agent GraphRAG architecture indexing 470 academic theses with Neo4j and LangGraph, incorporating OKF zero-hallucination verification protocols."
    )

    add_bullet(
        "Data-Driven Impact for Climate & Vulnerable Regions",
        "Driven by the 'Leave No One Behind' principle, I co-developed VigieSahel, an agro-climatic forecasting system combining XGBoost predictive models and Supabase to reduce crop seeding losses by 35% and anticipate epidemic risks by 14 days in the Sahel region. Additionally, through Dataset Automator (Google Cloud Hackathon), I built MLOps pipelines implementing KS/PSI data drift monitoring and EU AI Act alignment frameworks."
    )

    add_bullet(
        "Rigor, Ethics & Operational Crisis Management",
        "In addition to my AI expertise, my background as an Aviation Security Officer (AVSEC) at the Cameroon Civil Aviation Authority has instilled a deep respect for strict international regulatory frameworks (ICAO Annex 17), crisis coordination, and high-pressure delivery. I apply this operational discipline to AI governance, emphasizing explainability (SHAP Sentinel Audit), fairness, and responsible data policies."
    )

    # Conclusion
    add_p(
        "Joining the UNDP DAI Hub represents an exceptional opportunity to put cutting-edge technology at the service of "
        "Country Offices, local communities, and multilateral digital transformation. Available for a 3-month home-based arrangement, "
        "I am prepared to contribute immediately with dedication, cultural adaptability, and high energy."
    )

    add_p("Thank you very much for your time and consideration. I welcome the opportunity to discuss my application with you.", after=4)

    # Sign-off
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(0)
    p_sign.paragraph_format.space_after  = Pt(1)
    r_sg = p_sign.add_run("Sincerely,")
    r_sg.font.name = 'Segoe UI'
    r_sg.font.size = Pt(8.8)
    r_sg.font.color.rgb = NAVY

    p_author = doc.add_paragraph()
    p_author.paragraph_format.space_before = Pt(0)
    p_author.paragraph_format.space_after  = Pt(0)
    r_au = p_author.add_run("KOA MARIE GERVAIS NELLY")
    r_au.font.name = 'Segoe UI'
    r_au.font.bold = True
    r_au.font.size = Pt(9.5)
    r_au.font.color.rgb = NAVY

    p_sub_au = doc.add_paragraph()
    p_sub_au.paragraph_format.space_before = Pt(0)
    p_sub_au.paragraph_format.space_after  = Pt(0)
    r_sau = p_sub_au.add_run("Lead AI Engineer & Graduate Student in Applied AI  │  Founder @ Archi Cam AI")
    r_sau.font.name = 'Segoe UI'
    r_sau.font.size = Pt(8.2)
    r_sau.font.color.rgb = OCEAN

    # Trailing 1pt paragraph
    p_tail = doc.add_paragraph()
    p_tail.paragraph_format.space_before = Pt(0)
    p_tail.paragraph_format.space_after  = Pt(0)
    p_tail.paragraph_format.line_spacing = Pt(1)
    pPr = p_tail._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:spacing {nsdecls("w")} w:before="0" w:after="0" w:line="20" w:lineRule="exact"/>'))
    pPr.append(parse_xml(f'<w:rPr {nsdecls("w")}><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr>'))
    r_tail = p_tail.add_run()
    r_tail.font.size = Pt(1)

    # Save
    out_docx = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_COVER_LETTER_UNDP.docx"
    doc.save(out_docx)
    print(f"Saved DOCX: {out_docx}")

    # PDF Export with Word COM
    try:
        import win32com.client
        import pythoncom
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc_com = word.Documents.Open(out_docx)
        page_count = doc_com.ComputeStatistics(2)
        print(f"Cover Letter Page Count: {page_count}")
        out_pdf = r"c:\Users\HP\Desktop\portfolio-gervais\KOA_MARIE_GERVAIS_NELLY_COVER_LETTER_UNDP.pdf"
        doc_com.SaveAs(out_pdf, FileFormat=17)
        doc_com.Close()
        word.Quit()
        print(f"Exported PDF: {out_pdf}")
    except Exception as e:
        print(f"PDF export warning: {e}")

if __name__ == "__main__":
    create_undp_cover_letter()
