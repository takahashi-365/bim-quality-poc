# 5月成果物一覧_260524

## BIM Data Quality Engineering & AI Analysis PoC

## 位置づけ

5月までに、**BIM Data Quality Engineering & AI Analysis PoC** の土台を作成した。

当初は、BIM品質チェック、Power BI可視化、RuleId検索、生成AI向けプロンプト生成を中心とした軽めのPoCとして整理していた。

その後、方針を変更し、単なるBIM品質チェックツールではなく、以下を含む **BIMデータ品質エンジニアリング・AI分析PoC** として再整理した。

- Revit/BIMデータ処理
- データクレンジング
- RuleIdベース品質チェック
- 品質メトリクス作成
- 特徴量設計
- 修正優先度分類プロトタイプ
- 生成AI向け構造化コンテキスト生成
- Streamlitを主とした可視化・簡易UI化
- Power BIによる補助的な可視化

5月時点では、全機能を完成させることではなく、**Revit由来データをPython処理へ接続し、RuleIdベースの品質チェック結果CSVを出力できること**、さらにその結果を可視化・RuleId検索・生成AI向け説明生成へ接続できることを確認することを目的とした。

また、6月以降に本実装へ進めるため、README、リポジトリ構成、サンプルデータ、ルールマスタ、Pythonファイル構成、各種設計メモを整備した。

---

# 5月成果物一覧：処理パイプライン別整理

## A. BIM/Revitデータ準備

### 1. PoC管理フォルダ

**bim_quality_poc**

BIM Data Quality Engineering & AI Analysis PoC 全体を管理するための作業フォルダ。

目的は、Revit/BIMデータをPythonで処理し、品質チェック、品質メトリクス作成、特徴量設計、機械学習プロトタイプ、生成AI向け構造化コンテキスト生成へつなげるための一連の流れを検証すること。

5月時点では、既存の `08_python`、`06_ai_demo`、`00_docs` を残しつつ、新方針に合わせて `src` と `docs` を追加した。

---

### 2. 検証用Revitモデル

**01_revit_model/BIM_Quality_Check_Sample_Model_R2024_v001.rvt**

Autodesk日本仕様 意匠サンプルモデル Revit 2024を検証用データとして使用。

実案件データや社外秘データは使用せず、転職活動用ポートフォリオとして説明しやすい安全な検証環境としている。

面接では、以下のように説明できる。

> 実案件データや社外秘情報は使わず、Autodesk日本仕様のサンプルモデルを使って検証環境を構築しています。

---

### 3. Revit集計表書き出しテストファイル

Revitからタブ区切りテキストとして書き出し、Excelで開けることを確認済み。

作成・確認済みファイル：

- `03_input_csv/door_schedule_SD_export_test_v001.txt`
- `03_input_csv/material_schedule_export_test_v001.txt`
- `03_input_csv/room_finish_schedule_export_test_v001.txt`

確認済み集計表：

- 20 ドア 建具表 SD
- 04 材料表 作業用
- 05 部屋 仕上表

5月時点では、Revitから集計表データを書き出せることを確認した。

その後、`door_schedule_SD_export_test_v001.txt` をPython/pandasで読み込み、品質チェック用CSVへ変換する初期試作まで実施した。

---

### 4. Revit書き出しTXT読み込みテスト

**08_python/test_read_revit_txt.py**

Revitから書き出したTXTをPython/pandasで読み込めるか確認するためのテストスクリプト。

対象ファイル：

- `03_input_csv/door_schedule_SD_export_test_v001.txt`

確認結果：

- Revit書き出しTXTをPythonで読み込めることを確認
- 26行 × 33列として読み込めることを確認
- 空欄が `NaN` として表示されることを確認

このタスクにより、Revit由来データをPythonで扱う準備ができた。

---

## B. Pythonデータ処理

### 5. 入力CSV初版

**03_input_csv/sample_bim_data_v001.csv**

Python品質チェックの初期実装に使用する検証用サンプルCSV。

含まれるカテゴリ：

- Doors
- Rooms
- Walls

主な列：

- ElementId
- Category
- FamilyName
- TypeName
- Level
- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone
- SourceFile
- ModelName

R-001、R-002、R-003のチェックを検証できるように、意図的に以下のエラーを含めている。

- BIM_ClassificationCode 未入力
- BIM_ModelRole 未入力
- BIM_Zone 未入力
- FamilyName の命名規則違反

現時点では、Revitから直接書き出したデータではなく、品質チェックロジック作成用の検証CSVとして位置づけている。

---

### 6. Python品質チェックツール初期版

**08_python/check_bim_quality.py**

入力CSVとRuleIdルールマスタを読み込み、BIM品質ルールに基づいて品質チェックを行い、RuleId付きチェック結果CSVを出力するPythonスクリプト。

入力ファイル：

- `03_input_csv/sample_bim_data_v001.csv`

ルールマスタ：

- `02_rule_master/bim_rule_master_v001.csv`

出力ファイル：

- `04_output_csv/check_results_v001.csv`

実行コマンド：

```powershell
python .\08_python\check_bim_quality.py
```

実行結果：

```text
9 issues found
```

