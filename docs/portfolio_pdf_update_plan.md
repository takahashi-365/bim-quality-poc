# Portfolio PDF Update Plan

## 目的

このドキュメントでは、`BIM Data Quality & AI Readiness Assessment PoC` の完成成果物として、Portfolio PDFを更新するための構成案を整理する。

READMEはGitHub上で詳細を説明する役割を持つ。
Portfolio PDFは、面接・ポートフォリオ確認・説明資料として、短時間でPoCの目的、構成、成果、制約、今後の展開を理解できるようにする。

---

## 更新方針

Portfolio PDFでは、READMEの内容をすべて載せるのではなく、以下を中心に整理する。

```text
PoCの背景
何を解決しようとしたか
どのような入力データを扱ったか
どのような処理フローか
Phase 3A〜3Eで何を拡張したか
どのような成果物があるか
何を実装していないか
今後どの方向へ展開できるか
```

PDFでは、技術詳細よりも「何を考え、どう構成し、どこまで検証したか」が伝わることを重視する。

---

## 想定ページ数

初期版は、以下の **10〜12ページ程度** を目安とする。

```text
最小構成：10ページ
標準構成：11ページ
詳細構成：12ページ
```

READMEより短く、GitHub上の詳細資料へ誘導できる構成にする。

---

# PDF構成案

## 1. 表紙

### 目的

PoC名とテーマを一目で伝える。

### 掲載内容

```text
BIM Data Quality & AI Readiness Assessment PoC
BIMデータ品質・AI活用準備度評価PoC
Revit / BIM data quality check for AI, RAG, BI, and future ML workflows
```

### 補足

以下を小さく入れる。

```text
Python / pandas / pytest / Streamlit / pyRevit / Local LLM / RAG Design
```

---

## 2. 背景・課題

### 目的

なぜこのPoCを作ったかを説明する。

### 掲載内容

BIM導入支援やRevit運用支援では、モデルを作るだけでなく、後工程で使えるデータ品質になっているかが重要になる。

BI、データ分析、生成AI、RAG、将来的な機械学習にBIMデータを使う場合、以下の問題があると活用しにくい。

```text
必須パラメータが未入力
分類コードが未入力
命名規則が統一されていない
RoomName / RoomNumber / Area / Level などが不足している
ElementId / UniqueId などの参照キーが整理されていない
人間確認が必要な箇所が明確でない
RAGで参照すべき根拠情報が整理されていない
```

---

## 3. PoCの目的

### 目的

このPoCが何をするものか、何をしないものかを明確にする。

### 掲載内容

このPoCは、BIMデータをAIやRAGに渡す前に、以下を整理するためのもの。

```text
BIM品質ルール
品質チェック結果
QualityScore
AI Readiness Score
HumanReviewRequired
AI Context
Fix Guide
RAG向けメタデータ
FixPriority教師データ候補
```

### 強調する制約

```text
AIが設計判断をしない
AIが施工判断をしない
AIが法規判断をしない
Revitモデルを自動修正しない
最終判断はBIM担当者が行う
```

---

## 4. 全体フロー図

### 目的

PoC全体の流れを視覚的に説明する。

### 掲載内容

READMEに追加したMermaid全体フロー図をもとに、PDF向けに図版化する。

対象図：

```text
docs/poc_overall_flow_mermaid.md
```

### 図で示す流れ

```text
Revit集計表TXT / pyRevitメタデータCSV
↓
CSV変換 / データクレンジング
↓
RuleIdベース品質チェック
↓
QualityScore / FixPriority / AI Readiness Score
↓
AI Context / Fix Guide
↓
Local LLM / RAG Design / FixPriority Training Data Design
```

### 備考

PDFでは、Mermaidをそのまま貼るより、PNG化またはPowerPoint図形化した方が見やすい可能性がある。

---

## 5. 主な機能

### 目的

PoCで実装・整理した機能を短く示す。

### 掲載内容

```text
Revit Schedule TXT のCSV変換
Door / Roomデータのクレンジング
RuleIdベース品質チェック
QualityScore算出
AI Readiness Score算出
AI Context JSON / Markdown生成
Fix Guide Markdown生成
Streamlit簡易可視化
Local LLM説明文生成デモ
pyRevit ElementId / UniqueId取得MVP
RAG / Azure AI Search構成検討
FixPriority教師データ設計
```

---

## 6. Phase 3A〜3E 拡張内容

### 目的

第3段階で何を拡張したかをまとめる。

### 掲載内容

```text
Phase 3A：Local LLM Explanation Demo
Phase 3B：Room Category Extension
Phase 3C：pyRevit Element Metadata Export MVP
Phase 3D：RAG / Azure AI Search Architecture Design
Phase 3E：FixPriority Training Data Design
```

### 使用する図

対象図：

```text
docs/phase3_extension_mermaid.md
```

PDFでは、A〜Eを横並びまたは放射状に整理する。

---

## 7. 成果物・出力ファイル

### 目的

PoCでどのような成果物が作られたかを説明する。

### 掲載内容

代表的な出力のみ掲載する。

