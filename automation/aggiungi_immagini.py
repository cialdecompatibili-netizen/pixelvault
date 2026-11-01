# -*- coding: utf-8 -*-
r"""
aggiungi_immagini.py - dalla cartella di immagini al negozio, in un colpo solo.

Uso (da qualsiasi posto):
  python automation\aggiungi_immagini.py                      # prende tutto da ...\pixelvault_originali\_da_importare
  python automation\aggiungi_immagini.py --collezione "Paesaggi 8-bit" --artista "Nome" --pixelart
  python automation\aggiungi_immagini.py --prezzo 7.90 --licenza "Uso commerciale singolo"
  python automation\aggiungi_immagini.py --push               # dopo, commit e push

Cosa fa per ogni immagine:
  1. ORIGINALE (alta risoluzione) -> spostato in ...\pixelvault_originali\originali\ (FUORI dalla repo: GitHub Pages e' pubblico,
     l'originale in repo si potrebbe scaricare gratis). Scrive anche originali\_indice.csv (id, file, sha256) per la consegna dopo il pagamento.
  2. ANTEPRIMA con filigrana (lato lungo 1000 px, webp) -> assets/images/prodotti/<id>.webp  (questa e' l'unica cosa pubblica)
  3. Scheda prodotto in _data/catalogo.json + pagine _negozio/<id>.md e en/negozio/<id>.md (IT+EN, idempotente: se l'id esiste lo salta)
  4. La COLLEZIONE (= categoria dello shop) viene creata se manca; ogni prodotto ha anche artista e tipo (pixel art / immagine).
     Con --pixelart l'anteprima e' ingrandita SENZA sfumare i pixel (nearest). Esempi del template tolti alla prima esecuzione.
Il nome del file diventa titolo e id: "tramonto_sul_lago.png" -> "Tramonto sul lago". Poi si rifinisce dall'admin.
PREZZO e LICENZA di default sono segnaposto da confermare.
"""
import os, re, io, sys, json, csv, shutil, hashlib, argparse, subprocess, unicodedata
from PIL import Image, ImageDraw, ImageFont

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))                 # repo pixelvault
ORIG = os.path.join(os.path.dirname(os.path.dirname(R)), 'pixelvault_originali')  # Desktop\pixelvault_originali
DA_IMPORTARE = os.path.join(ORIG, '_da_importare')
OUT_ORIG = os.path.join(ORIG, 'originali')
ANTEPRIMA_DIR = os.path.join(R, 'assets', 'images', 'prodotti')
CAT = os.path.join(R, '_data', 'catalogo.json')
EXT = ('.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff', '.bmp')
BRAND = 'PIXELVAULT'

ICONE = {'pixelart': '\U0001F47E', 'immagini': '\U0001F5BC'}

def categoria_info(nome, artista, pixel):
    tipo_it = 'pixel art' if pixel else 'immagini'
    tipo_en = 'pixel art' if pixel else 'images'
    return dict(nome=nome, icona=ICONE['pixelart' if pixel else 'immagini'], en=nome,
        desc='Collezione NFT di %s di %s.' % (tipo_it, artista), desc_en='NFT collection of %s by %s.' % (tipo_en, artista), perm_en=slug(nome))

def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-') or 'immagine'

def titolo(nome):
    t = re.sub(r'[_\-]+', ' ', os.path.splitext(nome)[0]).strip()
    return (t[:1].upper() + t[1:]) if t else 'Immagine'

def scrivi(rel, txt):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(txt)

def font(px):
    for f in ('arialbd.ttf', 'arial.ttf', 'DejaVuSans-Bold.ttf'):
        try: return ImageFont.truetype(f, px)
        except Exception: pass
    return ImageFont.load_default()