検出対象ルール：

- R-001：必須パラメータ未入力
- R-002：分類コード未入力
- R-003：ファミリ命名規則違反

初期版では、Revit APIや自動修正は行わず、CSVを読み込んで品質チェック結果を出力する構成。

この処理は、BIMデータをAI・機械学習・データ分析に利用するための前処理として位置づけている。

---

### 7. チェック結果CSV

**04_output_csv/check_results_v001.csv**

Python品質チェックツールによって出力されたチェック結果CSV。

主な出力項目：

- CheckId
- ElementId
- Category
- FamilyName
- TypeName
- Level
- ParameterName
- CurrentValue
- RuleId
- RuleName
- Severity
- Status
- FixGuide
- DetectedAt
- SourceFile
- ModelName

Excelで開けることも確認済み。

このCSVをPower BIに取り込むことで、RuleId別、Severity別、Category別などの可視化に接続している。

今後は、このチェック結果CSVを品質メトリクス作成、特徴量設計、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成へ接続する。

---

### 8. Revit集計表TXT変換スクリプト試作

**08_python/convert_revit_schedule.py**

Revit書き出しTXTを品質チェック用CSVへ変換する試作スクリプト。

入力ファイル：

- `03_input_csv/door_schedule_SD_export_test_v001.txt`

出力ファイル：

- `03_input_csv/door_schedule_converted_v001.csv`

実行結果：

- 元データ：26行 × 33列
- 変換後CSV：26行 × 10列

この段階では、必要な列だけを抽出・再構成し、品質チェック用CSVとして出力した。

列マッピングは仮設定。

今後、正式な列対応、列名標準化、不要行削除、欠損値処理を整理する予定。

---

### 9. Revit由来変換CSV

**03_input_csv/door_schedule_converted_v001.csv**

Revit書き出しTXTを、品質チェック用の列構成に変換したCSV。

主な列：

- Category
- ElementId
- FamilyName
- TypeName
- Level
- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone
- SourceFile
- ModelName

このCSVを `check_bim_quality.py` に入力し、Revit由来データでも品質チェック結果CSVを出力できるか確認した。

現時点では列マッピングが仮設定のため、正式な品質評価ではなく、Revit由来データをPython品質チェック処理へ接続できるかを確認するための初期試作として位置づける。

---

### 10. Revit由来データ品質チェック結果CSV

**04_output_csv/check_results_revit_v001.csv**

`door_schedule_converted_v001.csv` を `check_bim_quality.py` に入力し、出力したRevit由来データの品質チェック結果CSV。

実行結果：

```text
104 issues found
```

Excelで開き、以下の列が出力されていることを確認した。

- RuleId
- RuleName
- Severity
- FixGuide
- SourceFile
- DetectedAt
- ModelName

104件検出された理由は、現時点の `door_schedule_converted_v001.csv` では、以下の列が空欄になっているため。

- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone

今回の目的は、正確な品質評価ではなく、**Revit由来TXTから品質チェック結果CSVを出力する一連の処理フローが動くことを確認すること**。

この結果は、6月以降の列マッピング整理、データ辞書作成、品質ルール整理へつなげる。

---

## C. RuleId品質管理

### 11. RuleIdルールマスタ初版

**02_rule_master/bim_rule_master_v001.csv**

Python品質チェック、Power BI可視化、RuleId検索デモ、生成AI向け説明生成デモで共通利用するルールマスタ。

初期ルールは以下。

| RuleId | 内容 |
|---|---|
| R-001 | 必須パラメータ未入力 |
| R-002 | 分類コード未入力 |
| R-003 | ファミリ命名規則違反 |

新方針では、将来的に `bim_quality_rules.csv` 相当のルール定義CSVへ発展させる予定。

現時点では、`bim_quality_rules.csv` 相当のルール定義CSVとして、既存の `02_rule_master/bim_rule_master_v001.csv` を使用する。

このRuleIdルールマスタは、品質チェック結果、可視化、RuleId検索、生成AI向け構造化コンテキスト生成を接続するための共通キーとして位置づける。

---

### 12. RuleId検索デモ初期版

**06_ai_demo/ruleid_lookup_demo.py**

Power BIなどで確認したRuleIdをもとに、該当するBIM品質ルールの内容、重大度、業務影響、AI活用時の影響、修正方針を確認できるPythonデモ。

参照データ：

- `02_rule_master/bim_rule_master_v001.csv`

実行コマンド：

```powershell
python .\06_ai_demo\ruleid_lookup_demo.py
```

確認できる内容：

- RuleId
- RuleName
- Category
- Severity
- TargetField
- CheckLogic
- BusinessImpact
- AIUseImpact
- FixGuide
- Reference

R-001、R-002、R-003を入力し、それぞれ該当ルールの内容を表示できることを確認済み。

存在しないRuleIdや空欄入力時には、該当するRuleIdが見つからない旨を表示する。

`q` を入力すると終了できる。

このデモは、RuleIdを起点にBIM品質ルールを参照する仕組みとして、今後の生成AI向け構造化コンテキスト生成へ接続する。

---

## D. 可視化

### 13. Power BIダッシュボード初期版

