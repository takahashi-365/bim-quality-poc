# BIM Data Quality & AI Readiness Assessment PoC

## Portfolio Document v004 Draft

---

# 1. 表紙

## BIM Data Quality & AI Readiness Assessment PoC

## BIMデータ品質・AI活用準備度評価PoC

Revit / BIMデータを対象に、PythonによるBIMデータ品質チェック、AI Readiness評価、生成AI向け構造化コンテキスト生成、Fix Guide生成、Local LLM説明文生成デモ、pyRevitメタデータ取得、RAG / Azure AI Search構成検討、FixPriority教師データ設計までを整理した個人開発PoC。

### 作成目的

BIM導入支援・Revit運用支援の実務経験をもとに、建築BIMデータをAI、RAG、BI、将来的な機械学習で扱うための前処理、品質評価、AI活用準備度評価、構造化コンテキスト生成、人間レビュー設計までの一連の流れを個人PoCとして構築する。

本PoCは、生成AI APIやRAGシステムそのものを作ることではなく、AIに渡す前のBIMデータ品質、参照情報、修正方針、人間確認要否を整理することを主目的とする。

### 使用技術

```text
Python
pandas
pytest
Streamlit
CSV / TXT
JSON / JSONL
Markdown
Revit Schedule Export
pyRevit
Revit API
Local LLM
Ollama / LM Studio
Mermaid
Power BI
RAG / Azure AI Search Design
```

---

# 2. 背景・課題

BIM導入支援やRevit運用支援の現場では、モデル内のパラメータ未入力、分類コード未入力、命名規則違反、属性情報のばらつきなどにより、集計、検索、品質管理、後工程確認、AI活用の精度が下がる課題がある。

BIMデータは、図面作成やモデル作成だけでなく、数量集計、品質確認、BI可視化、データ分析、生成AI、RAG、将来的な機械学習などへ接続できる可能性がある。

しかし、データ品質が低い状態では、AIやデータ分析にそのまま活用することは難しい。

特に、生成AIやRAGにBIMデータを渡す場合、属性情報、分類コード、命名規則、要素ID、パラメータの意味、修正方針、人間確認要否が整理されていなければ、AIが誤った前提で回答したり、修正優先度を誤って判断する可能性がある。

そのため本PoCでは、BIMデータをAIに直接判断させるのではなく、RuleIdベースの品質チェック結果、QualityScore、AI Readiness Score、AI Context、Fix Guide、RAG向けメタデータ、FixPriority教師データ候補を整理し、AI活用前のデータ準備度を評価する仕組みを検証する。

---

# 3. PoCの目的

このPoCの目的は、Revit / BIMデータをPythonで処理し、AI、RAG、BI、将来的な機械学習に利用しやすい構造化データへ変換することである。

本PoCでは、AIモデルそのものの精度を高く見せることではなく、AIやデータ分析が扱えるBIMデータをどのように整備するかを重視している。

## 実装・整理した主な内容

```text
Revit Schedule TXTのCSV変換
Door / Roomデータのクレンジング
RuleIdベース品質チェック
QualityScore算出
AI Readiness Score算出
HumanReviewRequired判定
AI Context JSON / Markdown生成
Fix Guide Markdown生成
Streamlit簡易可視化
Local LLM説明文生成デモ
pyRevit ElementId / UniqueId取得MVP
RAG / Azure AI Search構成検討
FixPriority教師データ設計
```

## このPoCで行わないこと

```text
AIによる設計判断
AIによる施工判断
AIによる法規判断
Revitモデルの自動修正
Azure AI Searchの実デプロイ
Azure OpenAI / OpenAI API接続
Embedding生成
ベクトル検索
RAGチャットUI
機械学習モデル作成
fine-tuning
FixPriority完全自動判定
```

最終判断はBIM担当者が行う前提である。

---

# 4. 全体フロー図

本PoCでは、Revit集計表TXTやpyRevitメタデータCSVを起点として、Pythonによる品質チェック、メトリクス作成、AI Readiness Assessment、生成AI向け構造化コンテキスト生成、Fix Guide生成、Local LLM、RAG設計、FixPriority教師データ設計までを接続している。

## 処理フロー

```text
Revit集計表TXT / pyRevitメタデータCSV
↓
CSV変換 / メタデータCSV出力
↓
データクレンジング
↓
RuleIdベース品質チェック
↓
QualityScore算出
↓
FixPriorityプロトタイプ
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
人間レビュー
```

## PDF用図版

READMEでGitHub上のMermaid表示を確認済み。
v004 PDFでは、このMermaid図をもとにPDF向け図版として掲載する。

参照元：

```text
docs/poc_overall_flow_mermaid.md
docs/portfolio_visual_plan.md
```