def anteprima(img, dest, pixel=False):
    """Lato lungo 1000 px + filigrana diagonale ripetuta (si toglie male, ma l'originale non e' comunque online)."""
    im = img.convert('RGB')
    if pixel:   # pixel art: ingrandisce a multipli interi senza sfumare, cosi' i pixel restano netti
        k = max(1, 1000 // max(im.size)); im = im.resize((im.size[0] * k, im.size[1] * k), Image.NEAREST)
    else:
        im.thumbnail((1000, 1000))
    w, h = im.size
    layer = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    f = font(max(22, w // 18))
    for y in range(0, h * 2, max(90, h // 5)):
        for x in range(0, w * 2, max(260, w // 2)):
            d.text((x, y), BRAND, font=f, fill=(255, 255, 255, 80), stroke_width=1, stroke_fill=(0, 0, 0, 50))
    layer = layer.rotate(30, resample=Image.BICUBIC).crop((w // 2, h // 2, w // 2 + w, h // 2 + h))
    im = Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest, 'WEBP', quality=90 if pixel else 78)

def carica_catalogo():
    d = json.load(io.open(CAT, encoding='utf-8'))
    if any(c.get('id') == 'esempio' for c in d.get('categorie', [])):      # prima esecuzione: via gli esempi del template
        d['categorie'] = [c for c in d['categorie'] if c.get('id') != 'esempio']
        d['prodotti'] = [p for p in d['prodotti'] if p.get('id') != 'prodotto-esempio']
        for rel in ('_negozio/categoria-esempio.md', '_negozio/prodotto-esempio.md',
                    'en/negozio/categoria/esempio.md', 'en/negozio/prodotto-esempio.md'):
            p = os.path.join(R, rel)
            if os.path.exists(p): os.remove(p)
    return d

def assicura_categoria(d, cid, c):
    if any(c0['id'] == cid for c0 in d['categorie']): return
    d['categorie'].append({'nome': c['nome'], 'id': cid, 'icona': c['icona'], 'descrizione': c['desc'],
                           'tr': {'en': {'nome': c['en'], 'descrizione': c['desc_en']}}})
    scrivi('_negozio/categoria-%s.md' % cid, '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /negozio/categoria/%s/\ndescription: "%s"\nref: shop-cat-%s\n---\n' % (c['nome'], cid, cid, c['desc'], cid))
    scrivi('en/negozio/categoria/%s.md' % cid, '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /en/shop/category/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-cat-%s\n---\n' % (c['en'], cid, c['perm_en'], c['desc_en'], cid))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--collezione', default='Nuove immagini', help='nome collezione (= categoria shop), creata se manca')
    ap.add_argument('--artista', default='PixelVault', help='nome artista mostrato sulle schede')
    ap.add_argument('--pixelart', action='store_true', help='sono pixel art (anteprima nitida)')
    ap.add_argument('--prezzo', type=float, default=4.90, help='euro (default 4.90, SEGNAPOSTO)')
    ap.add_argument('--licenza', default='Licenza personale e commerciale singola (da confermare)')
    ap.add_argument('--licenza-en', default='Single personal and commercial license (to be confirmed)')
    ap.add_argument('--push', action='store_true')
    a = ap.parse_args()
    os.makedirs(DA_IMPORTARE, exist_ok=True); os.makedirs(OUT_ORIG, exist_ok=True)
    files = sorted(f for f in os.listdir(DA_IMPORTARE) if f.lower().endswith(EXT))
    if not files:
        print('Nessuna immagine in', DA_IMPORTARE); return
    d = carica_catalogo()
    cid = slug(a.collezione); cinfo = categoria_info(a.collezione, a.artista, a.pixelart)
    assicura_categoria(d, cid, cinfo)
    tipo = 'pixel art' if a.pixelart else 'immagine'
    esistenti = {p['id'] for p in d['prodotti']}
    idx_path = os.path.join(OUT_ORIG, '_indice.csv')
    nuovo_idx = not os.path.exists(idx_path)
    idx = io.open(idx_path, 'a', encoding='utf-8', newline='')
    wr = csv.writer(idx)
    if nuovo_idx: wr.writerow(['id', 'file', 'sha256'])
    fatti = 0
    for f in files:
        pid = slug(os.path.splitext(f)[0])
        if pid in esistenti:
            print('  salto (id gia presente):', pid); continue
        src = os.path.join(DA_IMPORTARE, f)
        img = Image.open(src); W, H = img.size
        anteprima(img, os.path.join(ANTEPRIMA_DIR, pid + '.webp'), a.pixelart)
        img.close()
        h = hashlib.sha256(io.open(src, 'rb').read()).hexdigest()
        dest = os.path.join(OUT_ORIG, pid + os.path.splitext(f)[1].lower())
        shutil.move(src, dest)
        wr.writerow([pid, os.path.basename(dest), h])
        nome = titolo(f); fmt = os.path.splitext(f)[1][1:].upper().replace('JPEG', 'JPG')
        ic = cinfo['icona']
        d['prodotti'].append({
            'tipo': 'digitale', 'id': pid, 'nome': nome, 'categoria': cid,
            'prezzo_centesimi': int(round(a.prezzo * 100)),
            'descrizione': 'NFT %s di %s, %d x %d px.' % (tipo, a.artista, W, H), 'artista': a.artista, 'collezione': a.collezione, 'tipo_immagine': tipo,
            'descrizione_completa': '\n'.join(['NFT %s di %s, collezione "%s": %d x %d pixel, formato %s.' % (tipo, a.artista, a.collezione, W, H, fmt),
                'Dopo l\'acquisto ricevi il file originale senza filigrana. L\'anteprima mostrata qui ha la filigrana.',
                'Licenza: %s.' % a.licenza]),
            'immagine': 'assets/images/prodotti/%s.webp' % pid, 'icona': ic, 'visibile': True,
            'tr': {'en': {'nome': nome,
                'descrizione': 'NFT %s by %s, %d x %d px.' % ('pixel art' if a.pixelart else 'image', a.artista, W, H),
                'descrizione_completa': '\n'.join(['NFT %s by %s, collection "%s": %d x %d pixels, %s format.' % ('pixel art' if a.pixelart else 'image', a.artista, a.collezione, W, H, fmt),
                    'After purchase you receive the original file without watermark. The preview shown here is watermarked.',
                    'License: %s.' % a.licenza_en])}}})
        scrivi('_negozio/%s.md' % pid, '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /negozio/%s/\ndescription: "%s"\nref: shop-prod-%s\n---\n' % (nome, pid, pid, 'Immagine digitale: ' + nome, pid))
        scrivi('en/negozio/%s.md' % pid, '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /en/shop/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-prod-%s\n---\n' % (nome, pid, pid, 'Digital image: ' + nome, pid))
        print('  OK', pid, '(%dx%d)' % (W, H)); fatti += 1
    idx.close()
    io.open(CAT, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=2))  # MAI ensure_ascii=True
    json.load(io.open(CAT, encoding='utf-8'))                                                         # rilettura di controllo
    print('Aggiunte %d immagini. Originali in %s (NON in repo).' % (fatti, OUT_ORIG))
    if a.push and fatti:
        subprocess.run(['git', '-C', R, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', R, 'commit', '-q', '-m', 'Nuove immagini: %d' % fatti], check=True)
        subprocess.run(['git', '-C', R, 'push', '-q'], check=True)
        print('Pubblicato.')

if __name__ == '__main__':
    main()
