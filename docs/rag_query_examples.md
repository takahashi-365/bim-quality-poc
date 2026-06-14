# RAG Query Examples

## 目的

このドキュメントは、`BIM Data Quality & AI Readiness Assessment PoC` の成果物を、将来的にRAG / Azure AI Searchで活用する場合の検索クエリ例と想定回答方針を整理するものである。

第3段階Dでは、RAGシステムやAzure AI Searchを本格実装しない。

目的は、既存PoCの成果物を検索・回答生成に接続する場合に、どのような質問を想定し、どのメタデータで検索し、どの根拠を表示するかを整理することである。

---

## このドキュメントの位置づけ

このドキュメントは、第3段階D「RAG / Azure AI Search構成検討」の一部である。

親ドキュメントは以下とする。

```text
docs/rag_azure_ai_search_architecture_plan.md
```

関連ドキュメントは以下とする。

```text
docs/rag_chunk_design.md
docs/rag_metadata_design.md
docs/rag_answer_policy.md
docs/rag_limitations.md
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl
```

このドキュメントでは、実装ではなく、検索・回答の想定パターンを設計メモとして整理する。

---

## 基本方針

RAGの検索クエリは、BIM担当者がデータ品質やAI活用準備度を確認する場面を想定する。

主な検索軸は以下である。

```text
ElementId
UniqueId
RuleId
Category
Severity
AI Readiness Score
HumanReviewRequired
FixPriority
SourceFile
```

回答では、可能な範囲で以下の根拠を表示する。

```text
ElementId
UniqueId
Category
RuleId
RuleName
Severity
AI Readiness Score
HumanReviewRequired
Fix Guide
SourceFile
```

RAG回答は、BIMデータ品質確認の補助情報であり、設計判断・施工判断・法規適合性判断・Revitモデル自動修正を行わない。

---

# 1. ElementIdで検索する質問

## 想定質問

```text
このElementId 100001 の品質問題を説明して。
```

## 想定検索条件

```text
element_id = "100001"
chunk_type = "Element"
```

## 参照候補

```text
Element単位チャンク
RuleId単位チャンク
Fix Guide単位チャンク
```

## 想定回答

```text
ElementId 100001 の Door 要素では、RuleId D-002 に該当する品質問題が検出されています。

Severity は High であり、AI Readiness Score は 72.5 です。
HumanReviewRequired が true のため、BIM担当者による確認が必要です。

Fix Guideでは、分類コードまたは関連パラメータを確認することが推奨されています。

この回答は参考情報です。
最終判断はBIM担当者が行ってください。
```

## 表示する根拠

```text
ElementId: 100001
UniqueId: 00000000-0000-0000-0000-000000000001-00000001
Category: Door
RuleId: D-002
Severity: High
AI Readiness Score: 72.5
HumanReviewRequired: true
SourceFile: 04_output_csv/ai_context_v002.md
```

---

# 2. UniqueIdで検索する質問

## 想定質問

```text
このUniqueIdのAI Readiness Scoreが低い理由を教えて。
```

## 想定検索条件

```text
unique_id = "00000000-0000-0000-0000-000000000001-00000001"
chunk_type = "Element"
```

## 参照候補

```text
Element単位チャンク
pyRevit Metadata
RuleId単位チャンク
Fix Guide単位チャンク
```

## 想定回答

```text
このUniqueIdに対応するDoor要素では、RuleId D-002に該当する品質問題が検出されています。

D-002は分類コードまたは関連分類情報の不足に関するルールです。
分類情報が不足している場合、BI集計、標準分類連携、生成AIやRAGでの意味解釈に影響する可能性があります。

HumanReviewRequired が true のため、BIM担当者が元モデルまたは集計表を確認する必要があります。
```

## 表示する根拠

```text
UniqueId: 00000000-0000-0000-0000-000000000001-00000001
ElementId: 100001
Category: Door
RuleId: D-002
RuleName: Missing classification code
Severity: High
HumanReviewRequired: true
SourceFile: 04_output_csv/ai_context_v002.md
```

---

# 3. RuleIdで検索する質問

## 想定質問

```text
R-101の意味と修正方針を教えて。
```

## 想定検索条件

```text
rule_id = "R-101"
chunk_type IN ["RuleId", "FixGuide"]
```

## 参照候補

```text
RuleId単位チャンク
Fix Guide単位チャンク
```

## 想定回答

```text
RuleId R-101 は、RoomカテゴリにおけるRoomName未入力を検出するルールです。

RoomNameが未入力の場合、空間の意味をAIやBIが判断しにくくなります。
Roomを検索、集計、RAG回答の文脈として利用する前に、BIM担当者が部屋用途やRoom Scheduleを確認することが推奨されます。

入力情報から判断できない場合は、判断できないと明記します。
最終判断はBIM担当者が行います。
```

