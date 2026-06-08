# 第3段階ロードマップ

## BIM Data Quality & AI Readiness Assessment PoC 拡張計画

## 保存先

```text
docs/phase3_roadmap.md
```

このドキュメントは、第3段階A〜E全体の上位ロードマップとして扱う。

各段階の詳細計画は、必要に応じて個別の `docs/` ファイルとして作成する。

例：

```text
docs/local_llm_extension_plan.md
docs/room_category_extension_plan.md
docs/pyrevit_element_metadata_export_plan.md
docs/rag_azure_ai_search_architecture.md
docs/fix_priority_training_data_design.md
```

---

## 目的

第3段階では、第2段階で完成した `BIM Data Quality & AI Readiness Assessment PoC` を崩さず、既存成果物を活用しながら段階的に拡張する。

第2段階では、Revit/BIMデータに対して以下を実装した。

```text
Revit集計表TXT
↓
CSV変換
↓
データクレンジング
↓
RuleIdベース品質チェック
↓
QualityScore
↓
AI Readiness Score
↓
AI Context v002
↓
Fix Guide Markdown
↓
Streamlit表示
```

第3段階では、この流れを以下の方向へ拡張する。

```text
1. 後段AI活用を小さく検証する
2. BIMデータの対象カテゴリを広げる
3. Revitモデルからの直接取得に近づける
4. 将来的なRAG / Azure AI Search構成を検討する
5. FixPriority仮ラベルを実務教師データ設計へつなげる
```

---

## 基本方針

第3段階では、新しい別PoCを作成するのではなく、既存PoCの拡張として進める。

理由：

* 既存のREADME、docs、Streamlit、出力CSV / Markdown、ポートフォリオPDFとの整合を保てる
* 第2段階で作成した `AI Context v002` と `Fix Guide Markdown` を活用できる
* BIMデータ品質評価からAI活用準備度評価、後段AI活用まで自然につながる
* GitHub上のポートフォリオの軸が分散しない
* 「BIM導入支援 × AI・データ活用支援」の方向性を強化できる

---

## 第3段階でやらないこと

第3段階では、以下をいきなり本格実装しない。

```text
本格RAGシステム構築
Azure AI Search本格実装
Azure OpenAI / OpenAI API本格接続
Revitモデル自動修正
設計判断・施工判断の自動化
深層学習
ファインチューニング
機械学習モデルの精度追求
複雑なPower BI再設計
別PoCの新規作成
```

第3段階では、あくまで既存PoCの延長として、実験・設計・小規模拡張に留める。

---

# 第3段階 全体構成

```text
第3段階A：Local LLM Explanation Demo
第3段階B：Roomカテゴリ追加
第3段階C：pyRevitでElementId / UniqueId取得PoC
第3段階D：RAG / Azure AI Search構成検討
第3段階E：FixPriority教師データ設計
```

---

## フェーズ間の関係

| フェーズ                                 | 依存する成果物                                        | 次フェーズへの影響              |
| ------------------------------------ | ---------------------------------------------- | ---------------------- |
| A: Local LLM Explanation Demo        | AI Context v002 / Fix Guide Markdown           | AI Contextの後段活用を確認する   |
| B: Roomカテゴリ追加                        | Door用既存パイプライン / RuleId設計                       | 複数カテゴリ対応、RAG対象拡張につながる  |
| C: pyRevitでElementId / UniqueId取得PoC | 既存CSV列設計 / Revit列マッピング                         | Revitモデルからの直接取得への入口になる |
| D: RAG / Azure AI Search構成検討         | AI Context / Fix Guide / docs / Rule Master    | 将来の検索・回答構成設計につながる      |
| E: FixPriority教師データ設計                | FixPriority仮ラベル / 品質メトリクス / AI Readiness Score | 実務ラベル設計、将来的な分類改善につながる  |

---

## 各段階の成果物の位置づけ

| 段階 | 成果物の種類            | 位置づけ                             |
| -- | ----------------- | -------------------------------- |
| A  | Local LLM実験デモ     | 既存AI Contextの後段活用検証              |
| B  | 既存PoC本体の機能拡張      | Door以外のBIMカテゴリへ対象拡張              |
| C  | Revit連携の小規模PoC    | Revit内部ElementId / UniqueId取得の入口 |
| D  | RAG / Azure構成検討資料 | 本格実装前のアーキテクチャ検討                  |
| E  | 教師データ設計資料         | FixPriority仮ラベルを実務ラベル設計へ接続       |

