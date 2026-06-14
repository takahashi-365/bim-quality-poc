# RAG Metadata Design

## 目的

このドキュメントは、`BIM Data Quality & AI Readiness Assessment PoC` の成果物を、将来的にRAG / Azure AI Searchで活用する場合のメタデータ設計を整理するものである。

第3段階Dでは、Azure AI SearchやRAGシステムを本格実装しない。

目的は、既存PoCで生成したAI Context、Fix Guide、Rule Master、品質チェック結果、AI Readiness Score、pyRevit Metadataを、検索・フィルタ・回答根拠表示に使いやすい形へ整理することである。

---

## このドキュメントの位置づけ

このドキュメントは、第3段階D「RAG / Azure AI Search構成検討」の一部である。

親ドキュメントは以下とする。

```text id="f2o8zl"
docs/rag_azure_ai_search_architecture_plan.md
```

関連ドキュメントは以下とする。

```text id="qjli5s"
docs/rag_chunk_design.md
docs/rag_query_examples.md
docs/rag_answer_policy.md
docs/rag_limitations.md
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl
```

このドキュメントでは、`docs/rag_chunk_design.md` で定義したチャンクに対して、どのメタデータを付与するかを整理する。

---

## メタデータ設計の基本方針

RAGで利用するチャンクには、検索本文である `content` とは別に、検索・フィルタ・根拠表示・将来のRevit連携に使うメタデータを持たせる。

基本方針は以下とする。

```text id="1qod3i"
文書種別で絞り込めること
Door / Room などのカテゴリで絞り込めること
ElementId / UniqueIdで要素参照できること
RuleIdでRule Master / Fix Guideと関連付けられること
Severityで重要度を絞り込めること
AI Readiness ScoreでAI活用準備度を参照できること
HumanReviewRequiredで人間確認要否を扱えること
SourceFileで元データに戻れること
実案件情報や機密情報を含めないこと
```

RAG回答では、LLMの生成文だけでなく、参照したRuleId、Severity、AI Readiness Score、HumanReviewRequired、SourceFileを表示できるようにする。

---

# 共通メタデータ

第3段階Dの初期MVPでは、すべてのチャンクに以下の共通メタデータを持たせることを基本とする。

```text id="uagyc3"
id
content
document_type
chunk_type
category
element_id
unique_id
rule_id
severity
quality_score
ai_readiness_score
ai_readiness_level
human_review_required
fix_priority
source_file
generated_date
```

ただし、すべてのチャンクで全項目が必ず埋まるとは限らない。

例：

```text id="a9mpxf"
RuleId単位チャンクでは element_id が空欄になる
Category単位チャンクでは element_id / rule_id が複数または空欄になる
Fix Guide単位チャンクでは quality_score が空欄になる
pyRevit Metadata由来のチャンクでは rule_id が空欄になる場合がある
```

空欄があること自体は問題としない。

重要なのは、チャンク種別ごとに使うメタデータの意味を揃えることである。

---

# id

## 目的

`id` は、RAG用チャンクまたはAzure AI Search上のドキュメントを一意に識別するためのIDである。

## 方針

`id` は、DocumentType、Category、ElementId、RuleIdなどから生成する。

例：

```text id="rygdkb"
element-door-12345-d002
rule-room-r101
fixguide-door-d002
category-room-summary
```

## 注意点

Azure AI Searchを将来使う場合、`id` は一意である必要がある。

既存PoCのElementIdとRevit内部ElementIdが混在する可能性があるため、ID生成時には意味が分かる接頭辞を付ける。

例：

```text id="81bdqo"
poc-element-door-12345
revit-element-100001
uniqueid-00000000-0000-0000-0000-000000000001-00000001
```

---

# content

## 目的

`content` は、検索対象となる本文である。

LLMへ渡すコンテキストの主な本文として使う。

## 方針

`content` には、検索・回答生成に必要な自然文または半構造化テキストを格納する。

