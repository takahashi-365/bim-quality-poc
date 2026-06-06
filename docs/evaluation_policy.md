# Evaluation Policy

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、`BIM Data Quality & AI Readiness Assessment PoC` における評価方針を整理するための資料です。

本PoCでは、AIモデルの精度そのものを主目的にするのではなく、BIM品質チェック結果を、品質評価、特徴量設計、修正優先度分類プロトタイプ、AI Readiness Score、生成AI向け構造化コンテキスト、Fix Guide Markdownへ接続する流れを検証することを目的とします。

この資料では、以下の評価方針を整理します。

* QualityScoreの評価方針
* FixPriority仮ラベルの評価方針
* 修正優先度分類プロトタイプの評価方針
* AI Readiness Scoreの評価方針
* HumanReviewRequiredの扱い
* AI Context v002の評価方針
* Fix Guide Markdownの評価方針
* 実務適用時に必要な追加データ

---

## 1. 評価対象

本PoCで評価する対象は、完成された本格的なAIモデルや実務品質評価システムではありません。

評価対象は、以下の一連の処理です。

* Revit書き出しTXTを品質チェック用CSVへ変換する
* Revit由来CSVをクレンジングする
* RuleIdベースで品質チェックを行う
* 品質チェック結果CSVを出力する
* 品質メトリクスを作成する
* QualityScoreを算出する
* 機械学習用の特徴量を設計する
* FixPriority仮ラベルを作成する
* scikit-learnで修正優先度分類プロトタイプを作成する
* classification_report、混同行列、予測結果を出力する
* AI Readiness Scoreを算出する
* AI Readiness Levelを分類する
* HumanReviewRequiredを判定する
* AI Context v002をJSON / Markdownで生成する
* Fix Guide Markdownを生成する
* Streamlitで各出力を確認する
* モデルやスコアの限界と実務適用条件を整理する

---

## 2. 評価の目的

評価の目的は、モデル精度を高く見せることではありません。

目的は、以下を確認することです。

* BIM品質チェック結果を機械学習用データに変換できるか
* RuleId、Severity、違反数、品質スコアなどを特徴量として扱えるか
* 修正優先度を分類するための仮ラベルを設計できるか
* scikit-learnを使って学習・予測・評価の基本フローを実装できるか
* BIMデータがAI活用に使える状態かを簡易評価できるか
* AI Readiness ScoreをRuleIdベースで算出できるか
* AI Context v002として、生成AIやRAGへ渡す前段階の構造化コンテキストを作れるか
* Fix Guide Markdownとして、人間確認向けの修正方針を出力できるか
* 実務適用にはどのような教師データ、BIM標準、業務ルールが必要かを整理できるか

---

## 3. モデル精度を主目的にしない理由

本PoCでは、モデル精度を主目的にしません。

理由は、現時点では実務の正解ラベルが存在しないためです。

修正優先度 High / Medium / Low は、初期段階ではRuleId、Severity、違反数、QualityScoreなどをもとにした仮ラベルとして設計しています。

そのため、分類結果は実務判断を完全に再現するものではありません。

また、現時点のデータでは全25要素の `FixPriority` が `High` であり、本格的な分類精度評価には適していません。

本PoCで重視するのは、以下です。

* BIM品質チェック結果を特徴量データセットへ変換すること
* 機械学習プロトタイプの流れを実装すること
* 評価指標を出力できること
* AI Readiness Scoreを算出できること
* 生成AI向け構造化コンテキストを作成できること
* RuleIdベースでFix Guideを生成できること
* 実務データが必要な理由を説明できること

---

## 4. QualityScoreの評価方針

本PoCでは、BIM品質チェック結果をもとに、要素ごとの簡易品質スコアである `QualityScore` を作成します。

`QualityScore` は、現時点ではPoC用の簡易指標であり、実務上の正式な品質評価基準ではありません。

初期設計では、100点を初期値とし、検出された違反の重大度に応じて減点します。

| Severity |  減点 |
| -------- | --: |
| High     | 10点 |
| Medium   |  5点 |
| Low      |  1点 |

