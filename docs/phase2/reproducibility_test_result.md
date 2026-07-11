# Phase 2 Reproducibility Test Result

## Date

2026-07-11

## Purpose

既存のグローバルPython環境とは別に新しい仮想環境を作成し、
requirements.txtのみからPoC 1のテスト環境と分類処理を再現できるか確認した。

## Virtual Environment

.venv_repro

## Python

Python 3.12.10

## Python Executable

.venv_repro\Scripts\python.exe

## Installed Core Packages

- pandas 2.3.3
- pytest 9.0.3
- scikit-learn 1.8.0
- streamlit 1.52.1

## Test Result

37 passed

## FixPriority Script

`src/train_fix_priority_model.py`を実行した。

現行データはFixPriorityがHighのみの単一クラスであるため、
実際の分類性能評価は行わず、DummyClassifierを使用して
機械学習処理経路を確認した。

生成確認済みファイル：

- `fix_priority_classification_report_v001.csv`
- `fix_priority_confusion_matrix_v001.csv`
- `fix_priority_predictions_v001.csv`

Feature Importanceは、DummyClassifier使用時には生成されない。

## Conclusion

`requirements.txt`から新規仮想環境を構築し、
全37テストとFixPriority分類処理を再現できることを確認した。
