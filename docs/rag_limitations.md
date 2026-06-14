# RAG Limitations

## 目的

このドキュメントは、`BIM Data Quality & AI Readiness Assessment PoC` の第3段階D「RAG / Azure AI Search構成検討」における制約を整理するものである。

第3段階Dでは、RAGシステムやAzure AI Searchを本格実装しない。

目的は、将来的にRAG / Azure AI Searchへ拡張する場合の構成検討を行う一方で、この段階で実装しないこと、判断しないこと、扱わないデータ、公開範囲の制約を明確にすることである。

---

## このドキュメントの位置づけ

このドキュメントは、第3段階D「RAG / Azure AI Search構成検討」の一部である。

親ドキュメントは以下とする。

```text
docs/rag_azure_ai_search_architecture_plan.md
```

関連ドキュメントは以下とする。

```text
docs/rag_chunk_design.md
docs/rag_metadata_design.md
docs/rag_query_examples.md
docs/rag_answer_policy.md
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl
```

このドキュメントでは、RAG / Azure AI Search構成検討における範囲外事項、技術的制約、データ制約、回答制約、セキュリティ・公開範囲を整理する。

---

# 第3段階Dの範囲

第3段階Dで扱う範囲は、構成検討と設計メモ作成に限定する。

扱う内容は以下である。

```text
RAG化対象データの整理
主検索対象 / 補助対象の整理
チャンク設計
チャンク間の関連付けキー整理
メタデータ設計
Azure AI Searchを想定した概念スキーマ
サンプルRAGドキュメント
検索クエリ例
RAG回答方針
制約・セキュリティ方針
```

この段階では、検索システムとして実際に動作するものは作らない。

---

# 第3段階Dで実装しないこと

第3段階Dでは、以下を実装しない。

```text
本格RAGシステム構築
Azure AI Searchの実デプロイ
Azure OpenAI / OpenAI API接続
Embedding生成
ベクトル検索
Azure Blob Storage連携
クラウド環境構築
認証・権限設計の実装
インデックス作成の自動化
大量データ投入
RAGチャットUI開発
Streamlit / FastAPI連携
LangChain / Semantic Kernelなどのフレームワーク導入
検索精度評価
回答品質評価
本番運用設計
コスト試算
```

第3段階Dは、あくまで将来実装に向けたアーキテクチャ検討である。

---

# Azure AI Searchに関する制約

第3段階Dでは、Azure AI Searchを実際には利用しない。

作成する以下のファイルは、概念設計用のサンプルである。

```text
05_rag_design/sample_index_schema_v001.json
```

このファイルは、Azure AI Searchへそのまま投入することを目的としない。

## 未実施事項

```text
Azure AI Searchサービスの作成
Indexの作成
Indexerの作成
Data Sourceの作成
Skillsetの作成
Semantic ranker設定
Vector Search設定
Analyzer設定
Field属性の実検証
検索クエリの実行
検索結果の評価
```

## 注意点

Azure AI Searchの実装時には、以下を改めて確認する必要がある。

```text
Azure AI Searchの最新仕様
フィールド型
key / searchable / filterable / sortable / facetable / retrievable の制約
日本語検索の扱い
Analyzer設定
ベクトル検索を使う場合のVector field設計
Semantic Searchを使う場合の構成
権限管理
コスト
運用管理
```

第3段階Dでは、これらを実装・検証しない。

---

# Azure OpenAI / OpenAI APIに関する制約

第3段階Dでは、Azure OpenAIまたはOpenAI APIへ接続しない。

未実施事項は以下である。

```text
APIキー設定
.env作成
API呼び出し
チャット補完API利用
Embedding API利用
モデル選定
プロンプト実行
トークン数評価
APIコスト評価
レート制限確認
```

第3段階Dで作成するRAG回答例は、実際のLLM出力ではなく、設計上の想定回答例である。

---

# Embedding / ベクトル検索に関する制約

第3段階Dでは、Embedding生成やベクトル検索を行わない。

未実施事項は以下である。

```text
Embeddingモデル選定
Embedding生成処理
ベクトルDB構築
Azure AI Search Vector Search設定
ハイブリッド検索の実装
ベクトル類似度評価
チャンクサイズの実験
検索精度比較
```

第3段階Dでは、ベクトル検索を使うかどうかの最終判断は行わない。

まずは、AI Context / Fix Guide / Rule Master を検索対象候補として整理するところまでとする。

---

# データ投入に関する制約

第3段階Dでは、実案件データをクラウドや検索サービスへ投入しない。

扱うデータは以下に限定する。

```text
公開可能なサンプルデータ
匿名化したPoC用データ
自作サンプルJSONL
概念スキーマ
設計メモ
```

扱わないデータは以下である。

```text
実案件データ
社外秘モデル由来情報
顧客名
プロジェクト名
個人情報
社内固有の分類コード
機密性の高い仕様情報
大量の実モデル由来パラメータ
```

---

# GitHub公開範囲の制約

GitHubへ含めてよいものは以下である。

```text
docs配下の設計メモ
匿名化済みPoCサンプル
自作サンプルJSONL
概念スキーマ
制約メモ
回答方針メモ
検索クエリ例
```

GitHubへ含めないものは以下である。

```text
実案件名
顧客名
個人名
実モデル由来のUniqueId
実モデル由来のElementId
社外秘モデル名
社内固有の分類コード
機密性の高い仕様
APIキー
接続文字列
Azureリソース名
.env
ログファイル
モデルファイル
キャッシュ
```

