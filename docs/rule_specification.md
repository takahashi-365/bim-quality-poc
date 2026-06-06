# Rule Specification

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、`BIM Data Quality & AI Readiness Assessment PoC` で使用する RuleId ルールマスタの仕様を整理するための資料です。

RuleId は、BIM品質チェック、チェック結果CSV、品質メトリクス、特徴量データセット、AI Readiness Score、AI Context v002、Fix Guide Markdown、Streamlit表示を接続するための共通キーとして使用します。

この資料では、RuleIdルールマスタの各列の意味、初期ルールの内容、Severityの考え方、AI Readiness拡張列の考え方、今後の拡張方針を整理します。

---

## 1. RuleIdルールマスタの位置づけ

RuleIdルールマスタは、BIM品質チェックに使用するルールを外部CSVとして管理するためのファイルです。

現時点では、以下の2つのルールマスタを扱います。

第1段階の品質チェック用ルールマスタ：

```text
02_rule_master/bim_rule_master_v002.csv
```

第2段階のAI Readiness対応ルールマスタ：

```text
02_rule_master/bim_rule_master_v003.csv
```

`bim_rule_master_v002.csv` は、RuleIdベース品質チェック、品質メトリクス、特徴量データセット、AI Context v001のために使用します。

`bim_rule_master_v003.csv` は、v002を拡張し、AI Readiness Score算出、AI Context v002、Fix Guide Markdown生成のために使用します。

---

## 2. RuleIdを共通キーとして使う理由

RuleIdを共通キーとして使用することで、以下の処理を接続します。

* BIM品質チェック
* 品質チェック結果CSV
* RuleId別集計
* Category別集計
* ElementId別集計
* QualityScore算出
* 特徴量データセット作成
* FixPriority仮ラベル作成
* 修正優先度分類プロトタイプ
* AI Readiness Score算出
* AI Context JSON / Markdown v002生成
* Fix Guide Markdown生成
* Streamlit画面表示

RuleIdを共通キーにすることで、どの品質ルールが、どの要素に、どの程度の影響を与えているかを追跡しやすくします。

また、生成AI向け構造化コンテキストやFix Guide Markdownでも、AIに自由判断させるのではなく、RuleIdを基準に参照情報を整理できるようにします。

---

## 3. Rule Master v002

Rule Master v002は、第1段階で使用するBIM品質チェック用ルールマスタです。

対象ファイル：

```text
02_rule_master/bim_rule_master_v002.csv
```

目的：

* 品質チェックルールを外部CSVとして管理する
* Python品質チェックで参照する
* 品質メトリクス作成でRuleIdを使用する
* 特徴量データセット作成でRuleIdを使用する
* AI Context v001生成でRuleIdを使用する

主な列は以下です。

| 列名             | 意味          |
| -------------- | ----------- |
| RuleId         | ルールID       |
| RuleName       | ルール名        |
| Category       | 対象カテゴリ      |
| Severity       | 重大度         |
| TargetField    | チェック対象フィールド |
| CheckLogic     | チェックロジック    |
| BusinessImpact | 業務上の影響      |
| AIUseImpact    | AI活用時の影響    |
| FixGuide       | 修正方針        |
| Reference      | 参照情報        |

v002では、v001に含まれていた不要な空行を削除し、3行 × 10列のルールマスタとして整理しています。

---

## 4. Rule Master v003

Rule Master v003は、第2段階で使用するAI Readiness対応ルールマスタです。

対象ファイル：

```text
02_rule_master/bim_rule_master_v003.csv
```

目的：

* Rule Master v002を拡張する
* RuleIdごとのAI活用への影響度を管理する
* RuleIdごとのAI Readiness Score減点値を管理する
* AI Readiness Score算出に使用する
* AI Context v002生成に使用する
* Fix Guide Markdown生成に使用する

Rule Master v003では、Rule Master v002に以下の列を追加しています。

| 追加列                | 意味                        |
| ------------------ | ------------------------- |
| AIReadinessImpact  | AI活用準備度への影響度              |
| AIReadinessPenalty | AI Readiness Score算出時の減点値 |

---

## 5. Rule Master v003の列構成

Rule Master v003の列構成は以下です。

