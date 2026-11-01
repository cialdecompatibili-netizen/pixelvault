# pixelvault - progetto: negozio di immagini digitali e file NFT

Repo `cialdecompatibili-netizen/pixelvault`, cartella `C:\Users\mirco\Desktop\repository\pixelvault`. Clone di mistraltemplate1 (guida tecnica in `CLAUDE.md`). Sito: https://cialdecompatibili-netizen.github.io/pixelvault/ (admin: /admin/). Nome e brand "PixelVault" sono provvisori: si cambiano in `_config.yml`.

## Idea (da Mirco, 1/11/2026)
E-commerce che vende **immagini digitali e file NFT**, con la maggior parte del lavoro **automatizzato**: le immagini si generano (vedi `C:\Users\mirco\Desktop\copilot immagini`), si caricano in una cartella e diventano prodotti da sole.

## Logica
```
immagini generate -> cartella _da_importare -> aggiungi_immagini.py -> anteprima con filigrana + scheda prodotto IT+EN -> sito
cliente -> sceglie -> paga -> riceve il file originale (senza filigrana)   [pagamento e consegna: DA FARE]
```

## Regola di sicurezza fondamentale
GitHub Pages e' **pubblico**. Nella repo ci sono SOLO le anteprime con filigrana (1000 px). Gli originali stanno **fuori dalla repo**, in `C:\Users\mirco\Desktop\pixelvault_originali\originali\` (con `_indice.csv`: id, file, sha256). Mai mettere un originale in `assets/`.

## Fatto
- Repo creata da `nuovo_sito.ps1` (IT+EN, shop acceso, accento viola), Pages attivo. Tolta la cartella `.github/workflows` perche' il token GitHub non ha lo scope `workflow` (stessa scelta degli altri siti).
- `automation/aggiungi_immagini.py`: cartella -> anteprima con filigrana + scheda prodotto IT+EN + categorie `immagini` e `nft`. Idempotente (salta gli id gia' presenti). Prezzo e licenza di default sono SEGNAPOSTO.

Uso: mettere le immagini in `C:\Users\mirco\Desktop\pixelvault_originali\_da_importare`, poi `python automation\aggiungi_immagini.py [--nft] [--prezzo 7.90] [--push]`.

## Da fare, in ordine
1. **Pagamento**: oggi lo shop del template invia solo una "richiesta d'ordine" (tracker Apps Script, nessun pagamento, `ordini.tracker` vuoto). Serve un metodo reale: Stripe Payment Links o PayPal; per gli NFT anche pagamento in crypto.
2. **Consegna automatica**: dopo il pagamento il cliente riceve un link temporaneo all'originale. Strada prevista: Cloudflare Worker (come quello dei contatti) + archivio R2 con link firmato a scadenza, collegato al webhook del pagamento.
3. **NFT (deciso 1/11/2026: via di mezzo)**: ora si vende il file digitale in categoria 
ft con scheda e impronta (sha256 in _indice.csv) come base di un certificato. L'NFT vero, coniato su un marketplace (servono wallet, costi di rete, regole della piattaforma), si aggiunge dopo, per le sole immagini che vendono meglio. Rete e marketplace da scegliere.
4. **Testi legali**: licenze d'uso, rimborsi sui beni digitali, termini; verificare diritti sulle immagini generate con AI e le regole dei marketplace NFT. Per i testi serve verifica prima di pubblicarli.
5. **Contenuti**: home, chi siamo, servizi con testi veri IT+EN (ora sono segnaposto del template).
6. Automazione a monte: collegare il sistema `copilot immagini` alla cartella `_da_importare`, e titoli/descrizioni migliori dei semplici nomi file.

## Da decidere con Mirco
- Nome definitivo del sito/brand.
- Prezzi e licenze (personale, commerciale, esclusiva).
- Pagamento: Stripe, PayPal, crypto o tutti.
- NFT: rete e marketplace per la fase 2 (NFT coniato), quando si arriva li'.
- Che tipo di immagini si vendono (stili, temi): serve per categorie, home e SEO.

## Regole editoriali
- Nessuna promessa di guadagno o di rivalutazione degli NFT.
- Dati e cifre solo verificati e con fonte.
- Terminologia chiara; IT + EN.