**05_powerbi/bim_quality_dashboard_v001.pbix**

Python品質チェックツールで出力した `check_results_v001.csv` をPower BI Desktopに読み込み、BIM品質チェック結果を可視化した初期版ダッシュボード。

作成した可視化：

- 総違反件数カード
- RuleId別違反件数
- Severity別違反件数
- Category別違反件数
- 違反一覧テーブル

違反一覧テーブルに含めた主な項目：

- CheckId
- ElementId
- Category
- FamilyName
- RuleId
- RuleName
- Severity
- Status
- FixGuide

初期版では1ページ構成とし、複雑なDAXや複数ページ構成は行っていない。

新方針では、Power BIは主役ではなく、**Pythonで作成した品質チェック結果や品質メトリクスを可視化する補助要素**として位置づける。

今後の主役は、Python、pandas、RuleIdベース品質チェック、品質メトリクス、特徴量設計、Streamlit、生成AI向け構造化コンテキスト生成である。

---

### 14. 画面・資料用スクリーンショット

**07_portfolio/screenshots**

保存済みスクリーンショット：

- powerbi_dashboard_v001.png
- check_results_csv_v001.png
- ruleid_lookup_demo_v001.png
- prompt_generator_demo_v001.png
- generated_prompt_txt_v001.png

用途：

- ポートフォリオPDF用素材
- Loop進捗メモ用素材
- 面接説明用素材
- READMEやdocsの補足資料

5月時点で、PoCの画面説明に使える最低限の素材を保存済み。

今後は、Streamlit画面、Revit由来CSV変換結果、品質メトリクス、生成AI向け構造化コンテキスト生成結果のスクリーンショットを追加する。

---

## E. 生成AI連携前処理

### 15. RuleId連携型プロンプト生成デモ初期版

**06_ai_demo/ruleid_prompt_generator_demo.py**

RuleIdをキーにルールマスタから該当ルールを取得し、生成AIに渡すためのプロンプトを自動生成するPythonデモ。

参照データ：

- `02_rule_master/bim_rule_master_v001.csv`

出力先：

- `06_ai_demo/generated_prompts`

生成済みプロンプト：

- `06_ai_demo/generated_prompts/prompt_R-001_20260517_172551.txt`
- `06_ai_demo/generated_prompts/prompt_R-002_20260517_172615.txt`
- `06_ai_demo/generated_prompts/prompt_R-003_20260517_172644.txt`

プロンプトに含めた条件：

- 参照ルールに書かれている内容を優先する
- 参照元RuleIdを必ず明記する
- 資料にない内容は断定しない
- 自動修正を前提にしない
- 設計判断、施工判断、モデル修正の最終判断は人間が行う

初期版ではOpenAI APIなどを直接呼び出さず、生成AIに渡すプロンプトを生成する構成。

新方針では、この成果物を単なる「プロンプト生成デモ」としてではなく、**RuleIdベース生成AI向け構造化コンテキスト生成に発展させるための初期デモ**として位置づける。

今後は、RuleId、違反内容、重大度、修正提案、品質スコア、修正優先度などをJSONまたはMarkdown形式で構造化し、生成AIに渡す情報を制御する仕組みへ発展させる。

---

### 16. generate_ai_context.py 設計メモ

**00_docs/generate_ai_context_design_memo.md**

`src/generate_ai_context.py` の設計メモ。

目的は、BIM品質チェック結果、RuleIdルール情報、品質メトリクス、修正優先度などをもとに、生成AIへ渡すための構造化コンテキストを作成する処理を設計すること。

整理した内容：

- 目的
- PoC全体での位置づけ
- 入力データ
- 出力データ
- JSON出力の考え方
- Markdown出力の考え方
- 生成AIに渡す制約条件
- 関数構成案
- 既存プロンプト生成デモからの発展方向
- 面接・ポートフォリオでの説明文

このタスクにより、既存のRuleId連携型プロンプト生成デモを、生成AI向け構造化コンテキスト生成へ発展させる方針を整理した。

---

## F. 今後のAI・機械学習拡張

### 17. 特徴量設計構想メモ

**00_docs/create_bim_features_concept_memo.md**

BIM品質チェック結果から、機械学習や分析に使える特徴量データセットを設計するための構想メモ。

整理した特徴量候補：

- MissingFieldCount
- RuleViolationCount
- CriticalViolationCount
- WarningViolationCount
- HasClassificationCode
- FamilyNameValid
- SeverityScore
- QualityScore
- CategoryEncoded

このメモにより、7月以降の特徴量設計に向けた方向性を整理した。

---

### 18. 修正優先度分類プロトタイプ設計メモ

**00_docs/fix_priority_model_design_memo.md**

BIM品質チェック結果から作成した特徴量をもとに、修正優先度 High / Medium / Low を分類する機械学習プロトタイプの設計メモ。

整理した内容：

- プロトタイプの目的
- 入力特徴量候補
- 出力ラベル
- 仮ラベル設計
- 使用予定技術
- DecisionTreeClassifier
- RandomForestClassifier
- classification_report
- confusion_matrix
- feature_importance
- モデルの限界