```text
04_output_csv/check_results_revit_v002.csv
04_output_csv/quality_metrics_v001.csv
04_output_csv/ai_readiness_scores_v001.csv
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
04_output_csv/fix_guides_v001.md

04_output_csv/room_quality_metrics_v001.csv
04_output_csv/room_ai_readiness_scores_v001.csv
04_output_csv/room_ai_context_v001.json
04_output_csv/room_fix_guides_v001.md

03_input_csv/pyrevit_element_metadata_sample_v001.csv

05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl

07_fixpriority_training/fixpriority_training_samples_v001.csv
07_fixpriority_training/fixpriority_label_examples_v001.md
```

### 備考

PDFでは全ファイル一覧にしない。
詳細はREADMEまたはGitHubに誘導する。

---

## 8. 技術スタック

### 目的

使った技術を整理する。

### 掲載内容

```text
Python
pandas
pytest
Streamlit
Markdown
CSV
JSON
JSONL
Revit Schedule TXT
pyRevit
Revit API
Ollama
LM Studio
Local LLM
Mermaid
```

### 将来拡張候補

```text
Power BI
Azure AI Search
Azure OpenAI
OpenAI API
Embedding
Vector Search
RAG
FastAPI
```

### 注意

Azure AI Search、Azure OpenAI、OpenAI API、Embedding、Vector Search、RAG UIは、本PoCでは未実装であることを明記する。

---

## 9. テスト結果

### 目的

PoCが最低限のテストで検証されていることを示す。

### 掲載内容

```text
pytest
37 passed
```

主なテスト対象：

```text
RuleIdベース品質チェック
AI Readiness Score
HumanReviewRequired
Room Pipeline
pyRevit Metadata CSV
FixPriority Training Data CSV
```

実行例：

```powershell
$env:PYTHONPATH = "."
pytest -q
```

---

## 10. 制約・対象外

### 目的

このPoCの範囲を明確にし、過剰に見せない。

### 掲載内容

```text
Azure AI Search実デプロイは未実装
Azure OpenAI / OpenAI API接続は未実装
Embedding生成は未実装
ベクトル検索は未実装
RAGチャットUIは未実装
機械学習モデル作成は未実装
fine-tuningは未実装
FixPriority完全自動判定は未実装
Revitモデル自動修正は対象外
設計判断・施工判断・法規判断は対象外
実案件データは扱わない
```

### 強調点

このPoCは、AIモデルそのものを作るものではなく、AIに渡す前のBIMデータ品質・構造化・人間レビュー設計を整理するもの。

---

## 11. 今後の展開

### 目的

完成扱い後の展開候補を示す。

### 掲載内容

```text
pyRevit Metadataを既存品質チェックパイプラインへ接続
AI Context / Fix Guide / Rule Masterを対象とした小規模RAG検証
ElementId / UniqueIdをRAGメタデータとして活用
HumanReviewRequired=Trueを考慮したRAG回答制御
ActualFixPriorityの記録設計
実務レビュー履歴を使った教師データ設計
次成果物としてCOBie / BIMデータ統合作業を切り出し
```

---

## 12. まとめ

### 目的

ポートフォリオとして何を示せたかを締める。

### 掲載内容

このPoCでは、BIM導入支援・Revit運用支援の経験を、建設業界向けのAI・データ活用支援へ拡張する流れを示した。

BIMデータをAIやRAGで安全に活用するためには、単にAIへ渡すのではなく、以下が必要である。

```text
品質チェック
スコア化
構造化コンテキスト
修正ガイド
人間確認要否
RAG向けメタデータ
教師データ設計
制約整理
```

本PoCは、それらを一連の小規模ワークフローとして整理した成果物である。

---

# PDFに入れない情報

Portfolio PDFには以下を入れない。

```text
実案件名
顧客名
個人名
社内固有の分類コード
実モデル由来のUniqueId
実モデル由来のElementId
ローカルパス
APIキー
接続文字列
Azureリソース名
.env
ログファイル
```

---

# 図の扱い

## 使用候補図

```text
PoC全体フロー図
Phase 3A〜3E拡張図
```

## 元ファイル

```text
docs/poc_overall_flow_mermaid.md
docs/phase3_extension_mermaid.md
docs/portfolio_visual_plan.md
```

## PDF向け変換候補

```text
GitHub上のMermaid表示を参考にPowerPoint図形で作成
MermaidをPNG化
draw.ioで清書
PowerPointで再作図
```

初期版では、READMEで正常表示確認済みのMermaid構成をもとに、PDF用にPowerPointまたはPNGで扱う。

---

# 完了条件

Portfolio PDF更新作業は、以下を満たしたら完了とする。

```text
PDF構成案を作成した
全体フロー図をPDFに載せた
Phase 3A〜3Eの拡張内容を載せた
主要成果物を載せた
技術スタックを載せた
37 passed のテスト結果を載せた
制約・対象外を載せた
今後の展開を載せた
実案件・顧客情報・個人情報を含めていない
```

---

# 次の作業

次の作業は以下。

```text
1. この構成案を保存する
2. GitHubにコミットする
3. 既存Portfolio PDFがあるか確認する
4. PDFを新規作成するか、既存PDFを更新するか判断する
```