---

## README / Portfolio PDF 更新方針

第3段階A〜Eの各作業完了ごとに、READMEを大幅更新しない。

まずは各作業の詳細を `docs/` に記録する。
READMEには、成果がMVPとして安定し、ポートフォリオ上の説明価値が明確になった段階で小さく反映する。

Portfolio PDFは、第3段階A〜C程度までまとまった段階で更新を検討する。
第3段階A単体では、原則としてPDF更新は必須としない。

この方針により、READMEとPDFの肥大化を防ぎ、GitHubトップページの見やすさを維持する。

---

# 第3段階A：Local LLM Explanation Demo

## 目的

第2段階で生成した `AI Context v002` と `Fix Guide Markdown` を、ローカルLLMに読み込ませ、BIM担当者向けの説明文を生成できるかを検証する。

目的は、LLMに設計判断や施工判断をさせることではない。

既存PoCで構造化した以下の情報をもとに、BIM担当者が確認しやすい説明文へ変換できるかを確認する。

```text
RuleId
Severity
QualityScore
AI Readiness Score
HumanReviewRequired
FixGuide
BlockingRuleIds
```

## 位置づけ

第3段階Aは、既存PoCの後段AI活用デモである。

```text
AI Context v002
+ Fix Guide Markdown
↓
Local LLM
↓
BIM担当者向け説明文
↓
人間確認前提の修正方針案
```

## 主な成果物

```text
docs/local_llm_extension_plan.md
docs/local_llm_prompt_template.md
docs/local_llm_experiment.md
06_local_llm/README.md
06_local_llm/local_llm_prompt_input_sample_v001.md
06_local_llm/local_llm_explanation_examples_v001.md
```

## 完了条件

* ローカルLLM環境で日本語応答を確認する
* ElementId 1件単位のAI Contextを入力に使う
* 該当RuleIdのFix Guideを入力に使う
* BIM担当者向け説明文を1〜3例生成する
* 出力をMarkdownで記録する
* Raw LLM OutputとHuman Reviewを分けて記録する
* 評価表でOK / Partial / NGを記録する
* LLMの回答は参考情報であり、最終判断は人間が行うことを明記する

---

# 第3段階B：Roomカテゴリ追加

## 目的

現在のPoCは、主にドア建具表を対象としている。

Roomカテゴリを追加することで、部材情報だけでなく、空間情報に対してもBIMデータ品質とAI Readinessを評価できるようにする。

## Roomカテゴリを追加する理由

Roomは、BIMにおける空間情報・用途情報・面積情報として重要である。

以下の情報が整備されていないと、BI、データ分析、生成AI、RAGで使いにくくなる。

```text
RoomName
RoomNumber
Area
Level
Zone
Department
Finish
ClassificationCode
```

## ルール案

| RuleId | 内容                    | AI活用上の影響            |
| ------ | --------------------- | ------------------- |
| R-101  | RoomName未入力           | 空間の意味をAIが判断しにくい     |
| R-102  | RoomNumber未入力         | 部屋識別・検索・参照が不安定になる   |
| R-103  | Area未入力または0           | 面積分析・BI・コスト分析に使いにくい |
| R-104  | Level未入力              | 階別集計・空間把握に使いにくい     |
| R-105  | Zone未入力               | 管理区分・検索・RAGの文脈が弱くなる |
| R-106  | ClassificationCode未入力 | 標準分類・データ連携に使いにくい    |

## 想定処理フロー

```text
Revit Room Schedule TXT
↓
CSV変換
↓
データクレンジング
↓
Room用RuleIdベース品質チェック
↓
QualityScore
↓
AI Readiness Score
↓
AI Context
↓
Fix Guide
↓
Streamlit表示
```

## 想定成果物

```text
03_input_csv/room_schedule_export_test_v001.txt
03_input_csv/room_schedule_converted_v001.csv
03_input_csv/cleaned_room_data_v001.csv

04_output_csv/check_results_room_v001.csv
04_output_csv/room_quality_metrics_v001.csv
04_output_csv/room_ai_readiness_scores_v001.csv
04_output_csv/room_ai_context_v001.md
04_output_csv/room_fix_guides_v001.md

docs/room_category_extension_plan.md
```

