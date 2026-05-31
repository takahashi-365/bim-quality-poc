# Interview Pitch 3min

## BIM Data Quality Engineering & AI Analysis PoC

## 3分説明文

個人開発として、Revit/BIMデータを対象にした「BIM Data Quality Engineering & AI Analysis PoC」を作成しました。

背景として、BIM導入支援やRevit運用支援の現場では、パラメータ未入力、分類コード未入力、命名規則違反、属性情報のばらつきなどが課題になります。  
これらがあると、集計、検索、品質確認、AI活用の精度が下がります。

このPoCでは、その課題に対して、Revit/BIM由来データをPythonで処理し、品質チェック、品質メトリクス作成、特徴量データセット作成、簡易可視化までをつなげる流れを実装しました。

具体的には、Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換しています。  
その後、データクレンジングを行い、RuleIdベースで、必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反を検出します。

チェック結果はCSVとして出力し、RuleId、RuleName、Severity、FixGuideを持つ形に整理しています。  
さらに、RuleId別、Category別、ElementId別の集計を作成し、SeverityScore、QualityScore、FixPriority仮ラベルを作成しました。

Streamlitでは、品質メトリクス概要、RuleId別違反件数、ElementId別品質スコア、特徴量データセット、品質チェック結果一覧を確認できる簡易画面を作成しています。

このPoCで重視しているのは、AIモデルの精度を高く見せることではありません。  
BIMデータを、AI・機械学習・データ分析で扱える状態に整える前処理と設計を重視しています。

現時点では、QualityScoreやFixPriorityはPoC用の簡易指標・仮ラベルです。  
今後は、実際の修正履歴や修正工数などの教師データを使い、修正優先度分類や生成AI向け構造化コンテキスト生成へ拡張したいと考えています。