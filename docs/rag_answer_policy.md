# RAG Answer Policy

## 目的

このドキュメントは、`BIM Data Quality & AI Readiness Assessment PoC` の成果物を、将来的にRAG / Azure AI Searchで活用する場合の回答方針を整理するものである。

第3段階Dでは、RAGシステムやAzure AI Searchを本格実装しない。

目的は、将来的にRAG回答を生成する場合に、LLMが何を回答してよいか、何を回答してはいけないか、どの根拠を表示するか、人間確認をどのように扱うかを明確にすることである。

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
docs/rag_query_examples.md
docs/rag_limitations.md
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl
```

このドキュメントでは、RAG回答時の表現ルール、禁止事項、根拠表示、HumanReviewRequiredの扱いを整理する。

---

## RAG回答の目的

RAG回答の目的は、BIM担当者がデータ品質やAI活用準備度を確認しやすくすることである。

RAG回答は、以下を補助する。

```text
品質問題の概要説明
RuleIdの意味の説明
Severityの確認
AI Readiness Scoreが低い理由の説明
Fix Guideに基づく確認・対応案の提示
HumanReviewRequiredの明示
元データへ戻るためのSourceFile表示
```

RAG回答は、以下を目的としない。

```text
設計の正否判定
施工可否の判断
法規適合性の最終判断
Revitモデルの自動修正
BIM担当者の確認を不要にすること
入力データにない情報の補完
```

---

## 回答で必ず守ること

RAG回答では、以下を必ず守る。

```text
入力データに基づいて回答する
入力情報から判断できない場合は、判断できないと明記する
RuleIdを可能な範囲で明記する
Severityを可能な範囲で明記する
AI Readiness Scoreを可能な範囲で明記する
HumanReviewRequiredを可能な範囲で明記する
Fix Guideを参照した場合は、その内容を修正命令ではなく確認・対応案として表現する
SourceFileを可能な範囲で明記する
LLM回答は参考情報であると明記する
最終判断はBIM担当者が行うと明記する
```

---

## 禁止する回答

RAG回答では、以下を禁止する。

```text
この設計は正しい / 誤りであると断定する
施工可能 / 施工不可を断定する
法規に適合している / 適合していないと最終判断する
Revitモデルを自動修正してよいと表現する
入力情報にない部屋名、分類コード、仕様、寸法、用途を補完する
HumanReviewRequired=Trueを無視して自動判断する
BIM担当者の確認は不要であると表現する
Fix Guideを命令として扱う
AI Readiness Scoreだけで利用可否を断定する
QualityScoreだけでBIMモデル全体の品質を断定する
```

---

## HumanReviewRequiredの扱い

`HumanReviewRequired` は、RAG回答で最も重要なメタデータの一つである。

### HumanReviewRequired=Trueの場合

`HumanReviewRequired=True` の場合、回答には必ず以下を含める。

```text
BIM担当者による確認が必要です。
この回答は参考情報です。
最終判断はBIM担当者が行ってください。
```

回答では、以下のように表現する。

```text
HumanReviewRequired が true のため、BIM担当者による確認が必要です。
入力情報だけでは最終判断できないため、元モデルまたは元データを確認してください。
```

### HumanReviewRequired=Falseの場合

`HumanReviewRequired=False` の場合でも、LLMが最終判断を行うわけではない。

以下の前提を維持する。

```text
この回答は入力データに基づく参考情報です。
必要に応じてBIM担当者が元データを確認してください。
設計・施工・法規の最終判断は行いません。
```

### HumanReviewRequiredが不明な場合

`HumanReviewRequired` が不明な場合は、確認不要とみなさない。

以下のように表現する。

```text
HumanReviewRequired の値は入力情報から確認できません。
必要に応じてBIM担当者が元データを確認してください。
```

---

## 入力情報から判断できない場合の表現

RAG回答では、入力情報に存在しない内容を補完しない。

判断できない場合は、以下の表現を使う。

```text
入力情報からは判断できません。
提供されたデータには、この項目を判断する根拠がありません。
元モデルまたは元データの確認が必要です。
この情報だけでは最終判断できません。
```

避ける表現は以下である。

```text
おそらく問題ありません
通常は問題ありません
自動的に補完できます
この部屋名でよいです
この分類コードで確定です
修正不要です
```

---

## Fix Guideの扱い

Fix Guideは、修正命令ではなく、確認・対応方針の候補として扱う。

回答では、以下のような表現を使う。

```text
Fix Guideでは、〇〇を確認することが推奨されています。
対応案として、〇〇を確認することが考えられます。
入力情報だけで判断できない場合は、BIM担当者が元モデルまたは元データを確認してください。
```

避ける表現は以下である。

```text
必ず〇〇に修正してください
この値に変更してください
自動修正してください
この分類コードで確定してください
確認なしで修正できます
```

---

## RuleIdの扱い

RuleIdは、品質チェック結果、Rule Master、Fix Guideを結び付ける重要なキーである。

回答では、可能な範囲でRuleIdを明記する。

例：

```text
この要素では、RuleId D-002 に該当する品質問題が検出されています。
RuleId R-101 は、RoomName未入力を検出するルールです。
```

RuleIdを説明する場合は、以下を含める。

```text
RuleId
RuleName
対象カテゴリ
Severity
AI活用上の影響
Fix Guide上の確認方針
```

---

## Severityの扱い

Severityは、PoC上のデータ品質評価における重要度として扱う。

Severityは、設計・施工・安全性・法規適合性の最終判断ではない。

回答では、以下のように表現する。

```text
Severity は High です。
これはPoC上のデータ品質評価における重要度です。
設計品質や施工品質そのものを直接判定するものではありません。
```

---

## QualityScore / AI Readiness Scoreの扱い

QualityScoreは、BIMデータ品質の参考指標として扱う。

AI Readiness Scoreは、BI、データ分析、生成AI、RAGなどで活用する前段階のデータ準備度として扱う。

回答では、以下を避ける。

```text
QualityScoreが高いのでモデル品質は完全です
AI Readiness Scoreが高いのでAIで自動判断できます
AI Readiness Scoreが低いので使えません
```

回答では、以下のように表現する。

```text
AI Readiness Scoreは、AI活用前のデータ準備度を示す参考指標です。
Scoreが低い場合は、該当RuleIdやFix Guideを確認し、BIM担当者が元データを確認することが推奨されます。
```

---

## SourceFileの表示方針

RAG回答では、可能な範囲でSourceFileを表示する。

SourceFileは、回答の根拠となる元データへ戻るための情報である。

表示例：

```text
SourceFile:
- 04_output_csv/ai_context_v002.md
- 02_rule_master/bim_rule_master_v003.csv
- 04_output_csv/fix_guides_v001.md
```

SourceFileを表示することで、BIM担当者が元データを確認できるようにする。

---

## 回答に含める根拠

RAG回答では、可能な範囲で以下を含める。

```text
ElementId
UniqueId
Category
RuleId
RuleName
Severity
QualityScore
AI Readiness Score
AI Readiness Level
HumanReviewRequired
FixPriority
Fix Guide
SourceFile
```

ただし、すべての回答で全項目が必ず存在するとは限らない。

存在しない項目は、無理に補完しない。

---

## 回答テンプレート：ElementId確認

```text
ElementId {element_id} の {category} 要素では、RuleId {rule_id} に該当する品質問題が検出されています。

