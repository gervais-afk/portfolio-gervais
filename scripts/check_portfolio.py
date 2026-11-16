"""Local regression checks. Requires installed Playwright, Edge and pypdf.
Run from the repository root while http.server listens on 127.0.0.1:4173.
Does not test external websites or download the large audio archives.
"""
from pathlib import Path
import json
import re
import unicodedata
from urllib.parse import unquote, urlparse
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch' / 'qa'
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:4173'
results = []

def record(name, data):
    results.append({'check': name, 'result': data})
    print(name, json.dumps(data, ensure_ascii=False))

with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
    errors, failures = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: failures.append(f'{response.status} {response.url}') if response.status >= 400 else None)
    page.goto(BASE)
    page.locator('h1').wait_for()
    assert page.locator('.project-card').count() == 3
    assert page.locator('.secondary-card').count() == 3
    assert page.locator('.journey-item').count() == 4
    assert page.locator('[data-i18n]').evaluate_all('(els)=>els.every(el=>window.PORTFOLIO_CONTENT.fr.ui[el.dataset.i18n]!==undefined)')
    assert not page.locator('audio').get_attribute('src')
    assert page.evaluate("performance.getEntriesByType('resource').filter(r=>r.name.includes('/audio/')).length") == 0
    record('Initial audio requests', 0)
    page.evaluate('document.fonts.ready')
    assert page.evaluate('document.fonts.check(\'600 16px "Manrope"\')')
    assert page.evaluate('document.fonts.check(\'italic 400 32px "Newsreader"\')')
    assert page.locator('.project-art').count() == 3
    for art in page.locator('.project-art').all():
        art.scroll_into_view_if_needed()
        art.evaluate('(el)=>el.decode()')
        assert art.get_attribute('alt') == ''
        assert art.evaluate('(el)=>el.naturalWidth > 0')
    assert page.locator('.art-caption').count() == 3
    assert not page.evaluate("performance.getEntriesByType('resource').some(r=>/fonts\\.(googleapis|gstatic)\\.com/.test(r.name))")
    record('Local fonts and three labelled project compositions', 'OK')
    # All internal resources, assets and in-document destinations resolve.
    paths = page.locator('[href], [src]').evaluate_all('(els)=>els.map(el=>el.getAttribute("href")||el.getAttribute("src"))')
    for path in paths:
        if path.startswith('#'):
            assert page.locator(path).count() == 1, path
        elif not re.match(r'^[a-zA-Z]+:', path):
            local = ROOT / unquote(urlparse(path).path)
            assert local.is_file(), str(local)
    # Content equivalence and source parity in both languages.
    for lang in ['fr', 'en']:
        page.locator(f'[data-lang="{lang}"]').click()
        assert page.locator('html').get_attribute('lang') == lang
        assert page.locator('[data-i18n]').evaluate_all('(els)=>els.every(el=>el.textContent===window.PORTFOLIO_CONTENT[document.documentElement.lang].ui[el.dataset.i18n])')
        assert page.locator('.hero-buttons [data-cv-page]').get_attribute('href') == f'cv.html?lang={lang}'
        assert page.locator('[data-cv-page]').first.get_attribute('href') == f'cv.html?lang={lang}'
        for project in ['k1', 'archi', 'dataset', 'sovereign', 'asu', 'vigie']:
            button = page.locator(f'[data-project="{project}"]')
            button.click()
            assert page.locator('dialog').evaluate('(el)=>el.open')
            assert page.locator('#project-dialog-title').evaluate('(el)=>el===document.activeElement')
            expected_images = {'k1':2,'archi':2,'dataset':1}.get(project,0)
            assert page.locator('.project-gallery img').count() == expected_images
            for image in page.locator('.project-gallery img').all():
                image.scroll_into_view_if_needed()
                image.evaluate('(el)=>el.decode()')
                assert image.get_attribute('alt')
                assert image.evaluate('(el)=>el.naturalWidth > 0')
            assert page.locator('#project-dialog-content .scope-note').is_visible() or page.locator('#project-dialog-content .scope-note').count() == 1
            for key in ['Tab'] * 10 + ['Shift+Tab'] * 10:
                page.keyboard.press(key)
                assert page.evaluate('document.querySelector("dialog").contains(document.activeElement)')
            page.keyboard.press('Escape')
            assert not page.locator('dialog').evaluate('(el)=>el.open')
            assert button.evaluate('(el)=>el===document.activeElement')
        record('Language and six accessible dialogs', lang)
    # Close button, backdrop and clipboard feedback without modifying the system clipboard.
    page.locator('[data-project="k1"]').click()
    page.locator('.dialog-close').click()
    assert not page.locator('dialog').evaluate('(el)=>el.open')
    page.locator('[data-project="k1"]').click()
    page.mouse.click(2, 2)
    assert not page.locator('dialog').evaluate('(el)=>el.open')
    page.evaluate('Object.defineProperty(navigator, "clipboard", {configurable:true,value:{writeText:async text=>{window.__copied=text;}}})')
    page.locator('.copy-email').click()
    assert page.evaluate('window.__copied') == 'contact@archicam-ai.com'
    assert page.locator('#copy-status').inner_text() == 'Address copied'
    record('Close controls and email feedback', 'OK')
    # All common viewport widths have no horizontal overflow; mobile menu works.
    for width in [320, 375, 390, 768, 1024, 1440, 1920]:
        page.set_viewport_size({'width': width, 'height': 900})
        page.goto(BASE)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow {width}'
        if width <= 800:
            toggle = page.locator('.menu-toggle')
            toggle.click()
            assert toggle.get_attribute('aria-expanded') == 'true'
            assert page.locator('#main-nav').is_visible()
            page.keyboard.press('Escape')
            assert toggle.get_attribute('aria-expanded') == 'false'
            toggle.click()
            page.locator('#main-nav a[href="#contact"]').click()
            assert toggle.get_attribute('aria-expanded') == 'false'
        record('Responsive viewport', width)
    # Changing the motion preference during a visit must reveal every entrance.
    page.emulate_media(reduced_motion='reduce')
    assert page.locator('.reveal-ready:not(.is-visible)').count() == 0
    # Full-page shots with reduced motion; no hidden one-shot entrances.
    for lang in ['fr', 'en']:
        page.set_viewport_size({'width': 1440, 'height': 1000})
        page.goto(BASE + '/?lang=' + lang)
        assert page.locator('.reveal-ready').count() == 0
        for image in page.locator('.project-art').all():
            image.evaluate('(el)=>{el.loading="eager";}')
            image.evaluate('(el)=>el.decode()')
        page.screenshot(path=str(OUT / f'portfolio_{lang}_desktop.png'), full_page=True)
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(BASE)
    for image in page.locator('.project-art').all():
        image.evaluate('(el)=>{el.loading="eager";}')
        image.evaluate('(el)=>el.decode()')
    page.screenshot(path=str(OUT / 'portfolio_fr_mobile.png'), full_page=True)
    # Audio selection never auto-plays or preloads media.
    page.locator('#audio-details summary').click()
    assert page.locator('audio').get_attribute('preload') == 'none'
    assert page.locator('audio').evaluate('(el)=>el.paused')
    page.locator('#audio-select').select_option('5')
    assert 'aviation_security' in page.locator('audio').get_attribute('src')
    assert page.locator('audio').evaluate('(el)=>el.paused')
    for filename in page.evaluate('Array.from(document.scripts).map(s=>s.src)'):
        assert filename.startswith(BASE)
    # CV Web print one page A4, all text selectable, desktop and mobile fit.
    for lang in ['fr', 'en']:
        page.set_viewport_size({'width': 1440, 'height': 1000})
        page.goto(BASE + '/cv.html?lang=' + lang)
        page.locator('#cv h1').wait_for()
        assert page.locator('html').get_attribute('lang') == lang
        assert page.locator('#download-pdf').get_attribute('href').endswith(f'_{lang.upper()}.pdf')
        assert page.locator('.cv-photo').evaluate('(el)=>el.complete && el.naturalWidth >= 400')
        assert page.locator('#cv section h2').first.get_attribute('id') == 'heading-projects'
        assert page.locator('#heading-additional + p').inner_text() == json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))['cv'][lang]['languages']
        page.screenshot(path=str(OUT / f'cv_{lang}_web.png'), full_page=True)
        pdf = OUT / f'cv_{lang}_web_print.pdf'
        page.pdf(path=str(pdf), format='A4', print_background=True, prefer_css_page_size=True)
        reader = PdfReader(pdf)
        assert len(reader.pages) == 1, f'{lang} CV Web printed as {len(reader.pages)} pages'
        text = re.sub(r'\s+', '', unicodedata.normalize('NFKC', reader.pages[0].extract_text())).lower()
        profile = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
        data = profile['cv'][lang]
        assert page.locator('#download-ats').get_attribute('href') == data['files']['atsPdf']
        assert page.locator('#download-ats').get_attribute('aria-describedby') == 'download-note'
        for selector in ['#download-ats', '#download-pdf']:
            assert page.locator(selector).inner_text() in page.locator(selector).get_attribute('aria-label')
        assert page.locator('#heading-award + p').inner_text() == data['award']
        assert page.locator('.project-details').count() == 3
        assert page.locator('.project-details li').count() == sum(len(item['details']) for item in data['projects'])
        for key in ['pdf', 'atsPdf', 'docx']:
            response = page.request.get(BASE + '/' + data['files'][key])
            assert response.status == 200, f'{lang}: {key} download unavailable'
            assert response.body() == (ROOT / data['files'][key]).read_bytes(), f'{lang}: stale {key} download'
        expected = [profile['identity']['name'], data['title'], data['summary'], data['languages'], data['award'], *data['labels'].values()]
        for key in ['projects', 'experience', 'education']:
            for entry in data[key]:
                expected.extend([entry['title'], *entry['details']])
                expected.extend(entry[k] for k in ['context', 'date', 'stack'] if k in entry)
        for item in data['skills']: expected.extend(item.values())
        for value in expected:
            assert re.sub(r'\s+', '', unicodedata.normalize('NFKC', value)).lower() in text, f'{lang}: Web print missing {value}'
        images = reader.pages[0]['/Resources']['/XObject'].get_object()
        assert any(obj.get_object().get('/Subtype') == '/Image' for obj in images.values())
        assert page.locator('.project-index').count() == 0
        for width in [320, 390, 600, 640, 641, 768, 840, 1024]:
            page.set_viewport_size({'width': width, 'height': 844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'CV overflow {width}'
            main = page.locator('.cv-main').bounding_box()
            sidebar = page.locator('.cv-sidebar').bounding_box()
            if width <= 640:
                assert sidebar['y'] >= main['y'] + main['height'], f'{lang}: mobile columns overlap'
            else:
                assert sidebar['x'] + sidebar['width'] <= main['x'], f'{lang}: desktop columns overlap'
            assert page.locator('#heading-projects').evaluate('(el)=>getComputedStyle(el,"::before").content') == 'none'
        page.set_viewport_size({'width':390,'height':844})
        page.screenshot(path=str(OUT / f'cv_{lang}_mobile.png'), full_page=True)
        record('CV Web responsive, embedded portrait and full A4 single-page content', lang)
    # The French fallback actually contains the selected projects without scripts.
    context = browser.new_context(java_script_enabled=False, viewport={'width':1440,'height':1000})
    fallback = context.new_page()
    fallback.goto(BASE)
    assert fallback.locator('.project-card h3').all_text_contents() == ['K1-MathInfo','Archi Cam AI','Dataset Automator']
    assert fallback.locator('.journey-item').count() == 4
    assert fallback.locator('.skill-card').count() == 3
    assert fallback.locator('.article-card').count() == 2
    record('French static fallback', 'complete')
    assert not errors, errors
    assert not failures, failures
    record('Browser JavaScript errors / HTTP errors', {'errors':errors,'http':failures})
    browser.close()
(OUT / 'checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print('All portfolio checks passed.')
