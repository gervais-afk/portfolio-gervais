"""Optional Word pagination check (Windows + Microsoft Word + pywin32).
Opens the generated DOCX read-only, exports temporary QA PDFs, closes its own Word instance.
Never replaces the canonical ReportLab PDFs.
"""
from pathlib import Path
import json
import re
import unicodedata
import win32com.client
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch' / 'qa'
OUT.mkdir(exist_ok=True)
profile = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
normalise = lambda text: re.sub(r'\s+', '', unicodedata.normalize('NFKC', text)).replace('\u00ad', '').lower()
word = win32com.client.DispatchEx('Word.Application')
word.Visible = False
word.DisplayAlerts = 0
results = []
try:
    for lang in ['fr', 'en']:
        data = profile['cv'][lang]
        doc = word.Documents.Open(str(ROOT / data['files']['docx']), ReadOnly=True, AddToRecentFiles=False)
        try:
            doc.Repaginate()
            pages = doc.ComputeStatistics(2)
            assert pages == 1, f'{lang}: {pages} Word pages'
            target = OUT / f'cv_{lang}_word_print.pdf'
            doc.ExportAsFixedFormat(str(target), 17)
        finally:
            doc.Close(False)
        reader = PdfReader(target)
        assert len(reader.pages) == 1
        text = normalise(reader.pages[0].extract_text())
        expected = [profile['identity']['name'], data['title'], data['summary'], data['languages'], data['award']]
        for key in ['experience', 'projects', 'education']:
            for entry in data[key]:
                expected.extend([entry['title'], *entry['details']])
                expected.extend(entry[k] for k in ['context', 'date', 'stack'] if k in entry)
        for item in data['skills']: expected.extend(item.values())
        for value in expected: assert normalise(value) in text, f'{lang}: missing text: {value}'
        results.append({'lang': lang, 'wordPages': pages, 'pdfPages': len(reader.pages), 'fullText': True})
        print(f'{lang.upper()}: Word and exported PDF 1 page, full content selectable.')
finally:
    word.Quit()
(OUT / 'word_checks.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
