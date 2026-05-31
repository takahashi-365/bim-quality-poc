# Interview Pitch 5min

## BIM Data Quality Engineering & AI Analysis PoC

## 5分説明文

個人開発として、Revit/BIMデータを対象にした「BIM Data Quality Engineering & AI Analysis PoC」を作成しました。

これまで私は、インテリア内装設計、建築CAD/BIMオペレーター、BIM導入支援、Revitコンサルティングを経験してきました。  
その中で、BIMモデルを作るだけでなく、モデル内の情報をどう標準化し、品質管理し、後工程やデータ活用につなげるかが重要だと感じていました。

BIM導入支援やRevit運用支援の現場では、パラメータ未入力、分類コード未入力、命名規則違反、属性情報のばらつきなどが発生します。  
これらは、数量集計、検索、品質確認、Power BIによる可視化、機械学習、生成AI、RAG活用にも影響します。

そこでこのPoCでは、Revit/BIM由来データをPythonで処理し、AI・機械学習・データ分析で扱いやすい構造化データへ整える流れを検証しました。

実装内容としては、まずRevitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換しています。  
その後、列順整理、空欄処理、前後スペース削除、ElementId空欄行除外、重複除外などのデータクレンジングを行っています。

次に、RuleIdベースの品質チェックを実装しました。  
初期ルールとして、R-001は必須パラメータ未入力、R-002は分類コード未入力、R-003はファミリ命名規則違反としています。  
チェック結果は、RuleId、RuleName、Severity、FixGuide付きのCSVとして出力しています。

さらに、品質チェック結果CSVから、RuleId別違反件数、Category別違反件数、ElementId別違反件数を集計し、SeverityScoreとQualityScoreを作成しました。  
QualityScoreは、100点を初期値として、違反の重大度に応じて減点するPoC用の簡易スコアです。

そのうえで、機械学習や分析に使える特徴量データセットを作成しました。  
特徴量には、違反数、未入力項目数、High違反件数、Medium違反件数、分類コード有無、命名規則判定、SeverityScore、QualityScore、FixPriorityなどを含めています。

Streamlitでは、品質メトリクス概要、RuleId別違反件数、ElementId別品質スコア、特徴量データセット、品質チェック結果一覧を確認できる簡易画面を作成しました。

このPoCで大事にしているのは、完成版のAIモデルを作ったと見せることではありません。  
現時点のFixPriorityは、実務の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。

そのため、このPoCは完成版の業務アプリではなく、BIMデータをAI・機械学習で扱うための前処理、品質評価、特徴量設計、可視化までの流れを示すものです。

今後は、scikit-learnによる修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Revit API / pyRevit連携へ拡張する予定です。  
特に生成AI活用では、自由回答させるのではなく、RuleId、違反内容、Severity、FixGuide、QualityScoreなどを含む構造化コンテキストを生成し、AIが参照する情報を制御する方向で考えています。

このPoCを通じて、BIM・建築情報・Revitデータを理解したうえで、PythonによるPoC開発、データクレンジング、品質チェック、Power BIやStreamlitによる可視化、生成AI活用設計へ接続できることを示したいと考えています。