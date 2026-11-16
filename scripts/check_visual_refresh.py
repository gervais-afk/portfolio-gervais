"""Extra regression checks for the portfolio's local visual refresh.
Requires the local preview on port 4173, Playwright and installed Edge.
No external site requests, deployment or commercial accessibility certification.
"""
from pathlib import Path
import hashlib
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch' / 'qa'
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:4173'
report = []

with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(reduced_motion='reduce')
    page = context.new_page()
    for lang in ['fr', 'en']:
        for width in [320, 375, 390, 600, 768, 800, 801, 1024, 1280, 1440, 1920]:
            page.set_viewport_size({'width': width, 'height': 1000})
            page.goto(BASE + '/?lang=' + lang)
            page.evaluate('document.fonts.ready')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (lang, width, 'overflow')
            assert page.locator('.hero-role').inner_text() == ('Ingénieur IA & Architecte Data' if lang == 'fr' else 'AI Engineer & Data Architect')
            for selector in ['.hero-copy', '.portrait-frame', '.project-copy', '.project-visual', '.email-address']:
                for element in page.locator(selector).all():
                    box = element.bounding_box()
                    assert box and box['x'] >= -1 and box['x'] + box['width'] <= width + 1, (lang, width, selector, box)
            # Genuine prose should never require tiny type, including tablet layouts.
            for selector in ['.hero-description', '.project-description', '.skill-card > p:not(.tools)', '.article-card > p:not(.eyebrow)']:
                for element in page.locator(selector).all():
                    size = element.evaluate('(el)=>parseFloat(getComputedStyle(el).fontSize)')
                    assert size >= 14, (lang, width, selector, size)
            report.append({'language':lang, 'width':width, 'overflow':False})
        page.set_viewport_size({'width':1440,'height':1000})
        page.goto(BASE + '/?lang=' + lang)
        page.evaluate('document.fonts.ready')
        page.screenshot(path=str(OUT / f'refresh_{lang}_hero.png'))
        for image in page.locator('.project-art').all():
            image.evaluate('(el)=>{el.loading="eager";}')
            image.evaluate('(el)=>el.decode()')
        for selector, name in [('#projects','projects'), ('#contact','contact')]:
            page.locator(selector).screenshot(path=str(OUT / f'refresh_{lang}_{name}.png'))
    # Supplied-image galleries fit the native dialog and enlargement links work.
    for lang in ['fr', 'en']:
        for width in [320, 768, 1440]:
            page.set_viewport_size({'width':width,'height':900})
            page.goto(BASE + '/?lang=' + lang)
            for project, count in [('k1',2),('archi',2),('dataset',1)]:
                page.locator(f'[data-project="{project}"]').click()
                assert page.locator('.project-gallery img').count() == count
                assert page.locator('dialog').evaluate('(el)=>el.scrollWidth <= el.clientWidth')
                for image in page.locator('.project-gallery img').all():
                    image.scroll_into_view_if_needed()
                    image.evaluate('(el)=>el.decode()')
                if lang == 'fr' and width == 1440 and project == 'archi':
                    page.locator('dialog').screenshot(path=str(OUT / 'archi_media_gallery.png'))
                page.keyboard.press('Escape')
    page.goto(BASE)
    with page.expect_popup() as popup_info:
        page.locator('.project-k1 .project-art-link').click()
    popup = popup_info.value
    popup.wait_for_load_state()
    assert popup.url.endswith('/k1-composition-1440.webp')
    popup.close()
    # Full operation without a server remains supported; local font CORS restrictions
    # may cause system font fallback in some browsers, but content must remain usable.
    page.goto((ROOT / 'index.html').as_uri())
    assert page.locator('.project-open').count() == 6
    page.locator('[data-lang="en"]').click()
    assert page.locator('html').get_attribute('lang') == 'en'
    page.locator('[data-project="dataset"]').click()
    assert page.locator('dialog').evaluate('(el)=>el.open')
    page.keyboard.press('Escape')
    assert not page.locator('dialog').evaluate('(el)=>el.open')
    # French content is still usable with JavaScript disabled on a narrow viewport.
    nojs = browser.new_context(java_script_enabled=False, viewport={'width':320,'height':900})
    fallback = nojs.new_page()
    fallback.goto(BASE)
    assert fallback.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert fallback.locator('.project-art').count() == 3
    assert fallback.locator('.hero-buttons a[href*="cv.html"]').is_visible()
    browser.close()

# All five supplied source files are preserved exactly.
manifest = json.loads((ROOT / 'assets/images/projects/media-sources.json').read_text(encoding='utf-8'))
assert len(manifest) == 5
for item in manifest.values():
    assert hashlib.sha256((ROOT / item['source']).read_bytes()).hexdigest() == item['sourceSha256']
    assert (ROOT / 'assets/images/projects' / item['output']).is_file()
# Fingerprint the existing CV files for comparison in delivery notes.
cv_hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('KOA*CV*.pdf')}
(OUT / 'visual_refresh_checks.json').write_text(json.dumps({'viewports':report,'fileMode':True,'mobileNoJS':True,'cvSha256':cv_hashes},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Visual refresh: {len(report)} FR/EN viewport checks; local file interactions; mobile no-JS passed.')
