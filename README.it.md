<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.md">English</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="600" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/portlight/"><img src="https://img.shields.io/pypi/v/portlight" alt="PyPI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-handbook-blue" alt="Handbook"></a>
</p>

Gioco di strategia marittima incentrato sul commercio. Costruisci una carriera commerciale in cinque regioni attraverso l'arbitraggio delle rotte, i contratti, le infrastrutture, la finanza e la reputazione, il tutto partendo dalla tua base.

## Installazione

```bash
pip install portlight
```

Non hai Python? Utilizza l'interfaccia npm:

```bash
npx @mcptoolshop/portlight
```

## Perché Portlight

La maggior parte dei giochi di commercio semplifica il commercio in un numero che aumenta. Portlight considera il commercio come una disciplina commerciale:

- **I prezzi reagiscono alle tue transazioni.** Se vendi grano in un porto, il prezzo crolla. Ogni vendita influenza il mercato locale.
- **I porti hanno vere e proprie economie.** Porto Novo produce grano a basso costo. Silk Haven esporta seta in grandi quantità. Queste sono caratteristiche strutturali, non casuali.
- **I viaggi comportano dei rischi.** Tempeste, pirati, ispezioni, pericoli stagionali. Le tue provviste, lo scafo e l'equipaggio sono importanti.
- **I contratti richiedono prove.** Consegna le merci giuste al porto giusto entro la scadenza. La provenienza viene tracciata.
- **Le infrastrutture cambiano il modo in cui fai affari.** I magazzini stoccano le merci. I broker migliorano i contratti. Le licenze sbloccano l'accesso a servizi premium.
- **La reputazione apre e chiude le porte.** Fiducia commerciale, controlli doganali, posizione regionale e contatti nel sottobosco: quattro fattori che influenzano ciò che puoi fare e dove.
- **Il gioco analizza ciò che hai costruito.** La tua storia commerciale, le infrastrutture, la reputazione e le rotte formano un profilo di carriera. Quattro percorsi di vittoria distinti, basati sul tipo di commerciante che sei diventato.

## Il Mondo

Cinque regioni. Venti porti. Quaranta-tre rotte. Un'economia dinamica.

| Regione | Porti | Personaggio |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Grano, legname, mercati delle spezie. Acque iniziali sicure. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Ferro, armi, commercio militare. Controlli rigorosi. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Cotone, rum, perle. Provviste più economiche. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Seta, spezie, porcellana, tè. Margini più alti. Rischio dei monsoni. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Perle, medicinali. Acque di fine gioco più remote. |

134 PNG (personaggi non giocanti) con nomi in ogni porto. Quattro fazioni pirata che controllano diverse aree. Condizioni meteorologiche stagionali che influenzano i pericoli e la domanda. Un sistema culturale con feste, superstizioni e morale dell'equipaggio.

## Nove Capitani

| Capitano | Casa | Vantaggio | Compromesso |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Prezzi migliori, la fiducia cresce rapidamente | Penalità per la "calore" raddoppiate |
| **Smuggler** | Corsair's Rest | Mercato nero, commercio di contrabbando | Maggiore attenzione, più ispezioni |
| **Navigator** | Monsoon Reach | Navi più veloci, maggiore autonomia | Posizione iniziale più debole |
| **Privateer** | Ironhaven | Combattimento navale, vantaggio negli abbordaggi | Scarsa reputazione commerciale |
| **Corsair** | Corsair's Rest | Equilibrio tra combattimento e commercio | Maestro di nulla |
| **Scholar** | Jade Port | Vantaggio informativo, contratti migliori | Capitale iniziale basso, fragile |
| **Merchant Prince** | Porto Novo | Alto capitale iniziale, accesso a servizi premium | Tariffe più alte, bersaglio dei pirati |
| **Dockhand** | Crosswind Isle | Equipaggio più economico, intraprendente | Capitale iniziale più basso |
| **Bounty Hunter** | Stormwall | Maestria nel combattimento, posizione nella fazione | Prezzi scadenti, diffidenza |

Ogni capitano inizia in un porto diverso, vede contratti diversi e tende verso un percorso di vittoria diverso. Il gioco non ti limita: osserva ciò che fai e ti dice cosa hai costruito.

## Ciclo Principale

```
Inspect market → Buy cargo → Sail → Sell → Reinvest → Build access → Pursue destiny
```