計算式は以下です。

```text
QualityScore = 100 - SeverityScore
```

ただし、スコアは0点から100点の範囲に丸めます。

現時点では、以下のように扱います。

* `QualityScore` が低い要素ほど、品質上の確認・修正優先度が高い可能性がある
* `QualityScore` は、修正優先度分類プロトタイプの入力特徴量として利用する
* `QualityScore` は、StreamlitでElementId別品質スコアとして表示する
* `QualityScore` は、実務の正解ラベルではなく、PoC用の参考指標である
* 実務適用する場合は、プロジェクト条件、BIM実行計画、発注者要件、後工程での利用目的に応じて調整が必要である

今回の初期データでは、各要素に `High` 違反が3件、`Medium` 違反が1件発生しているため、1要素あたりの減点は以下となります。

```text
High 3件 × 10点 = 30点
Medium 1件 × 5点 = 5点
合計減点 = 35点
```

そのため、該当要素の `QualityScore` は以下となります。

```text
100 - 35 = 65
```

このスコアは、現時点では正確な実務評価ではなく、品質チェック結果を数値化し、特徴量設計やStreamlit表示へ接続するための簡易スコアとして扱います。

---

## 5. FixPriority仮ラベルの評価方針

本PoCでは、特徴量データセットに `FixPriority` を付与しています。

ただし、現時点の `FixPriority` は実務の正解ラベルではありません。

`QualityScore` と `HighViolationCount` をもとにした仮ラベルであり、修正優先度分類プロトタイプへ接続するための初期設計です。

想定するラベルは以下です。

| ラベル    | 意味          | 想定条件                          |
| ------ | ----------- | ----------------------------- |
| High   | 優先的に修正すべき違反 | Highの違反が多い、QualityScoreが低い    |
| Medium | 通常の修正対象     | 違反はあるが重大度が中程度                 |
| Low    | 優先度が低い修正対象  | 軽微な違反、またはQualityScoreへの影響が小さい |

現時点の初期データでは、全25要素の `FixPriority` が `High` です。

そのため、現時点のFixPriorityは分類精度を評価するための正解ラベルではなく、機械学習処理フローを確認するための仮ラベルとして扱います。

---

## 6. 使用する特徴量

現時点で作成している特徴量は以下です。

| 特徴量                   | 内容                      |
| --------------------- | ----------------------- |
| ElementId             | 要素ID。現時点では建具番号を仮IDとして使用 |
| Category              | BIMカテゴリ。現時点ではDoors      |
| RuleViolationCount    | 要素ごとの違反数                |
| MissingFieldCount     | 未入力項目数                  |
| HighViolationCount    | High違反数                 |
| MediumViolationCount  | Medium違反数               |
| LowViolationCount     | Low違反数                  |
| HasClassificationCode | 分類コード有無                 |
| FamilyNameValid       | ファミリ名が命名規則に合うか          |
| SeverityScore         | 重大度を数値化した値              |
| QualityScore          | 品質スコア                   |
| FixPriority           | 修正優先度仮ラベル               |

これらの特徴量は、BIM品質チェック結果CSVや品質メトリクスから作成します。

---

## 7. 修正優先度分類プロトタイプの評価方針

修正優先度分類プロトタイプでは、以下の出力を作成しています。

```text
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
```

評価指標としては、以下を扱います。

| 指標                    | 目的                              |
| --------------------- | ------------------------------- |
| accuracy_score        | 全体の分類一致率を確認する                   |
| classification_report | precision、recall、f1-scoreを確認する  |
| confusion_matrix      | High / Medium / Low の誤分類傾向を確認する |
| predictions           | 要素ごとの予測結果を確認する                  |

ただし、現時点では `FixPriority` が1クラスのみであり、評価指標はモデル性能の証明ではなく、分類プロトタイプの動作確認として扱います。

避ける表現：

* 高精度なAIモデルを作成した
* 修正優先度を正確に予測できる
* 実務適用可能なAIモデルを完成させた

使用する表現：

