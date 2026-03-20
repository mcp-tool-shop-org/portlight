<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.md">English</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-landing_page-blue" alt="Landing Page"></a>
</p>

这是一款以贸易为核心的海上策略游戏，您将通过路线套利、合同、基础设施、金融和商业声誉，在充满活力的区域经济中构建您的商业帝国。

## 为什么选择Portlight

大多数贸易游戏将贸易简化为单纯的数字增长。Portlight 将贸易视为一种商业纪律：

- **价格会根据您的交易而变化。** 如果您在一个港口大量倾销粮食，价格就会暴跌。每一次销售都会影响当地市场。
- **每个港口都有独特的经济特征。** 波尔托诺沃（Porto Novo）以低廉的价格生产粮食。阿尔-马纳尔（Al-Manar）渴望进口丝绸。这些并非随机现象，而是结构性的。
- **航行充满风险。** 遭遇风暴、海盗和检查。您的补给、船体和船员都至关重要。
- **合同需要提供证明。** 必须将正确的货物运送到正确的港口，并提供可追溯的来源证明。不能作弊。
- **基础设施会改变您的贸易方式。** 仓库可以帮助您储存货物。经纪人可以提高合同质量。许可证可以解锁高级权限。
- **金融是具有风险的杠杆。** 信用可以帮助您更快地发展。如果违约，您将失去一切。
- **游戏会根据您的成就进行评估。** 您的贸易历史、基础设施、声誉和航线将形成您的职业生涯档案。游戏会告诉您您实际上是哪种类型的贸易公司。

## 核心循环

1. 考察市场——找到哪里商品便宜，哪里商品贵。
2. 购买货物——装载您的船只。
3. 航行——在天气、船员和补给压力下穿越航线。
4. 销售——赚取利润，影响当地市场。
5.  reinvest——升级您的船只，租赁仓库，开设经纪人办公室。
6. 积累影响力——赢得信任，降低风险，解锁合同和许可证。
7. 实现商业目标——根据您的实际成就，选择四种不同的胜利路径。

## 快速开始

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

请参考[docs/START_HERE.md](docs/START_HERE.md)以获得引导式的首次游戏体验，并参考[docs/FIRST_VOYAGE.md](docs/FIRST_VOYAGE.md)以获得详细的早期游戏指南。

## 船长类型

| 船长 | 身份 | 优势 | 权衡 |
|---------|----------|------|-----------|
| **Merchant** | 持有许可证的贸易商，地中海为基地 | 更好的价格，更低的检查率，信任更容易建立 | 无法访问黑市 |
| **Smuggler** | 隐秘的经营者，西非为基地 | 可以访问黑市，享受奢侈品利润，进行走私贸易 | 更高的风险，更多的检查 |
| **Navigator** | 深海探险家，地中海为基地 | 船只速度更快，航程更远，可以更早地进入东印度群岛 | 初始商业地位较弱 |

## 系统

**经济**——在10个港口、8种商品和17条航线上，价格受稀缺性驱动。倾销会受到惩罚。市场波动会带来区域机会。

**航行**——多日航行，会遇到天气事件、海盗和检查。补给、船体和船员是真实的资源。

**船长**——三种不同的角色，具有8-20%的价格差异、独特的起始位置和不同的权限。

**合同**——六个合同类型，受信任度和声誉限制。提供可追溯的货物交付。有真实的截止日期和真实的后果。

**声誉**——区域声誉、港口特定声誉、海关风险和商业信任。一种多维度的权限模型，可以打开和关闭机会之门。

**基础设施**——仓库（3个等级）、经纪人办公室（3个区域的2个等级）和5个可购买的许可证。每个都会改变贸易的时机、规模或权限。

**保险**——船体、货物和合同保证保险。会收取风险附加费。解决索赔时会存在拒绝条件。

**信用**——三种等级的信用额度，带有利息、还款期限和违约后果。具有风险的杠杆。

**职业** — 涵盖6个领域，共27个里程碑。职业档案解读（主要/次要/新兴标签）。四种胜利路径：合法贸易公司、影子网络、海洋扩张、商业帝国。

## 胜利路径

- **合法贸易公司** — 严谨的合法性。高信任度、优质合同、良好声誉、广泛的基础设施。
- **影子网络** — 盈利的隐秘贸易。利润丰厚，但需谨慎，需要风险管理，具有韧性的运营。
- **海洋扩张** — 远距离的商业力量。可进入印度群岛，拥有远距离的基础设施，精通航线。
- **商业帝国** — 集成的多区域运营。每个区域都有基础设施，收入来源多元化，具有财务杠杆。

请参阅 [docs/CAREER_PATHS.md](docs/CAREER_PATHS.md) 以获取面向玩家的详细描述。

## 命令参考

在游戏中运行 `portlight guide` 以获取分组的命令参考，或参阅 [docs/COMMANDS.md](docs/COMMANDS.md)。

| 组 | 命令 |
|-------|----------|
| 贸易 | `market`, `buy`, `sell`, `cargo` |
| 导航 | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| 合同 | `contracts`, `accept`, `obligations`, `abandon` |
| 基础设施 | `warehouse`, `office`, `license` |
| 财务 | `insure`, `credit` |
| 职业 | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| 系统 | `save`, `load`, `guide` |

## Alpha版本状态

Portlight 处于 Alpha 阶段。核心系统已完成并经过压力测试，但平衡性正在积极调整中。

**已完成的功能：**
- 所有系统端到端功能正常
- 24个文件中的609个测试
- 在9种复合压力场景下，强制执行14个跨系统不变性
- 具有7个策略机器人的平衡测试，涵盖7个场景包

**正在调整的内容：**
- 走私者规模（目前在飞船升级方面表现不佳）
- 地中海航线集中度（波尔图新港/西尔瓦湾占据了大部分流量）
- 合同完成率（自动化运行中存在交付逻辑漏洞）
- 保险采用率（在模拟游戏中目前接近于零）

请参阅 [docs/ALPHA_STATUS.md](docs/ALPHA_STATUS.md) 以获取详细信息，以及 [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) 以获取具体问题。

## 安全与数据

Portlight 是一款**仅本地运行的命令行游戏**。在游戏过程中，它不会建立任何网络连接。涉及的数据：本地存档文件 (`saves/`) 和报告文件 (`artifacts/`)，所有文件均为 JSON 格式，存储在本地文件系统中。没有敏感信息、凭据、遥测数据或远程服务。不需要任何管理员权限。请参阅 [SECURITY.md](SECURITY.md) 以获取完整策略。

## 开发

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

## 许可证

MIT

---

由 <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> 构建。