## Guida Rapida

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight routes
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight milestones
```

Consulta [docs/START_HERE.md](docs/START_HERE.md) per una sessione introduttiva guidata.

## Sistemi

**Economia** — Prezzi influenzati dalla scarsità in 20 porti, riguardanti 18 merci, 43 rotte. Le penalità per le pratiche scorrette puniscono il dumping. Le crisi di mercato creano opportunità. I modificatori regionali della domanda fanno sì che ogni porto abbia una chiara identità in termini di importazioni/esportazioni.

**Viaggi** — Viaggi di più giorni con condizioni meteorologiche, incontri con pirati, ispezioni. Le provviste si consumano quotidianamente. Lo scafo subisce danni. Il morale dell'equipaggio varia. Le zone pericolose stagionali modificano le rotte considerate sicure.

**Contratti** — Sei famiglie, legate da fiducia e reputazione. Approvvigionamento, mitigazione delle carenze, beni di lusso discreti, trasporto di merci di ritorno, circuiti commerciali e commissioni di fazioni. Scadenze reali, conseguenze reali.

**Reputazione** — Quattro assi: reputazione regionale, fiducia commerciale, attenzione delle autorità doganali e legami con il sottobosco. Un'alta reputazione sblocca contratti premium. Un'alta attenzione delle autorità doganali innesca ispezioni e divieti di accesso ai porti. Diversi capitani adottano diverse "economie" morali.

**Combattimento** — Combattimento personale completo (triangolo delle posture: affondo/fendente/parata) con 7 armi da mischia, 7 armi da distanza e stili di combattimento regionali. Combattimento navale con abbordaggi e cannoni. Breve, brutale, con conseguenze significative.

**Fazioni Pirata** — Crimson Tide (Mar Mediterraneo), Iron Wolves (Oceano Atlantico settentrionale), Deep Reef Brotherhood (Mari del Sud), Monsoon Syndicate (Estremo Oriente). Ogni fazione ha un territorio, merci preferite, capitani nominati e un atteggiamento nei tuoi confronti.

**Infrastrutture** — Magazzini (3 livelli), uffici di intermediazione, 5 licenze acquistabili. Costi di manutenzione reali. Ogni elemento modifica i tempi, la scala o l'accesso al commercio.

**Finanza** — Assicurazione (scafo, carico, garanzia contrattuale) e credito (3 livelli con interessi). Leva finanziaria con condizioni stringenti.

**Compagni** — Cinque ruoli di ufficiale (marinai, navigatore, chirurgo, contrabbandiere, timoniere). Compagni con nomi, personalità, morale e condizioni di partenza.

**Carriera** — 27 tappe fondamentali in 6 famiglie. 13 profili di carriera. Quattro percorsi di vittoria: Casa commerciale legale, Rete clandestina, Portata oceanica, Impero commerciale.

## Percorsi per la vittoria

- **Casa Commerciale Legale** — Legittimità disciplinata. Elevata fiducia, contratti premium, reputazione impeccabile, vasta infrastruttura.
- **Rete Ombra** — Commercio discreto e redditizio. Margini di lusso sotto controllo, gestione del rischio, operazioni resilienti.
- **Portata Oceanica** — Potenza commerciale a lungo raggio. Accesso alle Indie Orientali, infrastrutture distanti, padronanza delle rotte premium.
- **Impero Commerciale** — Operazione integrata in più regioni. Infrastrutture in ogni regione, diversificazione delle entrate, leva finanziaria.

## Gioco da tavolo "Print-and-Play"

Genera una completa adattamento del gioco da tavolo: carte, tabellone, manuale di istruzioni, tracciati dei punteggi:

```bash
pip install portlight[printandplay]
portlight print-and-play
```

Un'avventura commerciale competitiva da 2 a 4 giocatori (circa 90 minuti) con capitani asimmetrici, competizione per i contratti e tensione tra reputazione e "attenzione". Consulta [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md) per il manuale di istruzioni completo.

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
| Mondo | `map`, `port` |
| Interfaccia | `tui`, `captain-select` |
| Sistema | `save`, `load`, `guide`, `print-and-play` |

## Qualità

- 1.832 test in oltre 72 file
- 14 invarianti di sistema applicati in 9 scenari di stress complessi
- Sistema di bilanciamento: 7 bot di politica in 7 pacchetti di scenari
- Formato di salvataggio v12 con catena di migrazione completa
- Codice pulito, Python 3.11/3.12/3.13

## Sicurezza

Gioco eseguibile solo localmente. Nessuna connessione di rete durante il gioco. I salvataggi vengono effettuati nelle cartelle `saves/` e `artifacts/` come file JSON nel file system locale. Nessun segreto, nessuna telemetria, nessuna autorizzazione elevata. Consulta [SECURITY.md](SECURITY.md).

## Sviluppo

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

## Licenza

MIT

---

Creato da <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
