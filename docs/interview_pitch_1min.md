# Interview Pitch 1min

## BIM Data Quality Engineering & AI Analysis PoC

## 1分説明文

個人開発として、Revit/BIMデータを対象にした「BIM Data Quality Engineering & AI Analysis PoC」を作成しました。

このPoCでは、Revitから書き出した集計表TXTをPythonで読み込み、品質チェック用CSVに変換しています。  
その後、データクレンジング、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlitによる簡易可視化まで実装しました。

目的は、BIMデータを単なる図面やモデル情報として扱うのではなく、AI・機械学習・データ分析で扱いやすい構造化データに整えることです。

現時点では完成版の業務アプリではなく、応募・面接で説明できるPoC段階です。  
今後は、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Revit API / pyRevit連携へ拡張する予定です。