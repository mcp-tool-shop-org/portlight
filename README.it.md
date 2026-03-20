<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.md">English</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-landing_page-blue" alt="Landing Page"></a>
</p>

Un gioco di strategia marittima incentrato sul commercio, in cui si costruisce una carriera commerciale attraverso l'arbitraggio di prezzi, i contratti, le infrastrutture, la finanza e la reputazione commerciale in un'economia regionale dinamica.

## Perché Portlight

La maggior parte dei giochi di commercio semplifica il commercio in un numero che aumenta. Portlight considera il commercio come una disciplina commerciale:

- **I prezzi reagiscono alle vostre transazioni.** Se vendete grandi quantità di grano in un porto, il prezzo crolla. Ogni vendita modifica il mercato locale.
- **I porti hanno vere identità economiche.** Porto Novo produce grano a basso costo. Al-Manar consuma avidamente seta. Queste caratteristiche non sono casuali, ma strutturali.
- **I viaggi comportano dei rischi.** Tempeste, pirati, ispezioni. Le vostre provviste, lo scafo e l'equipaggio sono importanti.
- **I contratti richiedono prove.** Consegnate le merci giuste al porto giusto, con una tracciabilità verificabile. Non si può barare.
- **Le infrastrutture cambiano il modo in cui commerciate.** I magazzini vi permettono di accumulare merci. Gli agenti migliorano la qualità dei contratti. Le licenze sbloccano l'accesso a servizi premium.
- **La finanza è una leva potente.** Il credito vi permette di agire più rapidamente. Se non riuscite a pagare, le opportunità si chiudono.
- **Il gioco valuta ciò che avete costruito.** La vostra storia commerciale, le infrastrutture, la reputazione e le rotte formano un profilo professionale. Il gioco vi dice che tipo di azienda commerciale siete realmente.

## Il Ciclo Principale

1. Analizzate il mercato: trovate ciò che è economico qui e costoso altrove.
2. Acquistate merci: caricate il vostro carico.
3. Navigate: percorrete le rotte, tenendo conto delle condizioni meteorologiche, dell'equipaggio e delle provviste.
4. Vendete: guadagnate un margine di profitto e influenzate il mercato locale.
5. Reinvestite: migliorate la vostra nave, affittate un magazzino, aprite una filiale di un'agenzia.
6. Aumentate l'accesso: guadagnate fiducia, riducete l'attenzione indesiderata, sbloccate contratti e licenze.
7. Perseguite un destino commerciale: quattro percorsi di vittoria distinti, basati su ciò che avete effettivamente costruito.

## Guida Rapida

```bash
# Install
pip install -e ".[dev]"

# Start a new game
portlight new "Captain Hawk" --type merchant

# Look at what's for sale
portlight market

# Buy cheap goods
portlight buy grain 10

# Check available routes
portlight routes

# Sail to where grain sells high
portlight sail al_manar

# Advance through the voyage
portlight advance

# Sell at destination
portlight sell grain 10

# See your trade history
portlight ledger

# Check your career progress
portlight milestones
```

Consultate [docs/START_HERE.md](docs/START_HERE.md) per una sessione introduttiva guidata e [docs/FIRST_VOYAGE.md](docs/FIRST_VOYAGE.md) per una guida dettagliata delle prime fasi del gioco.

## Tipi di Capitano

| Capitano | Identità | Vantaggio | Compromesso |
|---------|----------|------|-----------|
| **Merchant** | Commerciante con licenza, base nel Mediterraneo | Prezzi migliori, tassi di ispezione più bassi, la fiducia cresce più rapidamente | Nessun accesso al mercato nero |
| **Smuggler** | Operatore discreto, base in Africa occidentale | Accesso al mercato nero, margini elevati per i beni di lusso, commercio di contrabbando | Maggiore attenzione, più ispezioni |
| **Navigator** | Esploratore delle acque profonde, base nel Mediterraneo | Navi più veloci, maggiore autonomia, accesso anticipato alle Indie Orientali | Posizione commerciale iniziale più debole |

## Sistemi

**Economia** — Prezzi determinati dalla scarsità in 10 porti, con 8 merci e 17 rotte. Le penalità per l'eccessiva offerta puniscono la vendita a prezzi troppo bassi. Gli shock del mercato creano opportunità regionali.

**Viaggi** — Viaggi di più giorni con eventi meteorologici, incontri con pirati e ispezioni. Provviste, scafo e equipaggio sono risorse reali.

