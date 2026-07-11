# PoC 1 Reliability Refactoring Plan

## 1. 目的

PoC 1へ新機能を追加する前に、コード、テスト、実行方法、ドキュメントの整合性を改善する。

特に、以下を重視する。

* テストが本番コードを直接検証すること
* 空または未使用の本番ファイルを残さないこと
* 過去の試作コードと現在の正式実装を区別すること
* PoC独自のスコアや仮ラベルを過大評価しないこと
* GitHub閲覧者が、実装済み・試作・未実装を判断できること

---

## 2. フェーズ構成

### Phase 0：現状確認とバックアップ

リファクタリング前のコード、ファイル構成、テスト結果、Git状態を記録する。

### Phase 1：本番コードとテストの接続

品質チェックおよびAI Readinessのテストを、本番コードへ直接接続する。

あわせて、未使用の空ファイルを削除し、主要ドキュメントを現在の実装へ合わせる。

### Phase 2：実行再現性とCI

一括実行、仮想環境、依存関係、GitHub Actionsなどを整備する。

### Phase 3：説明・評価設計の改善

README、FixPriority、AI Readiness Score、制約説明を全体的に見直す。

---

## 3. 修正対象一覧

| ID   | フェーズ    | 対象                                 | 修正前の問題                                | 対応内容                                                                                          | 確認方法                 | 状態   |
| ---- | ------- | ---------------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------- | -------------------- | ---- |
| R-01 | Phase 1 | `src/check_bim_quality.py`         | 0バイトだが、複数資料で品質チェック本番ファイルとして説明されていた    | `08_python`配下の試作コードを確認し、本番関数として`src`へ整理。Rule Master v003を参照する構成へ修正                            | 本番実行、pytest、コード確認    | 完了   |
| R-02 | Phase 1 | `src/convert_revit_schedule.py`    | 0バイト。本番実装は存在せず、過去の試作は`08_python`配下に存在 | 空ファイルを削除し、現在の正式パイプライン対象外として整理                                                                 | 削除、参照箇所確認            | 完了   |
| R-03 | Phase 1 | `src/utils.py`                     | 0バイトで、コードからの参照がない                     | 未使用の空ファイルを削除                                                                                  | 削除、import確認          | 完了   |
| R-04 | Phase 1 | `tests/test_quality_rules.py`      | テスト内に品質チェックロジックが複製されていた               | `src/check_bim_quality.py`の本番関数を直接importする構成へ変更                                               | 品質ルールテスト5件成功         | 完了   |
| R-05 | Phase 1 | `tests/test_ai_readiness_score.py` | テスト内にスコア計算・レベル分類ロジックが複製されていた          | `src/calculate_ai_readiness_score.py`の本番関数を直接importする構成へ変更                                    | AI Readinessテスト11件成功 | 完了   |
| R-06 | Phase 1 | 品質ルール実装                            | 本番ロジックの配置と実行経路が不明確だった                 | 品質チェック関数を`src/check_bim_quality.py`へ整理し、テストと本番実行を接続                                           | 本番実行、100件出力、pytest成功 | 完了   |
| R-07 | Phase 1 | データ変換処理                            | 資料記述と空ファイルの状態が一致していなかった               | 過去の変換試作を`08_python`として明記し、現在の主要パイプラインは整形済みCSVを入力起点として整理                                       | ファイル削除、主要文書確認        | 完了   |
| R-08 | Phase 2 | 実行パイプライン                           | 主要処理の一括実行手順がない                        | サンプル入力から主要出力までを1コマンド化する                                                                       | 一括実行結果確認             | 未着手  |
| R-09 | Phase 2 | 依存関係                               | グローバルPython環境を使用している                  | 仮想環境、依存関係、セットアップ手順を整理する                                                                       | 新規環境で再実行             | 未着手  |
| R-10 | Phase 2 | CI                                 | GitHub Actionsが未整備                    | pytest自動実行ワークフローを追加する                                                                         | GitHub Actions成功確認   | 未着手  |
| R-11 | Phase 1 | 主要設計資料                             | 空ファイルや過去試作を現在の正式実装として説明している箇所があった     | `portfolio_summary.md`、`system_overview.md`、`revit_schedule_column_mapping.md`を現在の実装へ合わせて全面更新 | コード・資料照合、pytest成功    | 完了   |
| R-12 | Phase 3 | AI Readiness Score説明               | 独自指標であることの説明を再確認する必要がある               | 主要設計資料では、仮ペナルティを用いる説明可能なルールベース指標と明記。READMEを含む全体確認はPhase 3で実施する                                | README・主要資料確認        | 一部完了 |
| R-13 | Phase 3 | FixPriority説明                      | 仮ラベルと機械学習性能の関係が誤解される可能性がある            | 現行データは単一クラスであり、分類性能を示す成果ではないことを主要資料へ明記。READMEを含む全体確認はPhase 3で実施する                             | README・主要資料確認        | 一部完了 |

