"""Build portfolio compositions from user-supplied images; never alter originals.
No invented UI, external assets or generative imagery. Pillow is required.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'images' / 'projects'
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = {
    'archi-site': 'archi cameroun ai.png',
    'archi-building': 'enleve_la_zone_de_selection_202605290101.jpeg',
    'k1-interface': 'capture k1 interface princi.png',
    'k1-graph': 'capture graph k1.png',
    'dataset-interface': 'DATASET AUTOMATOR.png',
}
images, manifest = {}, {}
for key, name in SOURCES.items():
    source = ROOT / name
    image = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
    original_size = image.size
    processing = 'WebP conversion; original proportions retained.'
    if key == 'archi-building':
        # Building imagery only: excludes headline, old contact details and footer.
        image = image.crop((0, round(image.height * .29), image.width, round(image.height * .87)))
        processing = 'Crop y=29%..87%: architectural illustration only; no original headline/contact/footer.'
    if key == 'k1-graph':
        # Names/labels in the graph are not needed to explain its visual structure.
        box = (286, 143, min(1245,image.width), min(484,image.height))
        image.paste(image.crop(box).filter(ImageFilter.GaussianBlur(4.5)), box)
        processing = 'Graph label area blurred for privacy; no nodes or results added.'
    images[key] = image
    derivative = image.copy()
    derivative.thumbnail((1800,1200),Image.Resampling.LANCZOS)
    derivative.save(OUT / (key + '.webp'), 'WEBP', quality=88, method=6)
    manifest[key] = {'source':name, 'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                     'originalSize':original_size, 'processing':processing,
                     'output':key+'.webp'}

def canvas(size, base, end):
    im = Image.new('RGB',size)
    d = ImageDraw.Draw(im)
    for y in range(size[1]):
        t = y / max(1,size[1]-1)
        d.line((0,y,size[0],y), fill=tuple(round(a*(1-t)+b*t) for a,b in zip(base,end)))
    # Subtle drafting grid, purely decorative.
    for x in range(32,size[0],64): d.line((x,0,x,size[1]), fill=(30,55,65),width=1)
    for y in range(32,size[1],64): d.line((0,y,size[0],y), fill=(30,55,65),width=1)
    return im.convert('RGBA')

def panel(base, image, xy, width, chrome=True):
    image = image.copy()
    height = round(image.height*width/image.width)
    image = image.resize((width,height),Image.Resampling.LANCZOS).convert('RGBA')
    bar = 30 if chrome else 0
    x,y = xy
    w,h = width,height+bar
    shadow = Image.new('RGBA',base.size)
    ImageDraw.Draw(shadow).rounded_rectangle((x,y+14,x+w,y+h+14),radius=13,fill=(0,0,0,110))
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(15)))
    card = Image.new('RGBA',(w,h),(17,29,45,255))
    card.alpha_composite(image,(0,bar))
    if chrome:
        draw=ImageDraw.Draw(card)
        for i,color in enumerate([(109,149,143),(141,161,153),(185,199,184)]):
            draw.ellipse((15+i*17,11,23+i*17,19),fill=color)
        draw.line((0,bar-1,w,bar-1),fill=(58,75,89),width=1)
    mask=Image.new('L',card.size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=10,fill=255)
    base.paste(card,(x,y),mask)
    ImageDraw.Draw(base).rounded_rectangle((x,y,x+w-1,y+h-1),radius=10,outline=(91,119,125,255),width=1)

k1=canvas((1440,1100),(15,36,45),(22,53,57))
panel(k1,images['k1-interface'],(48,40),1344)
graph=images['k1-graph'].crop((280,130,1245,489))
panel(k1,graph,(332,660),1060)
archi=canvas((1440,1100),(18,40,47),(35,54,52))
panel(archi,images['archi-building'],(48,40),1344,False)
panel(archi,images['archi-site'],(144,540),1248)
dataset=canvas((1440,800),(14,32,51),(22,51,65))
panel(dataset,images['dataset-interface'],(48,72),1344)
for key,im in [('k1',k1),('archi',archi),('dataset',dataset)]:
    for width in [800,1440]:
        resized=im.convert('RGB').resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS)
        name=f'{key}-composition-{width}.webp'
        resized.save(OUT/name,'WEBP',quality=86,method=6)
        print(name,(OUT/name).stat().st_size)
(OUT/'media-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('All original image hashes unchanged:', all(hashlib.sha256((ROOT/v['source']).read_bytes()).hexdigest()==v['sourceSha256'] for v in manifest.values()))
