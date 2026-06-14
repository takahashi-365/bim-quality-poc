# 第3段階D：RAG / Azure AI Search構成検討 計画

## 目的

第3段階Dでは、既存の `BIM Data Quality & AI Readiness Assessment PoC` で生成した成果物を、将来的にRAGやAzure AI Searchで活用する場合の構成を検討する。

この段階では、RAGシステムやAzure AI Searchを本格実装しない。
目的は、既存PoCの成果物を検索・回答生成に接続する場合の設計方針を整理することである。

整理対象は以下とする。

```text
どのデータを検索対象にするか
どの単位でチャンク化するか
どのメタデータを持たせるか
チャンク同士をどのキーで関連付けるか
AI Context / Fix Guide / Rule Masterをどう使うか
Door / Room / ElementId / UniqueIdをどう検索軸にするか
RAG回答で何を扱わせないか
回答時にどの根拠を表示するか
どこまでをPoCで扱い、どこから先を将来拡張にするか
```

---

## 位置づけ

第3段階Dは、新規PoCではなく、既存PoCの成果物を将来的なRAG構成へ接続するための設計検討である。

第2段階まで：

```text
Revit Schedule TXT
↓
CSV変換
↓
品質チェック
↓
AI Readiness Score
↓
AI Context
↓
Fix Guide
↓
Streamlit表示
```

第3段階A〜C：

```text
A：Local LLM Explanation Demo
B：Roomカテゴリ追加
C：pyRevitでElementId / UniqueId取得PoC
```

第3段階D：

```text
AI Context
Fix Guide
Rule Master
Door / Room 品質チェック結果
AI Readiness Score
ElementId / UniqueId
pyRevit Metadata
↓
RAG / Azure AI Searchで使う場合の構成検討
```

---

## 第3段階Dでやること

* RAG化の対象データを整理する
* 検索対象データを主検索対象と補助対象に分ける
* AI Contextを検索対象にする場合の単位を検討する
* Fix Guideを検索対象にする場合の単位を検討する
* Rule Masterを参照情報として扱う方針を整理する
* Door / Roomカテゴリをメタデータとして扱う方針を整理する
* ElementId / UniqueIdを検索・参照キーとして扱う方針を整理する
* チャンク設計を検討する
* チャンク間の関連付けキーを整理する
* メタデータ設計を検討する
* Azure AI Searchの概念構成を整理する
* Azure AI Searchのフィールド属性を簡易整理する
* 検索クエリ例を整理する
* 想定回答例を整理する
* 回答時の根拠表示方針を整理する
* RAG回答で扱わないことを明確にする
* セキュリティ・公開範囲を整理する
* 実装しない範囲を明確にする
* docsに設計メモとして記録する

---

## 第3段階Dでやらないこと

```text
本格RAGシステム構築
Azure AI Searchの本格実装
Azure OpenAI / OpenAI API接続
クラウド環境構築
認証・権限設計の実装
ベクトル検索の実装
Embedding生成の実装
インデックス作成の自動化
実案件データ投入
Revitモデル自動修正
設計判断・施工判断の自動化
チャットUIの本格開発
LangChain / Semantic Kernelなどのフレームワーク選定
コスト試算
本番運用設計
```

この段階では、**構成検討・設計メモ作成・サンプル設計** に限定する。

---

## RAG回答で扱わないこと

RAGを使う場合でも、LLMに以下を回答させない。

```text
設計の正否判定
施工可否の判断
Revitモデルの修正指示
法規適合性の最終判断
コスト・工程・安全性の断定
入力データに存在しない部屋名・分類コード・仕様の補完
HumanReviewRequired=Trueを無視した自動判断
BIM担当者の確認を不要とする判断
```

RAG回答は、BIMデータ品質確認を補助するための参考情報とする。
最終判断はBIM担当者が行う。

---

## 検索対象データの区分

第3段階Dでは、検索対象を「主検索対象」と「補助対象」に分けて整理する。

### 主検索対象

初期検討では、以下を主検索対象とする。

```text
AI Context
Fix Guide
Rule Master
```

理由：

```text
LLM回答の本文生成に使いやすい
RuleIdやSeverityなどの意味を説明しやすい
品質問題と修正方針を結び付けやすい
BIM担当者向け説明の根拠になりやすい
```

### 補助対象

以下は、検索フィルタ、メタデータ、補助情報として扱う。

```text
Check Results
AI Readiness Score
pyRevit Metadata
README
docs
```

理由：

```text
構造化データとしてフィルタに使いやすい
ElementId / UniqueId / Category / Severityで絞り込みやすい
回答本文の主根拠というより、検索条件や参照情報として使いやすい
```

