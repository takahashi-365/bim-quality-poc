# BIM Data Quality & AI Readiness Assessment PoC 完成扱い方針

## 目的

このドキュメントでは、`BIM Data Quality & AI Readiness Assessment PoC` を現時点で完成扱いとするための方針を整理する。

本PoCは、BIMデータをAI、RAG、データ分析、将来的な機械学習で活用する前段階として、BIMデータ品質、AI Readiness、Fix Guide、HumanReviewRequired、RAG向け構造、FixPriority教師データ設計を整理することを目的として実施した。

第3段階A〜Eの完了により、PoCとしての主要な検証範囲は一通り完了したため、今後は新機能追加ではなく、README、図解、Portfolio PDFなどの見せ方を整えるフェーズへ移行する。

---

## 完成扱いとする理由

本PoCは、以下の流れを一通り確認できた。

```text
Revit Schedule TXT
↓
CSV変換
↓
データクリーニング
↓
品質チェック
↓
QualityScore
↓
FixPriority prototype
↓
AI Readiness Score
↓
AI Context
↓
Fix Guide
↓
Local LLM Explanation Demo
↓
Roomカテゴリ拡張
↓
pyRevit ElementId / UniqueId取得PoC
↓
RAG / Azure AI Search構成検討
↓
FixPriority教師データ設計
```

これにより、本PoCは単なる品質チェックスクリプトではなく、BIMデータをAI活用前提で評価・整理するためのPoCとして成立した。

---

## 完成扱いとする範囲

完成扱いとする範囲は以下とする。

```text
DoorカテゴリのBIMデータ品質チェック
RoomカテゴリのBIMデータ品質チェック
QualityScore算出
AI Readiness Score算出
HumanReviewRequired判定
AI Context生成
Fix Guide生成
Local LLM説明デモ設計
pyRevit ElementId / UniqueId取得MVP
RAG / Azure AI Search構成設計
FixPriority教師データ設計
サンプルデータ作成
pytestによる検証
GitHub公開可能な範囲でのドキュメント化
```

---

## 第3段階A〜Eの完了範囲

第3段階では、以下を完了した。

```text
A：Local LLM Explanation Demo
B：Roomカテゴリ追加
C：pyRevit ElementId / UniqueId取得PoC
D：RAG / Azure AI Search構成検討
E：FixPriority教師データ設計
```

それぞれの位置づけは以下。

| Phase | 内容                                | 完了内容                                                |
| ----- | --------------------------------- | --------------------------------------------------- |
| A     | Local LLM Explanation Demo        | AI Context / Fix Guideを使ったLLM説明文生成の設計とサンプル整理        |
| B     | Roomカテゴリ追加                        | Roomカテゴリの品質チェック、AI Readiness、AI Context、Fix Guide生成 |
| C     | pyRevit ElementId / UniqueId取得PoC | Revit選択要素からElementId / UniqueId等をCSV出力するMVP         |
| D     | RAG / Azure AI Search構成検討         | RAG対象データ、チャンク、メタデータ、回答方針、サンプル設計                     |
| E     | FixPriority教師データ設計                | FixPriorityの教師データ列設計、ラベル方針、サンプルCSV、pytest検証         |

---

## 今後このPoCで追加しないもの

このPoCでは、以下を現時点では追加しない。

```text
Azure AI Searchの実デプロイ
Azure OpenAI / OpenAI API接続
Embedding生成
ベクトル検索の本格実装
RAGチャットUI
機械学習モデル構築
深層学習
ファインチューニング
FixPriorityの完全自動判定
Revitモデル自動修正
設計判断・施工判断の自動化
法規適合性の自動判断
実案件データ投入
本番運用設計
```

これらは今後の別PoCまたは将来拡張として扱う。

---

## 完成後に行う作業

完成扱い後は、機能追加ではなく、見せ方の整理を行う。

主な作業は以下。

```text
READMEの最終整理
Portfolio PDFの更新
PoC全体フロー図の作成
第3段階A〜Eの拡張図の作成
主要成果物一覧の整理
テスト結果の整理
制約・対象外の明記
次成果物テーマの切り出し
```

---

## README更新方針

READMEは、既存構成を壊さず、必要最小限の更新に留める。

更新候補は以下。

```text
第3段階A〜E完了の明記
主要成果物一覧の整理
PoC全体の位置づけ整理
できること / できないことの整理
テスト結果の更新
Repository Structureの確認
Documentation一覧の確認
```

過去にREADMEを大きく変更した際、既存セクションが落ちるリスクがあったため、README編集時は必ず差分確認を行う。

---

## 図解作成方針

Portfolio PDFとREADMEで使うため、以下の図を作成する。

```text
図1：PoC全体フロー
図2：第3段階A〜Eの拡張図
```

図1では、Revit Schedule TXTからAI Context、Fix Guide、RAG設計、FixPriority教師データ設計までの流れを示す。

図2では、第3段階A〜Eで何を拡張したかを示す。

---

## Portfolio PDF更新方針

Portfolio PDFでは、細かい実装説明よりも、成果物として何を示しているかを分かりやすく整理する。

構成候補は以下。

```text
表紙
背景・課題
PoCの目的
全体フロー
Phase 1〜3の流れ
第3段階A〜Eの説明
主な成果物
技術スタック
テスト結果
制約・安全方針
今後の展開
```

---

## GitHub公開方針

GitHubに含めてよいものは以下。

```text
公開可能なPoC用サンプル
匿名化したサンプルCSV
設計ドキュメント
テストコード
README
Portfolio用の図解
公開可能なスクリーンショット
```

GitHubに含めないものは以下。

```text
実案件データ
顧客名
プロジェクト名
個人情報
社外秘モデル由来情報
実モデル由来のUniqueId
実モデル由来のElementId
APIキー
接続文字列
Azureリソース名
モデルファイル
ローカルキャッシュ
ログファイル
```

---

## 次成果物への切り出し方針

このPoCを完成扱いにした後、次の成果物は別テーマとして作成する。

候補は以下。

```text
COBie / BIMデータ統合作業の成果物化
Local RAG / BIM Rule Guide PoC
BIM実務データ整備ワークフロー
```

現時点では、次成果物としては `COBie / BIMデータ統合作業` を有力候補とする。

理由は、現在のPoCがAI・データ品質寄りであるのに対し、COBie成果物はBIM実務・データ統合寄りの成果物として整理できるためである。

---

## 完了判断

本PoCは、第3段階A〜Eの完了をもって、PoCとして完成扱いとする。

完成扱いの条件は以下を満たしている。

```text
主要処理フローが一通り成立している
Door / Roomカテゴリに対応している
AI Readiness Scoreを算出できる
AI ContextとFix Guideを生成できる
Local LLM説明デモの設計が完了している
pyRevit ElementId / UniqueId取得MVPが完了している
RAG / Azure AI Search構成設計が完了している
FixPriority教師データ設計が完了している
pytestが通過している
成果物がGitHubに反映済みである
```

---

## 現在の状態

```text
Latest Commit:
c3d965a Add Phase 3E FixPriority training data design

Test:
37 passed

GitHub:
main -> origin/main synced

Working tree:
clean
```

---

## 最終方針

今後は、このPoCに大きな機能を追加するのではなく、完成成果物として見せるための整理を行う。

次の作業は以下とする。

```text
README最終整理
PoC全体フロー図作成
第3段階A〜E拡張図作成
Portfolio PDF更新
次成果物テーマの切り出し
```

この方針により、`BIM Data Quality & AI Readiness Assessment PoC` を代表成果物として完成させ、次の別成果物へ進む。