**Capi** — Tre archetipi distinti con differenze di prezzo dell'8-20%, posizioni di partenza uniche e profili di accesso diversi.

**Contratti** — Sei famiglie di contratti accessibili in base alla fiducia e alla reputazione. Consegne con tracciabilità verificata. Scadenze reali con conseguenze reali.

**Reputazione** — Posizione regionale, reputazione specifica per ogni porto, attenzione delle autorità doganali e fiducia commerciale. Un modello di accesso multi-dimensionale che apre e chiude opportunità.

**Infrastrutture** — Magazzini (3 livelli), uffici di agenzia (2 livelli in 3 regioni) e 5 licenze acquistabili. Ognuna modifica i tempi, la scala o l'accesso al commercio.

**Assicurazione** — Polizze di assicurazione per lo scafo, le merci e la garanzia dei contratti. Sovraccarichi dovuti all'attenzione indesiderata. Risoluzione dei sinistri con condizioni di diniego.

**Credito** — Tre livelli di credito con interessi, scadenze di pagamento e conseguenze in caso di mancato pagamento. Una leva finanziaria con rischi reali.

**Carriera** — 27 tappe fondamentali suddivise in 6 aree. Interpretazione del profilo di carriera (etichette primarie/secondarie/emergenti). Quattro percorsi per la vittoria: Casa Commerciale Legale, Rete Ombra, Portata Oceanica e Impero Commerciale.

## Percorsi per la vittoria

- **Casa Commerciale Legale** — Legittimità disciplinata. Elevata fiducia, contratti premium, reputazione impeccabile, vasta infrastruttura.
- **Rete Ombra** — Commercio discreto e redditizio. Margini di lusso sotto controllo, gestione del rischio, operazioni resilienti.
- **Portata Oceanica** — Potenza commerciale a lungo raggio. Accesso alle Indie Orientali, infrastrutture distanti, padronanza delle rotte premium.
- **Impero Commerciale** — Operazione integrata in più regioni. Infrastrutture in ogni regione, diversificazione delle entrate, leva finanziaria.

Consultare [docs/CAREER_PATHS.md](docs/CAREER_PATHS.md) per descrizioni dettagliate rivolte ai giocatori.

## Riferimento dei comandi

Eseguire `portlight guide` all'interno del gioco per una guida raggruppata dei comandi, oppure consultare [docs/COMMANDS.md](docs/COMMANDS.md).

| Gruppo | Comandi |
|-------|----------|
| Commercio | `market`, `buy`, `sell`, `cargo` |
| Navigazione | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| Contratti | `contracts`, `accept`, `obligations`, `abandon` |
| Infrastrutture | `warehouse`, `office`, `license` |
| Finanza | `insure`, `credit` |
| Carriera | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| Sistema | `save`, `load`, `guide` |

## Stato Alpha

Portlight è in fase alpha. I sistemi principali sono completi e sottoposti a test di stress, ma la bilanciamento è in fase di ottimizzazione.

**Cosa è solido:**
- Tutti i sistemi funzionanti end-to-end
- 609 test su 24 file
- 14 invarianti inter-sistema applicati in 9 scenari di stress complessi
- Sistema di bilanciamento con 7 bot di policy su 7 pacchetti di scenari

**Cosa è in fase di ottimizzazione:**
- Scalabilità dei contrabbandieri (attualmente sottoperformante nella progressione della nave)
- Concentrazione delle rotte nel Mediterraneo (Porto Novo / Silva Bay dominano il traffico)
- Tassi di completamento dei contratti (lacune nella logica di consegna nelle esecuzioni automatizzate)
- Adozione dell'assicurazione (attualmente prossima allo zero nelle simulazioni)

Consultare [docs/ALPHA_STATUS.md](docs/ALPHA_STATUS.md) per i dettagli e [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) per problemi specifici.

## Sicurezza e dati

Portlight è un gioco **CLI esclusivamente locale**. Non stabilisce connessioni di rete durante il gioco. Dati utilizzati: file di salvataggio locali (`saves/`) e file di report (`artifacts/`), tutti in formato JSON sul file system locale. Nessuna informazione sensibile, credenziali, telemetria o servizi remoti. Non sono richieste autorizzazioni elevate. Consultare [SECURITY.md](SECURITY.md) per la politica completa.

## Sviluppo

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run balance simulation
python tools/run_balance.py

# Run stress tests
python tools/run_stress.py

# Lint
ruff check src/ tests/
```

## Licenza

MIT

---

Creato da <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
