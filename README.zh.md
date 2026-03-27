<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.md">English</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

这是一款以贸易为核心的海上策略游戏。通过路线套利、合同、基础设施、金融和声誉，在五个地区发展您的商业帝国——所有操作都可以在终端完成。

## 安装

```bash
pip install portlight
```

如果未安装 Python，请使用 npm 包装器：

```bash
npx @mcptoolshop/portlight
```

## 为什么选择 Portlight

大多数贸易游戏将贸易简化为不断增长的数字。Portlight 将贸易视为一种商业纪律：

- **价格会根据您的交易而变化。** 在一个港口倾销粮食，价格就会暴跌。每一次销售都会影响当地市场。
- **每个港口都有独特的经济特征。** 波尔托诺沃（Porto Novo）以低廉的价格生产粮食。丝绸港（Silk Haven）大量出口丝绸。这些是结构性的特点，而不是随机的。
- **航行充满风险。** 暴风雨、海盗、检查、季节性危险。您的补给、船体和船员都至关重要。
- **合同需要证明。** 在截止日期前将正确的货物运送到正确的港口。货物来源会被追踪。
- **基础设施会改变您的贸易方式。** 仓库用于储存货物。经纪人可以改善合同。许可证可以解锁高级权限。
- **声誉会打开和关闭机会。** 商业信任、海关检查、地区声誉和地下世界关系——这四个方面会影响您可以做什么以及去哪里。
- **游戏会分析您的成就。** 您的贸易历史、基础设施、声誉和航线会形成您的职业生涯档案。根据您最终成为哪种类型的商人，有四种不同的胜利途径。

## 世界

五个地区，二十个港口，四十三条航线，一个充满活力的经济体。

| 地区 | 港口 | 角色 |
|--------|-------|-----------|
| **Mediterranean** | 波尔托诺沃（Porto Novo）、阿尔·马纳尔（Al-Manar）、西尔瓦湾（Silva Bay）、海盗避风港（Corsair's Rest） | 粮食、木材、香料市场。安全的起始海域。 |
| **North Atlantic** | 铁港（Ironhaven）、风暴之墙（Stormwall）、荆棘港（Thornport） | 铁矿、武器、军事贸易。严格的检查。 |
| **West Africa** | 阳光港（Sun Harbor）、棕榈湾（Palm Cove）、铁脊山（Iron Point）、珍珠浅滩（Pearl Shallows） | 棉花、朗姆酒、珍珠。最便宜的补给。 |
| **East Indies** | 玉石港（Jade Port）、季风海（Monsoon Reach）、丝绸港（Silk Haven）、顺风岛（Crosswind Isle）、龙之门（Dragon's Gate）、香料狭道（Spice Narrows） | 丝绸、香料、瓷器、茶叶。最高的利润率。季风风险。 |
| **South Seas** | 炽焰岛（Ember Isle）、台风锚地（Typhoon Anchorage）、珊瑚王座（Coral Throne） | 珍珠、药品。偏远的终局海域。 |

在每个港口都有 134 个命名 NPC。四个海盗派系控制不同的海域。季节性天气会影响危险和需求。文化层面包括节日、迷信和船员士气。

## 九位船长

| 船长 | 家 | 优势 | 权衡 |
|---------|------|------|-----------|
| **Merchant** | 波尔托诺沃（Porto Novo） | 更好的价格，信任增长迅速 | 海关检查惩罚加倍 |
| **Smuggler** | 海盗避风港（Corsair's Rest） | 黑市，走私贸易 | 更高的海关检查，更多检查 |
| **Navigator** | 季风海（Monsoon Reach） | 更快的船只，更远的航程 | 初始声誉较弱 |
| **Privateer** | 铁港（Ironhaven） | 海军战斗，登船优势 | 商人的声誉较差 |
| **Corsair** | 海盗避风港（Corsair's Rest） | 平衡的战斗 + 贸易 | 样样不精 |
| **Scholar** | 玉石港（Jade Port） | 信息优势，更好的合同 | 启动资金低，脆弱 |
| **Merchant Prince** | 波尔托诺沃（Porto Novo） | 启动资金高，高级权限 | 更高的费用，海盗目标 |
| **Dockhand** | 顺风岛（Crosswind Isle） | 最便宜的船员，精打细算 | 启动资金最低 |
| **Bounty Hunter** | 风暴之墙（Stormwall） | 战斗精通，派系声誉 | 价格低廉，不受信任 |

