<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.md">English</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-landing_page-blue" alt="Landing Page"></a>
</p>

Une stratégie maritime axée sur le commerce, où vous construisez une carrière de commerçant grâce à l'arbitrage des routes, aux contrats, aux infrastructures, à la finance et à la réputation commerciale, le tout au sein d'une économie régionale dynamique.

## Pourquoi Portlight ?

La plupart des jeux de commerce réduisent le commerce à un simple chiffre qui augmente. Portlight considère le commerce comme une discipline commerciale :

- **Les prix réagissent à vos transactions.** Décharger une cargaison de céréales dans un port fait chuter le prix. Chaque vente modifie le marché local.
- **Les ports ont une identité économique réelle.** Porto Novo produit des céréales à bas prix. Al-Manar consomme avidement de la soie. Ce n'est pas aléatoire, c'est structurel.
- **Les voyages comportent des risques.** Tempêtes, pirates, inspections. Vos provisions, la coque de votre navire et votre équipage sont importants.
- **Les contrats exigent des preuves.** Livrez les bons produits au bon port avec une traçabilité vérifiée. Pas de fausses déclarations.
- **Les infrastructures modifient votre façon de commercer.** Les entrepôts vous permettent de stocker des marchandises. Les courtiers améliorent la qualité des contrats. Les licences débloquent un accès privilégié.
- **La finance est un levier puissant.** Le crédit vous permet d'agir plus rapidement. En cas de défaut de paiement, les portes se referment.
- **Le jeu analyse ce que vous avez construit.** Votre historique commercial, vos infrastructures, votre réputation et vos itinéraires forment un profil de carrière. Le jeu vous indique le type de société commerciale que vous êtes réellement.

## Le cycle principal

1. Analysez le marché : trouvez ce qui est bon marché ici et cher ailleurs.
2. Achetez des marchandises : chargez votre cale.
3. Naviguez : traversez des routes sous la pression des conditions météorologiques, de l'équipage et des provisions.
4. Vendez : réalisez des bénéfices, modifiez le marché local.
5. Réinvestissez : améliorez votre navire, louez un entrepôt, ouvrez un bureau de courtage.
6. Développez votre accès : gagnez la confiance, réduisez les risques, débloquez des contrats et des licences.
7. Suivez un destin commercial : quatre voies de victoire distinctes basées sur ce que vous avez réellement construit.

## Démarrage rapide

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

Consultez [docs/START_HERE.md](docs/START_HERE.md) pour une première session guidée et [docs/FIRST_VOYAGE.md](docs/FIRST_VOYAGE.md) pour un guide détaillé du début de partie.

## Types de capitaines

| Capitaine | Identité | Avantage | Compromis |
|---------|----------|------|-----------|
| **Merchant** | Commerçant agréé, base en Méditerranée | Meilleurs prix, taux d'inspection plus faibles, la confiance grandit plus rapidement. | Pas d'accès au marché noir. |
| **Smuggler** | Opérateur discret, base en Afrique de l'Ouest. | Accès au marché noir, marges sur les produits de luxe, commerce de contrebande. | Risque accru, plus d'inspections. |
| **Navigator** | Explorateur des mers, base en Méditerranée. | Navires plus rapides, plus grande portée, accès anticipé aux Indes orientales. | Position commerciale initiale plus faible. |

## Systèmes

**Économie** : Tarification basée sur la rareté dans 10 ports, avec 8 produits et 17 itinéraires. Les pénalités de surproduction punissent le déversement. Les chocs du marché créent des opportunités régionales.

**Voyages** : Trajets de plusieurs jours avec des événements météorologiques, des rencontres avec des pirates et des inspections. Les provisions, la coque et l'équipage sont des ressources réelles.

**Capitaines** : Trois archétypes distincts avec des écarts de prix de 8 à 20 %, des positions de départ uniques et des profils d'accès différents.

**Contrats** : Six familles de contrats verrouillées par la confiance et la réputation. Livraison validée par la traçabilité. Délais réels avec de réelles conséquences.