例：

```text id="xtokbf"
ElementId 12345 の Door 要素では、RuleId D-002 に該当する品質問題が検出されている。
Severity は High であり、AI Readiness Score に影響する。
HumanReviewRequired は True であるため、BIM担当者による確認が必要である。
```

## 注意点

`content` に実案件名、顧客名、個人情報、社外秘情報を含めない。

GitHubに公開するサンプルでは、匿名化したPoCデータまたは自作サンプルのみを使用する。

---

# document_type

## 目的

`document_type` は、チャンクの元となる文書またはデータ種別を示す。

## 候補値

```text id="adf3pa"
AIContext
FixGuide
RuleMaster
CheckResult
AIReadinessScore
pyRevitMetadata
Docs
Sample
```

## 用途

```text id="h07jw9"
AI Contextだけを検索する
Fix Guideだけを検索する
Rule Masterだけを参照する
pyRevit Metadataを補助情報として扱う
Docsをポリシー確認用に使う
```

## 初期MVP方針

初期MVPでは、主に以下を使う。

```text id="nh7u4n"
AIContext
FixGuide
RuleMaster
Sample
```

`CheckResult`、`AIReadinessScore`、`pyRevitMetadata` は、補助対象として扱う。

---

# chunk_type

## 目的

`chunk_type` は、RAG上のチャンク単位を示す。

## 候補値

```text id="pqu3cr"
Element
RuleId
Category
FixGuide
Policy
Docs
Summary
```

## 用途

```text id="0j63bq"
Element単位の品質問題を検索する
RuleId単位でルールの意味を検索する
FixGuide単位で修正方針を検索する
Category単位でカテゴリ全体の注意点を検索する
```

## 初期MVP方針

初期MVPでは、以下を優先する。

```text id="db7dqa"
Element
RuleId
FixGuide
```

`Category` は余力があれば扱う。

---

# category

## 目的

`category` は、対象BIM要素のカテゴリを示す。

## 候補値

```text id="xz68au"
Door
Room
Other
```

## 用途

```text id="56hl9x"
Doorカテゴリだけを検索する
Roomカテゴリだけを検索する
カテゴリ別にHigh Severityを確認する
カテゴリ別にAI Readiness上の注意点を整理する
```

## 正規化方針

pyRevit Metadataでは、Revit由来のカテゴリ名が日本語で出力される場合がある。

例：

```text id="pve3wu"
ドア
部屋
```

RAG設計上は、検索・フィルタの安定性を優先し、以下のように正規化する。

```text id="qt4yr2"
ドア → Door
部屋 / Room → Room
その他 → Other
```

第3段階Dでは、正規化処理の実装までは行わない。

設計方針として記録する。

---

# element_id

## 目的

`element_id` は、PoCまたはRevit上の要素を参照するためのIDである。

## 注意点

既存PoCでは、Revit内部ElementIdではなく、建具表上の建具番号などを仮ElementIdとして使っている場合がある。

一方、第3段階CではpyRevitによりRevit内部ElementIdを取得した。

このため、将来的には以下のように分けることを検討する。

```text id="aof4ap"
poc_element_id
revit_element_id
```

## 初期MVP方針

第3段階Dでは、`element_id` を共通名として扱う。

ただし、ドキュメント上で以下の注意を明記する。

```text id="zsthsw"
既存PoC上のElementIdとRevit内部ElementIdを混同しない
必要に応じてpoc_element_id / revit_element_idへ分離する
UniqueIdをRevit由来の安定識別子候補として扱う
```

---

# unique_id

## 目的

`unique_id` は、Revit由来の安定識別子候補である。

将来的に、RAG回答からRevit要素へ戻るための参照キーとして扱える可能性がある。

## 用途

```text id="ozjasn"
UniqueIdから対象要素の品質問題を検索する
pyRevit MetadataとAI Contextを関連付ける
Revitモデル側の要素確認に使う
```