* 修正優先度分類プロトタイプを作成した
* BIM品質チェック結果を特徴量データセットへ変換した
* scikit-learnを用いて分類・評価の流れを検証した
* 仮ラベルを用いた分類プロトタイプとして、classification_report、混同行列、予測結果を出力した
* 実務適用には修正履歴や修正工数などの教師データが必要である

---

## 8. AI Readiness Scoreの評価方針

本PoCでは、BIMデータがAIやデータ活用に使いやすい状態かを評価する簡易スコアとして `AIReadinessScore` を追加しています。

AI Readiness Scoreは、以下の観点をRuleIdベースで評価します。

* 必須属性が入力されているか
* 分類コードが入力されているか
* 命名規則が一定のルールに沿っているか
* AIやBIで検索・分類・集計しやすい状態か
* 人間確認が必要な状態か

初期計算式は以下です。

```text
AIReadinessScore = 100 - AIReadinessPenalty合計
```

初期レベル分類は以下です。

| AIReadinessScore | AIReadinessLevel |
| ---------------- | ---------------- |
| 80-100           | High             |
| 60-79            | Medium           |
| 0-59             | Low              |

現時点の初期データでは、全25要素が以下の結果となっています。

```text
AIReadinessScore = 40
AIReadinessLevel = Low
HumanReviewRequired = True
```

これは、各要素に以下の違反が含まれているためです。

* R-001 必須パラメータ未入力
* R-002 分類コード未入力
* R-003 ファミリ命名規則違反

この結果は、現時点の入力データが正式にAI活用不可であることを示すものではありません。

AIやBIに活用する前に、属性情報、分類コード、命名規則を整備する必要があることを説明するためのPoC結果として扱います。

---

## 9. HumanReviewRequiredの評価方針

`HumanReviewRequired` は、人間確認が必要かどうかを示すフラグです。

現時点では、以下の条件で `True` とします。

* `AIReadinessLevel` が `Low`
* `HighImpactRuleCount` が1件以上

このフラグは、BIMモデルを自動修正するためのものではありません。

AIやBIに利用する前に、人間のBIM担当者、設計者、管理者が確認すべき要素を示すための参考指標です。

現時点の初期データでは、全25要素が `HumanReviewRequired = True` です。

---

## 10. AI Context v002の評価方針

AI Context v002では、BIM品質チェック結果、特徴量データセット、AI Readiness Scoreをもとに、生成AIへ渡すための参照情報をJSON / Markdown形式で整理しています。

出力ファイルは以下です。

```text
04_output_csv/ai_context_v002.json
04_output_csv/ai_context_v002.md
```

評価観点は以下です。

* 品質チェック結果がElementId単位で整理されているか
* QualityScoreが含まれているか
* FixPriorityが含まれているか
* AIReadinessScoreが含まれているか
* AIReadinessLevelが含まれているか
* HumanReviewRequiredが含まれているか
* RuleId別の違反内容が含まれているか
* FixGuideが含まれているか
* 生成AIに渡す際の制約条件が明記されているか
* 生成AI API未接続であることが明記されているか

現時点では、OpenAI APIなどの生成AI APIは呼び出していません。

生成AIに自由回答させるのではなく、RuleId、品質チェック結果、QualityScore、FixPriority、AIReadinessScore、HumanReviewRequiredなどを明示的に渡す前処理として評価します。

---

## 11. Fix Guide Markdownの評価方針

Fix Guide Markdownでは、品質チェック結果、Rule Master v003、AI Readiness Scoreをもとに、RuleIdベースの修正方針をMarkdownとして出力しています。

出力ファイルは以下です。

```text
04_output_csv/fix_guides_v001.md
```

評価観点は以下です。

* Summaryが出力されているか
* Input Filesが出力されているか
* AI Readiness Level Summaryが出力されているか
* Blocking Rule Summaryが出力されているか
* ElementId別 Fix Guideが出力されているか
* 各ElementIdにAI Readiness Scoreが表示されているか
* 各ElementIdにHumanReviewRequiredが表示されているか
* RuleId別のFixGuideが表示されているか
* AIReadinessImpactとAIReadinessPenaltyが表示されているか
* 生成AI APIではなくルールベース生成であることが明記されているか

