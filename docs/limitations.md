# Limitations

## BIM Data Quality Engineering & AI Analysis PoC

## この資料の目的

この資料は、現時点における制約、注意点、未実装範囲、今後の改善予定を整理するための資料です。

---

## 現時点の主な制約

- Revit由来データ対応は初期試作である。
- `door_schedule_converted_v001.csv` の列マッピングは仮設定である。
- `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用している。
- `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納している。
- `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納している。
- `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用している。
- `check_results_revit_v001.csv` の104件の違反は、正確な品質評価ではなく、処理フロー確認のための結果である。
- 機械学習プロトタイプは未実装である。
- 生成AI向け構造化コンテキスト生成は未実装である。
- Revit APIやpyRevitとの直接連携は未実装である。
- RevitモデルやBIMデータの自動修正は対象外である。
- 設計判断、施工判断、モデル修正の最終判断は人間が行う前提である。

---

## 今後の対応

- Revit由来CSVの列マッピングを整理する。
- 先頭の非データ行を除外する。
- Revit内部ElementId、FamilyName、TypeName、Levelを取得できるか確認する。
- `convert_revit_schedule.py` をv0.2化する。
- `check_bim_quality.py` をv0.2化する。
- `clean_bim_data.py` を実装する。
- 品質メトリクスを作成する。
- 特徴量設計を行う。
- 品質スコアを設計する。
- 修正優先度分類プロトタイプを実装する。
- Streamlitで簡易UI化する。
- 生成AI向け構造化コンテキスト生成を実装する。