第3段階Dで作成する `05_rag_design/` のサンプルは、GitHub公開可能な内容に限定する。

---

# Revit / pyRevit連携に関する制約

第3段階Dでは、RevitやpyRevitとの実連携を拡張しない。

第3段階Cで取得したpyRevit Metadataは、RAG設計上の補助情報として扱う。

未実施事項は以下である。

```text
Revitモデルからの追加取得
全モデルスキャン
リンクモデル要素の取得
Revitパラメータ書き換え
Revitモデル自動修正
Revit UIとのRAG連携
pyRevitボタンからRAG検索実行
UniqueIdからRevit要素へジャンプする機能
```

第3段階Dでは、UniqueIdを将来的な安定識別子候補として整理するに留める。

---

# RAG回答に関する制約

RAG回答では、以下を行わない。

```text
設計の正否判定
施工可否の判断
法規適合性の最終判断
コスト・工程・安全性の断定
Revitモデル修正指示
BIM担当者の確認を不要とする判断
入力情報にない部屋名・分類コード・仕様・寸法の補完
HumanReviewRequired=Trueを無視した自動判断
```

RAG回答は、BIMデータ品質確認の補助情報として扱う。

最終判断はBIM担当者が行う。

---

# QualityScore / AI Readiness Scoreに関する制約

QualityScoreとAI Readiness Scoreは、参考指標である。

以下のような使い方はしない。

```text
QualityScoreが高いのでモデル品質は完全と判断する
AI Readiness Scoreが高いのでAIで自動判断できると判断する
AI Readiness Scoreが低いので対象データを使えないと断定する
スコアだけで修正優先度を確定する
```

Scoreは、RuleId、Severity、HumanReviewRequired、Fix Guide、SourceFileと合わせて確認する。

---

# HumanReviewRequiredに関する制約

HumanReviewRequiredは、人間確認の必要性を示す重要なメタデータである。

`HumanReviewRequired=True` の場合、回答では必ず人間確認が必要であることを明記する。

`HumanReviewRequired=False` の場合でも、LLMが設計・施工・法規の最終判断を行うわけではない。

値が不明な場合は、確認不要とみなさない。

---

# Fix Guideに関する制約

Fix Guideは、確認・対応方針の候補であり、修正命令ではない。

以下のような表現は避ける。

```text
必ず修正してください
この値に変更してください
確認せずに修正できます
自動修正してください
```

以下のような表現を使う。

```text
確認することが推奨されます
対応案として考えられます
入力情報からは判断できません
BIM担当者が元データを確認してください
```

---

# 検索精度評価に関する制約

第3段階Dでは、検索精度評価を行わない。

未実施事項は以下である。

```text
検索結果のランキング評価
Recall / Precision評価
Embeddingモデル比較
Hybrid Search比較
日本語検索品質評価
プロンプト評価
回答正確性評価
ユーザーテスト
```

第3段階Dでは、検索対象、チャンク、メタデータ、回答方針を整理することを優先する。

---

# セキュリティ・情報管理に関する制約

第3段階Dでは、情報管理を優先し、公開可能なサンプルのみを扱う。

禁止事項は以下である。

```text
実案件データをGitHubに含める
実モデル由来のUniqueIdをGitHubに含める
顧客名やプロジェクト名をGitHubに含める
個人情報をGitHubに含める
Azure接続情報やAPIキーをGitHubに含める
ログやキャッシュをGitHubに含める
```

公開前には、以下を確認する。

```text
実案件名が含まれていないか
顧客名が含まれていないか
個人名が含まれていないか
実モデル由来のElementId / UniqueIdが含まれていないか
APIキーや接続文字列が含まれていないか
```

---

# README反映に関する制約

第3段階Dでは、READMEを大きく更新しない。

READMEへ反映する場合は、以下のように小さく記載する程度に留める。

```text
RAG / Azure AI Searchを想定し、AI Context、Fix Guide、Rule Master、ElementId / UniqueIdを検索対象として扱う場合のチャンク設計・メタデータ設計を検討しました。
```

READMEの大幅更新やPortfolio PDF更新は、第3段階A〜DまたはA〜Eの整理がまとまってから検討する。

---

# 完了条件

このドキュメントの完了条件は以下である。

```text
第3段階Dの範囲を整理した
第3段階Dで実装しないことを整理した
Azure AI Searchに関する制約を整理した
Azure OpenAI / OpenAI APIに関する制約を整理した
Embedding / ベクトル検索に関する制約を整理した
データ投入に関する制約を整理した
GitHub公開範囲の制約を整理した
Revit / pyRevit連携に関する制約を整理した
RAG回答に関する制約を整理した
QualityScore / AI Readiness Scoreに関する制約を整理した
HumanReviewRequiredに関する制約を整理した
Fix Guideに関する制約を整理した
検索精度評価に関する制約を整理した
セキュリティ・情報管理に関する制約を整理した
README反映に関する制約を整理した
```

---

# 次に行う確認

次に、Phase 3Dで作成したファイル全体を確認する。

対象は以下である。

```text
docs/rag_azure_ai_search_architecture_plan.md
docs/rag_chunk_design.md
docs/rag_metadata_design.md
docs/rag_query_examples.md
docs/rag_answer_policy.md
docs/rag_limitations.md
05_rag_design/sample_index_schema_v001.json
05_rag_design/sample_rag_documents_v001.jsonl
```

確認後、必要に応じてREADMEへの小規模反映を判断する。
