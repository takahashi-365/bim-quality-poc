# Streamlit App Design

## BIM Data Quality Engineering & AI Analysis PoC

## この資料の目的

この資料は、7月に作成予定のStreamlit簡易画面の構成、目的、表示内容、入力データ、出力データを整理するための設計メモです。

本PoCでは、Streamlitを使って、Revit/BIMデータの品質チェック結果、品質メトリクス、特徴量データセットを画面上で確認できるようにします。

目的は、本格的な業務アプリを作ることではなく、面接やポートフォリオでPoCの処理内容を説明しやすくすることです。

---

## 1. Streamlit画面の位置づけ

Streamlitは、本PoCにおける簡易UIとして位置づけます。

本PoCの主役は、Pythonによる以下のデータ処理パイプラインです。

- Revit書き出しTXTの読み込み
- 品質チェック用CSVへの変換
- データクレンジング
- RuleIdベース品質チェック
- 品質メトリクス作成
- 特徴量データセット作成
- 将来的な修正優先度分類プロトタイプ
- 将来的な生成AI向け構造化コンテキスト生成

Streamlitは、これらの処理結果を確認しやすくするための画面です。

Power BIは補助的な可視化、StreamlitはPython処理と接続しやすい簡易UIとして扱います。

---

## 2. 画面の目的

Streamlit画面の目的は以下です。

- 品質チェック結果CSVを画面で確認する
- RuleId別、Severity別、Category別の違反件数を確認する
- 品質メトリクスを表示する
- ElementId別の品質スコアを確認する
- 特徴量データセットを確認する
- CSVをダウンロードできるようにする
- 面接時にPoCの流れを説明しやすくする

---

## 3. 想定する入力ファイル

Streamlit画面では、以下のCSVを読み込む想定です。

### 品質チェック結果CSV

- `04_output_csv/check_results_revit_v002.csv`

主な表示内容：

- CheckId
- ElementId
- Category
- FamilyName
- TypeName
- ParameterName
- CurrentValue
- RuleId
- RuleName
- Severity
- Status
- FixGuide
- SourceFile
- ModelName

### 品質メトリクスCSV

- `04_output_csv/quality_metrics_v001.csv`

主な表示内容：

- TotalIssues
- TotalElementsWithIssues
- AverageViolationsPerElement
- AverageQualityScore
- HighSeverityCount
- MediumSeverityCount
- LowSeverityCount
- R001Count
- R002Count
- R003Count

### RuleId別集計CSV

- `04_output_csv/rule_summary_v001.csv`

主な表示内容：

- RuleId
- RuleName
- Severity
- ViolationCount

### Category別集計CSV

- `04_output_csv/category_summary_v001.csv`

主な表示内容：

- Category
- ViolationCount

### ElementId別集計CSV

- `04_output_csv/element_summary_v001.csv`

主な表示内容：

- ElementId
- Category
- FamilyName
- TypeName
- RuleViolationCount
- SeverityScore
- QualityScore

---

## 4. 画面構成案

## 4-1. タイトルエリア

表示内容：

- PoC名
- 簡単な説明文
- 現時点の位置づけ

表示文案：

BIM Data Quality Engineering & AI Analysis PoC

Revit/BIMデータをPythonで処理し、RuleIdベースの品質チェック、品質メトリクス作成、特徴量設計へ接続する個人開発PoCです。

---

## 4-2. CSV読み込みエリア

表示内容：

- 品質チェック結果CSVの読み込み
- 品質メトリクスCSVの読み込み
- 集計CSVの読み込み

初期版では、ファイルアップロードではなく、固定パスから読み込む形でもよいです。

7月MVPでは、以下のどちらかで進めます。

- 固定パス読み込み
- CSVアップロード

初期実装では、固定パス読み込みを優先します。

理由：

- 実装が簡単
- デモで安定しやすい
- 既存の出力CSVをそのまま利用できる

---

## 4-3. サマリーカード

表示内容：

- 総違反件数
- 違反がある要素数
- 要素あたり平均違反件数
- 平均品質スコア
- High違反件数
- Medium違反件数

表示元：

- `quality_metrics_v001.csv`

目的：

PoC全体の品質状態を一目で確認できるようにする。

---

## 4-4. RuleId別違反件数

表示内容：

