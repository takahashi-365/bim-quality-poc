# Revit API / pyRevit Integration Plan

## BIM Data Quality Engineering & AI Analysis PoC

## この資料の目的

この資料は、現在のBIM Data Quality Engineering & AI Analysis PoCを、将来的にRevit APIまたはpyRevitと連携させるための検討メモです。

現時点では、Revit API / pyRevit連携は未実装です。

本PoCでは、Revitから書き出した集計表TXTを入力データとして使用し、Python/pandasで品質チェック、品質メトリクス作成、特徴量データセット作成、修正優先度分類プロトタイプ、生成AI向け構造化コンテキスト生成までを検証しています。

今後の拡張として、Revitモデルから直接データを取得し、品質チェック処理へ接続することを検討します。

---

## 1. 現在のPoCの入力方式

現在のPoCでは、Revitから書き出した集計表TXTを入力データとしています。

現在の流れ：

```text
Revit集計表
↓
TXT書き出し
↓
Python/pandasで読み込み
↓
品質チェック用CSVへ変換
↓
データクレンジング
↓
RuleIdベース品質チェック
↓
品質メトリクス作成
↓
特徴量データセット作成
↓
修正優先度分類プロトタイプ
↓
生成AI向け構造化コンテキスト生成
↓
Streamlit簡易画面で確認