## 注意点

第3段階Dでは、UniqueIdによるRevit実連携は行わない。

GitHub公開用サンプルでは、UniqueIdは匿名化した値を使う。

---

# rule_id

## 目的

`rule_id` は、品質チェック結果、Rule Master、Fix Guideを結び付けるキーである。

## 用途

```text id="j3ieou"
Element chunkからRuleId chunkへ接続する
Element chunkからFix Guide chunkへ接続する
Rule Master上の定義へ戻る
RuleIdごとのSeverityやAI Impactを確認する
```

## 例

```text id="5n9y22"
D-001
D-002
R-101
R-102
```

## 方針

RuleIdは、RAG設計上の最重要キーの一つとして扱う。

回答時には、可能な範囲で参照したRuleIdを明記する。

---

# severity

## 目的

`severity` は、品質問題の重要度を示す。

## 候補値

```text id="s198ed"
High
Medium
Low
None
Unknown
```

## 用途

```text id="klpuh5"
High Severityの問題だけを検索する
重大な品質問題を優先確認する
回答時に重要度を明記する
FixPriority設計への接続候補にする
```

## 注意点

Severityは、設計・施工上の危険度を直接判断するものではない。

PoC上のデータ品質評価における重要度として扱う。

---

# quality_score

## 目的

`quality_score` は、品質チェック結果に基づくスコアである。

## 用途

```text id="77vhc7"
品質状態の概要を把握する
AI Readiness Scoreと合わせて確認する
FixPriority設計への入力候補にする
```

## 注意点

QualityScoreは、BIMデータ品質の参考指標であり、設計品質や施工品質そのものを評価するものではない。

---

# ai_readiness_score

## 目的

`ai_readiness_score` は、BI、データ分析、生成AI、RAGなどで活用する前段階としてのデータ準備度を示す。

## 用途

```text id="shs1sv"
AI活用前に確認すべき要素を抽出する
AI Readiness Scoreが低い理由を説明する
カテゴリ別のAI活用準備度を確認する
```

## 注意点

AI Readiness Scoreは、AIでその要素を使ってよいかを最終判断するものではない。

HumanReviewRequiredと合わせて扱う。

---

# ai_readiness_level

## 目的

`ai_readiness_level` は、AI Readiness Scoreを段階的に表現するラベルである。

## 候補値

```text id="41twga"
High
Medium
Low
Unknown
```

## 用途

```text id="eg458d"
AI活用準備度を分かりやすく表示する
検索結果や回答で概要を伝える
```

---

# human_review_required

## 目的

`human_review_required` は、人間確認が必要かどうかを示す重要なメタデータである。

## 候補値

```text id="xluovp"
true
false
unknown
```

## 用途

```text id="ah1gr4"
人間確認が必要な要素を抽出する
RAG回答で確認要否を明記する
自動判断を避ける
```

## 回答方針

`human_review_required = true` の場合、RAG回答では必ず以下を明記する。

```text id="0tnx8f"
BIM担当者による確認が必要である
LLM回答は参考情報である
最終判断はBIM担当者が行う
```

`human_review_required = false` の場合でも、LLMが設計・施工・法規の最終判断を行うわけではない。

---

# fix_priority

## 目的

`fix_priority` は、修正優先度を示すラベルである。

## 用途

```text id="qhfu1d"
確認優先度の整理
第3段階Eの教師データ設計への接続
HumanReviewRequiredやSeverityとの組み合わせ分析
```

## 注意点

現時点のFixPriorityは仮ラベルであり、実務教師データに基づく最終ラベルではない。

第3段階Dでは、FixPriorityをRAG検索条件または補助メタデータ候補として扱う。

本格的な教師データ設計は、第3段階Eで整理する。

---

# Revit由来メタデータ