- RuleId別違反件数の表
- RuleId別違反件数の棒グラフ

表示元：

- `rule_summary_v001.csv`

目的：

どの品質ルールの違反が多いかを確認できるようにする。

---

## 4-5. Severity別違反件数

表示内容：

- High / Medium / Low の件数
- 重大度別の棒グラフ

表示元：

- `check_results_revit_v002.csv`

目的：

品質リスクの重大度を確認できるようにする。

---

## 4-6. Category別違反件数

表示内容：

- Category別違反件数の表
- Category別違反件数の棒グラフ

表示元：

- `category_summary_v001.csv`

目的：

どのカテゴリに違反が集中しているかを確認できるようにする。

---

## 4-7. ElementId別品質スコア

表示内容：

- ElementId別の違反件数
- SeverityScore
- QualityScore

表示元：

- `element_summary_v001.csv`

目的：

どの要素の品質スコアが低いかを確認できるようにする。

---

## 4-8. 品質チェック結果一覧

表示内容：

- 品質チェック結果CSVの一覧表
- RuleId、Severity、Categoryでフィルタできるようにする

表示元：

- `check_results_revit_v002.csv`

目的：

検出された違反内容を確認できるようにする。

---

## 4-9. CSVダウンロード

ダウンロード対象：

- 品質チェック結果CSV
- 品質メトリクスCSV
- RuleId別集計CSV
- Category別集計CSV
- ElementId別集計CSV

目的：

画面で確認した結果を、CSVとして再利用できるようにする。

---

## 5. 初期版で実装する機能

7月MVPの初期版では、以下を実装対象にします。

- 固定パスからCSVを読み込む
- 品質メトリクスを表示する
- RuleId別違反件数を表示する
- Category別違反件数を表示する
- ElementId別品質スコアを表示する
- 品質チェック結果一覧を表示する
- CSVダウンロードボタンを設置する

初期版では、以下は後回しにします。

- ログイン機能
- データベース連携
- Revit API連携
- pyRevit連携
- OpenAI API連携
- Azure AI連携
- 本格的なRAG
- 自動修正機能

---

## 6. 将来的に追加する機能

今後の拡張候補は以下です。

- CSVアップロード機能
- 品質チェックの画面実行
- 特徴量データセット表示
- 修正優先度分類結果の表示
- 生成AI向け構造化コンテキスト表示
- RuleIdごとの修正ガイド表示
- QualityScoreの低い要素の強調表示
- フィルタ機能の強化
- グラフ表示の改善

---

## 7. app/streamlit_app.py の想定構成

7月に作成するStreamlitファイルは、以下を想定します。

- `app/streamlit_app.py`

想定する処理構成：

1. ライブラリ読み込み
2. ファイルパス設定
3. CSV読み込み関数
4. タイトル表示
5. 品質メトリクス表示
6. RuleId別集計表示
7. Category別集計表示
8. ElementId別品質スコア表示
9. 品質チェック結果一覧表示
10. CSVダウンロードボタン

---

## 8. 面接・ポートフォリオでの説明文

Streamlit画面については、以下のように説明する。

> Pythonで出力したBIM品質チェック結果、品質メトリクス、ElementId別品質スコアをStreamlitで簡易可視化しました。  
> 目的は、本格的な業務アプリを作ることではなく、Revit/BIMデータをPythonで処理し、品質チェック、分析、特徴量設計へ接続する流れを画面上で説明しやすくすることです。

---

## 9. 現時点の判断

Streamlitは、7月時点の応募可能MVPにおいて重要な見せ方の要素です。

ただし、主役はStreamlit画面そのものではなく、PythonによるBIMデータ処理、品質チェック、品質メトリクス、特徴量設計です。

そのため、初期版では画面を作り込みすぎず、品質チェック結果とメトリクスを確認できる簡易UIとして実装します。

---

## 10. まとめ

`streamlit_app_design.md` は、7月に作成するStreamlit簡易画面の設計メモです。

この資料により、Streamlit画面で何を表示するのか、どのCSVを使うのか、どこまでを初期版とするのかを整理できます。

7月MVPでは、まず固定パスからCSVを読み込み、品質チェック結果、品質メトリクス、RuleId別集計、ElementId別品質スコアを表示する簡易UIを作成します。