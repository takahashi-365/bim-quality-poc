# BIM Data Quality & AI Readiness Assessment PoC

## Portfolio Document v005 Draft

---

# 1. 表紙

## BIM Data Quality & AI Readiness Assessment PoC

## BIMデータ品質・AI活用準備度評価PoC

Revit / BIMデータを、BI・データ分析・将来的な機械学習・生成AI・RAGで活用する前に、データ品質とAI活用準備度を評価するための個人開発PoCです。

本PoCでは、Revit集計表TXT、Room Schedule TXT、pyRevitで取得した選択要素メタデータCSVをPythonで処理し、品質チェック、AI Readiness評価、生成AI向け構造化、Fix Guide生成、Local LLM説明文生成デモ、RAG構成検討、FixPriority教師データ設計までを整理しています。

## 目的

AIに設計判断・施工判断・法規判断をさせることではなく、BIM担当者が確認・判断しやすいように、BIMデータ品質、修正方針、人間確認要否、RAG向け構造を整理することを目的としています。

---

# 2. 背景・課題

BIM導入支援やRevit運用支援の現場では、モデル内のパラメータ未入力、分類コード未入力、命名規則違反、Room情報不足、属性情報のばらつきなどにより、後工程での集計、検索、品質確認、BI可視化、AI活用が難しくなることがあります。

BIMデータは、図面作成だけでなく、BI、データ分析、生成AI、RAG、将来的な機械学習へ接続できる可能性があります。

一方で、データ品質が低い状態のままAIやRAGへ渡すと、AIが誤った前提で回答したり、根拠のない修正案を出す可能性があります。

そのため本PoCでは、AI活用前の準備として、BIMデータ品質、RuleId、Severity、QualityScore、AI Readiness Score、Fix Guide、HumanReviewRequiredを構造化します。

---

# 3. 全体フロー

```text
Revit集計表TXT / Room Schedule TXT / pyRevitメタデータCSV
↓
PythonによるCSV変換・データクレンジング
↓
RuleIdベース品質チェック
↓
QualityScore算出
↓
AI Readiness Score算出
↓
HumanReviewRequired判定
↓
AI Context JSON / Markdown生成
↓
Fix Guide Markdown生成
↓
Local LLM説明文生成デモ
↓
RAG / Azure AI Search構成検討
↓
FixPriority教師データ設計
↓
BIM担当者による確認・判断
```

## 重要な方針

* AIは設計判断・施工判断・法規判断を行わない
* Revitモデルの自動修正は行わない
* Fix Guideは修正命令ではなく確認・対応案として扱う
* HumanReviewRequired=True の場合は人間確認が必要
* 最終判断はBIM担当者が行う

---

# 4. 主な機能

## Revit Schedule TXTのCSV変換

Revit集計表から書き出したTXTをPythonで読み込み、品質チェックしやすいCSVへ変換します。

## Door / Roomデータのクレンジング

DoorカテゴリとRoomカテゴリのデータを整理し、品質チェック用の入力データを作成します。

## RuleIdベース品質チェック

品質チェックルールをRuleIdで管理し、違反内容、Severity、対象パラメータ、Fix Guideを出力します。

## QualityScore / AI Readiness Score

品質チェック結果をもとに、要素単位のQualityScoreとAI Readiness Scoreを算出します。

## AI Context生成

生成AIやRAGへ渡す前段階の構造化情報として、AI Context JSON / Markdownを生成します。

## Fix Guide生成

RuleId、Severity、AI Readinessへの影響をもとに、BIM担当者向けのFix Guide Markdownを生成します。

---

# 5. Phase 3A〜3E 拡張内容

## Phase 3A: Local LLM Explanation Demo

AI ContextとFix Guideを入力情報として、ローカルLLMでBIM担当者向け説明文を生成できるかを検証しました。

目的はLLM性能比較ではなく、AI Contextが説明文生成の入力として使えるかを確認することです。

## Phase 3B: Room Category Extension

Door中心だった品質チェック・AI Readiness AssessmentをRoomカテゴリにも拡張しました。

RoomName、RoomNumber、Area、Level、Room QualityScore、Room AI Readiness Score、Room Fix Guideを扱います。

## Phase 3C: pyRevit Element Metadata Export MVP

pyRevitを使い、Revitモデル上の選択要素からElementId、UniqueId、Category、FamilyName、TypeName、LevelNameなどをCSV出力するMVPを作成しました。

Revitモデルの自動修正やパラメータ書き換えは行っていません。

## Phase 3D: RAG / Azure AI Search Architecture Design

AI Context、Fix Guide、Rule Master、品質チェック結果、AI Readiness Score、pyRevit Metadataを、将来的にRAG / Azure AI Searchで扱う場合の構成を整理しました。

この段階では、Azure AI Search実デプロイ、Embedding生成、ベクトル検索、RAGチャットUIは実装していません。

## Phase 3E: FixPriority Training Data Design

FixPriorityを将来的な教師データ候補として扱うため、列設計、ラベル方針、LabelReason、HumanReviewRequiredとの関係、サンプルCSVを整理しました。

機械学習モデル作成やFixPriorityの完全自動判定は行っていません。

---

# 6. 主な成果

## Door Category Results

| 項目                  |           結果 |
| ------------------- | -----------: |
| 対象Revit集計表          | 20 ドア 建具表 SD |
| クレンジング後の入力行数        |           25 |
| 品質チェック結果            |         100件 |
| AI Readiness Score  |   25要素すべて 40 |
| AI Readiness Level  |          Low |
| HumanReviewRequired |         True |

