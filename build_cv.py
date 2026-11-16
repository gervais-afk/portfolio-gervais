"""Build bilingual CV assets from profile.json; no network, Word COM or installs.
Usage: python build_cv.py [--lang fr|en|all]
PDF layout fails rather than shrinking below 10 pt or silently adding a page.
"""
from pathlib import Path
import argparse
import html
import json
import shutil
import re
import unicodedata
import tempfile
import hashlib

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT
NAVY, TEXT, MUTED = '#172B3A', '#343A40', '#52606D'
PDF_ACCENT, CONTACT_BLUE = '#30363D', '#2167A5'
PEARL, LINE = '#F3F5F7', '#D5DBE1'
ATS_LABELS = {
    'fr': {'profile': 'Profil', 'projects': 'Projets'},
    'en': {'profile': 'Profile', 'projects': 'Projects'},
}
W, H = A4
MARGIN = 34
BODY = 10.5
LEADING = 13.2

def load_profile():
    return json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))

def contacts(profile, lang):
    i = profile['identity']
    return [
        ('mail', i['email'], 'mailto:' + i['email']),
        ('phone', i['phone'], i['phoneHref']),
        ('pin', i['location'][lang], None),
        ('github', i['github'].removeprefix('https://'), i['github']),
        ('linkedin', i['linkedin'].removeprefix('https://'), i['linkedin']),
        ('dev', i['devto'].removeprefix('https://'), i['devto']),
        ('link', i['website'].removeprefix('https://'), i['website']),
    ]

