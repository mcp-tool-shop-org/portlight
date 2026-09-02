<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.md">English</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

《港口之光》是一款以贸易为核心的航海策略游戏，适用于终端设备。你将扮演一位船长，管理你的船舱和声誉，穿梭于二十个港口之间。你的销售行为会影响商品价格。合同需要提供商品来源证明。经纪人和仓库会影响航运的价值。游戏有四种不同的胜利方式，最终评分将取决于你实际建立的职业生涯，而不是你在第一天选择的。

你可以在 **TUI** (`portlight tui`) 或 **CLI** 中进行游戏。存档相同，世界也相同。

## 安装

```bash
pip install "portlight[tui]"
```

Python 3.11+。 `tui` 插件会安装 Textual。仅 CLI 模式：`pip install portlight`。

没有 Python？npm 启动器会从 GitHub 获取发布版本的二进制文件。

```bash
npx @mcptoolshop/portlight
```

可打印的 PDF 套件：`pip install "portlight[printandplay]"`。

## 开始游戏

```bash
portlight tui
```

如果没有存档，TUI 会列出存档槽位，并显示“新建”。选择一个船长类型。然后：

| 按键 | 功能 |
|-----|----------------|
| **D** | 仪表盘（职业生涯/里程碑显示在这里） |
| **M / B / S** | 市场 · 购买 · 销售 |
| **G / A** | 航线选择器 · 推进一天 |
| **H** | 港口：补给、维修、招募；也可以进行工作、解雇、狩猎。在海上，H 代表狩猎。 |
| **K** | 合同。再次按 **K** 键来接受或放弃。 |
| **W** | 基础设施。再次按 **W** 键来租赁、存款、取款、开设经纪人、购买许可证或提取信用额度。 |
| **P** | 港口。再次按 **P** 键进入造船厂（购买船体、升级、进行干船坞维修）。 |
| **F** | 舰队。再次按 **F** 键来登上、停靠、转移或出售战利品船只。 |
| **V** | 世界地图 |
| **?** | 帮助 |

