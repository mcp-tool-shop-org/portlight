<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.md">English</a>
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

Jogo de estratégia marítima focado em comércio. Construa uma carreira como comerciante em cinco regiões, utilizando estratégias de arbitragem de rotas, contratos, infraestrutura, finanças e reputação — tudo a partir do terminal.

## Instalação

```bash
pip install portlight
```

Não tem Python? Use o wrapper npm em vez disso:

```bash
npx @mcptoolshop/portlight
```

## Por que Portlight?

A maioria dos jogos de comércio simplifica o comércio em um número que simplesmente aumenta. Portlight trata o comércio como uma disciplina comercial:

- **Os preços reagem às suas transações.** Despejar grãos em um porto faz com que o preço caia. Cada venda altera o mercado local.
- **Os portos têm identidades econômicas reais.** Porto Novo produz grãos a baixo custo. Silk Haven exporta seda em grande volume. Essas são características estruturais, não aleatórias.
- **As viagens envolvem riscos.** Tempestades, piratas, inspeções, perigos sazonais. Suas provisões, casco e tripulação são importantes.
- **Os contratos exigem comprovação.** Entregue os produtos certos no porto certo antes do prazo. A procedência é rastreada.
- **A infraestrutura muda a forma como você comercializa.** Armazéns armazenam carga. Corretores melhoram os contratos. Licenças desbloqueiam acesso premium.
- **A reputação abre e fecha portas.** Confiança comercial, rigor alfandegário, posição regional e conexões com o submundo — quatro fatores que moldam o que você pode fazer e onde.
- **O jogo analisa o que você construiu.** Seu histórico de comércio, infraestrutura, reputação e rotas formam um perfil de carreira. Quatro caminhos distintos para a vitória, baseados no tipo de comerciante que você realmente se tornou.

## O Mundo

Cinco regiões. Vinte portos. Quarenta e três rotas. Uma economia dinâmica.

| Região | Portos | Personagem |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Grãos, madeira, mercados de especiarias. Águas iniciais seguras. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Ferro, armas, comércio militar. Inspeções rigorosas. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Algodão, rum, pérolas. Provisões mais baratas. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Seda, especiarias, porcelana, chá. Margens mais altas. Risco de monções. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Pérolas, medicamentos. Águas remotas para o final do jogo. |

134 NPCs nomeados em todos os portos. Quatro facções de piratas controlando diferentes áreas. Clima sazonal que altera o perigo e a demanda. Uma camada cultural com festivais, superstições e moral da tripulação.

## Nove Capitães

| Capitão | Início | Vantagem | Compromisso |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Melhores preços, confiança aumenta rapidamente | Penalidades de "heat" dobradas |
| **Smuggler** | Corsair's Rest | Mercado negro, comércio de contrabando | Maior atenção indesejada, mais inspeções. |
| **Navigator** | Monsoon Reach | Navios mais rápidos, maior alcance | Reputação inicial mais fraca |
| **Privateer** | Ironhaven | Combate naval, vantagem de abordagem | Má reputação comercial |
| **Corsair** | Corsair's Rest | Combate equilibrado + comércio | Mestre de nada |
| **Scholar** | Jade Port | Vantagem de informações, melhores contratos | Capital inicial baixo, instável |
| **Merchant Prince** | Porto Novo | Alto capital inicial, acesso premium | Taxas mais altas, alvo de piratas |
| **Dockhand** | Crosswind Isle | Tripulação mais barata, aguerrida | Menor capital inicial |
| **Bounty Hunter** | Stormwall | Domínio do combate, posição na facção | Preços ruins, desconfiança |

Cada capitão começa em um porto diferente, vê contratos diferentes e tende a um caminho de vitória diferente. O jogo não te limita — ele observa o que você faz e te mostra o que você construiu.

## Ciclo Principal

```
Inspect market → Buy cargo → Sail → Sell → Reinvest → Build access → Pursue destiny
```

## Início Rápido

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

Consulte [docs/START_HERE.md](docs/START_HERE.md) para uma primeira sessão guiada.

## Sistemas

**Economia** — Preços determinados pela escassez em 20 portos, envolvendo 18 produtos, 43 rotas. Penalidades por descarte (dumping) são aplicadas. Crises de mercado criam oportunidades. Modificadores regionais de demanda fazem com que cada porto tenha uma identidade clara de importação/exportação.

**Viagens** — Viagens de vários dias, com condições climáticas, encontros com piratas e inspeções. As provisões são consumidas diariamente. O casco sofre danos. A moral da tripulação varia. Zonas de perigo sazonais alteram quais rotas são seguras.