| 列名                 | 意味                    | 使用箇所                                        |
| ------------------ | --------------------- | ------------------------------------------- |
| RuleId             | ルールID                 | 品質チェック、集計、AI Readiness、AI Context、Fix Guide |
| RuleName           | ルール名                  | 品質チェック結果、Streamlit、Fix Guide                |
| Category           | 対象カテゴリ                | ルール適用対象の整理                                  |
| Severity           | 品質チェック上の重大度           | QualityScore、Streamlit、Fix Guide            |
| TargetField        | チェック対象フィールド           | 品質チェック、Fix Guide                            |
| CheckLogic         | チェックロジック              | ルール仕様の説明                                    |
| BusinessImpact     | 業務上の影響                | AI Context、Fix Guide                        |
| AIUseImpact        | AI活用時の影響              | AI Context、Fix Guide                        |
| FixGuide           | 修正方針                  | 品質チェック結果、AI Context、Fix Guide               |
| Reference          | 参照情報                  | ルール根拠の補足                                    |
| AIReadinessImpact  | AI活用準備度への影響度          | AI Readiness Score、Fix Guide                |
| AIReadinessPenalty | AI Readiness Score減点値 | AI Readiness Score                          |

---

## 6. 初期ルール

現時点の初期ルールは以下の3つです。

| RuleId | RuleName   | Severity | TargetField              | 主な目的           |
| ------ | ---------- | -------- | ------------------------ | -------------- |
| R-001  | 必須パラメータ未入力 | High     | BIM_ModelRole / BIM_Zone | 必須属性の未入力を検出する  |
| R-002  | 分類コード未入力   | High     | BIM_ClassificationCode   | 分類コードの未入力を検出する |
| R-003  | ファミリ命名規則違反 | Medium   | FamilyName               | 命名規則違反を検出する    |

現時点では、ルール数を増やすことよりも、RuleIdを共通キーとして各処理を接続することを重視します。

---

## 7. Severityの考え方

Severityは、品質チェック上の重大度を示します。

現時点では以下の3段階を想定しています。

| Severity | 意味                     | QualityScore減点 |
| -------- | ---------------------- | -------------: |
| High     | 品質・運用・分析に大きく影響する違反     |             10 |
| Medium   | 品質・検索性・分類性に中程度の影響がある違反 |              5 |
| Low      | 軽微な違反                  |              1 |

現時点の初期ルールでは、以下のように設定しています。

| RuleId | RuleName   | Severity |
| ------ | ---------- | -------- |
| R-001  | 必須パラメータ未入力 | High     |
| R-002  | 分類コード未入力   | High     |
| R-003  | ファミリ命名規則違反 | Medium   |

Severityは、`QualityScore` の算出、Streamlit表示、Fix Guide Markdownの表示に使用します。

---

## 8. QualityScoreとの関係

QualityScoreは、品質チェック結果をもとにしたBIMデータ品質の簡易スコアです。

初期計算式は以下です。

```text
QualityScore = 100 - SeverityScore
```

SeverityScoreは、違反ごとのSeverityに応じた減点を合計して算出します。

| Severity | 減点 |
| -------- | -: |
| High     | 10 |
| Medium   |  5 |
| Low      |  1 |

今回の初期データでは、各要素にHigh違反が3件、Medium違反が1件発生しています。

そのため、1要素あたりのQualityScoreは以下になります。

```text
High 3件 × 10点 = 30点
Medium 1件 × 5点 = 5点
合計減点 = 35点
QualityScore = 100 - 35 = 65点
```

QualityScoreはPoC用の簡易指標であり、実務上の正式な品質評価基準ではありません。

---

## 9. AIReadinessImpactの考え方

AIReadinessImpactは、RuleIdごとの違反がAI活用準備度にどの程度影響するかを示す列です。

現時点では以下の3段階を想定しています。

| AIReadinessImpact | 意味                                |
| ----------------- | --------------------------------- |
| High              | AI活用、BI集計、検索、分類、将来的なRAG利用に大きく影響する |
| Medium            | AI活用や検索・分類に中程度の影響がある              |
| Low               | 影響は限定的だが、将来的には整理した方がよい            |

現時点の初期設定は以下です。

| RuleId | RuleName   | AIReadinessImpact |
| ------ | ---------- | ----------------- |
| R-001  | 必須パラメータ未入力 | High              |
| R-002  | 分類コード未入力   | High              |
| R-003  | ファミリ命名規則違反 | Medium            |

---

## 10. AIReadinessPenaltyの考え方