第3段階CでpyRevitにより取得したメタデータは、将来的なRAG / Azure AI Search接続において補助情報として扱う。

候補は以下である。

```text id="6fhv4d"
revit_element_id
unique_id
family_name
type_name
level_name
room_name
room_number
```

## family_name

Revitファミリ名を示す。

用途：

```text id="slmbgl"
要素種別の補足
同一ファミリの品質傾向確認
検索結果の理解補助
```

GitHub公開用サンプルでは匿名化する。

## type_name

Revitタイプ名を示す。

用途：

```text id="jx12tz"
タイプ単位の確認
要素説明の補助
検索結果の理解補助
```

GitHub公開用サンプルでは匿名化する。

## level_name

階情報を示す。

用途：

```text id="35j6gg"
階別の確認
検索結果の理解補助
Room / Door の配置文脈の補助
```

GitHub公開用サンプルでは必要に応じて匿名化する。

## room_name / room_number

Roomカテゴリの場合に利用する。

DoorなどRoom以外のカテゴリでは、初期MVPでは空欄を許容する。

Doorから関連Roomを推定しない。

---

# source_file

## 目的

`source_file` は、チャンクの元となったファイルを示す。

## 用途

```text id="a6eft1"
回答根拠を明記する
元データへ戻れるようにする
チャンク生成元を追跡する
```

## 例

```text id="b31a92"
04_output_csv/ai_context_v002.md
04_output_csv/ai_context_v002.json
04_output_csv/fix_guides_v001.md
02_rule_master/bim_rule_master_v003.csv
03_input_csv/pyrevit_element_metadata_sample_v001.csv
docs/rag_chunk_design.md
```

## 方針

RAG回答では、可能な範囲で `source_file` を明記する。

ただし、SourceFileは回答根拠を示す補助情報であり、LLMの判断を正当化するものではない。

---

# generated_date

## 目的

`generated_date` は、チャンクまたは元データの生成日を示す。

## 用途

```text id="1n44zx"
古いデータと新しいデータを区別する
再生成タイミングを確認する
将来的なインデックス更新管理に使う
```

## 初期MVP方針

第3段階Dでは、実際の自動生成処理を行わないため、サンプルでは任意項目とする。

将来実装時には、チャンク生成時の日付を入れることを検討する。

---

# Azure AI Searchを想定したフィールド用途

第3段階DではAzure AI Searchを実装しないが、将来の設計候補としてフィールド用途を整理する。

| フィールド                 | 用途                          | 想定属性                                           |
| --------------------- | --------------------------- | ---------------------------------------------- |
| id                    | 一意ID                        | key, retrievable                               |
| content               | 検索対象本文                      | searchable, retrievable                        |
| document_type         | 文書種別                        | filterable, facetable, retrievable             |
| chunk_type            | チャンク種別                      | filterable, facetable, retrievable             |
| category              | Door / Roomなど               | filterable, facetable, retrievable             |
| element_id            | 要素参照キー                      | filterable, searchable, retrievable            |
| unique_id             | Revit由来識別子                  | filterable, searchable, retrievable            |
| rule_id               | Rule Master / Fix Guide接続キー | filterable, searchable, facetable, retrievable |
| severity              | 重要度                         | filterable, facetable, retrievable             |
| quality_score         | 品質スコア                       | filterable, sortable, retrievable              |
| ai_readiness_score    | AI活用準備度                     | filterable, sortable, retrievable              |
| ai_readiness_level    | AI活用準備度ラベル                  | filterable, facetable, retrievable             |
| human_review_required | 人間確認要否                      | filterable, facetable, retrievable             |
| fix_priority          | 修正優先度                       | filterable, facetable, retrievable             |
| family_name           | Revitファミリ名                  | searchable, filterable, retrievable            |
| type_name             | Revitタイプ名                   | searchable, filterable, retrievable            |
| level_name            | 階情報                         | filterable, facetable, retrievable             |
| room_name             | 部屋名                         | searchable, filterable, retrievable            |
| room_number           | 部屋番号                        | searchable, filterable, retrievable            |
| source_file           | 出典ファイル                      | filterable, retrievable                        |
| generated_date        | 生成日                         | filterable, sortable, retrievable              |

