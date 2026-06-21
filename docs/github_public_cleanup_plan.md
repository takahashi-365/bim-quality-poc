# GitHub Public Cleanup Plan

## 目的

このドキュメントでは、`BIM Data Quality & AI Readiness Assessment PoC` のGitHub公開ファイルを、見る側にとって分かりやすい構成に整理するための方針をまとめる。

この整理は、単にファイルを「必要 / 不要」で判断するためのものではない。
GitHubを閲覧する人が、短時間で以下を理解できるようにすることを目的とする。

```text
このPoCが何を示しているか
最初に見るべきファイルはどれか
最新版のPortfolio PDFはどれか
詳細を知りたい場合にどこを見ればよいか
古い成果物や作業途中のファイルで混乱しないか
READMEの説明とファイル構成が矛盾していないか
```

---

## 基本方針

GitHub公開ファイルの整理では、以下の観点を重視する。

```text
見る人にとって分かりやすいか
ファイル一覧を見たときに迷わないか
最新版と旧版の区別がつくか
作業途中のファイルが完成物に見えないか
READMEの説明と実際のファイル構成が一致しているか
未実装のものが実装済みに見えないか
応募・面接で説明したい内容とズレていないか
```

削除するかどうかは、最後に判断する。
まずは、見る人が混乱しやすい箇所を特定する。

---

## 見る側の想定

GitHubを見る人は、以下の順で確認する可能性が高い。

```text
README.md
Portfolio PDF
ファイル一覧
src/
docs/
tests/
サンプルCSV / JSON / Markdown
```

そのため、READMEとPortfolio PDFで説明している内容と、ファイル一覧に見えている内容が矛盾しないことが重要である。

---

## 整理の判断基準

### 1. 見せたい主役か

以下は、積極的に見てもらいたいファイル・フォルダである。

```text
README.md
07_portfolio/bim_quality_poc_portfolio_v005.pdf
07_portfolio/screenshots/
docs/poc_completion_policy.md
docs/phase3_roadmap.md
docs/rag_azure_ai_search_architecture_plan.md
docs/fixpriority_training_data_design.md
05_rag_design/
06_local_llm/
07_fixpriority_training/
pyrevit_scripts/
src/
tests/
```

これらは、PoCの目的、実装、設計、検証結果を説明する中心的な成果物として扱う。

---

### 2. 補足として残してよいか

以下は、READMEやPortfolio PDFから直接最初に見せるものではないが、深掘りしたい人には役立つ可能性がある。

```text
03_input_csv/
04_output_csv/
docs/
05_powerbi/
01_revit_model/README.md
```

これらは、サンプル入力、サンプル出力、設計メモ、補足説明として残す価値がある。

ただし、ファイル名や内容が古い場合は、最新版との関係が分かるようにする。

---

### 3. 見る側が混乱しやすいか

以下のようなファイルは、公開上の混乱要因になりやすい。

```text
旧版Portfolio PDF
旧版draftファイル
最新版と旧版が並んでいるファイル
READMEで未実装と説明しているのに実装済みに見えるファイル
正式成果物と旧実験ファイルの区別がつきにくいフォルダ
古いRule Master
古いAI Demo
古いFixPriority分類プロトタイプ出力
```

混乱しやすい場合は、以下のいずれかを検討する。

```text
削除する
READMEやdocsで位置づけを明記する
legacyフォルダへ移す
最新版だけを残す
作成元として残す理由を説明する
```

---

## 優先して確認する候補

### 1. Portfolio PDF旧版

現在READMEで案内している最新版は以下である。

```text
07_portfolio/bim_quality_poc_portfolio_v005.pdf
```

一方で、GitHub上には旧版PDFやdraftが並んでいる。

```text
07_portfolio/bim_quality_poc_portfolio_v003.pdf
07_portfolio/bim_quality_poc_portfolio_v004.pdf
07_portfolio/bim_quality_poc_portfolio_v004_draft.md
07_portfolio/bim_quality_poc_portfolio_v005.pdf
07_portfolio/bim_quality_poc_portfolio_v005_draft.md
```

見る側は、どれが最新版か迷う可能性がある。

方針候補：