---

# 5. 主な機能

## 1. Revit Schedule TXTのCSV変換

Autodesk公式の日本仕様Revitサンプルモデルから書き出した集計表TXTを、Python / pandasで品質チェック用CSVへ変換する。

## 2. データクレンジング

Revit集計表から出力されたデータを、品質チェックしやすい形へ整理する。

主な処理：

```text
列名整理
必要列抽出
欠損値処理
Category付与
Door / Room別の基本整形
PoC用ElementId付与
```

## 3. RuleIdベース品質チェック

BIM品質ルールをRuleIdで管理し、Door / Roomカテゴリの品質チェック結果をCSVとして出力する。

品質チェック結果は以下へ接続する。

```text
QualityScore
AI Readiness Score
AI Context
Fix Guide
HumanReviewRequired
RAG設計用メタデータ
FixPriority教師データ設計
```

## 4. QualityScore / AI Readiness Score

品質チェック結果をもとに、要素単位でQualityScoreを算出する。
さらに、BIMデータをAIやRAGへ渡しやすい状態かを評価する参考指標としてAI Readiness Scoreを算出する。

## 5. AI Context / Fix Guide

AI Contextでは、生成AIやRAGへ渡すことを想定した構造化コンテキストをJSON / Markdownで生成する。

Fix Guideでは、RuleId、Severity、AI Readinessへの影響、人間確認要否をもとに、BIM担当者向けの修正ガイドMarkdownを生成する。

---

# 6. Phase 3A〜3E 拡張内容

第3段階では、既存PoCを壊さず、以下の5方向へ拡張した。

## Phase 3A: Local LLM Explanation Demo

AI ContextとFix Guideを入力情報として、ローカルLLMでBIM担当者向け説明文を生成できるかを小さく検証した。

この検証はLLM性能比較ではなく、AI Contextが説明文生成の入力として機能するかを確認するためのものである。

LLM回答は参考情報であり、最終判断はBIM担当者が行う。

## Phase 3B: Room Category Extension

Door中心だった品質チェック・AI Readiness Assessmentを、Room Schedule TXTにも適用できるように拡張した。

Roomカテゴリでは、RoomName、RoomNumber、Area、Level、Category、QualityScore、AI Readiness Score、HumanReviewRequired、Fix Guideを扱う。

## Phase 3C: pyRevit Element Metadata Export MVP

pyRevitを使い、Revitモデル上の選択要素からElementId / UniqueIdなどの基本メタデータをCSV出力するMVPを追加した。

取得対象：

```text
ElementId
UniqueId
Category
FamilyName
TypeName
Name
LevelName
RoomName
RoomNumber
```

このMVPは、Revit内部メタデータを既存PoCや将来のAI Context / RAG設計に接続できる可能性を確認するためのものである。

## Phase 3D: RAG / Azure AI Search Architecture Design

既存PoC成果物を将来的にRAG / Azure AI Searchで扱う場合の構成検討を追加した。

整理した内容：

```text
RAG対象データ
主検索対象 / 補助対象
チャンク設計
メタデータ設計
ElementId / UniqueId / RuleId / Category / SourceFile の関連付け
Azure AI Searchを想定した概念スキーマ
サンプルRAGドキュメント
検索クエリ例
RAG回答方針
制約・セキュリティ方針
```

この段階では、Azure AI Search実デプロイ、Azure OpenAI / OpenAI API接続、Embedding生成、ベクトル検索、RAGチャットUIは実装していない。

## Phase 3E: FixPriority Training Data Design

FixPriorityを将来的な教師データ候補として扱うための設計を追加した。

整理した内容：

```text
教師データ1行の単位
教師データ列設計
CurrentFixPriorityとProposedFixPriorityLabelの違い
High / Medium / Low / Reviewのラベル方針
LabelReasonの扱い
HumanReviewRequiredとの関係
GitHub公開可能なサンプル教師データ
制約・対象外
```

Phase 3Eは教師データ設計であり、機械学習モデルの作成やFixPriorityの完全自動判定ではない。

---

# 7. 成果物・出力ファイル

