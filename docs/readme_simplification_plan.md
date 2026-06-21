# README Simplification Plan

## 目的

このドキュメントでは、`BIM Data Quality & AI Readiness Assessment PoC` のREADMEを短縮し、GitHub訪問者が短時間で内容を理解できる構成へ整理する方針をまとめる。

現在のREADMEは、PoC完成版として詳細情報を多く含んでいる。一方で、GitHub上で最初に読む資料としては長いため、READMEは要約・入口として整理し、詳細は `docs/`、Portfolio PDF、各Phase資料へ誘導する。

---

## 基本方針

READMEは以下の役割に絞る。

```text
このPoCが何かを短く説明する
Portfolio PDFへ誘導する
全体フロー図を見せる
主な成果を要約する
Phase 3A〜3Eの位置づけを短く説明する
主要成果物へのリンクを示す
テスト結果を示す
制約・対象外を明確にする
詳細docsへ誘導する
```

READMEにすべての詳細説明を残さない。

---

## READMEに残す内容

短縮版READMEには、以下を残す。

```text
1. タイトル
2. 1段落の概要
3. Portfolio PDFリンク
4. 全体フロー図
5. このPoCで示すこと
6. Current Results
7. Phase 3A〜3Eの要約
8. 主な出力ファイル
9. Tests
10. Tech Stack
11. Limitations / Out of Scope
12. Documentation links
13. Summary
```

---

## READMEから短くする内容

以下はREADMEから短縮し、必要に応じて `docs/` へ誘導する。

```text
各Phaseの長い詳細説明
Room Category Extensionの詳細な実装説明
pyRevit実行環境の細かい説明
RAG / Azure AI Search設計の詳細説明
FixPriority教師データ設計の詳細説明
Repository Structureの巨大なツリー
Documentation一覧の長い列挙
Future Workの詳細すぎる項目
Summaryの長文
```

---

## READMEに追加・維持する導線

README冒頭には、以下の導線を維持する。

```text
Portfolio PDF v004
全体フロー図
docs/portfolio_visual_plan.md
docs/poc_overall_flow_mermaid.md
docs/phase3_extension_mermaid.md
```

Portfolio PDFはREADMEより詳しい説明資料として位置づける。

---

## 短縮後の想定構成

短縮版READMEの構成は以下とする。

```text
# BIM Data Quality & AI Readiness Assessment PoC

## Overview
## Portfolio PDF
## Overall Flow
## What This PoC Demonstrates
## Current Results
## Phase 3 Extensions
## Main Outputs
## Tests
## Tech Stack
## Documentation
## Limitations / Out of Scope
## Summary
```

---

## 注意点

短縮時に以下は削らない。

```text
AIが設計判断・施工判断・法規判断をしないこと
Revitモデルを自動修正しないこと
最終判断はBIM担当者が行うこと
Azure AI Search / OpenAI API / Embedding / RAG UI は未実装であること
FixPriority教師データ設計はモデル作成ではないこと
実案件データ・顧客名・個人情報・社外秘情報を扱わないこと
pytest 37 passed
Portfolio PDF v004リンク
```

---

## 完了条件

README短縮版の完了条件は以下とする。

```text
READMEの冒頭でPoCの目的が分かる
Portfolio PDF v004へ移動できる
全体フロー図が残っている
Phase 3A〜3Eが短く説明されている
Current Resultsが簡潔に確認できる
Testsが37 passedになっている
制約・対象外が明確に残っている
詳細docsへの導線がある
README全体が読みやすい長さになっている
```

---

## 次の作業

1. この方針ファイルを作成する
2. 現在のREADMEを短縮版に差し替える
3. `git diff` で削りすぎていないか確認する
4. GitHub上でMermaid図とPortfolio PDFリンクを確認する
5. README短縮版をコミットする
