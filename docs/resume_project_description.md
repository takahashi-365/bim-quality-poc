# Resume Project Description

## BIM Data Quality Engineering & AI Analysis PoC

## 職務経歴書向け記載案

### 個人開発 / BIM Data Quality Engineering & AI Analysis PoC

BIM導入支援・Revitコンサルティングの実務経験をもとに、Revit/BIMデータをAI・機械学習・データ分析で扱うための個人PoCを作成。

Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換。データクレンジング、RuleIdベースの品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlitによる簡易可視化までを実装。

BIMデータ内の必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反をRuleId付きで検出し、RuleName、Severity、FixGuide付きのチェック結果CSVとして出力。さらに、RuleId別・Category別・ElementId別の集計、SeverityScore、QualityScore、FixPriority仮ラベルを作成し、分析・機械学習に利用しやすいデータ構造へ変換。

Streamlit簡易画面では、品質メトリクス概要、RuleId別違反件数、ElementId別品質スコア、特徴量データセット、品質チェック結果一覧を表示。応募・面接で説明可能なMVPとして、README、ポートフォリオPDF、説明資料、テスト、制約整理も作成。

現時点では、QualityScoreおよびFixPriorityはPoC用の簡易指標・仮ラベルとして位置づけ、実務適用には修正履歴・修正工数・担当者判断などの教師データが必要であることを明記。今後は、scikit-learnによる修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成、Revit API / pyRevit連携へ拡張予定。

## 使用技術

- Python
- pandas
- Streamlit
- pytest
- CSV / TXT
- Revit Schedule Export
- Power BI
- Markdown
- RuleId-based Quality Check

## 実装内容

- Revit書き出しTXTのPython/pandas読み込み
- 品質チェック用CSVへの変換
- データクレンジング
- RuleIdベース品質チェック
- 品質チェック結果CSV出力
- 品質メトリクス作成
- RuleId別・Category別・ElementId別集計
- SeverityScore / QualityScore算出
- 特徴量データセット作成
- FixPriority仮ラベル作成
- Streamlit簡易画面作成
- pytestによる最小テスト
- README / ポートフォリオPDF / 説明資料作成

## 成果物

- `README.md`
- `docs/portfolio_summary.md`
- `docs/july_mvp_summary_260731.md`
- `07_portfolio/bim_quality_poc_portfolio_v002.pdf`
- `docs/interview_pitch_1min.md`
- `docs/interview_pitch_3min.md`
- `docs/interview_pitch_5min.md`
- `app/streamlit_app.py`
- `src/clean_bim_data.py`
- `src/calculate_quality_metrics.py`
- `src/create_bim_features.py`
- `08_python/convert_revit_schedule.py`
- `08_python/check_bim_quality.py`
- `tests/test_quality_rules.py`

## 職務経歴書に短く書く場合

BIM導入支援・Revitコンサルティングの経験をもとに、Revit/BIMデータを対象としたPython PoCを個人開発。Revit集計表TXTの読み込み、品質チェック用CSVへの変換、データクレンジング、RuleIdベース品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易可視化までを実装。BIMデータをAI・機械学習・データ分析で扱うための前処理パイプラインとして構築。

## 職務経歴書にさらに短く書く場合

個人開発として、Revit/BIMデータを対象にしたPython PoCを作成。データクレンジング、RuleIdベース品質チェック、品質メトリクス作成、特徴量データセット作成、Streamlit簡易可視化まで実装。