このメモにより、8月以降の修正優先度分類プロトタイプ作成に向けた方向性を整理した。

なお、実装時はRandomForestClassifierを中心に進め、DecisionTreeClassifierなどの比較は余力があれば行う。

---

### 19. clean_bim_data.py 設計メモ

**00_docs/clean_bim_data_design_memo.md**

`src/clean_bim_data.py` の設計メモ。

目的は、Revit/BIM由来データを品質チェックや特徴量設計に使いやすい形へ整えるための前処理スクリプトとして設計すること。

整理した内容：

- 目的
- PoC全体での位置づけ
- 入力データ
- 出力データ
- 主な処理内容
- 関数構成案
- 現時点の注意点
- 5月時点のゴール
- 面接・ポートフォリオでの説明文

このタスクにより、データクレンジング、列名標準化、欠損値処理の位置づけを明確にした。

---

### 20. calculate_quality_metrics.py 設計メモ

**00_docs/calculate_quality_metrics_design_memo.md**

`src/calculate_quality_metrics.py` の設計メモ。

目的は、BIM品質チェック結果CSVをもとに、分析・可視化・特徴量設計に使いやすい品質メトリクスへ変換する処理を設計すること。

整理した内容：

- 目的
- PoC全体での位置づけ
- 入力データ
- 出力データ
- 全体メトリクス
- RuleId別メトリクス
- Category別メトリクス
- Severity別メトリクス
- ElementId別メトリクス
- 品質スコアの仮方針
- 関数構成案
- 面接・ポートフォリオでの説明文

このタスクにより、違反一覧CSVを品質メトリクスや特徴量設計へ接続する考え方を整理した。

---

## G. ポートフォリオ・設計資料

### 21. README

**README.md**

PoC全体の説明ファイル。

現在のPoC名：

**BIM Data Quality Engineering & AI Analysis PoC**

READMEには以下を整理した。

- PoC概要
- 目的
- このPoCで示したいこと
- 現時点の入力データ
- 使用データ
- 対象カテゴリ
- RuleIdルールマスタ
- Revit集計表書き出し確認
- Python実行環境
- requirements.txt
- Python品質チェックツール初期版
- Revit由来データ対応初期版
- Power BIダッシュボード初期版
- RuleId検索デモ
- RuleId連携型プロンプト生成デモ
- 5月成果物一覧
- 進捗評価
- 今後の拡張予定
- ポートフォリオでの説明文

5月後半に、README冒頭を新方針に合わせて修正した。

旧方針では「BIM Data Quality Check & AI Analysis PoC」だったが、新方針では「BIM Data Quality Engineering & AI Analysis PoC」とし、単なる品質チェックではなく、BIMデータをAI・機械学習で扱うためのデータ処理パイプラインとして整理した。

---

### 22. ポートフォリオPDF骨子メモ

**07_portfolio/portfolio_outline_v001.md**

今後、転職用ポートフォリオPDFへ展開するための骨子メモ。

今後の用途：

- PoC全体像の説明
- 解決したい業務課題の整理
- Python品質チェックツールの説明
- Power BIダッシュボードの説明
- RuleId連携型プロンプト生成デモの説明
- ダイスネクストAIエンジニア求人向けの自己PR整理

5月後半の方針変更により、今後は `docs/portfolio_summary.md` とあわせて、ポートフォリオ用説明資料として整理していく。

今後のポートフォリオでは、Power BIを主役にしすぎず、PythonによるBIMデータ処理、RuleIdベース品質チェック、特徴量設計、生成AI向け構造化コンテキスト生成を中心に説明する。

---

### 23. Pythonコード説明メモ

**00_docs/python_code_explanation_memo.md**

既存Pythonコードの目的、処理フロー、主要関数の役割を日本語で整理したメモ。

対象ファイル：

- `08_python/check_bim_quality.py`
- `06_ai_demo/ruleid_lookup_demo.py`
- `06_ai_demo/ruleid_prompt_generator_demo.py`

目的は、作成したPythonコードを自分の言葉で説明できる状態にすること。

5月時点では、既存コード理解タスクとして完了。

---

### 24. src配下のPython空ファイル

**src**

作成済みファイル：

- `src/convert_revit_schedule.py`
- `src/clean_bim_data.py`
- `src/check_bim_quality.py`
- `src/calculate_quality_metrics.py`
- `src/create_bim_features.py`
- `src/train_fix_priority_model.py`
- `src/generate_ai_context.py`
- `src/utils.py`

これらは、今後の本実装用Pythonファイル。

現時点では中身は空でよい。

5月時点では、重めPoCとして必要な処理工程の構成を明確にするために作成した。

今後、既存の `08_python` や `06_ai_demo` の試作コードを整理し、`src` 配下へ移行・発展させる。

---

### 25. system_overview.md

**docs/system_overview.md**

PoC全体のシステム構成、処理フロー、各Pythonファイルの役割を整理した資料。

整理した内容：

- この資料の目的
- PoC全体の目的
- 全体処理フロー
- 現時点で確認済みの処理フロー
- 入力データ
- ルール定義
- 出力データ
- src配下の予定ファイル
- 既存実装ファイル
- Power BI / Streamlitの位置づけ
- 現時点の注意点
- 今後の拡張方針
- 5月時点の到達点