## 注意点

上記は概念設計であり、Azure AI Search上での実スキーマではない。

実装時には、Azure AI Searchの制約、データ型、検索方式、フィールド属性の組み合わせを確認する必要がある。

---

# 初期MVPで採用するメタデータ

第3段階Dの初期MVPでは、以下を優先する。

```text id="altelx"
id
content
document_type
chunk_type
category
element_id
unique_id
rule_id
severity
ai_readiness_score
human_review_required
source_file
```

理由：

```text id="g4bt0n"
検索対象の種別を分けられる
ElementId / UniqueIdで要素参照できる
RuleIdでRule Master / Fix Guideへ接続できる
Severityで重要度を扱える
AI Readiness ScoreでAI活用準備度を説明できる
HumanReviewRequiredで自動判断を避けられる
SourceFileで根拠表示できる
```

---

# 将来拡張候補

将来的には、以下のメタデータを追加することを検討する。

```text id="c3lo39"
poc_element_id
revit_element_id
project_id
model_id
discipline
system_name
zone
department
classification_code
parameter_name
parameter_value
review_status
reviewer_comment
actual_fix_priority
fix_completed_date
```

## 注意点

以下の情報は、GitHub公開用サンプルには含めない。

```text id="d4qjef"
実案件名
顧客名
個人情報
社外秘モデル名
社内固有の分類コード
機密性の高い仕様情報
```

---

# RAG回答時に表示する根拠

RAG回答では、可能な範囲で以下を表示する。

```text id="se0z13"
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

回答時には、以下を前提とする。

```text id="llql81"
LLM回答は参考情報である
入力情報から判断できない場合は、その旨を明記する
HumanReviewRequired=Trueの場合は人間確認が必要と明記する
最終判断はBIM担当者が行う
```

---

# 制約

第3段階Dでは、以下を行わない。

```text id="vb1p15"
Azure AI Searchの実装
Azure OpenAI / OpenAI API接続
Embedding生成
ベクトル検索
クラウド環境構築
認証・権限設計の実装
インデックス作成の自動化
大量データ投入
実案件データ投入
検索精度評価
RAGチャットUI開発
Revitモデル自動修正
設計判断・施工判断の自動化
```

このドキュメントは、将来実装に向けた設計メモである。

---

# セキュリティ・公開範囲

GitHubへ含めてよいものは以下に限定する。

```text id="g6cfab"
公開可能なサンプルデータ
匿名化したPoC用データ
自作サンプルJSONL
概念スキーマ
設計メモ
```

GitHubへ含めないものは以下である。

```text id="40w2m4"
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

```text id="fx4495"
共通メタデータを整理した
id / content / document_type / chunk_type を定義した
Categoryの正規化方針を整理した
ElementId / UniqueIdの扱いを整理した
RuleIdの役割を整理した
Severityの扱いを整理した
QualityScore / AIReadinessScoreの扱いを整理した
HumanReviewRequiredの扱いを整理した
FixPriorityの位置づけを整理した
Revit由来メタデータを整理した
SourceFile / GeneratedDateの扱いを整理した
Azure AI Searchを想定したフィールド用途を整理した
初期MVPで採用するメタデータを整理した
将来拡張候補を整理した
RAG回答時に表示する根拠を整理した
制約とセキュリティ方針を整理した
```

---

# 次に作成するファイル

次に作成するファイルは以下とする。

```text id="qk8te1"
05_rag_design/sample_index_schema_v001.json
```

`sample_index_schema_v001.json` では、このメタデータ設計をもとに、Azure AI Searchを想定した概念スキーマのサンプルを作成する。