## 表示する根拠

```text
RuleId: R-101
RuleName: RoomName missing
Category: Room
Severity: High
SourceFile: 02_rule_master/bim_rule_master_v003.csv
SourceFile: 04_output_csv/room_fix_guides_v001.md
```

---

# 4. Categoryで検索する質問

## 想定質問

```text
RoomカテゴリでAI活用前に確認すべき項目は？
```

## 想定検索条件

```text
category = "Room"
chunk_type IN ["Category", "RuleId", "FixGuide"]
```

## 参照候補

```text
Category単位チャンク
Room用RuleId単位チャンク
Room用Fix Guide単位チャンク
```

## 想定回答

```text
Roomカテゴリでは、RoomName、RoomNumber、Area、Levelなどの空間情報がAI Readinessに影響します。

RoomNameやRoomNumberが未入力の場合、空間の意味、部屋識別、検索、RAG回答の文脈が不安定になります。

AIやRAGでRoom情報を使う前には、BIM担当者が元モデルまたはRoom Scheduleを確認することが推奨されます。
```

## 表示する根拠

```text
Category: Room
Related RuleId: R-101
SourceFile: 05_rag_design/sample_rag_documents_v001.jsonl
SourceFile: 04_output_csv/room_fix_guides_v001.md
```

---

# 5. Severityで絞り込む質問

## 想定質問

```text
High Severityの品質問題を優先的に確認したい。
```

## 想定検索条件

```text
severity = "High"
chunk_type = "Element"
```

## 参照候補

```text
Element単位チャンク
RuleId単位チャンク
Fix Guide単位チャンク
```

## 想定回答

```text
High Severityとして確認対象になる要素には、Door要素のD-002、Room要素のR-101などがあります。

High Severityは、PoC上のデータ品質評価における重要度です。
設計品質や施工品質そのものを直接判定するものではありません。

HumanReviewRequiredがtrueの要素は、BIM担当者による確認を優先してください。
```

## 表示する根拠

```text
Severity: High
ElementId: 100001
RuleId: D-002
ElementId: 200001
RuleId: R-101
HumanReviewRequired: true
```

---

# 6. HumanReviewRequiredで検索する質問

## 想定質問

```text
HumanReviewRequired が true の要素を確認したい。
```

## 想定検索条件

```text
human_review_required = true
chunk_type = "Element"
```

## 参照候補

```text
Element単位チャンク
RuleId単位チャンク
Fix Guide単位チャンク
```

## 想定回答

```text
HumanReviewRequired が true の要素は、LLMやRAGの回答だけで判断せず、BIM担当者による確認が必要です。

サンプルでは、ElementId 100001 のDoor要素と、ElementId 200001 のRoom要素が該当します。

それぞれRuleId D-002、R-101に該当しており、分類情報やRoomNameの確認が必要です。
```

## 表示する根拠

```text
ElementId: 100001
Category: Door
RuleId: D-002
HumanReviewRequired: true

ElementId: 200001
Category: Room
RuleId: R-101
HumanReviewRequired: true
```

---

# 7. Fix Guideを使った対応案の質問

## 想定質問

```text
D-002に該当する要素はどう対応すればよい？
```

## 想定検索条件

```text
rule_id = "D-002"
chunk_type IN ["Element", "FixGuide", "RuleId"]
```

## 参照候補

```text
Element単位チャンク
Fix Guide単位チャンク
RuleId単位チャンク
```

## 想定回答

```text
D-002に該当するDoor要素では、分類コードまたは関連パラメータを確認することが推奨されます。

入力情報だけで判断できない場合は、BIM担当者が元モデル、集計表、または社内基準を確認してください。

修正は自動実行せず、BIM担当者の確認後に行う前提です。
LLM回答は参考情報であり、最終判断はBIM担当者が行います。
```

## 表示する根拠

```text
RuleId: D-002
RuleName: Missing classification code
Category: Door
Severity: High
SourceFile: 04_output_csv/fix_guides_v001.md
```

---

# 8. AI Readiness Scoreで検索する質問

## 想定質問

```text
AI Readiness Scoreが低い要素は、何が原因ですか？
```

## 想定検索条件

```text
ai_readiness_score < threshold
chunk_type = "Element"
```

## 参照候補

```text
Element単位チャンク
RuleId単位チャンク
Fix Guide単位チャンク
```

## 想定回答

```text
AI Readiness Scoreが低い要素では、RuleIdに紐づく品質問題がAI活用前の準備度に影響している可能性があります。

たとえば、Door要素で分類コードが不足している場合、BI集計、標準分類連携、生成AIやRAGでの意味解釈が不安定になります。

Room要素でRoomNameが未入力の場合、空間の意味をAIやBIが判断しにくくなります。

HumanReviewRequiredがtrueの場合は、BIM担当者が元データを確認してください。
```