---

## 検討対象データ

### AI Context

```text
04_output_csv/ai_context_v002.md
04_output_csv/ai_context_v002.json
Room用AI Context
```

役割：

```text
ElementId単位または要素単位の品質チェック文脈
AI Readiness Score
HumanReviewRequired
RuleId
Severity
品質チェック結果
```

---

### Fix Guide

```text
04_output_csv/fix_guides_v001.md
Room用Fix Guide
```

役割：

```text
RuleIdごとの修正方針
BIM担当者向けの対応案
品質チェック結果に対する説明補助
LLM回答の根拠候補
```

---

### Rule Master

```text
02_rule_master/bim_rule_master_v003.csv
```

役割：

```text
RuleId定義
TargetCategory
RuleName
Severity
チェック内容
AI活用上の影響
```

---

### 品質チェック結果

```text
04_output_csv/check_results_revit_v002.csv
Room用品質チェック結果
```

役割：

```text
どの要素がどのRuleIdに該当したか
Severityごとの違反状況
ElementId単位の品質問題
```

---

### AI Readiness Score

```text
04_output_csv/ai_readiness_scores_v001.csv
Room用AI Readiness Score
```

役割：

```text
AI活用前のデータ準備度
HumanReviewRequired
FixPriority
QualityScoreとの接続
```

---

### pyRevit取得メタデータ

```text
03_input_csv/pyrevit_element_metadata_sample_v001.csv
```

役割：

```text
Revit内部ElementId
UniqueId
Category
FamilyName
TypeName
将来的な安定識別子候補
```

---

## RAG化する場合の基本方針

RAG化する場合、すべてのCSVをそのまま検索対象にするのではなく、検索しやすい単位に整理する。

基本方針：

```text
要素単位で検索できること
RuleId単位で検索できること
カテゴリ単位で検索できること
Severity単位で絞り込めること
HumanReviewRequiredで絞り込めること
ElementId / UniqueIdで参照できること
Fix Guideと品質チェック結果を関連付けられること
回答時に根拠へ戻れること
```

---

## 想定チャンク設計

### 1. Element単位チャンク

1つのBIM要素ごとに、品質チェック結果とAI Readiness情報をまとめる。

想定内容：

```text
ElementId
UniqueId
Category
FamilyName
TypeName
RuleId
RuleName
Severity
QualityScore
AI Readiness Score
HumanReviewRequired
Issue Summary
Fix Guide Reference
SourceFile
```

用途：

```text
この要素にどの品質問題があるか知りたい
この要素はAI活用に使える状態か確認したい
ElementIdから問題内容を検索したい
UniqueIdからRevit要素の文脈を確認したい
```

---

### 2. RuleId単位チャンク

RuleIdごとに、ルールの意味と修正方針をまとめる。

想定内容：

```text
RuleId
TargetCategory
RuleName
Severity
Check Description
AI Impact
Fix Guide
Example Issue
Human Review Policy
SourceFile
```

用途：

```text
R-101は何を意味するか
D-002の修正方針を知りたい
High Severityのルール一覧を確認したい
```

---

### 3. Category単位チャンク

Door / Roomなどカテゴリごとに、よくある品質問題をまとめる。

想定内容：

```text
Category
Common RuleIds
Common Issues
AI Readiness Impact
Recommended Review Points
SourceFile
```

用途：

```text
Doorカテゴリでよくある品質問題を知りたい
RoomカテゴリのAI Readiness上の注意点を知りたい
```

---

### 4. Fix Guide単位チャンク

Fix GuideをRuleId単位で分割し、LLM回答時の根拠として使える形にする。

想定内容：

```text
RuleId
Fix Guide Text
Recommended Action
Human Review Required
Notes
SourceFile
```

用途：

```text
このRuleIdに対する修正案を知りたい
BIM担当者向けの対応文を作りたい
```

---

## チャンク間の関連付けキー

複数種類のチャンクを扱うため、チャンク同士を関連付けるキーを明確にする。

主な関連付けキー：

```text
ElementId
UniqueId
RuleId
Category
SourceFile
```

想定する関連：

```text
Element chunk → RuleId → Rule chunk / Fix Guide chunk
Element chunk → UniqueId → pyRevit Metadata
Element chunk → Category → Category chunk
Rule chunk → RuleId → Fix Guide chunk
Category chunk → Category → Rule chunk
```

特に重要な考え方：