READMEよりもシステム構成に寄せた説明資料として作成。

今後は、Power BIを補助的な可視化要素、Streamlitを主UI候補として整理し直す。

---

### 26. portfolio_summary.md

**docs/portfolio_summary.md**

5月成果をポートフォリオ用に1ページでまとめた要約資料。

整理した内容：

- PoC概要
- 背景
- 現時点で実装・確認済みの内容
- 主な成果物
- 処理フロー
- 使用技術
- 今後の拡張予定
- 現時点の位置づけ
- ポートフォリオで伝えたいこと
- 面接での説明用メモ

5月成果1ページまとめの代替として作成。

今後は、特徴量設計、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成という表現に統一する。

---

### 27. requirements.txt

**requirements.txt**

Python品質チェックツールの実行に必要な外部ライブラリを明示するためのファイル。

配置場所：

- `bim_quality_poc` の直下

現時点の記載内容：

```text
pandas==3.0.3
```

目的は、別環境でもPoCを再現しやすくすること。

`pandas==3.0.3` は確認済みのため、このまま使用する。

今後、scikit-learn、streamlit などを使う段階で追記予定。

---

# 5月までに説明できること

5月までの成果物をもとに、以下のように説明できる。

Autodesk日本仕様のRevitサンプルモデルを検証用データとして準備し、既存集計表からドア・部屋・材料のデータをTXT形式で書き出せることを確認した。

そのうえで、BIM品質チェック用のRuleIdルールマスタを作成し、検証用サンプルCSVに対してPythonで必須パラメータ未入力、分類コード未入力、ファミリ命名規則違反を検出する初期版ツールを作成した。

チェック結果はCSVとして出力し、Power BIで総違反件数、RuleId別、重大度別、カテゴリ別に可視化する1ページダッシュボードを作成した。なお、Power BIは主役ではなく、Pythonで出力した品質チェック結果を確認するための補助的な可視化手段として位置づけている。

さらに、Power BIなどで確認したRuleIdを起点に、該当ルールの内容、重大度、業務影響、AI活用時の影響、修正方針を確認できるRuleId検索デモを作成した。

加えて、RuleIdをキーに該当ルールだけを取得し、生成AIに渡すためのプロンプトを自動生成するデモを作成した。このデモは、今後のRuleIdベース生成AI向け構造化コンテキスト生成に発展させるための前段階として位置づけている。

その後、Revit書き出しTXTをPython/pandasで読み込み、品質チェック用CSVへ変換し、そのCSVを既存の品質チェックツールに入力して、RuleId付き品質チェック結果CSVを出力できる初期試作まで確認した。

5月後半では方針を変更し、PoCを **BIM Data Quality Engineering & AI Analysis PoC** として再整理した。

README、src配下のPythonファイル構成、docs/system_overview.md、docs/portfolio_summary.md、各種設計メモを作成し、Revit/BIMデータをPythonで処理し、品質チェック、品質メトリクス作成、特徴量設計、機械学習プロトタイプ、生成AI向け構造化コンテキスト生成へ拡張できる土台を整えた。

---

# 5月残タスク

以下は、5月中に追加で対応する残タスクとする。

## 1. Revit由来CSVの列マッピング整理

対象ファイル：

- `03_input_csv/door_schedule_SD_export_test_v001.txt`
- `03_input_csv/door_schedule_converted_v001.csv`
- `04_output_csv/check_results_revit_v001.csv`
- `08_python/convert_revit_schedule.py`

確認する主な列：

- ElementId
- Category
- FamilyName
- TypeName
- Level
- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone
- SourceFile
- ModelName

現時点では、`door_schedule_converted_v001.csv` の列マッピングは仮設定。

この列マッピングを確認し、6月以降の正式なデータクレンジング、品質チェック、特徴量設計へつなげる。

---

## 2. data_dictionary.md の作成

作成予定ファイル：

- `docs/data_dictionary.md`

目的：

Revit由来CSV、品質チェック用CSV、チェック結果CSVで使用する列の意味を整理する。

定義する主な項目：

- ElementId
- Category
- FamilyName
- TypeName
- Level
- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone
- SourceFile
- ModelName
- RuleId
- Severity
- FixGuide
- DetectedAt

この資料により、PoCが単なるCSV処理ではなく、BIMデータをAI・機械学習で扱うためのデータ設計を行っていることを示す。

---

## 3. rule_specification.md の作成

作成予定ファイル：

- `docs/rule_specification.md`

目的：

RuleIdルールマスタの仕様を整理する。

整理する項目：

- RuleId命名規則
- RuleName
- TargetField
- CheckLogic
- Severity
- BusinessImpact
- AIUseImpact
- FixGuide
- Reference

この資料により、RuleIdを中心に品質チェック、可視化、生成AI向け構造化コンテキスト生成を接続する設計を明確にする。

---

## 4. limitations.md の作成

作成予定ファイル：

- `docs/limitations.md`

目的：

5月時点のPoCの限界と注意点を明記する。

記載する内容：

