
# pixelvault - progetto: negozio di COLLEZIONI NFT (pixel art e immagini) per artista

Repo `cialdecompatibili-netizen/pixelvault`, cartella `C:\Users\mirco\Desktop\repository\pixelvault`. Clone di mistraltemplate1 (guida tecnica in `CLAUDE.md`). Sito: https://cialdecompatibili-netizen.github.io/pixelvault/ (negozio: /negozio/, admin: /admin/). Nome e brand "PixelVault" sono provvisori: si cambiano in `_config.yml`.

**Questo file e' interno al progetto (repo di lavoro): non e' una pagina del sito.**

## Idea (da Mirco, aggiornata 1/11/2026)
SCOPO (corretto da Mirco il 1/11/2026): **vendere collezioni NFT**. Le opere sono pixel art e immagini, organizzate in **collezioni** e **per artista**. Ogni opera e' un NFT che appartiene a una collezione. Il file originale e l'impronta sha256 (`_indice.csv`) sono la base del certificato; il coniamento on-chain su marketplace (rete, wallet, costi, regole) va definito prima del lancio.

## Logica del sito
```
ARTISTA  ->  COLLEZIONE (= categoria dello shop)  ->  OPERA (prodotto: NFT di pixel art o immagine)
```
- **Collezione** = serie a tema (es. "Paesaggi 8-bit"). Ha pagina propria nel negozio (`/negozio/categoria/<collezione>/`).
- **Opera** = un file in vendita. Campi: nome, artista, collezione, tipo (pixel art / immagine), dimensioni, prezzo, licenza.
- **Artista** = chi ha creato l'opera. E' un campo di ogni scheda (`artista` in `catalogo.json`) e compare nel testo. Mirco e' l'artista principale; altri artisti si possono aggiungere con `--artista`.
- **Percorso del cliente**: home -> collezioni -> scheda NFT (anteprima con filigrana) -> acquisto -> riceve l'opera e il file originale.
- Menu: Home, Negozio (le collezioni), Chi siamo (storia dell'artista), Blog (dietro le quinte, come si fa pixel art), Contatti.

## Automazione (gia' fatta)
`python automation\aggiungi_immagini.py --collezione "Nome" --artista "Nome" [--pixelart] [--prezzo 4.90] [--push]`
```
immagini in C:\Users\mirco\Desktop\pixelvault_originali\_da_importare
 -> originale spostato in ...\originali\ (FUORI dalla repo) + _indice.csv (id, file, sha256)
 -> anteprima con filigrana in assets/images/prodotti/ (pixel art ingrandita a multipli interi, pixel nitidi)
 -> scheda prodotto IT+EN + collezione creata se manca
```
Idempotente: se l'id esiste lo salta. Prezzo e licenza di default sono SEGNAPOSTO.

## Regola di sicurezza fondamentale
GitHub Pages e' **pubblico**. Nella repo ci sono SOLO le anteprime con filigrana. Gli originali stanno **fuori dalla repo**. Mai mettere un originale in `assets/`.

## Da fare, in ordine
0. **NFT vero**: scegliere rete e marketplace/contratto, wallet, costi di rete; decidere se coniare prima della vendita o al momento dell'acquisto (lazy minting). Verificare diritti sulle immagini generate con AI e regole delle piattaforme.
1. **Pagamento**: oggi lo shop del template invia solo una "richiesta d'ordine" (nessun pagamento). Serve Stripe Payment Links o PayPal.
2. **Consegna automatica** dopo il pagamento: link temporaneo all'originale (Cloudflare Worker + R2 con link firmato a scadenza, come il worker contatti).
3. **Testi legali**: licenze d'uso (personale, commerciale), rimborsi sui beni digitali, termini. Da verificare prima di pubblicare.
4. **Contenuti**: caricare le prime collezioni, pagina Chi siamo con la storia dell'artista, titoli e descrizioni migliori dei nomi file.
5. Pagina artista dedicata (oggi l'artista e' un campo nella scheda): quando ci sono 2+ artisti.

## Da decidere con Mirco
- Nome definitivo del sito/brand.
- Nome d'arte da mostrare come artista (oggi il default e' "PixelVault").
- Prezzi e licenze (personale, commerciale, esclusiva).
- Pagamento: Stripe, PayPal e/o crypto.
- Rete e marketplace NFT.
- Prime collezioni da pubblicare.

## Regole editoriali
- Nessuna promessa di guadagno o di rivalutazione degli NFT, ne' di rendimenti.
- Dati e cifre solo verificati e con fonte.
- IT + EN.