## Door関連

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
04_output_csv/check_results_room_v001.csv
04_output_csv/room_quality_metrics_v001.csv
04_output_csv/room_ai_readiness_scores_v001.csv
04_output_csv/room_ai_context_v001.json
04_output_csv/room_ai_context_v001.md
04_output_csv/room_fix_guides_v001.md
```

## pyRevit関連

```text
03_input_csv/pyrevit_element_metadata_sample_v001.csv
pyrevit_scripts/export_selected_element_metadata.py
```

## Local LLM関連

```text
06_local_llm/README.md
06_local_llm/local_llm_prompt_input_sample_v001.md
06_local_llm/local_llm_explanation_examples_v001.md
```

## RAG設計関連

```text
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl
docs/rag_azure_ai_search_architecture_plan.md
docs/rag_answer_policy.md
docs/rag_limitations.md
```

## FixPriority教師データ設計関連

```text
07_fixpriority_training/fixpriority_training_samples_v001.csv
07_fixpriority_training/fixpriority_label_examples_v001.md
docs/fixpriority_training_data_design.md
docs/fixpriority_labeling_policy.md
docs/fixpriority_limitations.md
```

---

# 8. 画面・図解

## Streamlit簡易画面

Streamlitで、AI Readiness Score、AI Context、Fix Guideを確認できる簡易画面を作成した。

主な画面：

```text
AI Readiness Assessment Overview
AI Context v002 Preview
Fix Guide Preview
```

## README図解

READMEには、PoC全体フロー図をMermaidで追加した。
GitHub上で正常表示を確認済み。

参照資料：

```text
docs/poc_overall_flow_mermaid.md
docs/phase3_extension_mermaid.md
docs/portfolio_visual_plan.md
```

---

# 9. テスト結果

pytestで主要ロジックの最小テストを作成している。

## 主なテスト対象

```text
RuleIdベース品質チェック
AI Readiness Score
HumanReviewRequired
Room Pipeline
pyRevit Metadata CSV
FixPriority Training Data CSV
```

## 主なテストファイル

```text
tests/test_quality_check.py
tests/test_ai_readiness_score.py
tests/test_room_pipeline.py
tests/test_pyrevit_metadata_csv.py
tests/test_fixpriority_training_data.py
```

## 実行例

```powershell
$env:PYTHONPATH = "."
pytest -q
```

## 確認済み結果

```text
37 passed
```

---

# 10. 制約・対象外

現時点の主な制約と対象外は以下である。

```text
Revit由来データ対応は初期試作
Door / Roomカテゴリ中心
Door / RoomのElementIdは一部PoC用仮ID
QualityScoreとAI Readiness ScoreはPoC用の簡易指標
FixPriorityは実務の正解ラベルではなく仮ラベル
FixPriority教師データ設計は列設計・サンプル作成まで
Local LLMの出力は参考情報
Azure AI Search実デプロイは未実装
Azure OpenAI / OpenAI API接続は未実装
Embedding生成は未実装
ベクトル検索は未実装
RAGチャットUIは未実装
機械学習モデル作成は未実装
fine-tuningは未実装
Revitモデル自動修正は対象外
設計判断・施工判断・法規判断は対象外
実案件データは扱わない
```

本PoCは、AIモデルそのものを作るものではなく、AIに渡す前のBIMデータ品質・構造化・人間レビュー設計を整理するものである。

---

# 11. 今後の展開

今後の拡張候補は以下である。

```text
pyRevit Metadataを既存品質チェックパイプラインへ接続
Room要素選択時のRoomName / RoomNumber取得確認
AI Context / Fix Guide / Rule Masterを対象とした小規模RAG検証
ElementId / UniqueIdをRAGメタデータとして活用
HumanReviewRequired=Trueを考慮したRAG回答制御
ActualFixPriorityの記録設計
実務レビュー履歴を使った教師データ設計
Azure AI Search接続を行う場合のインデックス設計・権限管理・コスト管理
次成果物としてCOBie / BIMデータ統合作業を切り出し
```

---

# 12. まとめ

本PoCでは、Revit / BIMデータを対象に、Python / pandasによるデータ読み込み、データクレンジング、RuleIdベース品質チェック、QualityScore算出、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlit簡易可視化、ローカルLLMを使った説明文生成デモ、pyRevitメタデータ取得、RAG構成検討、FixPriority教師データ設計、pytestによる最小テストまでを整理した。

Phase 3A〜3Eを通じて、Local LLM、Roomカテゴリ、pyRevit ElementId / UniqueId、RAG / Azure AI Search設計、FixPriority教師データ設計まで拡張した。

なお、Azure AI Searchの実装、Embedding生成、ベクトル検索、RAGチャットUI、クラウド接続、機械学習モデル作成、fine-tuning、FixPriority完全自動判定は本段階では行っていない。

目的は、AIモデルそのものを作ることではなく、BIMデータをBI、データ分析、将来的な機械学習、生成AI、RAGで安全に活用するための前処理、品質評価、構造化、修正ガイド生成、説明文生成、RAG構成検討、教師データ設計、人間レビュー設計の流れを示すことである。

このPoCにより、BIM導入支援・Revit運用支援の経験を、建設業界向けのAI・データ活用支援へ拡張できることを示している。