## 表示する根拠

```text
AI Readiness Score
RuleId
Severity
HumanReviewRequired
SourceFile
```

---

# 9. SourceFileで確認する質問

## 想定質問

```text
この回答の根拠ファイルはどれですか？
```

## 想定検索条件

```text
retrieved_chunks.source_file
```

## 想定回答

```text
この回答では、以下のSourceFileを参照しています。

- 04_output_csv/ai_context_v002.md
- 02_rule_master/bim_rule_master_v003.csv
- 04_output_csv/fix_guides_v001.md

RAG回答は参考情報であり、必要に応じてBIM担当者が元ファイルを確認してください。
```

---

# 10. 複合条件の質問

## 想定質問

```text
Roomカテゴリで、HumanReviewRequiredがtrue、かつHigh Severityの問題を確認したい。
```

## 想定検索条件

```text
category = "Room"
human_review_required = true
severity = "High"
chunk_type = "Element"
```

## 参照候補

```text
Element単位チャンク
RuleId単位チャンク
Fix Guide単位チャンク
```

## 想定回答

```text
RoomカテゴリでHumanReviewRequiredがtrue、かつHigh Severityの問題として、RuleId R-101に該当するRoomName未入力が想定されます。

RoomNameが未入力の場合、空間の意味をAIやBIが判断しにくくなります。
Room情報を検索、集計、RAG回答で利用する前に、BIM担当者が元モデルまたはRoom Scheduleを確認することが推奨されます。

最終判断はBIM担当者が行います。
```

## 表示する根拠

```text
Category: Room
RuleId: R-101
RuleName: RoomName missing
Severity: High
HumanReviewRequired: true
SourceFile: 04_output_csv/room_ai_context_v001.md
```

---

# RAG回答で必ず守ること

RAG回答では、以下を守る。

```text
設計判断をしない
施工判断をしない
法規適合性の最終判断をしない
Revitモデルの自動修正を提案しない
入力情報にないことを断定しない
HumanReviewRequired=Trueの場合は人間確認が必要と明記する
RuleId / Severity / AI Readiness Score / Fix Guide / SourceFileを可能な範囲で示す
LLM回答は参考情報であると明記する
最終判断はBIM担当者が行うと明記する
```

---

# 初期MVPで優先する検索例

第3段階Dの初期MVPでは、以下の検索例を優先する。

```text
ElementIdで品質問題を確認する
RuleIdの意味と修正方針を確認する
Categoryごとの確認観点を確認する
HumanReviewRequired=Trueの要素を確認する
Fix Guideを使って対応案を確認する
```

---

# 将来拡張候補

将来的には、以下のような検索例も検討する。

```text
FixPriorityがHighの要素を優先表示する
LevelNameごとに品質問題を確認する
FamilyName / TypeNameごとに品質傾向を確認する
RoomName / RoomNumberで空間情報を検索する
SourceFileごとに生成元データを確認する
GeneratedDateで新旧データを比較する
複数モデルまたは複数プロジェクト横断で検索する
レビュー済み / 未レビューを検索する
```

ただし、これらは第3段階Dでは実装しない。

---

# 制約

第3段階Dでは、以下は行わない。

```text
Azure AI Searchの実装
Azure OpenAI / OpenAI API接続
Embedding生成
ベクトル検索
クラウド環境構築
認証・権限設計の実装
RAGチャットUIの開発
検索精度評価
実案件データ投入
Revitモデル自動修正
設計判断・施工判断の自動化
```

このドキュメントは、将来的なRAG / Azure AI Search活用を想定した検索例の設計メモである。

---

# 完了条件

このドキュメントの完了条件は以下である。

```text
ElementIdで検索する質問例を整理した
UniqueIdで検索する質問例を整理した
RuleIdで検索する質問例を整理した
Categoryで検索する質問例を整理した
Severityで絞り込む質問例を整理した
HumanReviewRequiredで検索する質問例を整理した
Fix Guideを使った対応案の質問例を整理した
AI Readiness Scoreで検索する質問例を整理した
SourceFileを確認する質問例を整理した
複合条件の質問例を整理した
RAG回答で守るべき制約を整理した
初期MVPで優先する検索例を整理した
将来拡張候補を整理した
```

---

# 次に作成するファイル

次に作成するファイルは以下とする。

```text
docs/rag_answer_policy.md
```

`rag_answer_policy.md` では、RAG回答時の表現ルール、禁止する回答、HumanReviewRequired=Trueの扱い、根拠表示方針、最終判断者を整理する。