- Revit由来データ対応は初期試作である
- `door_schedule_converted_v001.csv` の列マッピングは仮設定である
- `check_results_revit_v001.csv` の104件の違反は、現時点では正確な品質評価ではなく処理フロー確認である
- BIM_ClassificationCode、BIM_ModelRole、BIM_Zone が空欄のため未入力違反が多く出ている
- 機械学習プロトタイプは未実装である
- 実務適用には修正履歴、手戻り時間、担当者判断、プロジェクト条件、修正工数などの教師データが必要である

この資料により、PoCの限界を理解したうえで開発していることを示す。

---

## 5. business_requirements_mapping.md の作成

作成予定ファイル：

- `docs/business_requirements_mapping.md`

目的：

実務課題とPoCでの対応関係を整理する。

記載例：

| 実務課題 | PoCでの対応 | 使用技術 |
|---|---|---|
| BIM属性未入力が多い | 必須項目チェック | pandas, rules CSV |
| 命名規則が守られない | 正規表現チェック | Python |
| BIMデータをAIに使えない | データクレンジング | pandas |
| 修正優先度が属人的 | 修正優先度分類プロトタイプ | scikit-learn |
| AI回答の根拠が曖昧 | RuleId付き構造化コンテキスト | JSON / Markdown |
| 開発部門に要件を伝えにくい | ルール定義・設計ドキュメント化 | docs |

この資料により、単なるコードではなく、BIM実務課題を技術に落とし込めることを示す。

---

## 6. evaluation_policy.md の作成

作成予定ファイル：

- `docs/evaluation_policy.md`

目的：

今後作成する修正優先度分類プロトタイプの評価方針を整理する。

記載する内容：

- 本PoCの評価対象
- モデル精度を主目的にしない理由
- 仮ラベルの限界
- 実務適用に必要な教師データ
- 今後取得すべきデータ
- classification_report、混同行列、特徴量重要度の位置づけ

この資料により、機械学習を過大に見せず、実務適用条件を理解していることを示す。

---

## 7. tests/test_quality_rules.py の作成

作成予定ファイル：

- `tests/test_quality_rules.py`

目的：

RuleIdベース品質チェックの基本動作を確認するための最小テストを作成する。

テスト内容：

- 必須項目未入力を検出できるか
- 分類コード未入力を検出できるか
- ファミリ命名規則違反を検出できるか
- Severityが想定どおりに扱われるか
- RuleIdが正しく付与されるか

このテストにより、PoCを単なる学習メモではなく、開発成果物として見せやすくする。

---

# 5月時点の最終評価

5月時点では、BIM Data Quality Engineering & AI Analysis PoC の土台作りとして十分な成果がある。

特に、以下を確認できた点が大きい。

- Revitサンプルモデルを使った安全な検証環境
- Revit集計表TXTの書き出し
- Revit書き出しTXTのPython/pandas読み込み
- 品質チェック用CSVへの変換
- RuleIdベース品質チェック
- チェック結果CSV出力
- Power BIによる補助的可視化
- RuleId検索デモ
- 生成AI向け構造化コンテキスト生成へ発展可能な初期デモ
- 特徴量設計・修正優先度分類プロトタイプへ進むための設計メモ
- README、system_overview、portfolio_summaryによるポートフォリオ化の土台

5月の成果物は、単なるBIMチェックツールではなく、**BIMデータをAI・機械学習で扱うためのデータ品質エンジニアリングPoCの初期版**として整理できている。

今後は、5月残タスクを整理したうえで、6月以降に本実装へ進める。

---

# 進捗評価

## 総合評価

5月時点の進捗は、当初想定していた「軽めのBIM品質チェックPoC」を超えており、**BIM Data Quality Engineering & AI Analysis PoC の初期土台としては十分に進んでいる**。

特に、単なるサンプルCSVの品質チェックだけでなく、Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換し、そのCSVを既存の品質チェックツールに入力してRuleId付きチェック結果CSVを出力できた点は大きい。

5月時点では、PoCの全機能を完成させることではなく、以下を確認できたことが重要である。

- Revit由来データをPythonで読み込めること
- Revit由来TXTを品質チェック用CSVへ変換できること
- RuleIdベースの品質チェック結果CSVを出力できること
- Power BIで品質チェック結果を補助的に可視化できること
- RuleIdを起点にルール情報を検索できること
- RuleIdを起点に生成AI向け説明生成の前段階を作れること
- 今後の特徴量設計、品質メトリクス作成、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成へ拡張できる土台を作れたこと

したがって、5月成果物は、単なる学習記録ではなく、**BIMデータをAI・機械学習で扱うためのデータ品質エンジニアリングPoCの初期版**として評価できる。

---

## 良かった点

### 1. Revit由来データをPython処理へ接続できた

5月時点で最も大きな成果は、Revitから書き出した集計表TXTをPython/pandasで読み込み、品質チェック用CSVへ変換し、既存の品質チェックツールに入力できたことである。

これにより、単なる手作成CSVの検証ではなく、Revit由来データをPython処理パイプラインに接続する初期フローを確認できた。

現時点の処理フローは以下である。