**Contratos** — Seis famílias, ligadas por confiança e reputação. Inclui: aquisição, alívio de escassez, produtos de luxo discretos, transporte de carga de retorno, rotas específicas e comissões de facções. Prazos reais, com consequências reais.

**Reputação** — Quatro aspectos: reputação regional, confiança comercial, atenção das autoridades alfandegárias e conexões com o submundo. Alta confiança desbloqueia contratos premium. Alta atenção das autoridades alfandegárias aciona inspeções e proibições de acesso a portos. Diferentes capitães adotam diferentes modelos de ética nos negócios.

**Combate** — Combate pessoal completo (triângulo de posturas: ataque/corte/defesa) com 7 armas de combate corpo a corpo, 7 armas de longo alcance e estilos de luta regionais. Combate naval com abordagens e canhões. Curto, brutal e com consequências.

**Facções Piratas** — Crimson Tide (Mar Mediterrâneo), Iron Wolves (Atlântico Norte), Deep Reef Brotherhood (Oceanos do Sul), Monsoon Syndicate (Sudeste Asiático). Cada uma com seu território, produtos preferidos, capitães e atitude em relação ao jogador.

**Infraestrutura** — Armazéns (3 níveis), escritórios de corretores, 5 licenças disponíveis para compra. Custos de manutenção reais. Cada um altera o tempo, a escala ou o acesso ao comércio.

**Finanças** — Seguros (para o casco, a carga e a garantia de contratos) e crédito (3 níveis com juros). Alavancagem com riscos.

**Companheiros** — Cinco funções de oficiais (fuzileiro, navegador, médico, contrabandista, administrador). Companheiros com nomes, personalidade, moral e gatilhos para sua saída.

**Carreira** — 27 marcos em 6 famílias. 13 tags de perfil de carreira. Quatro caminhos para a vitória: Casa Comercial Legal, Rede Clandestina, Expansão Oceânica, Império Comercial.

## Caminhos para a Vitória

- **Casa Comercial Legal** — Legitimidade disciplinada. Alta confiança, contratos premium, reputação impecável, ampla infraestrutura.
- **Rede Sombria** — Comércio discreto e lucrativo. Margens de lucro elevadas sob escrutínio, gerenciamento de riscos, operações resilientes.
- **Alcance Oceânico** — Poder comercial de longo alcance. Acesso às Índias Orientais, infraestrutura distante, domínio de rotas premium.
- **Império Comercial** — Operação integrada em múltiplas regiões. Infraestrutura em todas as regiões, receita diversificada, alavancagem financeira.

## Jogo de tabuleiro para jogar e se divertir

Gere uma adaptação completa para jogo de tabuleiro — cartas, tabuleiro, manual de regras, rastreadores de pontuação:

```bash
pip install portlight[printandplay]
portlight print-and-play
```

Uma aventura comercial competitiva para 2 a 4 jogadores (aproximadamente 90 minutos) com capitães assimétricos, competição por contratos e tensão entre reputação e perigo. Consulte [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md) para o manual de regras completo.

## Referência de Comandos

Execute `portlight guide` no jogo para obter uma referência de comandos organizada, ou consulte [docs/COMMANDS.md](docs/COMMANDS.md).

| Grupo | Comandos |
|-------|----------|
| Comércio | `market`, `buy`, `sell`, `cargo` |
| Navegação | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| Contratos | `contracts`, `accept`, `obligations`, `abandon` |
| Infraestrutura | `warehouse`, `office`, `license` |
| Finanças | `insure`, `credit` |
| Carreira | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| Mundo | `map`, `port` |
| Interface | `tui`, `captain-select` |
| Sistema | `save`, `load`, `guide`, `print-and-play` |

## Qualidade

- 1.832 testes em mais de 72 arquivos
- 14 invariantes de sistema aplicadas em 9 cenários de estresse complexos
- Sistema de balanceamento: 7 bots de política em 7 pacotes de cenários
- Formato de salvamento v12 com cadeia completa de migração
- Código limpo, Python 3.11/3.12/3.13

## Segurança

Jogo de linha de comando (CLI) que funciona apenas localmente. Nenhuma conexão de rede durante o jogo. Os salvamentos são feitos em `saves/` e `artifacts/` como arquivos JSON no sistema de arquivos local. Sem segredos, sem telemetria, sem permissões elevadas. Consulte [SECURITY.md](SECURITY.md).

## Desenvolvimento

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

## Licença

MIT

---

Desenvolvido por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