```text
v005 PDFを主役にする
v005 draftはPDF作成元として残すか検討する
v003 / v004 / v004 draftは削除またはlegacy扱いを検討する
07_portfolio/README.md を作成し、最新版と旧版の位置づけを明記する
```

---

### 2. FixPriority分類プロトタイプ関連

READMEでは、Phase 3Eを「FixPriority教師データ設計」と説明しており、機械学習モデル作成や完全自動判定は未実装としている。

一方で、以下のようなファイルがある場合、見る側に「分類モデルを実装済みなのか」と誤解される可能性がある。

```text
src/train_fix_priority_model.py
04_output_csv/fix_priority_classification_report_v001.csv
04_output_csv/fix_priority_confusion_matrix_v001.csv
04_output_csv/fix_priority_predictions_v001.csv
```

方針候補：

```text
内容を確認する
旧プロトタイプとして残す必要があるか判断する
READMEの説明と矛盾しないか確認する
必要なら削除またはlegacy化する
```

---

### 3. AI Demo / Local LLM関連

正式なPhase 3A成果物は以下である。

```text
06_local_llm/
```

一方で、旧フォルダとして `06_ai_demo/` がある場合、見る側がどちらを見ればよいか迷う可能性がある。

方針候補：

```text
06_ai_demo/ の中身を確認する
READMEやdocsから参照されているか確認する
正式成果物が06_local_llmなら、06_ai_demoは削除またはlegacy化を検討する
```

---

### 4. Rule Master旧版

現在のAI Readiness評価では、主に以下を使用している。

```text
02_rule_master/bim_rule_master_v003.csv
```

一方で、旧版として以下がある。

```text
02_rule_master/bim_rule_master_v002.csv
```

方針候補：

```text
v002が現行コードやdocsから参照されているか確認する
参照がなければ削除候補とする
残す場合は旧版であることを明記する
```

---

## 確認コマンド

削除や移動の前に、まず参照状況を確認する。

### Portfolio PDF参照確認

```powershell
Select-String -Path README.md, docs/*.md -Pattern "bim_quality_poc_portfolio_v003|bim_quality_poc_portfolio_v004|bim_quality_poc_portfolio_v005"
```

### Rule Master参照確認

```powershell
Select-String -Path README.md, docs/*.md, src/*.py, tests/*.py -Pattern "bim_rule_master_v002|bim_rule_master_v003"
```

### FixPriority分類プロトタイプ参照確認

```powershell
Select-String -Path README.md, docs/*.md, src/*.py, tests/*.py -Pattern "fix_priority_classification_report|fix_priority_confusion_matrix|fix_priority_predictions|train_fix_priority_model"
```

### AI Demo / Local LLM参照確認

```powershell
Get-ChildItem 06_ai_demo -Recurse -File | Select-Object FullName
Select-String -Path README.md, docs/*.md -Pattern "06_ai_demo|06_local_llm"
```

---

## 整理時の注意

整理時には、以下に注意する。

```text
READMEからリンクされているファイルを削除しない
testsが参照しているファイルを削除しない
srcが参照しているCSVやRule Masterを削除しない
Portfolio PDFの最新版リンクを壊さない
GitHub上で見せたい成果物を消しすぎない
履歴として残したいものはGit履歴で追えるため、必ずしも現行ツリーに残さなくてよい
削除前に必ず参照確認を行う
```

---

## 完了条件

公開ファイル整理の完了条件は以下である。

```text
READMEを見れば最初に見るべきファイルが分かる
Portfolio PDFの最新版が分かる
旧版PDFやdraftで迷わない
READMEの説明とファイル構成が矛盾していない
未実装のものが実装済みに見えない
詳細資料はdocsに整理されている
GitHub上で閲覧者が混乱しにくい
```

---

## 次の作業

1. この方針メモを作成する
2. GitHubにコミットする
3. Portfolio PDF旧版の参照状況を確認する
4. FixPriority分類プロトタイプ関連の位置づけを確認する
5. 06_ai_demo / 06_local_llm の関係を確認する
6. Rule Master旧版の参照状況を確認する
7. 削除・legacy化・説明追加のどれで整理するか判断する