```text
ElementIdは既存PoC上の要素参照キーとして扱う
UniqueIdはRevit由来の安定識別子候補として扱う
RuleIdは品質チェック結果とFix Guideを結ぶキーとして扱う
CategoryはDoor / Roomなどの対象カテゴリを分けるキーとして扱う
SourceFileは回答根拠を元データへ戻すためのキーとして扱う
```

---

## メタデータ設計案

RAG / Azure AI Searchで扱う場合、以下のメタデータを候補とする。

```text
DocumentType
Category
ElementId
UniqueId
RuleId
RuleName
Severity
AIReadinessScore
QualityScore
HumanReviewRequired
FixPriority
FamilyName
TypeName
LevelName
RoomName
RoomNumber
SourceFile
GeneratedDate
```

### DocumentTypeの候補

```text
AIContext
FixGuide
RuleMaster
CheckResult
AIReadinessScore
pyRevitMetadata
Docs
```

### Categoryの候補

```text
Door
Room
Other
```

---

## Azure AI Search構成の概念案

この段階では実装しないが、概念構成として以下を整理する。

```text
PoC Output Files
↓
Pre-processing / Chunking
↓
Index Documents
↓
Azure AI Search Index
↓
Search / Retrieve
↓
LLM Prompt Context
↓
BIM担当者向け説明
```

想定インデックス設計：

```text
id
content
document_type
category
element_id
unique_id
rule_id
severity
ai_readiness_score
human_review_required
source_file
```

---

## Azure AI Searchフィールド属性の簡易整理

本段階では実装しないが、Azure AI Searchを想定した場合のフィールド用途を軽く整理する。

| フィールド                 | 用途                            |
| --------------------- | ----------------------------- |
| id                    | 一意ID                          |
| content               | 検索対象本文                        |
| document_type         | 文書種別フィルタ                      |
| category              | Door / Roomなどのカテゴリフィルタ        |
| element_id            | 要素参照キー                        |
| unique_id             | Revit由来の安定識別子候補               |
| rule_id               | Rule Master / Fix Guideとの関連付け |
| severity              | 重要度フィルタ                       |
| ai_readiness_score    | AI活用準備度の参照                    |
| human_review_required | 人による確認要否のフィルタ                 |
| source_file           | 出典表示                          |
| generated_date        | 生成日・更新日の参照                    |

必要に応じて、将来の実装時に `searchable`、`filterable`、`retrievable`、`sortable` などを設計する。
第3段階Dでは、フィールドの詳細実装までは行わない。

---

## インデックス設計方針

### 案A：単一インデックス

AI Context、Fix Guide、Rule Masterを1つのインデックスに入れる。

メリット：

```text
構成が単純
検索対象をまとめて扱える
PoC説明として分かりやすい
```

デメリット：

```text
DocumentTypeごとの違いをメタデータで管理する必要がある
検索結果に異なる種類の文書が混在する
```

---

### 案B：用途別インデックス

AI Context、Fix Guide、Rule Masterを別インデックスに分ける。

メリット：

```text
文書種別ごとの設計がしやすい
検索対象を制御しやすい
```

デメリット：

```text
構成が複雑になる
初期PoCにはやや重い
```

---

### 初期方針

第3段階Dでは、まず案Aの単一インデックスを基本案として検討する。

理由：

```text
PoCとして説明しやすい
既存成果物をまとめて扱いやすい
実装前の構成検討として十分
```

ただし、本番運用や大規模化を考える場合は、案Bも将来候補として記録する。

---

## サンプルRAGドキュメント案

第3段階Dでは、必要に応じてJSONL形式のサンプルを作る。

英語例：

```json
{"id":"element-Door-12345","document_type":"AIContext","category":"Door","element_id":"12345","unique_id":"sample-unique-id","rule_id":"D-002","severity":"High","human_review_required":true,"content":"Door element 12345 has a missing classification code. Fix guide suggests confirming the classification code with BIM personnel."}
```

日本語例：

```json
{"id":"element-Door-12345-ja","document_type":"AIContext","category":"Door","element_id":"12345","unique_id":"sample-unique-id","rule_id":"D-002","severity":"High","human_review_required":true,"content":"建具要素 12345 では分類コードが未入力です。AI Readiness Scoreが低下しており、BIM担当者による確認が必要です。"}
```

注意：

```text
実案件情報は使わない
サンプルデータまたは既存PoCの公開可能なデータのみ使う
顧客名・現場名・個人情報を含めない
```

---

## 想定検索クエリ例

RAGで想定する質問例を整理する。

