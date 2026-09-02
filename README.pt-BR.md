<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.md">English</a>
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

Portlight é um jogo de estratégia marítima focado no comércio, para ser jogado no terminal. Você controla um capitão, um navio e uma reputação em vinte portos. Os preços variam quando você vende. Os contratos exigem comprovação de origem. Corretores e armazéns alteram o valor de uma viagem. Quatro caminhos para a vitória avaliam a carreira que você realmente construiu — e não aquela que você escolheu no primeiro dia.

Jogue na **TUI** (`portlight tui`) ou na **CLI**. O mesmo arquivo de salvamento. O mesmo mundo.

## Instalação

```bash
pip install "portlight[tui]"
```

Python 3.11+. O pacote extra `tui` instala o Textual. Apenas para CLI: `pip install portlight`.

Não tem Python? O iniciador npm baixa o binário do GitHub Release:

```bash
npx @mcptoolshop/portlight
```

Kit PDF para imprimir e jogar: `pip install "portlight[printandplay]"`.

## Jogar

```bash
portlight tui
```

Se não houver um arquivo de salvamento, a TUI lista os espaços disponíveis e a opção **Novo**. Escolha um tipo de capitão. Em seguida:

| Tecla | O que ela faz |
|-----|----------------|
| **D** | Painel (a carreira/os marcos importantes estão aqui) |
| **M / B / S** | Mercado · comprar · vender |
| **G / A** | Seletor de viagens · avançar um dia |
| **H** | Porto: abastecer, reparar, contratar; também trabalhar, demitir, caçar. No mar, H caça. |
| **K** | Contratos. **K novamente** para aceitar ou abandonar. |
| **W** | Infraestrutura. **W novamente** para alugar, depositar, sacar, abrir um escritório de corretor, comprar uma licença ou obter crédito. |
| **P** | Porto. **P novamente** para estaleiro (comprar casco, melhorias, doca seca). |
| **F** | Frota. **F novamente** para embarcar, atracar, transferir ou vender um casco capturado. |
| **V** | Mapa do mundo |
| **?** | Ajuda |

