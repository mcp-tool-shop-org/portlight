<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.md">English</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

Portlight est un jeu de stratégie maritime axé sur le commerce, conçu pour être joué dans un terminal. Vous incarnez un capitaine, gérez un entrepôt et développez votre réputation dans vingt ports différents. Les prix fluctuent en fonction de vos ventes. Les contrats exigent une preuve d'origine. Les courtiers et les entrepôts influencent la valeur d'un voyage. Quatre voies de victoire évaluent la carrière que vous avez réellement construite, et non celle que vous avez choisie dès le premier jour.

Jouez dans l'**interface TUI** (`portlight tui`) ou dans l'**interface CLI**. Les sauvegardes sont les mêmes. Le même monde.

## Installation

```bash
pip install "portlight[tui]"
```

Python 3.11 ou version ultérieure. Le paquet `tui` supplémentaire inclut Textual. Version CLI uniquement : `pip install portlight`.

Pas de Python ? Le lanceur npm télécharge la version binaire de GitHub :

```bash
npx @mcptoolshop/portlight
```

Kit PDF pour jouer en version imprimée : `pip install "portlight[printandplay]"`.

## Jouer

```bash
portlight tui
```

S'il n'y a pas de sauvegarde, l'interface TUI affiche les emplacements disponibles et l'option **Nouveau**. Choisissez un type de capitaine. Ensuite :

