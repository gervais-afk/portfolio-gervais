"""Local automated accessibility regression, not a full WCAG certification.
Requires Playwright, Edge, preview :4173 and axe-core 4.10.3 at
scratch/qa/axe-4.10.3.min.js (audit dependency only; never shipped in the page).
Source: https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch' / 'qa'
AXE = OUT / 'axe-4.10.3.min.js'
assert AXE.is_file(), 'Download the documented axe-core audit dependency first.'
results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(reduced_motion='reduce')
    for lang, width in [('fr',1440), ('en',1440), ('fr',390), ('en',320)]:
        page.set_viewport_size({'width':width, 'height':1000})
        page.goto('http://127.0.0.1:4173/?lang=' + lang)
        page.evaluate('document.fonts.ready')
        page.add_script_tag(path=str(AXE))
        states = ['page', 'k1', 'archi', 'dataset', 'sovereign', 'asu', 'vigie'] if width == 1440 else ['page','dataset']
        for state in states:
            if state != 'page':
                page.locator(f'[data-project="{state}"]').click()
            result = page.evaluate("""async () => {
                const r = await axe.run(document, {runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});
                return {violations:r.violations,incomplete:r.incomplete.map(x=>({id:x.id,nodes:x.nodes.length})),passes:r.passes.length};
            }""")
            results.append({'lang':lang,'width':width,'state':state,**result})
            print(lang, width, state, 'violations:', len(result['violations']))
            if state != 'page':
                page.keyboard.press('Escape')
    browser.close()
(OUT / 'axe_visual_refresh.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
assert not any(r['violations'] for r in results), 'See scratch/qa/axe_visual_refresh.json'
print('No automated axe violations in tested states. Human review remains necessary.')
