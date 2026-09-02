<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.md">English</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/portlight/"><img src="https://img.shields.io/pypi/v/portlight" alt="PyPI"></a>
  <a href="https://www.npmjs.com/package/@mcptoolshop/portlight"><img src="https://img.shields.io/npm/v/@mcptoolshop/portlight" alt="npm"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/landing-page-blue" alt="Landing Page"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/handbook/"><img src="https://img.shields.io/badge/docs-handbook-blue" alt="Handbook"></a>
</p>

Portlight è un gioco di strategia marittima incentrato sul commercio, pensato per essere giocato su terminale. Si controlla un capitano, una stiva e una reputazione in venti porti diversi. I prezzi variano in base alle vendite. I contratti richiedono la verifica della provenienza. I broker e i magazzini influenzano il valore di una tratta. Ci sono quattro percorsi per la vittoria che valutano la carriera che si è effettivamente costruita, e non quella scelta all'inizio.

Si può giocare in **TUI** (`portlight tui`) o in **CLI**. Lo stesso salvataggio. Lo stesso mondo.

## Installazione

```bash
pip install "portlight[tui]"
```

Python 3.11 o superiore. L'extra `tui` installa Textual. Solo per CLI: `pip install portlight`.

Non si ha Python? Il launcher npm scarica il binario della versione di GitHub:

```bash
npx @mcptoolshop/portlight
```

Kit PDF per giocare stampando e ritagliando: `pip install "portlight[printandplay]"`.

## Giocare

```bash
portlight tui
```

Se non c'è un salvataggio, la TUI mostra gli slot disponibili e l'opzione **Nuovo**. Si sceglie il tipo di capitano. Quindi:

| Tasto | Funzione |
|-----|----------------|
| **D** | Dashboard (qui si trovano la carriera e gli obiettivi raggiunti) |
| **M / B / S** | Mercato · acquistare · vendere |
| **G / A** | Selezione della tratta · avanzare di un giorno |
| **H** | Porto: rifornimenti, riparazioni, assunzioni; si può anche lavorare, licenziare, cacciare. In mare, H caccia. |
| **K** | Contratti. Premere **K di nuovo** per accettare o abbandonare. |
| **W** | Infrastrutture. Premere **W di nuovo** per affittare, depositare, prelevare, aprire un ufficio di broker, acquistare una licenza o ottenere credito. |
| **P** | Porto. Premere **P di nuovo** per accedere al cantiere navale (acquistare lo scafo, effettuare miglioramenti, effettuare il dragaggio). |
| **F** | Flotta. Premere **F di nuovo** per salire a bordo, attraccare, trasferire o vendere uno scafo conquistato. |
| **V** | Mappa del mondo |
| **?** | Aiuto |