RuleName: {rule_name}
Severity: {severity}
AI Readiness Score: {ai_readiness_score}
HumanReviewRequired: {human_review_required}

Fix Guideでは、{fix_guide_summary} が推奨されています。

HumanReviewRequired が true の場合、BIM担当者による確認が必要です。
この回答は参考情報であり、最終判断はBIM担当者が行ってください。

SourceFile:
- {source_file}
```

---

## 回答テンプレート：RuleId説明

```text
RuleId {rule_id} は、{category}カテゴリにおける「{rule_name}」を検出するルールです。

Severity: {severity}

この品質問題は、BI、データ分析、生成AI、RAGで利用する前段階のデータ準備度に影響する可能性があります。

Fix Guideでは、{fix_guide_summary} が推奨されています。

この回答は参考情報であり、設計・施工・法規の最終判断は行いません。
最終判断はBIM担当者が行ってください。

SourceFile:
- {source_file}
```

---

## 回答テンプレート：Category確認

```text
{category}カテゴリでは、{common_issues} がAI Readinessに影響する可能性があります。

関連するRuleId:
- {rule_id_list}

確認観点:
- {review_point_list}

この回答はBIMデータ品質確認の参考情報です。
必要に応じてBIM担当者が元モデルまたは元データを確認してください。

SourceFile:
- {source_file}
```

---

## 回答テンプレート：判断できない場合

```text
入力情報からは判断できません。