A CLI é o mesmo jogo com comandos digitados:

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight tui
```

`portlight --json status` gera um dicionário estável (capitão, porto, carga, mercado, rotas, tripulação) sem ANSI. `portlight saves` lista os espaços disponíveis.

Sessão guiada para iniciantes: [docs/START_HERE.md](docs/START_HERE.md). Manual: [https://mcp-tool-shop-org.github.io/portlight/handbook/](https://mcp-tool-shop-org.github.io/portlight/handbook/).

## Por que Portlight?

A maioria dos jogos de comércio simplifica o comércio, transformando-o em um número que aumenta. Portlight trata o comércio como uma disciplina comercial:

- **Os preços reagem às suas transações.** Despeje grãos e o preço local despenca.
- **Os portos têm identidades econômicas.** Porto Novo cultiva grãos. Silk Haven exporta seda. Isso é estrutura, não ruído.
- **As viagens envolvem riscos.** Tempestades, piratas, inspeções, estações do ano. Provisões, casco e tripulação são custos reais.
- **Os contratos exigem comprovação.** Produtos corretos, porto correto, rastreamento da origem, prazos reais.
- **A infraestrutura altera o tempo.** Armazéns armazenam a carga. Corretores melhoram a tripulação. Licenças abrem acesso premium. Todas as cinco regiões têm escritórios de corretores e uma carta regional.
- **A reputação tem quatro eixos.** Confiança comercial, atenção alfandegária, posição regional, submundo. Eles abrem e fecham portas de forma independente.
- **O jogo analisa o que você construiu.** Marcos e quatro caminhos para a vitória avaliam as evidências, e não uma escolha de menu.

## O mundo

Cinco regiões. Vinte portos. Quarenta e três rotas.

| Região | Portos | Personagem |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Grãos, madeira, especiarias. Águas de partida seguras. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Ferro, armas, comércio de guarnição. Inspeções rigorosas. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Algodão, rum, pérolas. Provisões baratas. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Seda, especiarias, porcelana, chá. Margens mais altas. Risco de monções. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Pérolas, medicamentos. Águas de fim de jogo remotas. |

Dezoito produtos (incluindo peles e contrabando). Cento e trinta e quatro NPCs nomeados. Quatro facções de piratas com oito capitães nomeados ativos. Clima sazonal. Festivais, superstições, moral da tripulação.

## Nove capitães

| Capitão | Lar | Vantagem | Compromisso |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Melhores preços, a confiança cresce rapidamente | Penalidades de calor dobradas |
| **Smuggler** | Palm Cove | Mercado negro, contrabando | Maior atenção, mais inspeções |
| **Navigator** | Silva Bay | Navios mais rápidos, maior alcance | Posição inicial mais fraca |
| **Privateer** | Stormwall | Combate naval, embarque | Má reputação como comerciante |
| **Corsair** | Corsair's Rest | Combate + comércio | Mestre em nada |
| **Scholar** | Monsoon Reach | Informação, melhores contratos | Baixo capital, frágil |
| **Merchant Prince** | Al-Manar | Alto capital inicial | Taxas mais altas, alvo de piratas |
| **Dockhand** | Crosswind Isle | Tripulação barata | Menor capital inicial |
| **Bounty Hunter** | Crosswind Isle | Combate, posição da facção | Piores preços, não confiável |

`portlight new "Name"` sem `--type` abre a lista. Bounty Hunter não é apenas uma etiqueta: `portlight bounty accept <id>`, em seguida, `portlight bounty hunt <id>` força o capitão nomeado. Os IDs de fantasmas desapareceram; a lista exibe apenas os `PIRATE_CAPTAINS` ativos.

## Sistemas

**Economia** — Preços de escassez, penalidades de excesso, choques de mercado, identidade regional de importação/exportação.

**Viagens** — Viagens de vários dias. Clima, piratas, inspeções. Duelos de piratas nomeados preferem uma recompensa ativa quando ela corresponde às águas.

**Contratos** — Sete famílias, vinte e quatro modelos. Confiança e posição como requisitos. Entrega com comprovação de origem.

**Reputação** — Posição regional, confiança comercial, atenção alfandegária, conexões com o submundo. Eles abrem e fecham portas de forma independente.

**Combate** — Triângulo de postura pessoal (estocada / corte / defesa), combate corpo a corpo e à distância, estilos de luta (TUI **Y** ativa o ataque especial do estilo). Naval: ataque lateral, combate próximo, desviar, ataque de proa, fuga. Captura de prêmios com o casco de uma frota real.

**Infraestrutura** — Três níveis de armazéns. Escritórios de corretores: Local + Estabelecido em todas as cinco regiões. Sete licenças (cinco licenças regionais, incluindo o Atlântico Norte e os Mares do Sul, mais duas globais). Custos reais de manutenção.

**Finanças** — Seguro de casco, carga e garantia de contrato. Três níveis de crédito com juros e inadimplência.

**Frota** — Múltiplos cascos, atracar/embarcar no mesmo porto, transferência de carga, dezoito melhorias.

**Carreira** — Vinte e sete marcos, sete tags de perfil, quatro caminhos para a vitória. O painel exibe o livro-razão; o avanço diário notifica a conclusão de tarefas.

## Caminhos para a vitória

- **Empresa de Comércio Legal** — Alta confiança, contratos premium, reputação impecável, amplitude da infraestrutura.
- **Rede Sombria** — Margens de lucro elevadas sob pressão, sobreviveu a apreensões, ainda está à frente.
- **Alcance Oceânico** — Reputação nas Índias Orientais, infraestrutura distante, domínio em rotas de longa distância.
- **Império Comercial** — Armazéns multi-regionais, corretores, licenças, alavancagem financeira.

## Imprimir e jogar

```bash
pip install "portlight[printandplay]"
portlight print-and-play
```

PDF no tamanho do kit (retrato após o tabuleiro em paisagem, trilha prateada 0–100). Livro de regras: [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md).

## Grupos de comando

Execute `portlight guide` no jogo ou [docs/COMMANDS.md](docs/COMMANDS.md).

| Grupo | Comandos |
|-------|----------|
| Interface | `tui`, `saves`, `--json` |
| Comércio | `market`, `buy`, `sell`, `cargo` |
| Navegação | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire`, `fire`, `crew`, `hunt`, `work` |
| Combate | `duel`, `fight`, `encounter`, `naval`, `capture`, `spare`, `take-all`, `bounty` (`list` / `accept` / `hunt` / `claim`) |
| Equipamento | `inventory`, `equip`, `merchant`, `sell-gear`, `armory`, `train`, `equip-style`, `maintain`, `smith`, `field-repair`, `injuries`, `learn-skill` |
| Frota | `shipyard`, `drydock`, `fleet`, `dock`, `board`, `transfer`, `rename`, `upgrade` |
| Contratos | `contracts`, `accept`, `obligations`, `abandon` |
| Companheiros | `recruit`, `dismiss-companion`, `party` |
| Infraestrutura | `warehouse`, `office`, `license` |
| Finanças | `insure`, `credit` |
| Carreira | `captain`, `reputation`, `milestones`, `status`, `ledger` |
| Mundo | `map` |
| Sistema | `save`, `load`, `guide`, `print-and-play` |

## Qualidade

- 1.853 testes
- 14 invariantes entre sistemas sob 9 cenários de estresse composto
- Conjunto de balanceamento: 7 bots de política, 7 pacotes de cenários
- Formato de salvamento v12 com uma cadeia completa de migração
- Limpeza com Ruff. Python 3.11 / 3.12 / 3.13

## Segurança

Jogo apenas local. Sem rede durante o jogo. Salva em `saves/` e relata para `artifacts/` em formato JSON. Sem segredos, sem telemetria, sem permissões elevadas. Consulte [SECURITY.md](SECURITY.md).

## Desenvolvimento

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

`verify.sh` executa testes, Ruff, a criação de um pacote e uma importação de teste do artefato criado.

## Licença

MIT

---

Criado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