## 完了条件

* Room用の入力サンプルを作成する
* Room用RuleIdを設計する
* Roomデータを既存品質チェックフローに接続する
* RoomカテゴリのQualityScoreとAI Readiness Scoreを出力する
* READMEまたはdocsにDoor / Room複数カテゴリ対応として整理する

---

# 第3段階C：pyRevitでElementId / UniqueId取得PoC

## 目的

現在のPoCでは、Revit集計表TXTをPythonへ渡して処理している。

第3段階Cでは、pyRevitを使ってRevitモデルから直接、ElementId / UniqueIdなどのメタデータを取得する入口を作る。

## 背景

現在の制約として、`ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用している。

pyRevitで内部ElementIdやUniqueIdを取得できるようにすることで、Revit実務との接続が強くなる。

## MVP

最初は、選択要素に対して以下を取得する小さなPoCとする。

```text
ElementId
UniqueId
Category
FamilyName
TypeName
```

必要に応じて、以下も候補とする。

```text
Level
RoomName
ParameterName
ParameterValue
```

## 想定処理フロー

```text
Revitで要素選択
↓
pyRevitボタン実行
↓
ElementId / UniqueId / Category / FamilyName / TypeName取得
↓
CSV出力
↓
既存品質チェック用CSV形式へ接続検討
```

## 想定成果物

```text
docs/pyrevit_element_metadata_export_plan.md
pyrevit_scripts/export_selected_element_metadata.py
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

## 完了条件

* pyRevitで選択要素の基本メタデータを取得する
* CSVとして出力する
* 既存品質チェックパイプラインに接続可能かを整理する
* READMEまたはdocsに、Revit集計表TXTだけでなく直接取得へ拡張する方針を記載する

---

# 第3段階D：RAG / Azure AI Search構成検討

## 目的

本格実装ではなく、将来的にRAG / Azure AI Searchへ拡張する場合の構成を整理する。

以下を検討する。

```text
検索対象
チャンク単位
メタデータ設計
想定質問
回答時の制約
HumanReviewRequiredの扱い
```

## なぜ本格実装しないか

RAG / Azure AI Search本格実装には、以下が必要になる。

```text
Azure Blob Storage
Azure AI Search
Azure OpenAI
ベクトル化
チャンク設計
認証
APIキー管理
コスト管理
Streamlit / FastAPI連携
引用表示
回答評価
セキュリティ
```

第3段階Dでは、これらを本格実装せず、アーキテクチャ検討に留める。

## 検索対象候補

```text
ai_context_v002.md
fix_guides_v001.md
bim_rule_master_v003.csv
docs/rule_specification.md
docs/evaluation_policy.md
docs/limitations.md
docs/data_dictionary.md
docs/revit_schedule_column_mapping.md
README.md
```

Room追加後の候補：

```text
room_ai_context_v001.md
room_fix_guides_v001.md
room_rule_master
```

## チャンク設計案

| チャンク種類        | 単位          |
| ------------- | ----------- |
| Element chunk | ElementId単位 |
| Rule chunk    | RuleId単位    |
| Policy chunk  | docsの見出し単位  |

## メタデータ設計案

```text
id
source_file
chunk_type
element_id
category
rule_id
severity
quality_score
ai_readiness_score
ai_readiness_level
human_review_required
content
```

Room追加後の候補：

```text
level
room_name
room_number
zone
classification_code
```

## 想定成果物

```text
docs/rag_azure_ai_search_architecture.md
docs/rag_target_documents.md
docs/rag_chunking_policy.md
docs/rag_metadata_design.md
docs/rag_query_examples.md
docs/rag_risk_and_limitations.md
```

## 完了条件

* RAG / Azure AI Searchの検索対象を整理する
* チャンク単位を整理する
* メタデータ設計を整理する
* 想定質問と回答制約を整理する
* 本格実装前のアーキテクチャ検討資料としてdocsにまとめる

---

# 第3段階E：FixPriority教師データ設計

## 目的

現在のFixPriorityは、QualityScoreとHigh違反件数をもとにした仮ラベルである。

第3段階Eでは、実務修正履歴を使った教師データ設計方針を整理する。

## 背景

現時点のFixPriority分類プロトタイプは、機械学習モデルの精度追求ではなく、品質チェック結果を特徴量化して分類処理へ接続できることを確認する初期実装である。

