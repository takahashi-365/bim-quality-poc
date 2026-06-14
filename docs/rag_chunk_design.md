# RAG Chunk Design

## 目的

このドキュメントは、`BIM Data Quality & AI Readiness Assessment PoC` の成果物を、将来的にRAG / Azure AI Searchで活用する場合のチャンク設計を整理するものである。

第3段階Dでは、RAGシステムやAzure AI Searchを本格実装しない。

目的は、既存PoCで生成した以下の成果物を、将来的に検索・回答生成へ接続する場合の検索単位を明確にすることである。

```text
AI Context
Fix Guide
Rule Master
Check Results
AI Readiness Score
pyRevit Metadata
Door / Room 品質チェック結果
ElementId / UniqueId
```

このドキュメントでは、どの単位で情報を分割し、どのキーで関連付け、どの情報を回答根拠として扱うかを整理する。

---

## このドキュメントの位置づけ

このドキュメントは、第3段階D「RAG / Azure AI Search構成検討」の一部である。

親ドキュメントは以下とする。

```text
docs/rag_azure_ai_search_architecture_plan.md
```

関連ドキュメントは以下を想定する。

```text
docs/rag_metadata_design.md
docs/rag_query_examples.md
docs/rag_answer_policy.md
docs/rag_limitations.md
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl
```

第3段階Dでは、実装ではなく設計方針の整理に留める。

---

## チャンク設計の基本方針

RAGで利用する情報は、CSVやMarkdownをそのまま全文検索対象にするのではなく、検索しやすい単位に整理する。

基本方針は以下とする。

```text
要素単位で検索できること
RuleId単位で検索できること
Category単位で検索できること
Fix GuideをRuleIdと関連付けられること
ElementId / UniqueIdで参照できること
Severityで絞り込めること
HumanReviewRequiredで絞り込めること
回答時にSourceFileへ戻れること
```

RAG回答では、LLMの生成文だけに依存せず、元データに戻れる構成にする。

そのため、各チャンクには可能な範囲で以下を持たせる。

```text
DocumentType
Category
ElementId
UniqueId
RuleId
Severity
HumanReviewRequired
SourceFile
```

---

## チャンク種別

第3段階Dでは、以下の4種類のチャンクを基本候補とする。

```text
1. Element単位チャンク
2. RuleId単位チャンク
3. Category単位チャンク
4. Fix Guide単位チャンク
```

初期MVPでは、まず `Element単位チャンク` と `RuleId単位チャンク` を中心に考える。

`Category単位チャンク` と `Fix Guide単位チャンク` は、回答の補助情報または将来拡張候補として扱う。

---

# 1. Element単位チャンク

## 目的

Element単位チャンクは、1つのBIM要素に関する品質チェック結果、AI Readiness Score、人間確認要否、関連RuleIdをまとめるチャンクである。

主に以下の質問に対応する。

```text
このElementIdの品質問題を説明して
このUniqueIdのAI Readiness Scoreが低い理由を教えて
この要素をBIやRAGで使う前に何を確認すべきか
HumanReviewRequired=Trueの要素を確認したい
```

---

## 主な入力候補