每位船长从不同的港口开始，面对不同的合同，并倾向于不同的胜利途径。游戏不会限制您，它会观察您所做的事情，并告诉您您构建了什么。

## 核心循环

```
Inspect market → Buy cargo → Sail → Sell → Reinvest → Build access → Pursue destiny
```

## 快速开始

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

请参考 [docs/START_HERE.md](docs/START_HERE.md) 获取新手引导。

## 系统

**经济** — 20个港口、18种商品、43条航线，价格受供需关系影响。 洪水会带来惩罚，倾销行为会受到惩罚。 市场波动会带来机遇。 各个港口都有独特的进出口特征，由区域需求决定。

**航行** — 航行时间长达数天，会遇到天气、海盗和检查。 补给品会每日消耗。 船体会受到损伤。 船员士气会发生变化。 季节性危险区域会影响航线的安全性。

**合同** — 六个家族，通过信任和声誉建立联系。 提供采购、缓解短缺、高端商品、回程货物、线路运输和家族委托等服务。 存在真实的截止日期和后果。

**声誉** — 四个维度：区域声望、商业信任、海关关注度和地下世界关系。 高信任度可以解锁高级合同。 高关注度会触发检查和港口限制。 不同的船长会遵循不同的道德准则，从而影响经济模式。

**战斗** — 完整的个人战斗（攻击方式：刺击/劈砍/格挡），包含7种近战武器、7种远程武器和区域性的战斗风格。 海上战斗包含登船和炮击。 战斗短暂、残酷且具有重要意义。

**海盗势力** — 绯红潮汐（地中海）、铁狼（北大西洋）、深渊兄弟会（南洋）、季风集团（东印度）。 每个势力都有自己的领地、偏好的商品、指定的船长以及对你的态度。

**基础设施** — 仓库（3个等级）、经纪人办公室、5个可购买许可证。 存在真实的维护成本。 每个设施都会影响贸易的时机、规模或可访问性。

**金融** — 提供保险（船体、货物、合同保证）和信贷（3个等级，带利息）。 提供具有风险的杠杆。

**船员** — 五个船员角色：水手、航海员、医生、走私犯、物资官。 具有个性和士气的船员，并有离职的触发条件。

**职业** — 6个家族，共27个里程碑。 13个职业特征。 四种胜利途径：合法的贸易公司、影子网络、海洋霸权、商业帝国。

## 胜利途径

- **合法的贸易公司** — 纪律严明，信誉良好。 高信任度、高级合同、良好的声誉、完善的基础设施。
- **影子网络** — 在审查下进行有利可图的贸易。 高利润、风险管理、稳健的运营。
- **海洋霸权** — 远距离商业力量。 能够进入东印度，拥有远距离的基础设施，精通航线。
- **商业帝国** — 集成的多区域运营。 遍布各地的基础设施、多元化的收入来源、强大的金融杠杆。

## 实体桌游

可以生成完整的桌游版本，包括卡牌、游戏板、规则手册和计分表：

```bash
pip install portlight[printandplay]
portlight print-and-play
```

一款2-4人参与的竞争型商人冒险游戏（约90分钟），具有不对称的船长、合同竞赛以及声誉/风险的张力。 请参考 [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md) 获取完整的规则手册。

## 命令参考

运行 `portlight guide` 可以查看分组参考，或者参考 [docs/COMMANDS.md](docs/COMMANDS.md)。

| 分类 | 命令 |
|-------|----------|
| 贸易 | `market`, `buy`, `sell`, `cargo` |
| 航行 | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| 合同 | `contracts`, `accept`, `obligations`, `abandon` |
| 基础设施 | `warehouse`, `office`, `license` |
| 金融 | `insure`, `credit` |
| 职业 | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| 世界 | `map`, `port` |
| 界面 | `tui`, `captain-select` |
| 系统 | `save`, `load`, `guide`, `print-and-play` |

## 质量

- 包含1832个测试，分布在72+个文件中
- 强制执行9个复合压力场景下的14个跨系统不变性
- 策略机器人：7个策略机器人，分布在7个场景包中
- 保存格式为v12，并提供完整的迁移链
- 代码经过清理，使用Python 3.11/3.12/3.13

## 安全

纯本地运行的命令行游戏。游戏过程中不连接任何网络。游戏数据以 JSON 格式保存在本地文件系统的 `saves/` 和 `artifacts/` 目录下。不涉及任何敏感信息，不收集任何用户数据，也不需要任何特殊权限。请参阅 [SECURITY.md](SECURITY.md) 文件。

## 开发

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

## 许可证

MIT

---

由 <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> 构建。