AIReadinessPenaltyは、AI Readiness Score算出時に使用する減点値です。

初期設定は以下です。

| RuleId | RuleName   | AIReadinessImpact | AIReadinessPenalty |
| ------ | ---------- | ----------------- | -----------------: |
| R-001  | 必須パラメータ未入力 | High              |                 15 |
| R-002  | 分類コード未入力   | High              |                 20 |
| R-003  | ファミリ命名規則違反 | Medium            |                 10 |

各ルールの考え方は以下です。

### R-001 必須パラメータ未入力

必須属性が未入力の場合、AIに渡す属性情報が不足し、回答や分類の信頼性が下がります。

そのため、AIReadinessImpactはHigh、AIReadinessPenaltyは15とします。

### R-002 分類コード未入力

分類コードが未入力の場合、分類、検索、集計、将来的なRAG利用時の前提が弱くなります。

そのため、AIReadinessImpactはHigh、AIReadinessPenaltyは20とします。

### R-003 ファミリ命名規則違反

命名規則違反がある場合、名称ベースの分類や検索の信頼性が下がります。

そのため、AIReadinessImpactはMedium、AIReadinessPenaltyは10とします。

AIReadinessPenaltyはPoC用の仮設定であり、実務上の正式な評価基準ではありません。

---

## 11. AI Readiness Scoreとの関係

AI Readiness Scoreは、BIM要素ごとにAIやデータ活用に使いやすい状態かを評価する簡易スコアです。

初期計算式は以下です。

```text
AIReadinessScore = 100 - AIReadinessPenalty合計
```

スコアが0未満になる場合は0とします。

初期レベル分類は以下です。

| AIReadinessScore | AIReadinessLevel |
| ---------------- | ---------------- |
| 80-100           | High             |
| 60-79            | Medium           |
| 0-59             | Low              |

HumanReviewRequiredの判定は以下です。

* AIReadinessLevelがLowの場合は `True`
* HighImpactRuleCountが1件以上ある場合は `True`
* それ以外は `False`

今回の初期データでは、全25要素が以下の結果となっています。

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

これは、各要素に以下の違反が含まれているためです。

* R-001 必須パラメータ未入力
* R-002 分類コード未入力
* R-003 ファミリ命名規則違反

---

## 12. 各RuleIdの詳細

### R-001 必須パラメータ未入力

目的：

BIM要素に必要な必須パラメータが入力されているかを確認します。

対象フィールド：

* `BIM_ModelRole`
* `BIM_Zone`

Severity：

```text
High
```

AIReadinessImpact：

```text
High
```

AIReadinessPenalty：

```text
15
```

BusinessImpact：

必須パラメータが未入力の場合、BIMデータを設計管理、数量集計、運用管理、品質確認に利用しにくくなります。

AIUseImpact：

AIに渡す属性情報が不足するため、生成AIやRAGでの回答、分類、検索、要約の信頼性が下がります。

FixGuide：

該当要素に必要な `BIM_ModelRole` または `BIM_Zone` を入力します。

---

### R-002 分類コード未入力

目的：

BIM要素に分類コードが入力されているかを確認します。

対象フィールド：

* `BIM_ClassificationCode`

Severity：

```text
High
```

AIReadinessImpact：

```text
High
```

AIReadinessPenalty：

```text
20
```

BusinessImpact：

分類コードが未入力の場合、分類別集計、検索、標準チェック、数量集計、部材管理が難しくなります。

AIUseImpact：

分類コードが不足すると、BI集計、機械学習の特徴量化、生成AIやRAGでの検索・分類精度に影響します。

FixGuide：

分類コード表に従い、`BIM_ClassificationCode` を入力します。

---

### R-003 ファミリ命名規則違反

目的：

FamilyNameが命名規則に沿っているかを確認します。

対象フィールド：

* `FamilyName`

Severity：

```text
Medium
```

AIReadinessImpact：

```text
Medium
```

AIReadinessPenalty：

```text
10
```

BusinessImpact：

命名規則が統一されていない場合、ファミリ管理、検索、置換、標準化、レビューが難しくなります。

AIUseImpact：

名称ベースの分類や検索の信頼性が下がり、生成AIやRAGに渡す文脈の一貫性も下がります。

FixGuide：

命名規則に従い、カテゴリ・用途・識別情報が分かるファミリ名へ修正します。

注意点：