```text
Revit書き出しTXT
↓
convert_revit_schedule.py で品質チェック用CSVへ変換
↓
door_schedule_converted_v001.csv
↓
check_bim_quality.py で品質チェック
↓
check_results_revit_v001.csv を出力
```

この流れが確認できたことで、6月以降のデータクレンジング、列マッピング整理、品質メトリクス作成、特徴量設計へ進むための土台ができた。

---

### 2. RuleIdを共通キーにした設計ができている

RuleIdルールマスタを中心に、以下の処理を接続できている点は良い。

- Python品質チェック
- チェック結果CSV出力
- Power BIによる補助的可視化
- RuleId検索デモ
- RuleId連携型プロンプト生成デモ
- 今後の生成AI向け構造化コンテキスト生成

特に、RuleIdを単なるエラー番号として使うのではなく、ルール内容、重大度、業務影響、AI活用時の影響、修正方針と接続している点が重要である。

これにより、品質チェック結果を単なる一覧表で終わらせず、**AIに渡すための根拠付き構造化情報**へ発展させる方向性が見えている。

---

### 3. 実案件データを使わない安全な検証環境を作れている

Autodesk日本仕様 意匠サンプルモデル Revit 2024を検証用データとして使用し、実案件データや社外秘データを使わない方針を明確にできている。

これは転職用ポートフォリオとして重要である。

面接や職務経歴書で説明する際にも、情報管理・機密保持の観点で安心感がある。

説明例：

> 実案件データや社外秘情報は使わず、Autodesk日本仕様のサンプルモデルを使って検証環境を構築しています。

---

### 4. 軽めPoCから重めPoCへ再整理できた

当初は、BIM品質チェック、Power BI可視化、RuleId検索、生成AI向けプロンプト生成を中心とした軽めのPoCだった。

しかし、5月後半に方針を見直し、以下を含む重めのPoCとして再整理できた。

- Revit/BIMデータ処理
- データクレンジング
- RuleIdベース品質チェック
- 品質メトリクス作成
- 特徴量設計
- 修正優先度分類プロトタイプ
- 生成AI向け構造化コンテキスト生成
- Streamlitを主とした簡易UI化
- Power BIによる補助的可視化

この再整理により、PoCの見せ方が「BIMチェックツール」から、**BIMデータをAI・機械学習で扱うためのデータ処理パイプライン**へ変わった。

これは、ダイスネクストのAI・機械学習エンジニア求人に向けた見せ方として、より強い。

---

### 5. ポートフォリオ化に向けた説明資料も作成できている

READMEだけでなく、以下の資料を作成できている点も良い。

- `docs/system_overview.md`
- `docs/portfolio_summary.md`
- `00_docs/python_code_explanation_memo.md`
- `00_docs/create_bim_features_concept_memo.md`
- `00_docs/fix_priority_model_design_memo.md`
- `00_docs/clean_bim_data_design_memo.md`
- `00_docs/calculate_quality_metrics_design_memo.md`
- `00_docs/generate_ai_context_design_memo.md`

単にコードを書くだけでなく、目的、処理フロー、今後の拡張、面接での説明文まで整理できている。

これは、BIM導入支援経験を持つ人材として、業務課題を整理し、技術仕様に落とし込めることを示す材料になる。

---

## 注意点

### 1. Revit由来CSVの列マッピングはまだ仮設定

`door_schedule_converted_v001.csv` の列マッピングは現時点では仮設定である。

そのため、`check_results_revit_v001.csv` で出力された104件の違反は、正確な品質評価ではなく、処理フロー確認の結果として扱う必要がある。

特に、以下の列が空欄になっているため、未入力違反が多く検出されている。

- BIM_ClassificationCode
- BIM_ModelRole
- BIM_Zone

この点は、READMEや `limitations.md` で明記する必要がある。

---

### 2. Power BIを主役にしすぎない

Power BIダッシュボード初期版は成果物として有効である。

ただし、今回の主目的はBIレポート作成ではなく、BIMデータをAI・機械学習で扱うためのデータ処理パイプラインを作ることである。

そのため、Power BIは以下の位置づけにする。

> Pythonで出力した品質チェック結果や品質メトリクスを確認するための補助的な可視化手段。

今後の主役は以下である。

- Python
- pandas
- RuleIdベース品質チェック
- 品質メトリクス作成
- 特徴量設計
- Streamlit
- 修正優先度分類プロトタイプ
- 生成AI向け構造化コンテキスト生成

---

### 3. 「プロンプト生成」は構造化コンテキスト生成の前段階として扱う

`ruleid_prompt_generator_demo.py` は成果物として有効である。

ただし、「プロンプト生成デモ」という表現だけだと、少し軽く見える可能性がある。

今後は以下のように位置づける。

> RuleIdベース生成AI向け構造化コンテキスト生成に発展させるための初期デモ。

この表現にすることで、単なるプロンプト作成ではなく、RuleId、違反内容、重大度、修正提案、品質スコア、修正優先度などを構造化し、生成AIに渡す情報を制御する設計へ発展できる。

---

### 4. 「分類モデル」ではなく「分類プロトタイプ」として表現する

