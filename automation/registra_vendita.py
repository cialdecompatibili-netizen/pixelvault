# -*- coding: utf-8 -*-
r"""
registra_vendita.py - registra chi possiede un'opera e prepara il file da consegnare con il QR code.

Uso:
  python automation\registra_vendita.py --id tramonto-8bit --proprietario "alias o indirizzo wallet" [--tx HASH] [--push]
  python automation\registra_vendita.py --id tramonto-8bit --proprietario "nuovo alias" --rivendita     # passaggio di proprieta'
  python automation\registra_vendita.py --id tramonto-8bit --in-vendita 25.00                          # il proprietario la mette in vendita
  python automation\registra_vendita.py --id tramonto-8bit --non-in-vendita

Cosa fa:
  1. Aggiorna assets/data/proprietari.json (PUBBLICO: solo alias o wallet, MAI nomi reali ne' email) con opera, collezione, artista,
     proprietario, data, tx, stato vendita e storico dei passaggi. La pagina /verifica/?id=<id> legge questo file.
  2. Crea in ...\pixelvault_originali\consegna\ il file da consegnare: originale (da originali\) con QR in un angolo che punta alla pagina verifica.
     Nel QR c'e' solo l'indirizzo della pagina. Il file consegnato NON va mai messo nella repo.
Il QR non impedisce la copia dell'immagine: dice a chiunque la veda chi e' il proprietario.
"""
import os, io, sys, json, argparse, datetime, subprocess, glob

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(os.path.dirname(os.path.dirname(R)), 'pixelvault_originali')
REG = os.path.join(R, 'assets', 'data', 'proprietari.json')
CAT = os.path.join(R, '_data', 'catalogo.json')

def base_url():
    u = subprocess.run(['git', '-C', R, 'remote', 'get-url', 'origin'], capture_output=True, text=True).stdout.strip()
    u = u.replace('.git', '').rstrip('/')
    owner, repo = u.split('/')[-2], u.split('/')[-1]
    cn = os.path.join(R, 'CNAME')
    if os.path.exists(cn): return 'https://' + io.open(cn).read().strip() + '/'
    return 'https://%s.github.io/%s/' % (owner, repo)

def qr_su_originale(pid, url):
    import qrcode
    from PIL import Image
    f = glob.glob(os.path.join(ORIG, 'originali', pid + '.*'))
    if not f: print('  ATTENZIONE: originale non trovato in originali\\ per', pid); return
    im = Image.open(f[0]).convert('RGB'); W, H = im.size
    lato = max(120, min(W, H) // 6)
    q = qrcode.make(url).convert('RGB').resize((lato, lato), Image.NEAREST)
    m = max(8, lato // 12)
    im.paste(q, (W - lato - m, H - lato - m))
    out = os.path.join(ORIG, 'consegna'); os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, pid + '.png'); im.save(dest, 'PNG')
    print('  File da consegnare:', dest)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--proprietario')
    ap.add_argument('--tx', default='')
    ap.add_argument('--rivendita', action='store_true')
    ap.add_argument('--in-vendita', type=float)
    ap.add_argument('--non-in-vendita', action='store_true')
    ap.add_argument('--push', action='store_true')
    a = ap.parse_args()
    cat = json.load(io.open(CAT, encoding='utf-8'))
    p = next((x for x in cat['prodotti'] if x['id'] == a.id), None)
    if not p: sys.exit('Id non trovato in catalogo.json: ' + a.id)
    os.makedirs(os.path.dirname(REG), exist_ok=True)
    reg = json.load(io.open(REG, encoding='utf-8')) if os.path.exists(REG) else {}
    oggi = datetime.date.today().isoformat()
    o = reg.get(a.id)
    if a.proprietario:
        if o and not a.rivendita: sys.exit('Opera gia registrata: usa --rivendita per cambiare proprietario.')
        storico = (o or {}).get('storico', [])
        if o: storico.append({'proprietario': o['proprietario'], 'fino_al': oggi})
        o = {'opera': p['nome'], 'collezione': p.get('collezione', p['categoria']), 'artista': p.get('artista', ''),
             'proprietario': a.proprietario, 'data': oggi, 'tx': a.tx, 'in_vendita': False, 'prezzo': '', 'storico': storico}
        qr_su_originale(a.id, base_url() + 'verifica/?id=' + a.id)
    if not o: sys.exit('Opera non ancora registrata: serve --proprietario.')
    if a.in_vendita is not None: o['in_vendita'] = True; o['prezzo'] = '%.2f EUR' % a.in_vendita
    if a.non_in_vendita: o['in_vendita'] = False; o['prezzo'] = ''
    reg[a.id] = o
    io.open(REG, 'w', encoding='utf-8', newline='\n').write(json.dumps(reg, ensure_ascii=False, indent=2))
    json.load(io.open(REG, encoding='utf-8'))
    print('Registrato:', a.id, '->', o['proprietario'], '| in vendita:', o['in_vendita'])
    if a.push:
        subprocess.run(['git', '-C', R, 'add', 'assets/data/proprietari.json'], check=True)
        subprocess.run(['git', '-C', R, 'commit', '-q', '-m', 'Registro proprietari: ' + a.id], check=True)
        subprocess.run(['git', '-C', R, 'push', '-q'], check=True)
        print('Pubblicato.')

if __name__ == '__main__':
    main()