---

## 4. Phase 1で実施した内容

### 4.1 品質チェック本番コード

`src/check_bim_quality.py`へ、以下の本番関数を整理した。

* `check_required_parameters`
* `check_classification_code`
* `check_family_naming`
* `run_quality_checks`

品質チェックでは、以下のRule Masterを使用する。

```text
02_rule_master/bim_rule_master_v003.csv
```

本番実行結果：

```text
入力要素数：25
品質チェック結果：100件

R-001：50件
R-002：25件
R-003：25件
```

### 4.2 品質ルールテスト

`tests/test_quality_rules.py`は、テスト内の複製ロジックではなく、`src/check_bim_quality.py`の本番関数を直接importする構成へ変更した。

結果：

```text
5 passed
```

### 4.3 AI Readiness本番コード

`src/calculate_ai_readiness_score.py`に、以下の本番関数を整理した。

* `classify_ai_readiness_level`
* `calculate_ai_readiness_score`
* `is_human_review_required`
* `validate_columns`
* `validate_rule_master_v003_columns`
* `format_element_id`
* `main`

### 4.4 AI Readinessテスト

`tests/test_ai_readiness_score.py`は、テスト内の複製ロジックではなく、`src/calculate_ai_readiness_score.py`の本番関数を直接importする構成へ変更した。

結果：

```text
11 passed
```

### 4.5 空ファイルの削除

以下の0バイトファイルを削除した。

```text
src/convert_revit_schedule.py
src/utils.py
```

削除後、`src`および`tests`内に参照がないことを確認した。

### 4.6 主要文書の整合性修正

以下の文書を、現在の実装へ合わせて全面更新した。

```text
docs/portfolio_summary.md
docs/system_overview.md
docs/revit_schedule_column_mapping.md
```

主な修正内容：

* 過去の`08_python`試作と現在の`src`実装を区別
* 整形済みCSVを現在の主要入力起点として明記
* Rule Master v003へ統一
* 37テスト成功を反映
* 削除済み空ファイルの記載を修正
* pyRevit試作済みの事実を反映
* FixPriorityが単一クラスである制約を明記
* AI Readiness Scoreが独自のルールベース指標であることを明記

---

## 5. Phase 1のテスト結果

実行コマンド：

```powershell
python -m pytest -v
```

最終結果：

```text
37 passed
```

テスト対象：

* 品質ルール
* AI Readiness Score
* AI Readiness Level
* HumanReviewRequired
* Rule Master v003必須列
* FixPriority学習データ
* pyRevitメタデータCSV
* Roomパイプライン

---

## 6. Phase 1のGitコミット

```text
02fb571 docs: record PoC 1 baseline and reliability refactoring scope
5030507 refactor: connect quality rule tests to production code
8a30fab refactor: connect AI readiness tests to production code
5d22317 refactor: remove unused empty source files
36dae38 docs: align PoC 1 documentation with production code
```

---

## 7. Phase 1完了条件

| 完了条件                                   | 結果      |
| -------------------------------------- | ------- |
| 品質チェックテストが本番コードを直接importしている           | 達成      |
| AI Readinessテストが本番コードを直接importしている     | 達成      |
| 空または用途不明の`src`ファイルが整理されている             | 達成      |
| 全37テストが成功する                            | 達成      |
| 削除ファイルがコードから参照されていない                   | 達成      |
| 主要3文書と現在の実装が一致している                     | 達成      |
| 過去の試作と現在の正式実装が区別されている                  | 達成      |
| FixPriorityの単一クラス制約が主要文書に明記されている       | 達成      |
| AI Readiness Scoreが独自のルールベース指標と明記されている | 主要文書で達成 |
| working treeがcleanである                  | 達成      |
| リモートブランチへpush済み                        | 達成      |

---

## 8. Phase 1完了判定

```text
Phase 1：PoC 1の本番コードとテストの接続
状態：完了
完了日：2026年7月11日
```

Phase 1では、本番コードとテストの接続、空ファイル整理、主要設計資料の整合性修正までを完了した。

GitHub Actions、一括実行、仮想環境の再現性確認、README全体修正はPhase 2以降で実施する。

---

## 9. 次の作業

### Phase 2：実行再現性とCI

優先順位：

1. GitHub Actionsによるpytest自動実行
2. 主要処理の一括実行スクリプト
3. 仮想環境と依存関係手順の確認
4. 新規環境での再現確認

### Phase 3：説明・評価設計

優先順位：

1. READMEと現在の実装の整合性確認
2. FixPriorityの表現整理
3. AI Readiness Scoreの説明整理
4. limitationsとevaluation policyの更新
5. One-Pager・Portfolio PDFへの反映