Doorサンプルでは、必須パラメータ未入力、分類コード未入力、命名規則違反が検出される設定のため、全要素のAI Readiness LevelがLowとなっています。

## Room Category Results

| 項目                        |                    結果 |
| ------------------------- | --------------------: |
| Total Room records        |                   113 |
| Room rule violations      |                    11 |
| Violated Room elements    |                    11 |
| Clean Room elements       |                   102 |
| Average Room QualityScore |                 99.03 |
| Room AI Readiness Level   |             High: 113 |
| HumanReviewRequired       | True: 11 / False: 102 |

Roomカテゴリでは、Doorとは異なる空間情報の品質チェックを行い、Room AI ContextとRoom Fix Guideを生成しました。

## pyRevit Metadata Export Results

| 項目                                 | 結果                         |
| ---------------------------------- | -------------------------- |
| Revit / pyRevit環境                  | Revit 2024 / pyRevit 6.4.0 |
| 0件選択時の安全中断                         | 確認済み                       |
| Door 1件選択時のCSV出力                   | 確認済み                       |
| Door複数選択時のCSV出力                    | 確認済み                       |
| ElementId / UniqueId取得             | 確認済み                       |
| Category / FamilyName / TypeName取得 | 確認済み                       |
| 匿名化サンプルCSV                         | 作成済み                       |

---

# 7. 主な出力ファイル

## Door / AI Readiness関連

```text
04_output_csv/check_results_revit_v002.csv
04_output_csv/quality_metrics_v001.csv
04_output_csv/ai_readiness_scores_v001.csv
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
04_output_csv/fix_guides_v001.md
```

## Room関連

```text
04_output_csv/room_quality_metrics_v001.csv
04_output_csv/room_ai_readiness_scores_v001.csv
04_output_csv/room_ai_context_v001.json
04_output_csv/room_ai_context_v001.md
04_output_csv/room_fix_guides_v001.md
```

## pyRevit関連

```text
pyrevit_scripts/export_selected_element_metadata.py
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

## RAG設計関連

```text
docs/rag_azure_ai_search_architecture_plan.md
docs/rag_metadata_design.md
docs/rag_answer_policy.md
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl
```

## FixPriority教師データ設計関連

```text
docs/fixpriority_training_data_design.md
docs/fixpriority_labeling_policy.md
07_fixpriority_training/fixpriority_training_samples_v001.csv
07_fixpriority_training/fixpriority_label_examples_v001.md
```

---

# 8. テスト結果

pytestで主要ロジックの最小テストを作成しています。

主なテスト対象：

* RuleIdベース品質チェック
* AI Readiness Score
* HumanReviewRequired
* Room Pipeline
* pyRevit Metadata CSV
* FixPriority Training Data CSV

実行例：

```powershell
$env:PYTHONPATH = "."
pytest -q
```

確認済み結果：

```text
37 passed
```

---

# 9. 技術スタック

主に使用している技術：

```text
Python
pandas
pytest
Streamlit
CSV / TXT
JSON / JSONL
Markdown
Revit Schedule TXT
pyRevit
Revit API
Local LLM
Ollama / LM Studio
Mermaid
Power BI
```

将来的な拡張候補：

```text
Azure AI Search
Azure OpenAI
OpenAI API
Embedding
Vector Search
RAG
FastAPI
```

---

# 10. 制約・対象外

現時点の主な制約と対象外は以下です。

* 本PoCは検証用であり、本番用のBIM品質管理システムではありません
* Door / Roomカテゴリ中心の検証です
* ElementIdにはPoC用仮IDとRevit内部ElementIdが混在する可能性があります
* QualityScoreとAI Readiness ScoreはPoC用の簡易指標です
* FixPriorityは実務の正解ラベルではなく仮ラベルです
* Local LLMの出力は参考情報です
* Azure AI Searchの実デプロイは未実装です
* Azure OpenAI / OpenAI API接続は未実装です
* Embedding生成、ベクトル検索、RAGチャットUIは未実装です
* 機械学習モデル作成、fine-tuningは未実装です
* Revitモデルの自動修正は対象外です
* 設計判断、施工判断、法規判断は対象外です
* 最終判断はBIM担当者が行う前提です

---

# 11. GitHub公開方針

GitHubには、公開可能なサンプルデータ、匿名化データ、設計資料、PoCコードのみを含めます。

含めないもの：

```text
実案件データ
顧客名
プロジェクト名
個人情報
社外秘モデル由来情報
実モデル由来のUniqueId
実モデル由来のElementId
APIキー
接続文字列
Azureリソース名
.env
ログファイル
モデルファイル
キャッシュ
```

---

# 12. まとめ

本PoCでは、Revit / BIMデータを対象に、Pythonによるデータ変換、データクレンジング、RuleIdベース品質チェック、QualityScore算出、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlit簡易可視化、Local LLM説明文生成デモ、pyRevitメタデータ取得、RAG構成検討、FixPriority教師データ設計、pytestによる最小テストまでを整理しました。

目的は、AIモデルそのものを作ることではなく、BIMデータをAI、RAG、BI、将来的な機械学習で安全に活用するための前処理、品質評価、構造化、人間レビュー設計の流れを示すことです。

このPoCにより、BIM導入支援・Revit運用支援の経験を、建設業界向けのAI・データ活用支援へ拡張できることを示しています。