def register_fonts():
    font_dir = Path('C:/Windows/Fonts')
    for name, filename in [('CV', 'arial.ttf'), ('CV-Bold', 'arialbd.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold', italic='CV', boldItalic='CV-Bold')

def icon(c, kind, x, y):
    """Small vector paths, not font glyphs; y is the bottom of the icon."""
    c.saveState()
    c.translate(x, y)
    c.setStrokeColor(colors.HexColor(CONTACT_BLUE))
    c.setLineWidth(.7)
    p = c.beginPath()
    if kind == 'mail':
        c.roundRect(0, 0, 9, 6, .6, stroke=1, fill=0)
        p.moveTo(0, 6); p.lineTo(4.5, 2.6); p.lineTo(9, 6)
    elif kind == 'phone':
        p.moveTo(1, 7); p.curveTo(-1, 3, 5, -2, 8, 0)
        p.lineTo(6, 2); p.lineTo(4.6, 1.2); p.lineTo(2, 4)
        p.lineTo(3, 5.2); p.lineTo(1, 7)
    elif kind == 'pin':
        p.moveTo(4, -1); p.curveTo(-4, 6, 1, 10, 4, 8)
        p.curveTo(10, 9, 10, 4, 4, -1)
        c.circle(4.5, 5, 1.1, stroke=1, fill=0)
    elif kind == 'linkedin':
        c.roundRect(0, -.5, 9, 9, .8, stroke=1, fill=0)
        c.circle(2, 6, .3, stroke=1, fill=0)
        p.moveTo(2, 1.5); p.lineTo(2, 4.8)
        p.moveTo(4.3, 1.5); p.lineTo(4.3, 4.8)
        p.moveTo(4.3, 3.5); p.curveTo(4.4, 6, 7.2, 5.5, 7.2, 3.5); p.lineTo(7.2, 1.5)
    elif kind == 'github':
        c.circle(4.5, 4, 4.2, stroke=1, fill=0)
        p.moveTo(3.2, -.2); p.lineTo(3.2, 1.8)
        p.curveTo(-.5, 2, 1.5, 5.5, 1.5, 5.5)
        p.lineTo(1.7, 7); p.lineTo(3.3, 6.3)
        p.curveTo(4.2, 6.7, 5, 6.7, 5.8, 6.3)
        p.lineTo(7.3, 7); p.lineTo(7.5, 5.5)
        p.curveTo(9, 3, 6.8, 2, 5.8, 1.8); p.lineTo(5.8, -.2)
    elif kind == 'dev':
        c.roundRect(0, 0, 10, 7, .7, stroke=1, fill=0)
        c.setFillColor(colors.HexColor(CONTACT_BLUE)); c.setFont('CV-Bold', 3.7)
        c.drawString(.7, 2.2, 'DEV')
    else:
        c.circle(4.5, 3.5, 4, stroke=1, fill=0)
        c.ellipse(2.5, -.5, 6.5, 7.5, stroke=1, fill=0)
        p.moveTo(.5, 3.5); p.lineTo(8.5, 3.5)
    c.drawPath(p)
    c.restoreState()

class PDFLayout:
    def __init__(self, path, plain=False):
        self.c = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
        self.plain = plain
        self.y = H - MARGIN
        self.bottom = H
        self.x = MARGIN
        self.width = W - 2 * MARGIN
        self.sidebar = False

    def frame(self, x, width, top, sidebar=False):
        self.x, self.width, self.y, self.sidebar = x, width, top, sidebar

    def paragraph(self, text, size=BODY, bold=False, color=TEXT, indent=0):
        style = ParagraphStyle('cv', fontName='CV-Bold' if bold else 'CV',
                               fontSize=size, leading=LEADING if size == BODY else size * 1.25,
                               textColor=colors.HexColor(color),
                               leftIndent=8 if text.startswith('&#8226;') else 0,
                               firstLineIndent=-8 if text.startswith('&#8226;') else 0)
        paragraph = Paragraph(text, style)
        _, height = paragraph.wrap(self.width - indent, H)
        return paragraph, height

    def text(self, text, size=BODY, bold=False, color=TEXT, after=2, indent=0):
        paragraph, height = self.paragraph(text, size, bold, color, indent)
        self.y -= height
        if self.y < MARGIN:
            raise ValueError(f'CV overflow at {text[:60]!r}: bottom {self.y:.1f}pt')
        paragraph.drawOn(self.c, self.x + indent, self.y)
        self.bottom = min(self.bottom, self.y)
        self.y -= after

    def heading(self, title):
        self.y -= 5 if self.plain else 9
        self.text(html.escape(title.upper()), size=11 if self.sidebar or self.plain else 12,
                  bold=True, color=PDF_ACCENT, after=4 if self.plain else 6)
        if not self.plain:
            self.c.setStrokeColor(colors.HexColor(LINE))
            self.c.setLineWidth(.6)
            self.c.line(self.x, self.y, self.x + self.width, self.y)
            self.y -= 9

    def entry(self, entry, project_index=None):
        project = project_index is not None
        indent = 8 if project else 0
        title = html.escape(entry['title'])
        rows = [(title, 11 if project else BODY, True, PDF_ACCENT, 4)]
        if 'date' in entry:
            rows.append((html.escape(entry['date']), 9.5, False, MUTED, 3))
        if 'context' in entry:
            rows.append((html.escape(entry['context']), 9.5, False, MUTED, 2))
        rows.extend(('&#8226; ' + html.escape(detail) if project else html.escape(detail),
                     BODY, False, TEXT, 3 if project else 2) for detail in entry['details'])
        if 'stack' in entry:
            rows.append((html.escape(entry['stack']), 9.5, True, PDF_ACCENT, 1))
        if project:
            height = sum(self.paragraph(text, size, bold, color, indent)[1] + after for text, size, bold, color, after in rows) + 10
            top = self.y + 2
            self.c.setStrokeColor(colors.HexColor(CONTACT_BLUE if project_index == 1 else LINE))
            self.c.setLineWidth(1.2 if project_index == 1 else .6)
            self.c.line(self.x - 3, top, self.x - 3, top - height)
            self.y -= 4
        for text, size, bold, color, after in rows:
            self.text(text, size=size, bold=bold, color=color, after=after, indent=indent)
        self.y -= 8 if project else 4

def build_pdf(profile, lang):
    data = profile['cv'][lang]
    path = OUTPUT / data['files']['pdf']
    p = PDFLayout(path)
    p.c.setTitle(profile['identity']['name'] + ' | ' + data['title'])
    p.c.setAuthor(profile['identity']['name'])
    identity = profile['identity']
    # Photographic masthead: typography and geometry, not a flattened image of the CV.
    p.c.setFillColor(colors.HexColor(NAVY))
    p.c.rect(0, H - 112, W, 112, fill=1, stroke=0)
    p.c.setFillColor(colors.white)
    p.c.setFont('CV-Bold', 27)
    p.c.drawString(MARGIN, H - 36, identity['familyName'])
    p.c.setFont('CV', 20)
    p.c.drawString(MARGIN, H - 61, identity['givenNames'])
    p.c.setFillColor(colors.HexColor('#E3E9EF'))
    p.c.setFont('CV-Bold', 13.5)
    p.c.drawString(MARGIN, H - 88, data['title'])
    px, py, pw, ph = W - MARGIN - 72, H - 101, 72, 90
    # Fine light frame, restrained corner radius and an actual clipped portrait.
    p.c.setStrokeColor(colors.HexColor('#D5DFE8'))
    p.c.setLineWidth(.8)
    p.c.roundRect(px - 2.5, py - 2.5, pw + 5, ph + 5, 5, fill=0, stroke=1)
    p.c.saveState()
    clipping = p.c.beginPath()
    clipping.roundRect(px, py, pw, ph, 3)
    p.c.clipPath(clipping, stroke=0)
    p.c.drawImage(str(ROOT / identity['photo']), px, py, width=pw, height=ph, mask='auto')
    p.c.restoreState()
    # Contact order stays linear in extraction; all actual URLs remain clickable.
    p.c.setStrokeColor(colors.HexColor(LINE))
    p.c.setLineWidth(.5)
    p.c.line(MARGIN, H - 170, W - MARGIN, H - 170)
    p.y = H - 123
    rows = [contacts(profile, lang)[:3], contacts(profile, lang)[3:5], contacts(profile, lang)[5:]]
    for row_index, row in enumerate(rows):
        widths = [13 + pdfmetrics.stringWidth(label, 'CV', 9.5) for _, label, _ in row]
        available = W - 2 * MARGIN
        if row_index == 0:
            # Email, phone and location share the full width, with balanced gaps.
            gap = (available - sum(widths)) / (len(row) - 1)
            if gap < 10:
                raise ValueError('Contact row needs more horizontal space')
            positions = [MARGIN, MARGIN + widths[0] + gap, W - MARGIN - widths[2]]
        else:
            # Social and publication links align in two stable columns.
            positions = [MARGIN, MARGIN + available * .51]
        for (kind, label, href), x, width in zip(row, positions, widths):
            if x + width > W - MARGIN + .1:
                raise ValueError('Contact row exceeds page width')
            icon(p.c, kind, x, p.y - 8)
            p.c.setFont('CV', 9.5)
            p.c.setFillColor(colors.HexColor(NAVY))
            p.c.drawString(x + 13, p.y - 7, label)
            if href:
                p.c.linkURL(href, (x, p.y - 10, x + width, p.y + 2), relative=0)
        p.y -= 14
    p.y = H - 182
    p.text(html.escape(data['summary']), after=2)
    top = p.y - 4
    sidebar_width, gutter = 164, 24
    main_x = MARGIN + sidebar_width + gutter
    p.c.setFillColor(colors.HexColor(PEARL))
    p.c.roundRect(MARGIN - 9, MARGIN, sidebar_width + 18, top - MARGIN + 3, 5, fill=1, stroke=0)
    # Draw the principal reading column first so plain text extraction stays coherent.
    p.frame(main_x, W - MARGIN - main_x, top)
    p.heading(data['labels']['projects'])
    for index, entry in enumerate(data['projects'], start=1):
        p.entry(entry, project_index=index)
    p.heading(data['labels']['experience'])
    for entry in data['experience']:
        p.entry(entry)
    main_bottom = p.y
    p.frame(MARGIN, sidebar_width, top, sidebar=True)
    p.heading(data['labels']['skills'])
    for item in data['skills']:
        p.text(html.escape(item['label']), size=10, bold=True, color=PDF_ACCENT, after=3)
        p.text(html.escape(item['text']), size=10, after=8)
    p.heading(data['labels']['education'])
    for entry in data['education']:
        p.entry(entry)
    p.heading(data['labels']['additional'])
    p.text(html.escape(data['languages']), size=10, after=2)
    p.heading(data['labels']['award'])
    p.text(html.escape(data['award']), size=10, after=0, color=MUTED)
    print(f'{lang.upper()} columns: main bottom {main_bottom:.1f} pt; sidebar bottom {p.y:.1f} pt')
    p.c.save()
    print(f'{lang.upper()} PDF: 1 page, body {BODY} pt, bottom {p.bottom:.1f} pt')
    return path

def build_ats_pdf(profile, lang):
    """Single-column application companion: ordinary selectable text, no images or shapes."""
    data, identity = profile['cv'][lang], profile['identity']
    p = PDFLayout(OUTPUT / data['files']['atsPdf'], plain=True)
    p.c.setTitle(identity['name'] + ' | ' + data['title'] + ' | Application')
    p.c.setAuthor(identity['name'])
    p.text(html.escape(identity['name']), size=20, bold=True, after=4)
    p.text(html.escape(data['title']), size=12, bold=True, after=7)
    all_contacts = contacts(profile, lang)
    for row in [all_contacts[:3], all_contacts[3:5], all_contacts[5:]]:
        values = []
        for _, label, href in row:
            label = html.escape(label)
            values.append(f'<link href="{html.escape(href, quote=True)}">{label}</link>' if href else label)
        p.text(' | '.join(values), size=9.5, after=3)
    p.heading(ATS_LABELS[lang]['profile'])
    p.text(html.escape(data['summary']), after=2)
    for key in ['projects', 'experience']:
        p.heading(ATS_LABELS[lang].get(key, data['labels'][key]))
        for entry in data[key]:
            title = html.escape(entry['title'])
            if 'date' in entry:
                title += ' <font size="9.5"> | ' + html.escape(entry['date']) + '</font>'
            p.text(title, bold=True, after=2)
            if 'context' in entry:
                p.text(html.escape(entry['context']), size=9.5, after=2)
            for detail in entry['details']:
                p.text(html.escape(detail), after=2)
            if 'stack' in entry:
                p.text(html.escape(entry['stack']), size=9.5, after=2)
            p.y -= 3
    p.heading(data['labels']['skills'])
    for item in data['skills']:
        p.text('<b>' + html.escape(item['label']) + '</b> : ' + html.escape(item['text']), after=3)
    p.heading(data['labels']['education'])
    for entry in data['education']:
        title = html.escape(entry['title']) + ' <font size="9.5"> | ' + html.escape(entry['date']) + '</font>'
        p.text(title, bold=True, after=2)
        for detail in entry['details']:
            p.text(html.escape(detail), after=3)
    p.heading(data['labels']['additional'])
    p.text(html.escape(data['languages']), after=2)
    p.heading(data['labels']['award'])
    p.text(html.escape(data['award']), after=0)
    p.c.save()
    print(f'{lang.upper()} application PDF: 1 column, no photo, body {BODY} pt, bottom {p.bottom:.1f} pt')


def docx_hyperlink(paragraph, text, href):
    link = OxmlElement('w:hyperlink')
    link.set(qn('r:id'), paragraph.part.relate_to(href, RT.HYPERLINK, is_external=True))
    run = OxmlElement('w:r')
    props = OxmlElement('w:rPr')
    color = OxmlElement('w:color'); color.set(qn('w:val'), CONTACT_BLUE[1:]); props.append(color)
    size = OxmlElement('w:sz'); size.set(qn('w:val'), '19'); props.append(size)
    run.append(props)
    node = OxmlElement('w:t'); node.text = text; run.append(node)
    link.append(run); paragraph._p.append(link)

def build_docx(profile, lang):
    data = profile['cv'][lang]
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Mm(210), Mm(297)
    section.top_margin = section.bottom_margin = Mm(11)
    section.left_margin = section.right_margin = Mm(12)
    normal = doc.styles['Normal']
    normal.font.name = 'Arial'
    normal.font.size = Pt(BODY)
    normal.font.color.rgb = RGBColor.from_string(TEXT[1:])
    normal.paragraph_format.space_after = Pt(1)
    normal.paragraph_format.line_spacing = Pt(13.5)
    # Body content is in ordinary paragraphs; only the photographic masthead uses a table.
    def para(text='', bold=False, size=BODY, color=TEXT, after=1, before=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.widow_control = True
        r = p.add_run(text); r.bold = bold; r.font.size = Pt(size)
        r.font.color.rgb = RGBColor.from_string(color[1:])
        return p
    def heading(key):
        p = para(data['labels'][key].upper(), bold=True, size=11, color=PDF_ACCENT, before=6, after=4)
        p.paragraph_format.keep_with_next = True
        border = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        for key, value in [('val', 'single'), ('sz', '4'), ('color', LINE[1:]), ('space', '4')]: bottom.set(qn('w:' + key), value)
        border.append(bottom); p._p.get_or_add_pPr().append(border)
    def entry(e, project_index=None):
        text = e['title'] + (' · ' + e['date'] if 'date' in e else '')
        p = para(text, bold=True); p.paragraph_format.keep_with_next = True
        # Linear editable companion: no project cards or colour blocks.
        if 'context' in e:
            para(e['context'], size=9.5, color=MUTED)
        for text in e['details']:
            para(text, after=2)
        if 'stack' in e:
            para(e['stack'], size=9.5, color=MUTED)
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
    masthead = doc.add_table(rows=1, cols=2)
    masthead.autofit = False
    masthead.columns[0].width, masthead.columns[1].width = Mm(150), Mm(36)
    for cell in masthead.rows[0].cells:
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        fill = OxmlElement('w:shd'); fill.set(qn('w:fill'), NAVY[1:]); cell._tc.get_or_add_tcPr().append(fill)
    left, right = masthead.rows[0].cells
    name = left.paragraphs[0]
    name.paragraph_format.line_spacing = Pt(27)
    name.paragraph_format.space_after = Pt(4)
    for text, size, bold in [(profile['identity']['familyName'] + '\n', 28, True), (profile['identity']['givenNames'], 20, False)]:
        run = name.add_run(text); run.font.size = Pt(size); run.bold = bold; run.font.color.rgb = RGBColor(255,255,255)
    role = left.add_paragraph(data['title'])
    role.paragraph_format.space_after = Pt(8)
    for run in role.runs: run.font.size = Pt(13); run.font.color.rgb = RGBColor.from_string('E3E9EF')
    picture = right.paragraphs[0]
    picture.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    picture.paragraph_format.space_before = picture.paragraph_format.space_after = Pt(5)
    picture.add_run().add_picture(str(ROOT / profile['identity']['photo']), width=Mm(26), height=Mm(32.5))
    all_contacts = contacts(profile, lang)
    for row in [all_contacts[:3], all_contacts[3:5], all_contacts[5:]]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        for index, (_, label, href) in enumerate(row):
            if index: p.add_run('  ·  ').font.size = Pt(9.5)
            if href: docx_hyperlink(p, label, href)
            else: p.add_run(label).font.size = Pt(9.5)
    para(data['summary'], before=4, after=3)
    for key in ['projects', 'experience']:
        heading(key)
        for index, e in enumerate(data[key], start=1): entry(e, index if key == 'projects' else None)
    heading('skills')
    for item in data['skills']:
        p = para(); p.add_run(item['label'] + ' · ').bold = True; p.add_run(item['text'])
    heading('education')
    for e in data['education']: entry(e)
    heading('additional')
    para(data['languages'])
    heading('award')
    para(data['award'])
    doc.core_properties.title = profile['identity']['name'] + ' | ' + data['title']
    doc.core_properties.author = profile['identity']['name']
    doc.save(OUTPUT / data['files']['docx'])

def normalise(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text)).replace('\u00ad', '')

def validate(profile, lang, ats=False):
    data = profile['cv'][lang]
    reader = PdfReader(OUTPUT / data['files']['atsPdf' if ats else 'pdf'])
    assert len(reader.pages) == 1, f'{lang}: PDF is not one page'
    page = reader.pages[0]
    assert abs(float(page.mediabox.width) - W) < .1
    assert abs(float(page.mediabox.height) - H) < .1
    extracted = normalise(page.extract_text())
    expected = [profile['identity']['name'], data['title'], data['summary'], data['languages'], data['award']]
    expected += [label for _, label, _ in contacts(profile, lang)]
    labels = dict(data['labels'])
    if ats:
        labels.update(ATS_LABELS[lang])
    expected += list(labels.values())
    for key in ['experience', 'projects', 'education']:
        for e in data[key]:
            expected += [e['title'], *e['details']]
            expected += [e[k] for k in ['date', 'context', 'stack'] if k in e]
    for item in data['skills']: expected += list(item.values())
    for text in expected:
        assert normalise(text).lower() in extracted.lower(), f'{lang}: missing selectable text: {text}'
    uris = {a.get_object().get('/A', {}).get('/URI') for a in page.get('/Annots', [])}
    assert {href for _, _, href in contacts(profile, lang) if href} <= uris
    assert '\u25a0' not in extracted and '\ufffd' not in extracted
    resources = page['/Resources'].get('/XObject')
    images = resources.get_object() if resources else {}
    has_image = any(obj.get_object().get('/Subtype') == '/Image' for obj in images.values())
    if ats:
        assert not has_image, f'{lang}: application PDF must not contain a photo'
        painting = {b'Do', b're', b'S', b's', b'f', b'F', b'f*', b'B', b'B*', b'b', b'b*'}
        assert not any(operator in painting for _, operator in page.get_contents().operations), \
            f'{lang}: unexpected decoration in application PDF'
        order = [profile['identity']['name'], data['title'], ATS_LABELS[lang]['profile'], data['summary'],
                 ATS_LABELS[lang]['projects'], *[e['title'] for e in data['projects']],
                 labels['experience'], *[e['title'] for e in data['experience']],
                 labels['skills'], labels['education'], labels['additional'], labels['award']]
        cursor = 0
        for text in order:
            position = extracted.lower().find(normalise(text).lower(), cursor)
            assert position >= cursor, f'{lang}: non-linear application reading order at {text}'
            cursor = position + len(normalise(text))
    else:
        assert has_image, f'{lang}: portrait missing'
    print(f'{lang.upper()} {"application" if ats else "presentation"} QA: exact A4, full selectable content, '
          f'{"no photo, linear order" if ats else "embedded portrait"}, 6 clickable links, no missing glyph markers')

def build(languages=('fr', 'en')):
    global OUTPUT
    profile = load_profile()
    register_fonts()
    (ROOT / 'scratch').mkdir(exist_ok=True)
    # Generate and validate every requested PDF before replacing any published asset.
    with tempfile.TemporaryDirectory(prefix='cv_build_', dir=ROOT / 'scratch') as staging:
        OUTPUT = Path(staging)
        (OUTPUT / 'profile.js').write_text('// Generated by build_cv.py from profile.json. Do not edit.\nwindow.PORTFOLIO_PROFILE = ' + json.dumps(profile, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
        for lang in languages:
            build_pdf(profile, lang)
            build_ats_pdf(profile, lang)
            build_docx(profile, lang)
            validate(profile, lang)
            validate(profile, lang, ats=True)
            if lang == 'fr':
                shutil.copyfile(OUTPUT / profile['cv']['fr']['files']['pdf'], OUTPUT / 'KOA_MARIE_GERVAIS_NELLY_CV FR.pdf')
        for file in OUTPUT.iterdir():
            file.replace(ROOT / file.name)
    OUTPUT = ROOT
    cv_html = ROOT / 'cv.html'
    if cv_html.is_file():
        digest = hashlib.sha256((ROOT / 'profile.js').read_bytes()).hexdigest()[:10]
        source = cv_html.read_text(encoding='utf-8')
        source = re.sub(r'(src="profile\.js)(?:\?[^\"]*)?(\")', lambda match: match[1] + '?v=' + digest + match[2], source)
        cv_html.write_text(source, encoding='utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lang', choices=['fr', 'en', 'all'], default='all')
    args = parser.parse_args()
    build(('fr', 'en') if args.lang == 'all' else (args.lang,))