**Réputation** : Réputation régionale, réputation spécifique à chaque port, niveau de contrôle douanier et confiance commerciale. Un modèle d'accès multi-axes qui ouvre et ferme les portes.

**Infrastructures** : Entrepôts (3 niveaux), bureaux de courtage (2 niveaux dans 3 régions) et 5 licences à acheter. Chacun modifie le calendrier, l'échelle ou l'accès au commerce.

**Assurance** : Polices d'assurance pour la coque, les marchandises et la garantie des contrats. Surcharges liées au risque. Règlement des sinistres avec conditions de refus.

**Crédit** : Trois niveaux de crédit avec intérêts, échéances de paiement et conséquences en cas de défaut. Un levier avec un risque réel.

**Carrière** — 27 étapes clés réparties en 6 catégories. Interprétation du profil de carrière (tags principaux/secondaires/émergents). Quatre voies vers la victoire : Maison Commerciale Légitime, Réseau Clandestin, Influence Maritime, et Empire Commercial.

## Voies vers la victoire

- **Maison Commerciale Légitime** — Légitimité disciplinée. Forte confiance, contrats premium, réputation irréprochable, vaste infrastructure.
- **Réseau Clandestin** — Commerce discret et rentable. Marges de luxe sous surveillance, gestion des risques, opérations résilientes.
- **Influence Maritime** — Puissance commerciale à longue distance. Accès aux Indes, infrastructure distante, maîtrise des routes premium.
- **Empire Commercial** — Opération intégrée multi-régionale. Infrastructure dans chaque région, diversification des revenus, levier financier.

Consultez [docs/CAREER_PATHS.md](docs/CAREER_PATHS.md) pour des descriptions détaillées destinées aux joueurs.

## Référence des commandes

Utilisez la commande `portlight guide` dans le jeu pour accéder à une référence des commandes regroupées, ou consultez [docs/COMMANDS.md](docs/COMMANDS.md).

| Groupe | Commandes |
|-------|----------|
| Commerce | `market`, `buy`, `sell`, `cargo` |
| Navigation | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| Contrats | `contracts`, `accept`, `obligations`, `abandon` |
| Infrastructure | `warehouse`, `office`, `license` |
| Finance | `insure`, `credit` |
| Carrière | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| Système | `save`, `load`, `guide` |

## Statut Alpha

Portlight est en version alpha. Les systèmes principaux sont complets et ont été soumis à des tests de stress, mais l'équilibre est en cours d'ajustement.

**Ce qui est stable :**
- Tous les systèmes fonctionnent de bout en bout.
- 609 tests répartis sur 24 fichiers.
- 14 invariants inter-systèmes appliqués dans 9 scénarios de stress complexes.
- Système d'équilibrage avec 7 bots de politique répartis sur 7 ensembles de scénarios.

**Ce qui est en cours d'ajustement :**
- Échelle du contrebandier (actuellement sous-performant en termes de progression du vaisseau).
- Concentration des routes méditerranéennes (Porto Novo / Silva Bay domine le trafic).
- Taux de réussite des contrats (lacunes dans la logique de livraison lors des exécutions automatisées).
- adoption (du produit) de l'assurance (actuellement proche de zéro lors des simulations).

Consultez [docs/ALPHA_STATUS.md](docs/ALPHA_STATUS.md) pour plus de détails et [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) pour les problèmes spécifiques.

## Sécurité et données

Portlight est un jeu **CLI fonctionnant uniquement en local**. Il ne crée aucune connexion réseau pendant le jeu. Données utilisées : fichiers de sauvegarde locaux (`saves/`) et fichiers de rapport (`artifacts/`), tous au format JSON sur le système de fichiers local. Aucune information sensible, identifiant, télémétrie ou service distant. Aucune permission élevée requise. Consultez [SECURITY.md](SECURITY.md) pour la politique complète.

## Développement

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

## Licence

MIT

---

Développé par <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