現時点では、`FamilyName` に正式なRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。

そのため、R-003の結果は厳密なRevitファミリ命名規則チェックではなく、処理フロー確認用の参考結果として扱います。

---

## 13. RuleIdと出力ファイルの関係

RuleIdは、以下の出力ファイルで使用されます。

| 出力ファイル                         | RuleIdの使われ方                       |
| ------------------------------ | --------------------------------- |
| `check_results_revit_v002.csv` | どのルールに違反したかを記録                    |
| `rule_summary_v001.csv`        | RuleId別違反件数を集計                    |
| `element_summary_v001.csv`     | ElementId別品質スコア算出に使用              |
| `bim_features_v001.csv`        | 特徴量作成に使用                          |
| `ai_readiness_scores_v001.csv` | BlockingRuleIdsとして使用              |
| `ai_context_v002.json`         | violationsとAI Readiness情報に使用      |
| `ai_context_v002.md`           | Sample Element Contextに使用         |
| `fix_guides_v001.md`           | ElementId別Fix Guideに使用            |
| `streamlit_app.py`             | RuleId別表示、Blocking RuleIdランキングに使用 |

---

## 14. RuleIdとAI Context v002の関係

AI Context v002では、RuleIdをもとに、以下の情報を生成AI向けの参照情報として整理します。

* RuleId
* RuleName
* Severity
* ParameterName
* CurrentValue
* FixGuide
* QualityScore
* FixPriority
* AIReadinessScore
* AIReadinessLevel
* BlockingRuleIds
* HumanReviewRequired

これにより、生成AIに自由回答させるのではなく、品質チェック結果とルール情報をもとに、AIへ渡す情報を制御します。

現時点では生成AI APIは呼び出していません。

---

## 15. RuleIdとFix Guide Markdownの関係

Fix Guide Markdownでは、RuleIdをもとに、ElementId別の修正方針を整理します。

主な出力内容は以下です。

* ElementId
* Category
* FamilyName
* TypeName
* AI Readiness Score
* AI Readiness Level
* AI Readiness Penalty Total
* Blocking RuleIds
* Human Review Required
* RuleId
* RuleName
* Severity
* ParameterName
* CurrentValue
* AIReadinessImpact
* AIReadinessPenalty
* FixGuide

Fix Guide Markdownは、生成AI APIではなく、RuleIdベースのテンプレート方式で生成しています。

---

## 16. 現時点の注意点

* Rule Master v003はPoC用の初期ルールマスタです。
* 現時点では3ルールのみを対象としています。
* Severity、AIReadinessImpact、AIReadinessPenaltyはPoC用の仮設定です。
* QualityScoreは正式な実務品質評価基準ではありません。
* AIReadinessScoreは正式なAI活用準備度基準ではありません。
* FixPriorityは実務上の正解ラベルではありません。
* `FamilyName` は現時点では正式なRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
* R-003の結果は、厳密なRevitファミリ命名規則違反ではなく、処理フロー確認用の参考結果として扱います。
* 実務適用する場合は、社内BIM標準、BEP、プロジェクト要件、分類体系、AI利用目的に応じてルールを調整する必要があります。

---

## 17. 今後の拡張方針

今後の拡張方針は以下です。

* RuleIdの追加
* 対象カテゴリの追加
* Walls、Roomsなどへの対応
* Severityの見直し
* AIReadinessImpactの見直し
* AIReadinessPenaltyの見直し
* BusinessImpactの整理
* AIUseImpactの整理
* FixGuideの具体化
* 社内BIM標準やプロジェクト要件との対応付け
* Revit列マッピング改善後のルール再評価
* AI Readiness Score計算ロジックのテスト追加
* Rule Master v003必須列確認テストの追加

---

## 18. まとめ

RuleIdは、本PoCにおけるBIM品質チェック、品質メトリクス、特徴量作成、AI Readiness Score、AI Context v002、Fix Guide Markdown、Streamlit表示を接続するための共通キーです。

第2段階では、Rule Master v003として `AIReadinessImpact` と `AIReadinessPenalty` を追加し、BIMデータがAIやデータ活用に使える状態かを簡易評価できるようにしました。

現時点ではPoC用の初期設定ですが、RuleIdを中心に各処理を接続することで、BIMデータ品質、AI活用時の影響、修正方針、人間確認要否を一貫して説明できる構成になっています。