将来的に実務に近づけるには、以下のような実務情報が必要になる。

```text
修正工数
修正履歴
手戻り有無
後工程影響
発注者要件への影響
人間確認要否
実際の修正優先度
レビューコメント
```

## 教師データ設計項目

```text
ElementId
Category
RuleViolationCount
HighViolationCount
MediumViolationCount
QualityScore
AIReadinessScore
FixTimeEstimate
ReworkRisk
DownstreamImpact
OwnerRequirementImpact
HumanReviewRequired
ActualFixPriority
ReviewerComment
```

## 想定成果物

```text
docs/fix_priority_labeling_policy.md
docs/fix_priority_training_data_design.md
sample_data/fix_priority_training_sample_v001.csv
```

## 完了条件

* 現在のFixPriority仮ラベルの限界を整理する
* 実務教師データに必要な項目を整理する
* サンプル教師データ構造を設計する
* 将来的な分類モデル改善に必要なデータ条件を整理する

## 補足：随時メモの扱い

第3段階Eは最後に整理する想定だが、A〜Dの作業中に気づいたFixPriority教師データ設計に関するメモは随時記録する。

例：

```text
Roomカテゴリで修正優先度に影響しそうな項目
Local LLM説明生成で不足したFixPriority情報
RAG設計時に検索・回答へ使いたい優先度情報
pyRevit取得時に追加できそうな実務メタデータ
```

必要に応じて、以下の下書きに追記する。

```text
docs/fix_priority_training_data_design.md
```

---

# 推奨実行順

第3段階は、以下の順で進める。

```text
1. 第3段階A：Local LLM Explanation Demo
2. 第3段階B：Roomカテゴリ追加
3. 第3段階C：pyRevitでElementId / UniqueId取得PoC
4. 第3段階D：RAG / Azure AI Search構成検討
5. 第3段階E：FixPriority教師データ設計
```

## この順番にする理由

### Aを先にする理由

* 既存成果物をすぐ使える
* AIデスクトップPCを活かせる
* `AI Context v002` を作った意味が明確になる
* APIキーなしで検証できる
* 小さく始められる

### Bを次にする理由

* PoC本体をDoor以外へ拡張できる
* 「ドア建具表のみ」という弱点を補える
* RoomはAI ReadinessやRAGと相性が良い

### Cを次にする理由

* Revit実務との接続が強くなる
* 現在の仮ElementIdの制約を補強できる
* pyRevit / Revit API連携の入口になる

### Dを次にする理由

* AI導入支援・RAG構成検討力を示せる
* ただし本格実装は重いため、設計資料に留める

### Eを最後に置く理由

* FixPriority仮ラベルの弱点を補える
* 機械学習モデルの精度追求ではなく、実務教師データ設計として扱える
* 地味だが、実務適用を考える上で重要

---

# 第3段階全体の完成イメージ

第3段階が進むと、PoCは以下のような構成になる。

```text
Revit集計表TXT
または pyRevit取得データ
↓
Door / Room 複数カテゴリ対応
↓
データクレンジング
↓
RuleIdベース品質チェック
↓
QualityScore
↓
AI Readiness Score
↓
AI Context
↓
Fix Guide
↓
Local LLM説明生成デモ
↓
RAG / Azure AI Search構成検討
↓
将来的なAI導入支援提案へ接続
```

この状態により、以下を示せるようになる。

```text
BIMデータ品質評価
AI活用準備度評価
複数カテゴリ対応
Revit API連携入口
Local LLM説明生成
RAG / Azure構成検討
教師データ設計
```

---

# 注意点

第3段階では、範囲を広げすぎないことを重視する。

特に以下に注意する。

```text
Local LLMでモデル比較に深入りしない
Roomカテゴリ追加でルールを増やしすぎない
pyRevitで自動修正まで進まない
RAG / Azure AI Searchは設計に留める
FixPriorityは精度追求ではなく教師データ設計に留める
READMEやPDFを毎回大きく更新しすぎない
```

---

# 完了判断

第3段階全体は大きな拡張テーマであるため、一括完了ではなく、A〜Eごとに完了判断する。

まずは以下を最初の作業対象とする。

```text
第3段階A：Local LLM Explanation Demo
```

第3段階Aが完了した後、Roomカテゴリ追加へ進むか、Local LLMデモをREADMEへ反映するかを判断する。
