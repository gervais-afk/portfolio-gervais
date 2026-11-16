"""Read-only checks of presentation and application PDFs against profile.json.
Reports stay in scratch/qa; no network, recruitment platform or ATS certification.
"""
from pathlib import Path
import json
import re
import unicodedata
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch' / 'qa'
OUT.mkdir(exist_ok=True)
profile = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
normalise = lambda text: re.sub(r'\s+', '', unicodedata.normalize('NFKC', text)).replace('\u00ad', '').lower()
identity = profile['identity']
results = []

for lang in ['fr', 'en']:
    data = profile['cv'][lang]
    values = [identity['name'], data['title'], data['summary'], data['languages'], data['award'],
              identity['email'], identity['phone'], identity['location'][lang]]
    for key in ['github', 'linkedin', 'devto', 'website']:
        values.append(identity[key].removeprefix('https://'))
    for group in ['projects', 'experience', 'education']:
        for entry in data[group]:
            values.extend([entry['title'], *entry['details']])
            values.extend(entry[key] for key in ['date', 'context', 'stack'] if key in entry)
    for skill in data['skills']:
        values.extend(skill.values())
    for variant in ['pdf', 'atsPdf']:
        reader = PdfReader(ROOT / data['files'][variant])
        assert len(reader.pages) == 1, (lang, variant, 'page count')
        page = reader.pages[0]
        assert abs(float(page.mediabox.width) - 595.276) < .1
        assert abs(float(page.mediabox.height) - 841.89) < .1
        extracted = normalise(page.extract_text())
        for value in values:
            assert normalise(value) in extracted, (lang, variant, 'missing content', value)
        links = {annotation.get_object().get('/A', {}).get('/URI') for annotation in page.get('/Annots', [])}
        required = {identity[key] for key in ['github', 'linkedin', 'devto', 'website']}
        required.update(['mailto:' + identity['email'], identity['phoneHref']])
        assert required <= links, (lang, variant, 'missing clickable contact')
        objects = page['/Resources'].get('/XObject')
        images = [obj for obj in objects.get_object().values() if obj.get_object().get('/Subtype') == '/Image'] if objects else []
        if variant == 'atsPdf':
            assert not images, (lang, 'unexpected application image')
            painting = {b'Do', b're', b'S', b's', b'f', b'F', b'f*', b'B', b'B*', b'b', b'b*'}
            assert not any(operator in painting for _, operator in page.get_contents().operations)
            expected_order = [identity['name'], data['title'], data['summary']]
            for group in ['projects', 'experience', 'education']:
                expected_order.extend(entry['title'] for entry in data[group])
            expected_order.extend([data['languages'], data['award']])
            cursor = 0
            for value in expected_order:
                position = extracted.find(normalise(value), cursor)
                assert position >= cursor, (lang, 'non-linear application content', value)
                cursor = position + len(normalise(value))
            runs = []
            def visitor(text, cm, tm, font, size):
                if text.strip():
                    x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
                    y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
                    runs.append((x, y, size))
            page.extract_text(visitor_text=visitor)
            assert min(size for _, _, size in runs) >= 9.5, 'Unexpected small application text'
            assert min(x for x, _, _ in runs) >= 33, 'Text outside left margin'
            assert min(y for _, y, _ in runs) >= 33, 'Text outside bottom margin'
        else:
            assert images, (lang, 'presentation portrait missing')
        result = {'language': lang, 'variant': variant, 'file': data['files'][variant], 'pages': 1,
                  'fullContent': True, 'clickableContacts': 6, 'photo': bool(images)}
        results.append(result)
        print(f'{lang.upper()} {variant}: one A4 page, all common facts, six clickable contacts, photo={bool(images)}')

assert (ROOT / profile['cv']['fr']['files']['pdf']).read_bytes() == (ROOT / 'KOA_MARIE_GERVAIS_NELLY_CV FR.pdf').read_bytes()
(OUT / 'cv_variant_checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print('Presentation/application parity and French alias verified. No commercial ATS was tested.')