CLI 模式使用文本命令，游戏内容相同：

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight tui
```

`portlight --json status` 会导出稳定的字典（船长、港口、货物、市场、航线、船员），不包含 ANSI 字符。`portlight saves` 会列出存档槽位。

引导式新手教程：[docs/START_HERE.md](docs/START_HERE.md)。手册：[https://mcp-tool-shop-org.github.io/portlight/handbook/](https://mcp-tool-shop-org.github.io/portlight/handbook/)。

## 为什么选择《港口之光》

大多数贸易游戏都会将贸易简化为一个数字，使其不断增长。《港口之光》将贸易视为一种商业学科：

- **价格会根据你的贸易行为而变化。** 倾销谷物会导致当地价格暴跌。
- **港口具有独特的经济特征。** 波尔图诺沃盛产谷物。丝绸港出口丝绸。这是结构，而不是噪音。
- **航行存在风险。** 暴风雨、海盗、检查、季节。补给、船体和船员都是真实的成本。
- **合同需要提供证明。** 必须是正确的商品、正确的港口、可追溯的来源，以及实际的截止日期。
- **基础设施会改变时间安排。** 仓库可以储存货物。经纪人可以改善贸易。许可证可以提供高级服务。所有五个区域都有经纪人办公室和区域特许经营权。
- **声誉有四个维度。** 商业信誉、海关审查、区域地位、地下世界关系。它们会独立地开启或关闭不同的机会。
- **游戏会评估你所建立的事业。** 里程碑和四种胜利方式会根据证据进行评分，而不是菜单选项。

## 世界

五个区域。二十个港口。四十三条航线。

| 区域 | 港口 | 角色 |
|--------|-------|-----------|
| **Mediterranean** | 波尔图诺沃、阿尔-马纳尔、席尔瓦湾、海盗港 | 谷物、木材、香料。安全且适合新手的水域。 |
| **North Atlantic** | 铁港、风暴壁、荆棘港 | 铁、武器、驻军贸易。严格的检查。 |
| **West Africa** | 阳光港、棕榈湾、铁点、珍珠浅滩 | 棉花、朗姆酒、珍珠。廉价的补给。 |
| **East Indies** | 翡翠港、季风海滩、丝绸港、逆风岛、龙门、香料海峡 | 丝绸、香料、瓷器、茶叶。最高的利润。季风风险。 |
| **South Seas** | 灰烬岛、台风锚地、珊瑚王座 | 珍珠、药品。偏远的终局水域。 |

十八种商品（包括毛皮和违禁品）。一百三十四名已命名的 NPC。四个海盗派系，各有八名已命名的船长。季节性天气。节日、迷信、船员士气。

## 九个船长

| 船长 | 家乡 | 优势 | 权衡 |
|---------|------|------|-----------|
| **Merchant** | 波尔图诺沃 | 更好的价格，信誉增长更快 | 负面影响加倍 |
| **Smuggler** | 棕榈湾 | 黑市，违禁品 | 更高的负面影响，更多的检查 |
| **Navigator** | 席尔瓦湾 | 更快的船只，更长的航程 | 初始地位较弱 |
| **Privateer** | 风暴壁 | 海军战斗，登船 | 较差的商人声誉 |
| **Corsair** | 海盗港 | 战斗+贸易 | 没有特别擅长的领域 |
| **Scholar** | 季风海滩 | 信息，更好的合同 | 较低的资本，脆弱 |
| **Merchant Prince** | 阿尔-马纳尔 | 较高的初始资本 | 更高的费用，海盗的目标 |
| **Dockhand** | 逆风岛 | 廉价的船员 | 最低的初始资本 |
| **Bounty Hunter** | 逆风岛 | 战斗，派系地位 | 较差的价格，不受信任 |

`portlight new "Name"`（不带 `--type`）会打开角色列表。赏金猎人不仅仅是一个标签：`portlight bounty accept <id>`，然后 `portlight bounty hunt <id>` 会强制选择已命名的船长。幽灵 ID 已经消失；船员名单只会列出活跃的 `PIRATE_CAPTAINS`。

## 系统

**经济**——稀缺定价、过剩惩罚、市场冲击、区域进出口特征。

**航行**——多日航行。天气、海盗、检查。已命名的海盗决斗更倾向于在水域中存在活跃的赏金时发生。

**合同**——七个家族，二十四个模板。信誉和地位限制。需要提供经过验证的商品来源证明。

**声誉**——区域地位、商业信誉、海关审查、地下世界关系。

**战斗** — 个人战斗姿态三角（突刺/挥砍/招架），近战和远程，战斗风格（TUI **Y** 触发特殊技能）。海军：侧舷炮击、近距离、规避、横扫、撤退。使用真实的舰队船体进行战利品捕获。

**基础设施** — 三个仓库等级。经纪人办公室：在所有五个区域均设有本地和成熟的办公室。七个许可证（包括北大西洋和南海的五个区域许可证，以及两个全球许可证）。真实的维护成本。

**财务** — 船体、货物和合同保证保险。三个信用等级，包括利息和违约。

**舰队** — 多个船体，在同一港口停靠/登船，货物转移，十八项升级。

**职业** — 二十七个里程碑，七个个人资料标签，四个胜利路径。仪表板显示账本；每日推进会提示已完成的任务。

## 胜利路径

- **合法贸易公司** — 高度信任、优质合同、良好声誉、广泛的基础设施。
- **影子网络** — 在压力下获得奢侈利润，幸存于没收，仍然领先。
- **海洋势力** — 在东印度群岛的地位、遥远的基础设施、长途运输能力。
- **商业帝国** — 多个区域的仓库、经纪人、许可证、财务杠杆。

## 可打印游戏

```bash
pip install "portlight[printandplay]"
portlight print-and-play
```

套件大小的 PDF（纵向，位于横向游戏板之后，银色轨迹 0–100）。规则手册：[docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md)。

## 命令组

在游戏中运行 `portlight guide`，或 [docs/COMMANDS.md](docs/COMMANDS.md)。

| 组 | 命令 |
|-------|----------|
| 界面 | `tui`, `saves`, `--json` |
| 贸易 | `market`, `buy`, `sell`, `cargo` |
| 导航 | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire`, `fire`, `crew`, `hunt`, `work` |
| 战斗 | `duel`, `fight`, `encounter`, `naval`, `capture`, `spare`, `take-all`, `bounty` (`list` / `accept` / `hunt` / `claim`) |
| 装备 | `inventory`, `equip`, `merchant`, `sell-gear`, `armory`, `train`, `equip-style`, `maintain`, `smith`, `field-repair`, `injuries`, `learn-skill` |
| 舰队 | `shipyard`, `drydock`, `fleet`, `dock`, `board`, `transfer`, `rename`, `upgrade` |
| 合同 | `contracts`, `accept`, `obligations`, `abandon` |
| 伙伴 | `recruit`, `dismiss-companion`, `party` |
| 基础设施 | `warehouse`, `office`, `license` |
| 财务 | `insure`, `credit` |
| 职业 | `captain`, `reputation`, `milestones`, `status`, `ledger` |
| 世界 | `map` |
| 系统 | `save`, `load`, `guide`, `print-and-play` |

## 质量

- 1,853 次测试
- 9 种复杂压力场景下的 14 个跨系统不变性
- 平衡框架：7 个策略机器人，7 个场景包
- v12 版本的保存格式，具有完整的迁移链
- Ruff 清理。Python 3.11 / 3.12 / 3.13

## 安全性

仅本地游戏。游戏过程中没有网络连接。保存到 `saves/` 并以 JSON 格式报告到 `artifacts/`。没有秘密，没有遥测，没有提升的权限。请参阅 [SECURITY.md](SECURITY.md)。

## 开发

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

`verify.sh` 运行测试、ruff、wheel 构建以及构建后的制品导入测试。

## 许可证

MIT

---

由 <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> 构建
