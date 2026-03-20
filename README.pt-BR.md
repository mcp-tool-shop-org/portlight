<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.md">English</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-landing_page-blue" alt="Landing Page"></a>
</p>

Uma estratégia marítima focada em comércio, onde você constrói uma carreira como mercador através de arbitragem de rotas, contratos, infraestrutura, finanças e reputação comercial em uma economia regional dinâmica.

## Por que Portlight?

A maioria dos jogos de comércio simplifica o comércio em um número que simplesmente aumenta. Portlight trata o comércio como uma disciplina comercial:

- **Os preços reagem às suas transações.** Despejar grãos em um porto faz com que o preço caia. Cada venda altera o mercado local.
- **Os portos têm identidades econômicas reais.** Porto Novo produz grãos a baixo custo. Al-Manar consome seda avidamente. Isso não é aleatório — é estrutural.
- **As viagens envolvem riscos.** Tempestades, piratas, inspeções. Suas provisões, casco e tripulação são importantes.
- **Os contratos exigem comprovação.** Entregue os produtos certos no porto certo, com rastreabilidade. Não é possível falsificar.
- **A infraestrutura muda a forma como você comercializa.** Armazéns permitem que você prepare a carga. Corretores melhoram a qualidade dos contratos. Licenças desbloqueiam acesso premium.
- **O financiamento é uma alavancagem com consequências.** O crédito permite que você avance mais rapidamente. Se você não pagar, as portas se fecham.
- **O jogo analisa o que você construiu.** Seu histórico de comércio, infraestrutura, reputação e rotas formam um perfil de carreira. O jogo lhe diz que tipo de empresa comercial você realmente é.

## O Ciclo Principal

1. Analise o mercado — encontre o que é barato aqui e caro em outro lugar.
2. Compre carga — carregue sua embarcação.
3. Navegue — atravesse rotas sob a pressão do clima, da tripulação e das provisões.
4. Venda — obtenha lucro, altere o mercado local.
5. Reinvista — atualize seu navio, alugue um armazém, abra um escritório de corretagem.
6. Construa acesso — ganhe confiança, reduza a atenção indesejada, desbloqueie contratos e licenças.
7. Siga um destino comercial — quatro caminhos distintos para a vitória, baseados no que você realmente construiu.

## Início Rápido

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

Consulte [docs/START_HERE.md](docs/START_HERE.md) para uma primeira sessão guiada e [docs/FIRST_VOYAGE.md](docs/FIRST_VOYAGE.md) para uma análise detalhada do início do jogo.

## Tipos de Capitães

| Capitão | Identidade | Vantagem | Compromisso |
|---------|----------|------|-----------|
| **Merchant** | Comerciante licenciado, base no Mediterrâneo | Melhores preços, taxas de inspeção mais baixas, a confiança aumenta mais rapidamente. | Sem acesso ao mercado negro. |
| **Smuggler** | Operador discreto, base na África Ocidental. | Acesso ao mercado negro, margens de produtos de luxo, comércio de contrabando. | Maior atenção indesejada, mais inspeções. |
| **Navigator** | Explorador de águas profundas, base no Mediterrâneo. | Navios mais rápidos, maior alcance, acesso precoce às Índias Orientais. | Status comercial inicial mais fraco. |

## Sistemas

**Economia** — Preços determinados pela escassez em 10 portos, 8 produtos, 17 rotas. Penalidades por excesso de oferta punem o despejo. Choques de mercado criam oportunidades regionais.

**Viagens** — Viagens de vários dias com eventos climáticos, encontros com piratas, inspeções. Provisões, casco e tripulação são recursos reais.

**Capitães** — Três arquétipos distintos com diferenças de preços de 8 a 20%, posições iniciais únicas e perfis de acesso diferentes.

**Contratos** — Seis famílias de contratos bloqueadas por confiança e reputação. Entrega com rastreabilidade validada. Prazos reais com consequências reais.

**Reputação** — Reputação regional, reputação específica do porto, atenção indesejada alfandegária e confiança comercial. Um modelo de acesso de vários eixos que abre e fecha portas.

**Infraestrutura** — Armazéns (3 níveis), escritórios de corretagem (2 níveis em 3 regiões) e 5 licenças compráveis. Cada um altera o tempo, a escala ou o acesso ao comércio.

**Seguro** — Apólices de garantia de casco, carga e contrato. Taxas de atenção indesejada. Resolução de sinistros com condições de negação.

**Crédito** — Três níveis de crédito com juros, prazos de pagamento e consequências de inadimplência. Alavancagem com risco real.

**Carreira** — 27 marcos em 6 áreas. Interpretação do perfil de carreira (tags primárias/secundárias/emergentes). Quatro caminhos para a vitória: Casa Comercial Legal, Rede Sombria, Alcance Oceânico e Império Comercial.

## Caminhos para a Vitória

- **Casa Comercial Legal** — Legitimidade disciplinada. Alta confiança, contratos premium, reputação impecável, ampla infraestrutura.
- **Rede Sombria** — Comércio discreto e lucrativo. Margens de lucro elevadas sob escrutínio, gerenciamento de riscos, operações resilientes.
- **Alcance Oceânico** — Poder comercial de longo alcance. Acesso às Índias Orientais, infraestrutura distante, domínio de rotas premium.
- **Império Comercial** — Operação integrada em múltiplas regiões. Infraestrutura em todas as regiões, receita diversificada, alavancagem financeira.

Consulte [docs/CAREER_PATHS.md](docs/CAREER_PATHS.md) para descrições detalhadas voltadas para o jogador.

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
| Sistema | `save`, `load`, `guide` |

## Status Alpha

Portlight está em fase alpha. Os sistemas principais estão completos e foram testados sob carga, mas o equilíbrio está sendo ajustado ativamente.

**O que está funcionando:**
- Todos os sistemas funcionais de ponta a ponta
- 609 testes em 24 arquivos
- 14 invariantes entre sistemas aplicadas sob 9 cenários de teste complexos
- Sistema de balanceamento com 7 bots de política em 7 pacotes de cenários

**O que está sendo ajustado:**
- Escalonamento de contrabandistas (atualmente com desempenho abaixo do esperado na progressão da embarcação)
- Concentração de rotas no Mediterrâneo (Porto Novo / Silva Bay dominam o tráfego)
- Taxas de conclusão de contratos (falhas na lógica de entrega em execuções automatizadas)
- Adoção de seguros (atualmente próxima de zero em testes simulados)

Consulte [docs/ALPHA_STATUS.md](docs/ALPHA_STATUS.md) para detalhes e [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) para problemas específicos.

## Segurança e Dados

Portlight é um **jogo de linha de comando que funciona apenas localmente**. Não estabelece nenhuma conexão de rede durante o jogo. Dados acessados: arquivos de salvamento locais (`saves/`) e arquivos de relatório (`artifacts/`), todos em formato JSON no sistema de arquivos local. Não há senhas, credenciais, telemetria ou serviços remotos. Não são necessárias permissões elevadas. Consulte [SECURITY.md](SECURITY.md) para a política completa.

## Desenvolvimento

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

## Licença

MIT

---

Desenvolvido por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