La CLI è lo stesso gioco, ma con comandi testuali:

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight tui
```

`portlight --json status` salva un dizionario stabile (capitano, porto, carico, mercato, rotte, inventario) senza caratteri ANSI. `portlight saves` elenca gli slot disponibili.

Guida alla prima sessione: [docs/START_HERE.md](docs/START_HERE.md). Manuale: [https://mcp-tool-shop-org.github.io/portlight/handbook/](https://mcp-tool-shop-org.github.io/portlight/handbook/).

## Perché Portlight?

La maggior parte dei giochi di commercio semplificano il commercio riducendolo a un numero che aumenta. Portlight tratta il commercio come una disciplina commerciale:

- **I prezzi reagiscono alle vostre transazioni.** Se si scarica grano, il prezzo locale crolla.
- **I porti hanno identità economiche.** Porto Novo produce grano. Silk Haven esporta seta. Questa è una struttura, non rumore.
- **Le tratte comportano rischi.** Tempeste, pirati, ispezioni, stagioni. Le provviste, lo scafo e l'equipaggio sono costi reali.
- **I contratti richiedono prove.** Merci corrette, porto corretto, tracciabilità della provenienza, scadenze reali.
- **Le infrastrutture modificano i tempi.** I magazzini preparano il carico. I broker migliorano l'inventario. Le licenze aprono l'accesso a servizi premium. Tutte e cinque le regioni hanno uffici di broker e una carta regionale.
- **La reputazione si basa su quattro assi.** Fiducia commerciale, attenzione doganale, posizione regionale, mondo criminale. Questi aprono e chiudono le porte in modo indipendente.
- **Il gioco legge ciò che avete costruito.** Gli obiettivi e i quattro percorsi per la vittoria valutano le prove, non una scelta del menu.

## Il mondo

Cinque regioni. Venti porti. Quarantaquattro rotte.

| Regione | Porti | Personaggio |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Grano, legname, spezie. Acque di partenza sicure. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Ferro, armi, commercio di guarnigioni. Ispezioni rigorose. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Cotone, rum, perle. Provviste economiche. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Seta, spezie, porcellana, tè. Margini più alti. Rischio di monsoni. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Perle, medicinali. Acque di fine gioco remote. |

Diciotto merci (incluse pelli e merci di contrabbando). Centotrentaquattro PNG con nome. Quattro fazioni di pirati con otto capitani con nome attivi. Condizioni meteorologiche stagionali. Festival, superstizioni, morale dell'equipaggio.

## Nove capitani

| Capitano | Casa | Punto di forza | Compromesso |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Prezzi migliori, la fiducia cresce rapidamente | Penalità di calore raddoppiate |
| **Smuggler** | Palm Cove | Mercato nero, contrabbando | Calore più alto, più ispezioni |
| **Navigator** | Silva Bay | Navi più veloci, maggiore autonomia | Posizione iniziale più debole |
| **Privateer** | Stormwall | Combattimento navale, abbordaggio | Scarsa reputazione tra i mercanti |
| **Corsair** | Corsair's Rest | Combattimento + commercio | Non eccelle in nulla |
| **Scholar** | Monsoon Reach | Informazioni, contratti migliori | Basso capitale, fragile |
| **Merchant Prince** | Al-Manar | Alto capitale iniziale | Tariffe più alte, bersaglio dei pirati |
| **Dockhand** | Crosswind Isle | Equipaggio economico | Capitale iniziale più basso |
| **Bounty Hunter** | Crosswind Isle | Combattimento, posizione nella fazione | Scarsi prezzi, sfiducia |

`portlight new "Name"` senza `--type` apre l'elenco. Bounty Hunter non è solo un'etichetta: `portlight bounty accept <id>` seguito da `portlight bounty hunt <id>` forza l'assegnazione del capitano con nome. Gli ID fantasma sono stati eliminati; l'inventario elenca solo i `PIRATE_CAPTAINS` attivi.

## Sistemi

**Economia:** prezzi di scarsità, penalità per l'eccesso di offerta, shock di mercato, identità regionale di importazione/esportazione.

**Tratte:** viaggi di più giorni. Meteo, pirati, ispezioni. I duelli con pirati con nome preferiscono un mandato attivo quando questo corrisponde alle acque in cui si trovano.

**Contratti:** sette famiglie, ventiquattro modelli. Fiducia e posizione come prerequisiti. Consegna con verifica della provenienza.

**Reputazione:** posizione regionale, fiducia commerciale, attenzione doganale, connessioni nel mondo criminale. Questi aprono e chiudono le porte in modo indipendente.

**Combattimento** — Triangolo di posizioni personali (spinta / affondo / parata), combattimento ravvicinato e a distanza, stili di combattimento (TUI **Y** attiva l’abilità speciale dello stile). Combattimento navale: fuoco di fianco, combattimento ravvicinato, manovra evasiva, attacco laterale, fuga. Cattura di una nave con lo scafo di una vera flotta.

**Infrastruttura** — Tre livelli di magazzini. Uffici di intermediazione: locali + stabiliti in tutte e cinque le regioni. Sette licenze (cinque licenze regionali, tra cui Nord Atlantico e Mari del Sud, più due globali). Costi di manutenzione reali.

**Finanza** — Assicurazione sullo scafo, sul carico e sulla garanzia del contratto. Tre livelli di credito con interessi e penali per inadempienza.

**Flotta** — Più scafi, attracco/imbarco nello stesso porto, trasferimento del carico, diciotto potenziamenti.

**Carriera** — Ventisette traguardi, sette tag del profilo, quattro percorsi per la vittoria. La dashboard mostra il registro; il completamento giornaliero di un obiettivo viene segnalato.

## Percorsi per la vittoria

- **Compagnia commerciale legale** — Elevata affidabilità, contratti di alta qualità, reputazione impeccabile, ampiezza dell’infrastruttura.
- **Rete clandestina** — Margini di profitto elevati nonostante i rischi, sopravvissuta a sequestri, ancora in vantaggio.
- **Portata oceanica** — Posizione consolidata nelle Indie Orientali, infrastruttura distante, padronanza delle rotte a lunga distanza.
- **Impero commerciale** — Magazzini in più regioni, intermediari, licenze, leva finanziaria.

## Versione cartacea

```bash
pip install "portlight[printandplay]"
portlight print-and-play
```

PDF di dimensioni adatte per la stampa (formato verticale dopo la mappa orizzontale, traccia argento 0–100). Manuale delle regole: [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md).

## Gruppi di comandi

Esegui `portlight guide` nel gioco, oppure [docs/COMMANDS.md](docs/COMMANDS.md).

| Gruppo | Comandi |
|-------|----------|
| Interfaccia | `tui`, `saves`, `--json` |
| Commercio | `market`, `buy`, `sell`, `cargo` |
| Navigazione | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire`, `fire`, `crew`, `hunt`, `work` |
| Combattimento | `duel`, `fight`, `encounter`, `naval`, `capture`, `spare`, `take-all`, `bounty` (`list` / `accept` / `hunt` / `claim`) |
| Equipaggiamento | `inventory`, `equip`, `merchant`, `sell-gear`, `armory`, `train`, `equip-style`, `maintain`, `smith`, `field-repair`, `injuries`, `learn-skill` |
| Flotta | `shipyard`, `drydock`, `fleet`, `dock`, `board`, `transfer`, `rename`, `upgrade` |
| Contratti | `contracts`, `accept`, `obligations`, `abandon` |
| Compagni | `recruit`, `dismiss-companion`, `party` |
| Infrastruttura | `warehouse`, `office`, `license` |
| Finanza | `insure`, `credit` |
| Carriera | `captain`, `reputation`, `milestones`, `status`, `ledger` |
| Mondo | `map` |
| Sistema | `save`, `load`, `guide`, `print-and-play` |

## Qualità

- 1.853 test
- 14 invarianti inter-sistema sotto 9 scenari di stress combinati
- Sistema di bilanciamento: 7 bot di policy, 7 pacchetti di scenari
- Formato di salvataggio v12 con una catena completa di migrazione
- Pulizia con Ruff. Python 3.11 / 3.12 / 3.13

## Sicurezza

Gioco locale. Nessuna connessione di rete durante il gioco. Salvataggio in `saves/` e segnalazione a `artifacts/` in formato JSON. Nessun segreto, nessun tracciamento, nessun permesso elevato. Consulta [SECURITY.md](SECURITY.md).

## Sviluppo

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

`verify.sh` esegue test, Ruff, la creazione di un pacchetto e un test di importazione dell’artefatto creato.

## Licenza

MIT

---

Creato da <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
