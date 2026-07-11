# README Review Result

## 対象

- File: `README.md`
- Review phase: Phase 3-1
- Branch: `refactor/poc1-readme-presentation`

## Current size

- Lines: 916
- Characters: 17,315

## Main findings

### 1. 冒頭の価値訴求が弱い

現行READMEは内容が正確で詳細だが、初見の閲覧者が以下を把握するまでに時間がかかる。

- 何を解決するPoCか
- どこまで実装済みか
- 技術的な見どころは何か
- どこが設計のみか

### 2. 内容の重複が多い

主に以下が重複している。

- 「このPoCでできること」と「このPoCで示すこと」
- 「できないこと」と「Limitations / Out of Scope」
- FixPriorityの説明
- GitHub Actionsとテスト結果
- 最終判断はBIM担当者が行うという説明
- Summaryと冒頭説明

### 3. Quick Startの位置が早すぎる

Quick Startは重要だが、初見の閲覧者には以下を先に見せた方がよい。

- PoC概要
- 主要成果
- 全体フロー
- Current Results
- Demo Screenshots

### 4. 開発履歴がREADME内に入りすぎている

Phase 3A〜3EやDevelopment Statusは記録として有用だが、READMEでは概要にとどめ、詳細は`docs/`へ誘導した方が読みやすい。

### 5. FixPriorityの表現整理が必要

現行データは単一クラスであり、DummyClassifierは処理経路確認用である。

分類モデルが完成しているように誤読されないよう、以下を明確にする。

- 実装済み：分類処理経路、出力生成
- 未実装：複数クラス評価、本番モデル、実務利用可能な自動判定

## Recommended structure

1. Title
2. PoC Overview
3. Key Outcomes
4. Portfolio PDF
5. Overall Workflow
6. Current Results
7. Demo Screenshots
8. Quick Start
9. Main Pipeline Runner
10. Tests and CI
11. Implemented Scope / Out of Scope
12. Tech Stack
13. Repository Structure
14. Documentation
15. Security / Public Data Policy
16. Limitations

## Target size

- 500〜650 lines
- 11,000〜14,000 characters

## Revision policy

- READMEは入口として読みやすくする
- 詳細設計・開発履歴は`docs/`へ分離する
- 実装済みと設計のみを明確に分ける
- 制約事項は必要最小限にまとめる
- 技術的な事実は維持し、誇張表現は避ける