現時点では、修正優先度分類はまだ設計メモ段階であり、実務の正解ラベルも存在しない。

そのため、今後も以下の表現を使う。

- 修正優先度分類プロトタイプ
- 機械学習プロトタイプ
- 分類・評価・特徴量重要度確認の流れを検証するプロトタイプ

「予測モデルを完成させた」とは言わず、BIM品質チェック結果を機械学習用データセットへ変換し、分類プロトタイプへ接続する流れを示すことを重視する。

---

## 現時点の弱点

5月時点の弱点は以下である。

- Revit由来CSVの列マッピングが仮設定である
- Revit由来データの品質評価はまだ正確性より処理フロー確認が中心である
- `src` 配下の本実装ファイルはまだ空ファイルが多い
- `08_python`、`06_ai_demo`、`src` の役割整理が今後必要である
- `data_dictionary.md` が未作成である
- `rule_specification.md` が未作成である
- `limitations.md` が未作成である
- `business_requirements_mapping.md` が未作成である
- `evaluation_policy.md` が未作成である
- `tests/test_quality_rules.py` が未作成である
- Streamlitは未実装である
- 品質メトリクス作成は未実装である
- 特徴量設計は構想段階である
- 修正優先度分類プロトタイプは設計段階である
- 生成AI向け構造化コンテキスト生成は設計段階である

ただし、これらは5月時点では問題ではない。

5月の目的は、全機能を完成させることではなく、PoCとして成立する土台を作ることである。  
その意味では、現時点の弱点は、6月以降の開発テーマとして整理できている。

---

## 5月時点の到達点

5月時点では、以下の状態まで到達している。

- Revitサンプルモデルを使った安全な検証環境を準備した
- Revit集計表TXTを書き出せることを確認した
- Revit書き出しTXTをPython/pandasで読み込めることを確認した
- Revit書き出しTXTを品質チェック用CSVへ変換できることを確認した
- 検証用サンプルCSVに対してRuleIdベース品質チェックを実行できた
- Revit由来CSVに対してもRuleIdベース品質チェック結果CSVを出力できた
- Power BIで品質チェック結果を補助的に可視化できた
- RuleId検索デモを作成した
- RuleId連携型プロンプト生成デモを作成した
- 生成AI向け構造化コンテキスト生成へ発展させる方向性を整理した
- 特徴量設計に向けた構想メモを作成した
- 修正優先度分類プロトタイプに向けた設計メモを作成した
- 品質メトリクス作成、データクレンジング、生成AI向け構造化コンテキスト生成の設計メモを作成した
- README、system_overview、portfolio_summaryを作成した
- `src` 配下に今後の本実装用ファイル構成を作成した

---

## 5月時点の評価

5月時点の評価は、**A-** とする。

理由は以下である。

### 評価できる点

- 5月時点としては成果物の量が十分である
- 手作成CSVだけでなく、Revit由来TXTの読み込み・変換まで進んでいる
- RuleIdを共通キーにした設計ができている
- Python、Power BI、RuleId検索、生成AI向け説明生成の前段階まで接続できている
- 実案件データを使わない安全な検証環境がある
- 5月後半でPoCの方向性を重めのAI・データ分析向けPoCへ再整理できている
- 6月以降の開発に必要な設計メモが揃っている

### 減点理由

- Revit由来CSVの列マッピングが仮設定である
- `src` 配下への本実装移行はまだこれからである
- 品質メトリクス、特徴量設計、Streamlit、機械学習プロトタイプ、生成AI向け構造化コンテキスト生成は未実装である
- README、system_overview、portfolio_summaryの表現統一がまだ必要である

総合すると、5月時点では十分合格であり、作り直しは不要である。

今後は、5月の試作を整理し、Revit由来データを扱える本実装の土台へ整えていく。

---

## 今後の優先順位

5月成果を踏まえ、次に優先すべきことは以下である。

1. Revit由来CSVの列マッピング整理
2. `08_python`、`06_ai_demo`、`src` の役割整理
3. `README`、`system_overview.md`、`portfolio_summary.md` の表現統一
4. `data_dictionary.md` の作成
5. `rule_specification.md` の作成
6. `limitations.md` の作成
7. `business_requirements_mapping.md` の作成
8. `evaluation_policy.md` の作成
9. `tests/test_quality_rules.py` の作成
10. `08_python` と `06_ai_demo` の試作コードを `src` 配下へ段階的に移行する

---

## 5月時点の結論

5月成果物は、このまま進めて問題ない。

ただし、現時点の成果物は完成版ではなく、**BIM Data Quality Engineering & AI Analysis PoC の初期土台**である。

5月で確認できたことは、以下である。

> Revit由来データをPythonで読み込み、品質チェック用CSVへ変換し、RuleIdベースの品質チェック結果CSVを出力できる。さらに、その結果を補助的に可視化し、RuleId検索や生成AI向け説明生成の前段階へ接続できる。

今後は、これをもとに、列マッピング、データ辞書、ルール仕様、品質メトリクス、特徴量設計、Streamlit、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成へ発展させる。

5月時点では、作り直しではなく、**良い初期PoCを本実装・ポートフォリオ向けに整える段階**である。