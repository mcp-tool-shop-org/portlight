<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

ポートライトは、ターミナル向けの、貿易を重視した海洋戦略ゲームです。あなたは船長、積荷、そして評判を、20の港を巡って管理します。商品の売却価格は変動します。契約には、商品の出所証明が必要です。仲介業者や倉庫は、航海の価値に影響を与えます。4つの勝利条件は、あなたが実際に築き上げたキャリアを評価します。最初の日に選んだものではなく。

**TUI**（`portlight tui`）または**CLI**でプレイできます。セーブデータは共通です。同じ世界です。

## インストール

```bash
pip install "portlight[tui]"
```

Python 3.11以上が必要です。`tui`を追加すると、Textualがインストールされます。CLIのみ：`pip install portlight`。

Pythonがない場合、npmランチャーがGitHubのリリースバイナリをダウンロードします。

```bash
npx @mcptoolshop/portlight
```

印刷して遊べるPDFキット：`pip install "portlight[printandplay]"`。

## プレイ

```bash
portlight tui
```

セーブデータがない場合、TUIにはスロットと「新規」が表示されます。船長のタイプを選択します。その後：

| キー操作 | 操作内容 |
|-----|----------------|
| **D** | ダッシュボード（キャリア／マイルストーンがここに表示されます） |
| **M / B / S** | 市場・購入・販売 |
| **G / A** | 航路選択・1日進める |
| **H** | 港：物資の補給、修理、乗組員の雇用。また、作業、解雇、狩りも可能です。航海中、Hで狩りを行います。 |
| **K** | 契約。**Kをもう一度**押すと、契約を承認または放棄できます。 |
| **W** | インフラ。**Wをもう一度**押すと、リース、預金、引き出し、仲介業者の開設、ライセンスの購入、または信用枠の利用ができます。 |
| **P** | 港。**Pをもう一度**押すと、造船所（船体、アップグレード、ドック）が表示されます。 |
| **F** | 艦隊。**Fをもう一度**押すと、乗船、ドッキング、転送、または賞金船の売却ができます。 |
| **V** | 世界地図 |
| **?** | ヘルプ |

