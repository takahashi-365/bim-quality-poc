# Phase 2 GitHub Actions CI

## Date

2026-07-11

## Purpose

PoC 1のテストおよび主要パイプラインを、GitHubへのpushまたは
Pull Request作成時に自動実行する。

## Workflow

`.github/workflows/python-ci.yml`

## Triggers

- `main`ブランチへのpush
- `refactor/poc1-reliability`ブランチへのpush
- `main`ブランチを対象とするPull Request
- GitHub Actions画面からの手動実行

## Environment

- Runner: `ubuntu-latest`
- Python: `3.12`
- Package manager: `pip`
- Dependency file: `requirements.txt`

## CI Steps

1. リポジトリをチェックアウト
2. Python 3.12をセットアップ
3. pip依存関係キャッシュを復元
4. requirements.txtをインストール
5. pytestを実行
6. 主要パイプラインを実行

## Test Command

`python -m pytest -v`

ローカル確認時点のテスト結果：

`44 passed`

## Pipeline Command

`python scripts/run_pipeline.py`

ローカル確認時点の結果：

- 7ステップ成功
- 終了コード0
- 期待出力ファイルの存在確認成功
- 0バイト出力なし

## Failure Behavior

次の場合はGitHub Actionsを失敗として終了する。

- 依存関係をインストールできない
- pytestが1件以上失敗する
- パイプライン内のスクリプトが異常終了する
- 期待する出力ファイルが生成されない
- 出力ファイルが0バイトになる