```text
このElementIdの品質問題を説明して
このUniqueIdのAI Readiness Scoreが低い理由を教えて
DoorカテゴリでHigh Severityの問題を一覧化して
RoomカテゴリでAI活用前に確認すべき項目を教えて
R-101の意味と修正方針を説明して
HumanReviewRequiredがTrueの要素を優先的に確認したい
FixPriorityが高い要素の対応案を出して
この要素をBIやRAGで使う前に何を直すべきか
```

---

## RAG回答方針

LLMが回答する場合は、以下の制約を守る。

```text
設計判断・施工判断をしない
Revitモデルの自動修正を提案しない
入力情報にないことを断定しない
RuleId / Severity / AI Readiness Score / Fix Guideを根拠として示す
HumanReviewRequiredがTrueの場合は、人による確認が必要と明記する
修正案は提案として表現する
最終判断はBIM担当者が行う
```

---

## 回答時の根拠表示方針

RAG回答では、可能な範囲で参照した根拠を明記する。

表示候補：

```text
RuleId
RuleName
Severity
AI Readiness Score
HumanReviewRequired
Fix Guide
SourceFile
ElementId
UniqueId
```

方針：

```text
回答には、可能な範囲で参照したRuleId、Severity、AI Readiness Score、Fix Guide、SourceFileを明記する
LLM回答だけを最終判断とせず、BIM担当者が元データを確認できるようにする
入力情報から判断できない場合は、判断できないと明記する
HumanReviewRequired=Trueの場合は、人による確認が必要であることを明記する
```

---

## セキュリティ・公開範囲

第3段階Dでは、RAGやAzure AI Searchへの将来接続を想定するが、実案件データや社外秘データは扱わない。

禁止するもの：

```text
実案件データ
社外秘モデル
顧客名
プロジェクト名
個人情報
社内固有の分類コード
機密性の高い仕様情報
大量の実モデル由来パラメータ
```

GitHubに含めてよいもの：

```text
公開可能なサンプルデータ
匿名化したPoC用データ
自作のサンプルJSONL
設計メモ
概念スキーマ
```

方針：

```text
GitHubには、公開可能なサンプルデータまたは匿名化したPoC用データのみを含める
Azure AI Searchやクラウド環境への投入は本段階では行わない
実装前の構成検討として扱う
```

---

## 作成予定ファイル

### docs

```text
docs/rag_azure_ai_search_architecture_plan.md
docs/rag_chunk_design.md
docs/rag_metadata_design.md
docs/rag_query_examples.md
docs/rag_limitations.md
docs/rag_answer_policy.md
```

### optional sample

```text
05_rag_design/sample_rag_documents_v001.jsonl
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_queries_v001.md
```

第3段階Dでは、`05_rag_design/` を新規フォルダとして作成してもよい。

---

## 作業手順

### Step 1：作業前状態を確認する

```powershell
git status
```

作業ブランチを分ける場合：

```powershell
git checkout -b phase3d-rag-architecture-design
```

---

### Step 2：RAG設計用フォルダを作成する

```text
05_rag_design/
```

作成候補：

```powershell
mkdir 05_rag_design
```

---

### Step 3：構成検討メインドキュメントを作成する

作成ファイル：

```text
docs/rag_azure_ai_search_architecture_plan.md
```

記載内容：

```text
目的
対象範囲
やること
やらないこと
RAG回答で扱わないこと
対象データ
主検索対象 / 補助対象
チャンク設計
チャンク間の関連付けキー
メタデータ設計
Azure AI Search概念構成
フィールド属性の簡易整理
回答時の根拠表示方針
セキュリティ・公開範囲
制約
完了条件
```

---

### Step 4：対象データを棚卸しする

既存PoC成果物を確認する。

```text
AI Context
Fix Guide
Rule Master
Check Results
AI Readiness Score
pyRevit Metadata
Door / Room outputs
```

どのファイルをRAG対象候補にするか整理する。

---

### Step 5：主検索対象と補助対象を分ける

主検索対象：

```text
AI Context
Fix Guide
Rule Master
```

補助対象：

```text
Check Results
AI Readiness Score
pyRevit Metadata
README
docs
```

---

### Step 6：チャンク設計を作成する

作成ファイル：

```text
docs/rag_chunk_design.md
```

検討する単位：

```text
Element単位
RuleId単位
Category単位
Fix Guide単位
```

---

### Step 7：チャンク間の関連付けキーを整理する

整理するキー：

```text
ElementId
UniqueId
RuleId
Category
SourceFile
```

想定関係：

```text
Element chunk → RuleId → Rule chunk / Fix Guide chunk
Element chunk → UniqueId → pyRevit Metadata
Category chunk → Category → Rule chunk
```

---