提供されたデータには、{unknown_item} を判断するための根拠が含まれていません。

必要に応じて、BIM担当者が元モデル、集計表、または関連ドキュメントを確認してください。

この回答は参考情報であり、最終判断はBIM担当者が行ってください。
```

---

## 回答時の優先順位

複数のチャンクが取得された場合、回答では以下の優先順位で根拠を使う。

```text
1. Element単位チャンク
2. RuleId単位チャンク
3. Fix Guide単位チャンク
4. Category単位チャンク
5. Docs / Policyチャンク
```

ただし、質問がRuleIdの意味を問う場合は、RuleId単位チャンクを優先する。

質問が修正方針を問う場合は、Fix Guide単位チャンクを優先する。

質問がカテゴリ全体の傾向を問う場合は、Category単位チャンクを優先する。

---

## 回答例：HumanReviewRequired=True

```text
ElementId 100001 の Door 要素では、RuleId D-002 に該当する品質問題が検出されています。

Severity は High、AI Readiness Score は 72.5 です。
HumanReviewRequired が true のため、BIM担当者による確認が必要です。

Fix Guideでは、分類コードまたは関連パラメータを確認することが推奨されています。

この回答は参考情報です。
最終判断はBIM担当者が行ってください。

SourceFile:
- 04_output_csv/ai_context_v002.md
- 04_output_csv/fix_guides_v001.md
```

---

## 回答例：入力情報から判断できない場合

```text
入力情報からは判断できません。

提供されたデータには、この要素の正しい分類コードを特定するための根拠が含まれていません。

BIM担当者が元モデル、集計表、または社内基準を確認してください。

この回答は参考情報であり、最終判断はBIM担当者が行ってください。
```

---

# セキュリティ・公開範囲

RAG回答では、実案件データ、顧客名、個人情報、社外秘モデル情報を扱わない。

GitHubに公開するサンプルでは、以下に限定する。

```text
公開可能なサンプルデータ
匿名化したPoC用データ
自作サンプル
概念スキーマ
設計メモ
```

以下は含めない。

```text
実案件データ
顧客名
プロジェクト名
個人情報
社外秘モデル由来情報
社内固有の分類コード
機密性の高い仕様情報
```

---

# 制約

第3段階Dでは、以下は行わない。

```text
Azure AI Searchの実装
Azure OpenAI / OpenAI API接続
Embedding生成
ベクトル検索
クラウド環境構築
RAGチャットUIの開発
検索精度評価
実案件データ投入
Revitモデル自動修正
設計判断・施工判断の自動化
```

このドキュメントは、将来RAG実装を検討する際の回答方針メモである。

---

# 完了条件

このドキュメントの完了条件は以下である。

```text
RAG回答の目的を整理した
回答で必ず守ることを整理した
禁止する回答を整理した
HumanReviewRequired=Trueの扱いを整理した
HumanReviewRequired=Falseの扱いを整理した
HumanReviewRequired不明時の扱いを整理した
入力情報から判断できない場合の表現を整理した
Fix Guideの扱いを整理した
RuleIdの扱いを整理した
Severityの扱いを整理した
QualityScore / AI Readiness Scoreの扱いを整理した
SourceFileの表示方針を整理した
回答に含める根拠を整理した
回答テンプレートを作成した
回答時の優先順位を整理した
セキュリティ・公開範囲を整理した
制約を整理した
```

---

# 次に作成するファイル

次に作成するファイルは以下とする。

```text
docs/rag_limitations.md
```

`rag_limitations.md` では、第3段階Dで実装しないこと、Azure AI Search未実装の制約、Embedding未実施、ベクトル検索未実施、実案件データを扱わない方針などを整理する。