CLIは、テキストコマンドを使用する同じゲームです。

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight tui
```

`portlight --json status`は、ANSIコードを含まない安定した辞書（船長、港、積荷、市場、航路、乗組員）を出力します。`portlight saves`は、スロットを一覧表示します。

最初のチュートリアル：[docs/START_HERE.md](docs/START_HERE.md)。ハンドブック：[https://mcp-tool-shop-org.github.io/portlight/handbook/](https://mcp-tool-shop-org.github.io/portlight/handbook/)。

## なぜポートライトなのか

ほとんどの貿易ゲームは、貿易を単なる数値として扱い、その数値が上昇するように単純化しています。ポートライトは、貿易を商業的な分野として扱います。

- **価格はあなたの取引に反応します。**穀物を大量に売り払うと、地元の価格が暴落します。
- **各港には独自の経済的特徴があります。**ポルト・ノヴォは穀物を生産します。シルク・ヘイブンは絹を輸出します。これは構造であり、単なるノイズではありません。
- **航海にはリスクが伴います。**嵐、海賊、検査、季節。物資、船体、乗組員は、実際のコストです。
- **契約には証拠が必要です。**適切な商品、適切な港、追跡可能な出所、実際の期限。
- **インフラはタイミングを変えます。**倉庫は貨物を保管します。仲介業者は取引を円滑にします。ライセンスは、より優れたアクセスを提供します。5つの主要地域には、仲介業者のオフィスと地域憲章があります。
- **評判は4つの軸で評価されます。**商業的な信頼、税関での評価、地域での地位、裏社会とのつながり。これらは独立して、機会を開いたり閉じたりします。
- **ゲームは、あなたが築き上げたものを読み取ります。**マイルストーンと4つの勝利条件は、メニューの選択ではなく、証拠を評価します。

## 世界

5つの地域、20の港、43の航路。

| 地域 | 港 | キャラクター |
|--------|-------|-----------|
| **Mediterranean** | ポルト・ノヴォ、アル・マナール、シルバ・ベイ、コルセアーズ・レスト | 穀物、木材、スパイス。安全な出発点となる海域。 |
| **North Atlantic** | アイアンヘイブン、ストームウォール、ソーンポート | 鉄、武器、駐屯部隊の貿易。厳格な検査。 |
| **West Africa** | サン・ハーバー、パーム・コーブ、アイアン・ポイント、パール・シャローズ | 綿、ラム酒、真珠。安価な物資。 |
| **East Indies** | ジェイド・ポート、モンスーン・リーチ、シルク・ヘイブン、クロスウィンド・アイル、ドラゴンズ・ゲート、スパイス・ナローズ | 絹、スパイス、磁器、茶。最も高い利益率。モンスーンのリスク。 |
| **South Seas** | エンバー・アイル、タイフーン・アンカレッジ、コーラル・スローン | 真珠、薬。遠く離れた終盤の海域。 |

18種類の品物（毛皮や違法品を含む）。134人の名前付きNPC。8人の名前付き船長を持つ4つの海賊勢力。季節による天候。祭り、迷信、乗組員の士気。

## 9人の船長

| 船長 | 拠点 | 強み | トレードオフ |
|---------|------|------|-----------|
| **Merchant** | ポルト・ノヴォ | より良い価格、信頼が急速に向上 | ペナルティが2倍 |
| **Smuggler** | パーム・コーブ | 闇市場、違法品 | より高いペナルティ、より多くの検査 |
| **Navigator** | シルバ・ベイ | より速い船、より長い航続距離 | 初期の地位が低い |
| **Privateer** | ストームウォール | 海戦、乗船 | 商人の評判が低い |
| **Corsair** | コルセアーズ・レスト | 戦闘＋貿易 | 特定の分野に特化していない |
| **Scholar** | モンスーン・リーチ | 情報、より良い契約 | 低い資本、不安定 |
| **Merchant Prince** | アル・マナール | 高い初期資本 | より高い手数料、海賊の標的 |
| **Dockhand** | クロスウィンド・アイル | 安価な乗組員 | 最も低い初期資本 |
| **Bounty Hunter** | クロスウィンド・アイル | 戦闘、勢力との関係 | 低い価格、信頼されていない |

`portlight new "Name"`で、リストを開きます（`--type`がない場合）。賞金稼ぎは単なるフレーバーラベルではありません。`portlight bounty accept <id>`を押してから`portlight bounty hunt <id>`を押すと、名前付きの船長が強制的に選択されます。ゴーストIDは削除されました。ボードには、生きている`PIRATE_CAPTAINS`のみが表示されます。

## システム

**経済** - 希少性に基づいた価格設定、過剰在庫によるペナルティ、市場の変動、地域ごとの輸出入の特徴。

**航海** - 複数日の航海。天候、海賊、検査。名前付きの海賊との決闘では、海域にいる場合に、賞金が設定されていると、より積極的に戦います。

**契約** - 7つのファミリー、24のテンプレート。信頼と地位が条件。出所が証明された商品の配達。

**評判** - 地域での地位、商業的な信頼、税関での評価、裏社会とのつながり。これらは独立して、機会を開いたり閉じたりします。

**戦闘** — 個人の構えの三角形（突き／斬り／受け流し）、近接戦と遠距離戦、戦闘スタイル（TUI **Y**はスタイル固有の特殊能力を発動する）。海戦：舷側攻撃、接近、回避、掃射、撤退。実際の艦隊の船体で賞品を獲得。

**インフラストラクチャ** — 3つの倉庫レベル。仲介業者のオフィス：5つの地域すべてにローカル拠点と確立された拠点がある。7つのライセンス（北大西洋と南太平洋を含む5つの地域ライセンス、および2つのグローバルライセンス）。実際の維持費用。

**財務** — 船体、貨物、契約保証保険。金利とデフォルトを含む3つの信用レベル。

**艦隊** — 複数の船体、同じ港に停泊/乗船、貨物輸送、18のアップグレード。

**キャリア** — 27の節目、7つのプロフィールタグ、4つの勝利の道。ダッシュボードには帳簿が表示され、新たに完了したタスクが通知される。

## 勝利の道

- **合法的な貿易会社** — 高い信頼性、優良な契約、クリーンな評判、広範なインフラストラクチャ。
- **影のネットワーク** — 厳しい状況下での高級品取引、差し押さえを生き残り、依然として優位を保っている。
- **広大な海洋** — 東インドにおける地位、遠隔地のインフラストラクチャ、長距離航行の熟練。
- **商業帝国** — 複数の地域の倉庫、仲介業者、ライセンス、財務レバレッジ。

## 印刷してプレイ

```bash
pip install "portlight[printandplay]"
portlight print-and-play
```

キットサイズのPDF（風景形式のボードの後に縦向きの形式、シルバーのトラック0〜100）。ルールブック：[docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md)。

## コマンドグループ

ゲーム内で`portlight guide`を実行するか、[docs/COMMANDS.md](docs/COMMANDS.md)を参照。

| グループ | コマンド |
|-------|----------|
| インターフェース | `tui`, `saves`, `--json` |
| 取引 | `market`, `buy`, `sell`, `cargo` |
| 航行 | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire`, `fire`, `crew`, `hunt`, `work` |
| 戦闘 | `duel`、`fight`、`encounter`、`naval`、`capture`、`spare`、`take-all`、`bounty`（`list`／`accept`／`hunt`／`claim`） |
| 装備 | `inventory`, `equip`, `merchant`, `sell-gear`, `armory`, `train`, `equip-style`, `maintain`, `smith`, `field-repair`, `injuries`, `learn-skill` |
| 艦隊 | `shipyard`, `drydock`, `fleet`, `dock`, `board`, `transfer`, `rename`, `upgrade` |
| 契約 | `contracts`, `accept`, `obligations`, `abandon` |
| 仲間 | `recruit`, `dismiss-companion`, `party` |
| インフラストラクチャ | `warehouse`, `office`, `license` |
| 財務 | `insure`, `credit` |
| キャリア | `captain`, `reputation`, `milestones`, `status`, `ledger` |
| 世界 | `map` |
| システム | `save`, `load`, `guide`, `print-and-play` |

## 品質

- 1,853回のテスト
- 9つの複合ストレスシナリオにおける14のクロスシステム不変性
- バランス調整ツール：7つのポリシーボット、7つのシナリオパック
- 完全な移行チェーンを備えたv12形式のセーブデータ
- Ruffによるクリーン化。Python 3.11 / 3.12 / 3.13

## セキュリティ

ローカルでのみ実行されるゲーム。プレイ中はネットワークを使用しない。セーブデータは`saves/`に保存され、JSON形式で`artifacts/`にレポートされる。秘密情報、テレメトリー、昇格された権限は一切使用しない。詳細は[SECURITY.md](SECURITY.md)を参照。

## 開発

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

`verify.sh`は、テスト、ruff、ホイールビルド、およびビルドされた成果物の簡易インポートを実行する。

## ライセンス

MIT

---

<a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>によって作成