| Touches | Action |
|-----|----------------|
| **D** | Tableau de bord (c'est ici que se trouvent votre carrière et vos objectifs) |
| **M / B / S** | Marché · acheter · vendre |
| **G / A** | Sélection de la route · avancer d'un jour |
| **H** | Port : approvisionnement, réparation, embauche ; également travail, renvoi, chasse. En mer, H chasse. |
| **K** | Contrats. Appuyez sur **K** pour accepter ou abandonner. |
| **W** | Infrastructure. Appuyez sur **W** pour louer, déposer, retirer, ouvrir un bureau de courtier, acheter une licence ou obtenir un crédit. |
| **P** | Port. Appuyez sur **P** pour accéder au chantier naval (acheter une coque, des améliorations, effectuer un carénage). |
| **F** | Flotte. Appuyez sur **F** pour embarquer, accoster, transférer ou vendre une coque de navire. |
| **V** | Carte du monde |
| **?** | Aide |

L'interface CLI est la même que le jeu, mais avec des commandes saisies au clavier :

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight tui
```

`portlight --json status` enregistre un dictionnaire stable (capitaine, port, cargaison, marché, itinéraires, équipage) sans caractères ANSI. `portlight saves` affiche les emplacements disponibles.

Première session guidée : [docs/START_HERE.md](docs/START_HERE.md). Manuel : [https://mcp-tool-shop-org.github.io/portlight/handbook/](https://mcp-tool-shop-org.github.io/portlight/handbook/).

## Pourquoi Portlight ?

La plupart des jeux de commerce réduisent le commerce à un simple chiffre qui augmente. Portlight considère le commerce comme une discipline commerciale :

- **Les prix réagissent à vos transactions.** Vendez une grande quantité de céréales et le prix local s'effondrera.
- **Les ports ont des identités économiques.** Porto Novo produit des céréales. Silk Haven exporte de la soie. C'est une structure, pas du bruit.
- **Les voyages comportent des risques.** Tempêtes, pirates, inspections, saisons. Les provisions, la coque et l'équipage représentent des coûts réels.
- **Les contrats exigent une preuve.** Les bons produits, le bon port, une traçabilité vérifiée, des délais réels.
- **L'infrastructure modifie la planification.** Les entrepôts préparent la cargaison. Les courtiers améliorent l'efficacité. Les licences ouvrent un accès privilégié. Les cinq régions disposent de bureaux de courtiers et d'une charte régionale.
- **La réputation se décline en quatre axes.** Confiance commerciale, suspicion douanière, influence régionale, connexions avec le monde souterrain. Ils ouvrent et ferment des portes de manière indépendante.
- **Le jeu évalue ce que vous avez construit.** Les objectifs et les quatre voies de victoire évaluent les preuves, et non un simple choix de menu.

## Le monde

Cinq régions. Vingt ports. Quarante-trois itinéraires.

| Région | Ports | Personnage |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Céréales, bois, épices. Eaux de départ sûres. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Commerce du fer, des armes et des garnisons. Inspections strictes. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Coton, rhum, perles. Provisions bon marché. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Soie, épices, porcelaine, thé. Marges les plus élevées. Risque de mousson. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Perles, médicaments. Eaux de fin de partie isolées. |

Dix-huit marchandises (y compris les fourrures et la contrebande). Cent trente-quatre PNJ nommés. Quatre factions de pirates avec huit capitaines nommés actifs. Météo saisonnière. Festivals, superstitions, moral de l'équipage.

## Neuf capitaines

| Capitaine | Origine | Avantage | Compromis |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Meilleurs prix, la confiance se développe rapidement | Les pénalités de suspicion sont doublées |
| **Smuggler** | Palm Cove | Marché noir, contrebande | Suspicion plus élevée, plus d'inspections |
| **Navigator** | Silva Bay | Navires plus rapides, plus grande portée | Influence initiale plus faible |
| **Privateer** | Stormwall | Combat naval, abordage | Mauvaise réputation auprès des marchands |
| **Corsair** | Corsair's Rest | Combat + commerce | Maître de rien |
| **Scholar** | Monsoon Reach | Informations, meilleurs contrats | Faible capital, fragile |
| **Merchant Prince** | Al-Manar | Capital de départ élevé | Frais plus élevés, cible des pirates |
| **Dockhand** | Crosswind Isle | Équipage bon marché | Capital de départ le plus faible |
| **Bounty Hunter** | Crosswind Isle | Combat, influence de la faction | Mauvais prix, méfiance |

`portlight new "Name"` sans `--type` ouvre la liste. Bounty Hunter n'est pas une simple étiquette : `portlight bounty accept <id>` puis `portlight bounty hunt <id>` force le capitaine nommé. Les identifiants fantômes ont disparu ; la liste ne contient que les `PIRATE_CAPTAINS` actifs.

## Systèmes

**Économie** — Tarification basée sur la rareté, pénalités en cas de surproduction, chocs du marché, identité régionale des importations/exportations.

**Voyages** — Voyages de plusieurs jours. Météo, pirates, inspections. Les duels de pirates nommés préfèrent un objectif actif lorsqu'il correspond aux eaux.

**Contrats** — Sept familles, vingt-quatre modèles. Confiance et influence comme conditions préalables. Livraison avec preuve d'origine.

**Réputation** — Influence régionale, confiance commerciale, suspicion douanière, connexions avec le monde souterrain.

**Combat** — Triangle des postures personnelles (attaque / entaille / parade), combats au corps à corps et à distance, styles de combat (TUI **Y** déclenche la capacité spéciale du style). Marine : tir de flanc, combat rapproché, esquive, abordage, fuite. Capture de navires avec une coque de navire réelle.

**Infrastructure** — Trois niveaux d’entrepôts. Bureaux de courtiers : locaux + établis dans les cinq régions. Sept licences (cinq franchises régionales, dont l’Atlantique Nord et les mers du Sud, plus deux licences mondiales). Coûts d’entretien réels.

**Finance** — Assurance de la coque, du chargement et des contrats. Trois niveaux de crédit avec intérêts et défaut de paiement.

**Flotte** — Plusieurs coques, possibilité de s’amarrer/embarquer dans le même port, transfert de cargaison, dix-huit améliorations.

**Carrière** — Vingt-sept étapes importantes, sept balises de profil, quatre voies de victoire. Le tableau de bord affiche le registre ; l’avancement quotidien valide les étapes achevées.

## Voies de victoire

- **Maison de commerce légale** — Grande confiance, contrats de qualité, réputation irréprochable, infrastructure étendue.
- **Réseau clandestin** — Marges de luxe malgré les difficultés, a survécu aux saisies, reste en tête.
- **Portée océanique** — Influence dans les Indes orientales, infrastructure distante, maîtrise des longues distances.
- **Empire commercial** — Entrepôts, courtiers, licences et levier financier dans plusieurs régions.

## Version imprimable

```bash
pip install "portlight[printandplay]"
portlight print-and-play
```

PDF de la taille d’un kit (format portrait après le format paysage du plateau, échelle argentée de 0 à 100). Manuel des règles : [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md).

## Groupes de commandes

Exécuter `portlight guide` dans le jeu, ou [docs/COMMANDS.md](docs/COMMANDS.md).

| Groupe | Commandes |
|-------|----------|
| Interface | `tui`, `saves`, `--json` |
| Commerce | `market`, `buy`, `sell`, `cargo` |
| Navigation | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire`, `fire`, `crew`, `hunt`, `work` |
| Combat | `duel`, `fight`, `encounter`, `naval`, `capture`, `spare`, `take-all`, `bounty` (`list` / `accept` / `hunt` / `claim`) |
| Équipement | `inventory`, `equip`, `merchant`, `sell-gear`, `armory`, `train`, `equip-style`, `maintain`, `smith`, `field-repair`, `injuries`, `learn-skill` |
| Flotte | `shipyard`, `drydock`, `fleet`, `dock`, `board`, `transfer`, `rename`, `upgrade` |
| Contrats | `contracts`, `accept`, `obligations`, `abandon` |
| Compagnons | `recruit`, `dismiss-companion`, `party` |
| Infrastructure | `warehouse`, `office`, `license` |
| Finance | `insure`, `credit` |
| Carrière | `captain`, `reputation`, `milestones`, `status`, `ledger` |
| Monde | `map` |
| Système | `save`, `load`, `guide`, `print-and-play` |

## Qualité

- 1 853 tests
- 14 invariants inter-systèmes dans le cadre de 9 scénarios de stress combinés
- Ensemble d’équilibrage : 7 bots de politique, 7 ensembles de scénarios
- Format d’enregistrement v12 avec une chaîne de migration complète
- Nettoyage avec Ruff. Python 3.11 / 3.12 / 3.13

## Sécurité

Jeu local uniquement. Pas de réseau pendant le jeu. Enregistre les données dans `saves/` et les transmet à `artifacts/` au format JSON. Pas de secrets, pas de télémétrie, pas de privilèges élevés. Voir [SECURITY.md](SECURITY.md).

## Développement

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

`verify.sh` exécute les tests, Ruff, la création d’un paquet et un test d’importation de l’artefact créé.

## Licence

MIT

---

Créé par <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