Fix Guide Markdownは、生成AI APIによる文章生成ではなく、RuleIdベースのテンプレート方式で生成しています。

実際のモデル修正や設計判断を自動化するものではなく、人間確認向けの参考資料として扱います。

---

## 12. 実務適用に必要な教師データ

実務で修正優先度分類やAI Readiness評価を行うには、以下のような教師データや業務ルールが必要です。

* 実際の修正履歴
* 修正にかかった時間
* 修正工数
* 手戻り発生有無
* 担当者の判断結果
* 設計・施工上の影響度
* プロジェクト条件
* BIM実行計画上の重要度
* 発注者要件
* 後工程での利用有無
* 社内BIM標準
* 分類体系
* 命名規則
* AI利用目的
* RAGや生成AIに渡す情報の範囲
* 人間確認が必要な条件

これらのデータがなければ、実務判断に近い修正優先度モデルや正式なAI Readiness評価を作ることはできません。

そのため、本PoCでは、実務適用に必要なデータ条件を明記したうえで、プロトタイプとして検証します。

---

## 13. 評価結果の見せ方

評価結果を見せる際は、過大表現を避けます。

避ける表現：

* 高精度なAIモデルを作成した
* 修正優先度を正確に予測できる
* 実務適用可能なAIモデルを完成させた
* AI活用可否を正確に判定できる
* BIMモデルを自動修正できる
* 生成AIが修正内容を判断している

使用する表現：

* 修正優先度分類プロトタイプを作成した
* BIM品質チェック結果を特徴量データセットへ変換した
* scikit-learnを用いて分類・評価の流れを検証した
* AI Readiness ScoreをPoC用の簡易指標として算出した
* RuleIdベースでAI活用への影響を整理した
* AI Context v002として生成AI向け構造化コンテキストを作成した
* Fix Guide MarkdownをRuleIdベースのテンプレート方式で生成した
* 実務適用には修正履歴、修正工数、BIM標準、分類体系、AI利用目的などの追加情報が必要である

---

## 14. 本PoCで示したいこと

本PoCで示したいことは、AIモデルを完成させたことではありません。

示したいことは、以下です。

* BIM品質チェック結果を分析・機械学習で扱える形に変換できる
* BIM導入支援で扱う品質課題を、特徴量設計へ接続できる
* RuleId、Severity、品質スコアを機械学習用データとして扱える
* scikit-learnを使った分類プロトタイプを実装できる
* RuleIdベースでAI活用準備度を評価できる
* AI Readiness Scoreを算出できる
* 生成AI向け構造化コンテキストをJSON / Markdownで作成できる
* RuleIdベースでFix Guide Markdownを生成できる
* モデルやスコアの限界を理解し、実務適用条件を説明できる
* 建築BIMデータをAI活用につなげる前処理を設計できる

---

## 15. まとめ

本PoCの評価方針は、モデル精度の高さを示すことではなく、BIM品質チェック結果を、品質メトリクス、特徴量データセット、分類プロトタイプ、AI Readiness Score、AI Context v002、Fix Guide Markdownへ接続する一連の流れを検証することです。

修正優先度分類は、現時点では仮ラベルを用いたプロトタイプとして扱います。

AI Readiness Scoreは、現時点ではPoC用の簡易指標として扱います。

AI Context v002は、生成AIやRAGへ渡す前段階の構造化コンテキストとして扱います。

Fix Guide Markdownは、生成AI APIではなくRuleIdベースのテンプレート方式で生成した人間確認向け資料として扱います。

実務適用には、修正履歴、修正工数、担当者判断、プロジェクト条件、BIM標準、分類体系、AI利用目的などの追加データが必要です。

そのため、本PoCでは、過大表現を避けながら、BIMデータ品質チェックから特徴量設計、分類プロトタイプ、AI活用準備度評価、生成AI向け構造化コンテキスト生成、Fix Guide生成までの一連の流れを示します。
