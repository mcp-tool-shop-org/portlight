<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-landing_page-blue" alt="Landing Page"></a>
</p>

このゲームでは、ルートの価格差、契約、インフラ、金融、そして地域経済全体に影響を与える商業的評判を通じて、交易業者としてのキャリアを築き上げていきます。

## Portlightを選ぶ理由

多くの交易ゲームでは、交易は単に数値が上昇するだけのものとして扱われます。Portlightでは、交易を商業的な活動として捉えています。

- **価格はあなたの取引によって変動します。** ある港に穀物を大量に供給すると、価格が暴落します。すべての販売が地域の市場に影響を与えます。
- **各港には独自の経済的な特徴があります。** ポルトノボは安価な穀物を生産し、アル・マナールは絹を渇望しています。これらはランダムなものではなく、構造的なものです。
- **航海にはリスクが伴います。** 嵐、海賊、検査などがあります。積載量、船体、そして乗組員が重要になります。
- **契約には証拠が必要です。** 正しい商品を、追跡可能な供給元とともに、正しい港に配達する必要があります。不正は許されません。
- **インフラは交易方法を変えます。** 倉庫は貨物を一時的に保管できます。仲介業者は契約の質を向上させます。ライセンスは特別なアクセス権を付与します。
- **金融は強力なツールです。** 信用は取引を加速させますが、デフォルトすると、取引の機会が失われます。
- **ゲームはあなたが築き上げたものを評価します。** あなたの取引履歴、インフラ、評判、そして航路は、あなたのキャリアを形成します。ゲームは、あなたがどのような交易会社なのかを教えてくれます。

## ゲームの流れ

1. 市場を調査する：どこで安く、どこで高く売れるかを見つける。
2. 貨物を購入する：船倉に積み込む。
3. 航海する：天候、乗組員、そして食料の状況を考慮しながら、航路を進む。
4. 販売する：利益を得て、地域の市場を変動させる。
5. 再投資する：船をアップグレードしたり、倉庫を借りたり、仲介業者事務所を開設したりする。
6. アクセスを拡大する：信頼を築き、リスクを軽減し、契約やライセンスをアンロックする。
7. 商業的な目標を達成する：あなたが築き上げたものに基づいて、4つの異なる勝利ルートが存在する。

## 始め方

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

[docs/START_HERE.md](docs/START_HERE.md) で、ガイド付きの最初のセッションを体験し、[docs/FIRST_VOYAGE.md](docs/FIRST_VOYAGE.md) で、ゲーム序盤の詳細な解説を参照してください。

## 船長の種類

| 船長 | 特徴 | 利点 | 欠点 |
|---------|----------|------|-----------|
| **Merchant** | ライセンス付きの交易業者、地中海を拠点 | 価格が有利、検査の頻度が低い、信頼が築きやすい | 闇市場へのアクセス不可 |
| **Smuggler** | 秘密主義の取引業者、西アフリカを拠点 | 闇市場へのアクセス可能、高級品の取引、違法取引 | リスクが高い、検査の頻度が高い |
| **Navigator** | 探検家、地中海を拠点 | 船が速い、航続距離が長い、東インドへのアクセスが早い | 初期の商業的地位が弱い |

## システム

**経済:** 10の港、8種類の貨物、17の航路における需給に基づいた価格設定。大量の供給による価格暴落を防ぐペナルティ。市場の変動が地域に機会をもたらす。

**航海:** 嵐、海賊、検査などを含む、数日間の航海。食料、船体、乗組員は重要な資源。

**船長:** 8〜20%の価格差、独自の開始位置、異なるアクセス権を持つ、3つの異なるタイプ。

**契約:** 信頼と実績によって制限される、6種類の契約。供給元の情報が検証された配達。期限があり、結果も伴う。

**評判:** 地域での評判、港ごとの評判、税関の監視、商業的な信頼。アクセスを制限したり、開放したりする多角的なシステム。

**インフラ:** 倉庫（3段階）、仲介業者事務所（3つの地域に2段階）、購入可能なライセンス5種類。それぞれが取引のタイミング、規模、またはアクセスを変化させる。

**保険:** 船体、貨物、契約保証。リスクに対する追加料金。保険金請求の承認または拒否。

**信用:** 金利、支払い期限、デフォルト時のペナルティを含む、3段階の信用システム。リスクを伴うレバレッジ。

**キャリア** — 6つのカテゴリに分けられた27の重要なステップ。キャリアプロファイルの解釈（主要/二次/新興タグ）。勝利への4つの道筋：合法的な貿易会社、影のネットワーク、広大な海洋ルート、そして商業帝国。

## 勝利への道筋

- **合法的な貿易会社** — 厳格な正当性。高い信頼性、高額な契約、清廉な評判、広範なインフラ。
- **影のネットワーク** — 秘密裏で利益の高い取引。監視下にある高利益率、リスク管理、強靭な運営。
- **広大な海洋ルート** — 長距離の商業力。東インドへのアクセス、遠隔地のインフラ、主要ルートの支配。
- **商業帝国** — 統合された多地域運営。すべての地域にインフラを構築、多様な収入源、金融力。

詳細なプレイヤー向けの説明については、[docs/CAREER_PATHS.md](docs/CAREER_PATHS.md) を参照してください。

## コマンドリファレンス

ゲーム内で `portlight guide` コマンドを実行すると、グループ化されたコマンドリファレンスが表示されます。または、[docs/COMMANDS.md](docs/COMMANDS.md) を参照してください。

| グループ | コマンド |
|-------|----------|
| 取引 | `market`, `buy`, `sell`, `cargo` |
| 航行 | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| 契約 | `contracts`, `accept`, `obligations`, `abandon` |
| インフラ | `warehouse`, `office`, `license` |
| 金融 | `insure`, `credit` |
| キャリア | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| システム | `save`, `load`, `guide` |

## アルファ版

Portlight はアルファ版です。主要なシステムは完成しており、負荷テストも行われていますが、バランス調整は現在進行中です。

**安定している点:**
- すべてのシステムがエンドツーエンドで機能している
- 24のファイルにまたがる609件のテスト
- 9つの複合負荷シナリオ下で、14のシステム間の整合性が維持されている
- 7つのシナリオパックに7つのポリシーボットを使用したバランス調整システム

**調整中の点:**
- 密輸のスケール（現在のところ、船のアップグレードにおいてパフォーマンスが低い）
- 地中海ルートの集中度（ポルト・ノヴォ/シルバ・ベイが交通量を支配している）
- 契約の完了率（自動実行におけるデリバリーロジックの欠陥）
- 保険の導入（シミュレーションプレイではほぼゼロ）

詳細については、[docs/ALPHA_STATUS.md](docs/ALPHA_STATUS.md) を参照し、具体的な問題については [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) を参照してください。

## セキュリティとデータ

Portlight は、**ローカル環境でのみ動作するコマンドラインゲーム**です。ゲームプレイ中にネットワーク接続は一切行いません。アクセスするデータは、ローカルのセーブファイル (`saves/`) とレポートファイル (`artifacts/`) であり、すべてJSON形式でローカルファイルシステムに保存されます。機密情報、認証情報、テレメトリー、リモートサービスは一切使用しません。管理者権限も不要です。詳細については、[SECURITY.md](SECURITY.md) を参照してください。

## 開発

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

## ライセンス

MIT

---

制作：<a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