```text
04_output_csv/ai_context_v002.md
04_output_csv/ai_context_v002.json
04_output_csv/check_results_revit_v002.csv
04_output_csv/ai_readiness_scores_v001.csv
04_output_csv/room_ai_context_v001.md
04_output_csv/room_ai_readiness_scores_v001.csv
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

---

## 想定フィールド

```text
id
document_type
chunk_type
category
element_id
unique_id
family_name
type_name
level_name
room_name
room_number
rule_id
rule_name
severity
quality_score
ai_readiness_score
ai_readiness_level
human_review_required
fix_priority
issue_summary
fix_guide_reference
source_file
content
```

---

## contentに含める情報

Element単位チャンクの `content` には、検索・回答生成に使う本文を格納する。

例：

```text
ElementId 12345 の Door 要素では、RuleId D-002 に該当する品質問題が検出されている。
Severity は High であり、AI Readiness Score に影響する。
HumanReviewRequired は True であるため、BIM担当者による確認が必要である。
Fix Guide では、分類コードや関連パラメータを確認することが推奨されている。
```

---

## Element単位チャンクの役割

Element単位チャンクは、RAG検索における中心的な検索対象とする。

理由は以下である。

```text
BIM担当者が実際に確認する単位に近い
ElementId / UniqueIdでRevit要素へ戻りやすい
RuleId、Severity、AI Readiness Scoreをまとめて扱いやすい
HumanReviewRequiredの判断を回答に反映しやすい
```

---

## 注意点

ElementIdには2種類の意味が存在する可能性がある。

```text
既存PoC上の仮ElementId
Revit内部のElementId
```

第3段階CでpyRevitにより取得したRevit内部ElementId / UniqueIdを扱う場合は、既存PoC上の仮ElementIdと混同しないようにする。

将来的には、以下のように分けることも検討する。

```text
poc_element_id
revit_element_id
unique_id
```

第3段階Dでは、実装までは行わず、設計上の注意点として記録する。

---

# 2. RuleId単位チャンク

## 目的

RuleId単位チャンクは、品質チェックルールの意味、対象カテゴリ、Severity、AI活用上の影響、修正方針をまとめるチャンクである。

主に以下の質問に対応する。

```text
R-101は何を意味するか
D-002の修正方針を教えて
High Severityのルールを説明して
RoomカテゴリのRuleIdを確認したい
```

---

## 主な入力候補

```text
02_rule_master/bim_rule_master_v003.csv
04_output_csv/fix_guides_v001.md
04_output_csv/room_fix_guides_v001.md
docs/rule_specification.md
docs/evaluation_policy.md
```

---

## 想定フィールド

```text
id
document_type
chunk_type
category
rule_id
rule_name
target_category
severity
check_description
ai_impact
fix_guide
human_review_policy
source_file
content
```

---

## contentに含める情報

RuleId単位チャンクの `content` には、RuleIdの意味と修正方針を説明できる情報を格納する。

例：

```text
RuleId R-101 は RoomName 未入力を検出するルールである。
対象カテゴリは Room である。
RoomName が未入力の場合、空間の意味をAIやBIが判断しにくくなる。
修正方針として、Revit上のRoomNameを確認し、実際の部屋用途に基づいて入力することが推奨される。
最終判断はBIM担当者が行う。
```

---

## RuleId単位チャンクの役割

RuleId単位チャンクは、Element単位チャンクを説明するための補助根拠として扱う。

Element単位チャンクで検出された `RuleId` をキーにして、RuleId単位チャンクまたはFix Guide単位チャンクを参照する。

想定する関連は以下である。

```text
Element chunk
↓ RuleId
RuleId chunk
↓ RuleId
Fix Guide chunk
```

---

## 注意点

RuleId単位チャンクは、品質問題の意味を説明するための情報であり、設計判断・施工判断を行うものではない。

回答時には以下を避ける。

```text
設計の正否判定
施工可否の判断
法規適合性の最終判断
Revitモデルの自動修正指示
```

---

# 3. Category単位チャンク

## 目的

Category単位チャンクは、Door / Roomなどのカテゴリごとに、よくある品質問題やAI活用上の注意点をまとめるチャンクである。

主に以下の質問に対応する。

```text
Doorカテゴリでよくある品質問題を教えて
RoomカテゴリでAI活用前に確認すべき項目は？
カテゴリごとにHumanReviewRequiredが出やすい項目を整理したい
```

---

## 主な入力候補

```text
Door用Check Results
Room用Check Results
Door用AI Readiness Score
Room用AI Readiness Score
Rule Master
Fix Guide
```

---

## 想定フィールド

```text
id
document_type
chunk_type
category
common_rule_ids
common_issues
ai_readiness_impact
recommended_review_points
source_file
content
```

---

## contentに含める情報

Category単位チャンクの `content` には、カテゴリごとの傾向や確認観点を格納する。

例：

```text
Roomカテゴリでは、RoomName、RoomNumber、Area、Levelなどの空間情報がAI Readinessに影響する。
RoomNameが未入力の場合、空間の意味をAIが判断しにくくなる。
RoomNumberが未入力の場合、部屋識別や検索・参照が不安定になる。
AI活用前には、RoomName、RoomNumber、Area、Levelの確認を優先する。
```

---

## Category単位チャンクの役割

Category単位チャンクは、個別要素ではなく、カテゴリ全体の説明に使う。

初期MVPでは必須ではないが、BIM担当者向けの説明やレポート生成では有効である。

---

## 注意点

Category単位チャンクは、集計的・説明的な情報であり、個別要素の最終判断には使わない。

個別要素について回答する場合は、Element単位チャンクを優先する。

---

# 4. Fix Guide単位チャンク

## 目的

Fix Guide単位チャンクは、RuleIdごとの修正方針を検索・回答生成に使いやすい形へ整理するチャンクである。

主に以下の質問に対応する。

```text
このRuleIdに対する修正案を知りたい
BIM担当者向けの対応文を作りたい
この品質問題はどう確認すべきか
```

---

## 主な入力候補

```text
04_output_csv/fix_guides_v001.md
04_output_csv/room_fix_guides_v001.md
```

---

## 想定フィールド

```text
id
document_type
chunk_type
category
rule_id
severity
fix_guide_text
recommended_action
human_review_required
notes
source_file
content
```

---

## contentに含める情報

Fix Guide単位チャンクの `content` には、RuleIdごとの修正方針を格納する。

例：

```text
RuleId D-002 に該当する場合、対象要素の分類コードや関連パラメータを確認する。
入力情報だけで判断できない場合は、BIM担当者が元モデルまたは集計表を確認する。
修正は自動実行せず、BIM担当者による確認後に行う。
```

---

## Fix Guide単位チャンクの役割

Fix Guide単位チャンクは、LLM回答時の修正提案の根拠として扱う。

ただし、Fix Guideは修正命令ではなく、確認・対応方針の候補である。

回答時には以下の表現を優先する。

```text
確認することが推奨される
修正候補として考えられる
BIM担当者による確認が必要である
入力情報からは判断できない
```

以下のような断定表現は避ける。

```text
必ず修正する
この設計は誤りである
この施工は不可である
自動的に修正してよい
```

---

# チャンク間の関連付けキー

複数種類のチャンクを扱うため、チャンク同士を関連付けるキーを明確にする。

主な関連付けキーは以下である。

```text
ElementId
UniqueId
RuleId
Category
SourceFile
```

---

## ElementId

ElementIdは、PoC内で要素を参照するための基本キーである。

ただし、既存PoC上の仮ElementIdと、Revit内部ElementIdが混在する可能性があるため、将来的には以下のような整理を検討する。

```text
poc_element_id
revit_element_id
```

---

## UniqueId

UniqueIdは、Revit由来の安定識別子候補として扱う。

将来的にRAGやAzure AI SearchからRevit要素へ戻る場合、UniqueIdは重要な参照キーになる可能性がある。

ただし、第3段階Dでは、UniqueIdを使った実連携は行わない。

---

## RuleId

RuleIdは、品質チェック結果、Rule Master、Fix Guideを結び付ける最重要キーである。

想定する関連は以下である。

```text
Element chunk
↓ RuleId
RuleId chunk
↓ RuleId
Fix Guide chunk
```

---

## Category

Categoryは、Door / Roomなどの対象カテゴリを分けるキーである。

想定するカテゴリは以下である。

```text
Door
Room
Other
```

pyRevit Metadataでは、Revit由来のカテゴリ名が日本語で出力される場合がある。

例：

```text
ドア
```

この場合、RAG設計上は `Door` へ正規化することを検討する。

---

## SourceFile

SourceFileは、回答根拠を元ファイルへ戻すためのキーである。

RAG回答では、可能な範囲で参照元を明記する。

例：

```text
SourceFile: 04_output_csv/ai_context_v002.md
SourceFile: 04_output_csv/fix_guides_v001.md
SourceFile: 02_rule_master/bim_rule_master_v003.csv
```

---

# 想定する関連構造

第3段階Dで想定するチャンク間の関連構造は以下である。

```text
Element chunk
├── RuleId → RuleId chunk
├── RuleId → Fix Guide chunk
├── UniqueId → pyRevit Metadata
├── Category → Category chunk
└── SourceFile → 元データ
```

RuleIdを中心にした関連は以下である。

```text
RuleId chunk
├── RuleId → Fix Guide chunk
├── Category → Category chunk
└── SourceFile → Rule Master / docs
```

Categoryを中心にした関連は以下である。

```text
Category chunk
├── Category → Element chunk
├── Category → RuleId chunk
└── Category → Fix Guide chunk
```

---

# HumanReviewRequiredの扱い

HumanReviewRequiredは、RAG回答で特に重要なメタデータである。

`HumanReviewRequired=True` の場合、回答には必ず以下を含める。

```text
BIM担当者による確認が必要である
LLM回答は参考情報である
最終判断はBIM担当者が行う
```

`HumanReviewRequired=False` の場合でも、LLMが最終判断を行うわけではない。

回答では、以下の前提を維持する。

```text
入力データに基づく参考情報である
必要に応じてBIM担当者が確認する
設計・施工・法規の最終判断は行わない
```

---

# SourceFileの扱い

RAG回答では、チャンクの本文だけでなく、元ファイルに戻れることを重視する。

そのため、すべてのチャンクに `SourceFile` を持たせる。

SourceFileには、可能な範囲で以下を記録する。

```text
元ファイルパス
生成元CSVまたはMarkdown
生成日
処理バージョン
```

初期MVPでは、少なくとも元ファイルパスを保持する。

---

# 初期MVPで採用するチャンク設計

第3段階Dの初期MVPでは、以下を優先する。

```text
Element単位チャンク
RuleId単位チャンク
Fix Guide単位チャンク
```

Category単位チャンクは、余力があれば作成する。

優先順位は以下とする。

```text
1. Element単位チャンク
2. RuleId単位チャンク
3. Fix Guide単位チャンク
4. Category単位チャンク
```

理由：

```text
Element単位はBIM担当者の確認単位に近い
RuleId単位は品質問題の意味を説明しやすい
Fix Guide単位は対応案の根拠として使いやすい
Category単位は全体説明には有効だが、初期MVPでは必須ではない
```

---

# 将来拡張候補

将来的には、以下のチャンクを追加することも検討する。

```text
Policy chunk
Docs chunk
README chunk
Project summary chunk
AI Readiness summary chunk
FixPriority chunk
```

## Policy chunk

評価方針、制約、HumanReviewRequiredの扱いなどをまとめるチャンク。

入力候補：

```text
docs/evaluation_policy.md
docs/limitations.md
docs/rag_answer_policy.md
docs/rag_limitations.md
```

## Docs chunk

docs配下の説明資料を見出し単位で分割するチャンク。

## AI Readiness summary chunk

AI Readiness Scoreの分布やカテゴリ別傾向をまとめるチャンク。

## FixPriority chunk

第3段階Eで設計するFixPriority教師データと接続するチャンク。

---

# 制約

第3段階Dでは、以下は行わない。

```text
Azure AI Searchの実装
Azure OpenAI / OpenAI API接続
Embedding生成
ベクトル検索
インデックス作成の自動化
クラウド環境構築
認証・権限設計の実装
実案件データ投入
RAGチャットUIの開発
検索精度評価
Revitモデル自動修正
設計判断・施工判断の自動化
```

このドキュメントは、あくまで将来実装に向けた設計メモである。

---

# セキュリティ・公開範囲

RAG設計で扱うサンプルデータは、GitHub公開可能な情報に限定する。

含めてよいもの：

```text
公開可能なサンプルデータ
匿名化したPoC用データ
自作のサンプルJSONL
概念スキーマ
設計メモ
```

含めないもの：

```text
実案件データ
社外秘モデル由来情報
顧客名
プロジェクト名
個人情報
社内固有の分類コード
機密性の高い仕様情報
大量の実モデル由来パラメータ
```

---

# 完了条件

このドキュメントの完了条件は以下である。

```text
RAGで扱うチャンク種別を整理した
Element単位チャンクを定義した
RuleId単位チャンクを定義した
Category単位チャンクを定義した
Fix Guide単位チャンクを定義した
チャンク間の関連付けキーを整理した
ElementId / UniqueIdの扱いを整理した
RuleIdの役割を整理した
Categoryの扱いを整理した
SourceFileの扱いを整理した
HumanReviewRequiredの扱いを整理した
初期MVPで採用するチャンク設計を整理した
将来拡張候補を整理した
制約とセキュリティ方針を整理した
```

---

# 次に作成するドキュメント

次に作成するドキュメントは以下とする。

```text
docs/rag_metadata_design.md
```

`rag_metadata_design.md` では、各チャンクに付与するメタデータ項目と、Azure AI Searchを想定したフィールド用途を整理する。