### Step 8：メタデータ設計を作成する

作成ファイル：

```text
docs/rag_metadata_design.md
```

候補メタデータ：

```text
DocumentType
Category
ElementId
UniqueId
RuleId
Severity
AIReadinessScore
HumanReviewRequired
SourceFile
```

---

### Step 9：Azure AI Searchの概念スキーマを作る

作成候補：

```text
05_rag_design/sample_index_schema_v001.json
```

検討項目：

```text
id
content
document_type
category
element_id
unique_id
rule_id
severity
ai_readiness_score
human_review_required
source_file
```

この段階では、Azure上に実際のインデックスを作らない。

---

### Step 10：サンプルRAGドキュメントを作る

必要に応じて、JSONL形式のサンプルを作る。

作成候補：

```text
05_rag_design/sample_rag_documents_v001.jsonl
```

サンプルには、日本語例も含める。

---

### Step 11：検索クエリ例を作る

作成ファイル：

```text
docs/rag_query_examples.md
```

質問例：

```text
このElementIdの品質問題を説明して
R-101の修正方針を教えて
RoomカテゴリでAI活用前に確認すべき項目は？
HumanReviewRequiredがTrueの要素を優先確認したい
```

---

### Step 12：RAG回答方針を整理する

作成候補：

```text
docs/rag_answer_policy.md
```

整理内容：

```text
RAG回答で扱わないこと
回答時に明記する根拠
RuleId / Severity / AI Readiness Score / Fix Guideの使い方
HumanReviewRequired=Trueの場合の表現
最終判断はBIM担当者が行うこと
```

---

### Step 13：制約を整理する

作成ファイル：

```text
docs/rag_limitations.md
```

制約例：

```text
本段階ではAzure AI Searchを実装しない
実際のEmbedding生成は行わない
ベクトル検索は実装しない
クラウド接続は行わない
実案件データは使わない
回答品質評価は簡易検討に留める
```

---

### Step 14：セキュリティ・公開範囲を確認する

確認内容：

```text
実案件データを含めていないか
社外秘モデル由来の情報を含めていないか
顧客名・プロジェクト名・個人情報を含めていないか
GitHub公開可能なサンプルデータのみになっているか
Azureやクラウド環境へ投入していないか
```

---

### Step 15：README反映判断

第3段階D単体では、READMEを大きく更新しない。

READMEに反映する場合は、以下のように小さく記載する。

```text
RAG / Azure AI Searchを想定し、AI Context、Fix Guide、Rule Master、ElementId / UniqueIdを検索対象として扱う場合のチャンク設計・メタデータ設計を検討しています。
```

Portfolio PDFの更新は、第3段階A〜Dの整理がまとまってから検討する。

---

## 完了条件

第3段階Dの完了条件は以下。

```text
RAG化対象データを整理した
主検索対象 / 補助対象を整理した
AI Contextの使い方を整理した
Fix Guideの使い方を整理した
Rule Masterの使い方を整理した
ElementId / UniqueIdの検索キーとしての扱いを整理した
Door / Roomカテゴリをメタデータとして扱う方針を整理した
チャンク設計を作成した
チャンク間の関連付けキーを整理した
メタデータ設計を作成した
Azure AI Searchの概念構成を整理した
Azure AI Searchフィールド属性を簡易整理した
検索クエリ例を作成した
日本語を含むサンプルJSONL案を作成した
RAG回答で扱わないことを整理した
回答時の根拠表示方針を整理した
セキュリティ・公開範囲を整理した
制約をdocsに記録した
README反映要否を判断した
```

---

## 成功とみなす状態

以下の状態になれば、第3段階DのMVPとして成功とする。

```text
AI Context / Fix Guide / Rule Master / Check Results
↓
RAG対象データとして整理
↓
主検索対象 / 補助対象の整理
↓
チャンク設計
↓
関連付けキー設計
↓
メタデータ設計
↓
Azure AI Search概念構成
↓
検索クエリ例
↓
回答方針・根拠表示方針
↓
制約・セキュリティ整理
```

この段階では、Azure AI SearchやRAGを実装しない。
重要なのは、既存PoCの成果物を将来的に検索・回答生成に使う場合の設計方針を整理することである。

---

## 次段階への接続

第3段階Dが完了したら、以下へ接続する。

```text
第3段階E：FixPriority教師データ設計
```

第3段階Dで整理した `RuleId`、`Severity`、`AI Readiness Score`、`HumanReviewRequired`、`Fix Guide`、`ElementId`、`UniqueId` は、第3段階EのFixPriority教師データ設計にもつながる。
