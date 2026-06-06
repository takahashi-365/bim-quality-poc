# Limitations

## BIM Data Quality & AI Readiness Assessment PoC

## この資料の目的

この資料は、現時点における制約、注意点、未実装範囲、今後の改善予定を整理するための資料です。

本PoCは、Revit/BIMデータをPythonで処理し、BIM品質チェック、品質メトリクス作成、特徴量設計、修正優先度分類プロトタイプ、AI Readiness Score、AI Context v002、Fix Guide Markdown、Streamlit簡易可視化までを検証する個人開発PoCです。

本資料では、現時点の実装済み範囲と、実務適用に向けて残っている制約を明確にします。

---

## 1. PoC全体に関する制約

* このPoCは個人開発の検証用PoCであり、本番業務システムではありません。
* 実案件データ・社外秘データは使用していません。
* Autodesk日本仕様 意匠サンプルモデル Revit 2024をもとにした検証用データを使用しています。
* 現時点では、処理フローの検証、データ品質評価の考え方、AI活用前の構造化コンテキスト生成を目的としています。
* 正式なBIM品質基準、社内標準、プロジェクト標準に基づく評価システムではありません。
* 設計判断、施工判断、モデル修正判断を自動化するものではありません。
* 最終的な設計判断、施工判断、モデル修正判断は人間が行う前提です。

---

## 2. Revit由来データに関する制約

* Revit由来データ対応は初期試作です。
* 現時点で実処理しているのは、ドア建具表の書き出しTXTです。
* 壁、部屋、設備、構造など、他カテゴリのRevitデータ処理は未実装です。
* `door_schedule_converted_v002.csv` の列マッピングは仮設定です。
* `ElementId` はRevit内部ElementIdではなく、建具表上の建具番号を仮IDとして使用しています。
* `FamilyName` はRevitファミリ名ではなく、建具表上の種別記号 `SD` を仮格納しています。
* `TypeName` はRevitタイプ名ではなく、設置場所・室名に近い列を仮格納しています。
* `Level` は現時点では空欄です。
* `BIM_ClassificationCode`、`BIM_ModelRole`、`BIM_Zone` は現時点では空欄であり、未入力チェック対象として使用しています。
* 現在のRevit列マッピングは、正式なRevit内部情報ではなく、PoCの処理フローを成立させるための仮マッピングです。
* 正式なRevit内部ElementId、FamilyName、TypeName、Level、RoomNameなどの取得は未実装です。

詳細は以下に整理しています。

```text
docs/data_dictionary.md
docs/revit_schedule_column_mapping.md
```

---

## 3. 品質チェック結果に関する制約

* `check_results_revit_v002.csv` の100件の違反は、正確な実務品質評価ではなく、処理フロー確認のための結果です。
* 現時点の対象要素数は25件です。
* 100件の内訳は、各要素に対して `BIM_ModelRole`、`BIM_Zone`、`BIM_ClassificationCode`、`FamilyName` の違反が発生しているためです。
* `R-001`、`R-002`、`R-003` の3ルールのみを対象とした初期実装です。
* 現時点では、BIM品質ルールの網羅性は限定的です。
* ルール数、Severity、FixGuideはPoC用の初期設定です。
* 実務適用する場合は、社内BIM標準、プロジェクト要件、BEP、分類体系などに合わせてルールを調整する必要があります。

---

## 4. QualityScoreに関する制約

* `QualityScore` はPoC用の簡易指標であり、実務上の正式な品質評価基準ではありません。
* `QualityScore = 100 - SeverityScore` という単純な減点方式で算出しています。
* High、Medium、Lowの減点値はPoC用の仮設定です。
* 現時点では、違反内容の業務重要度、設計段階、用途、モデル種別などは十分に反映していません。
* 実務適用する場合は、BIM標準やプロジェクト要件に応じた重み付け調整が必要です。

---

## 5. FixPriorityに関する制約

* `FixPriority` は実務の正解ラベルではなく、QualityScoreとHigh違反件数をもとにした仮ラベルです。
* 現時点のデータでは、全25要素の `FixPriority` が `High` になっています。
* 修正優先度分類プロトタイプは初期実装済みですが、本格的な分類精度評価はできません。
* scikit-learnによる分類処理は、機械学習モデルの精度を追求するものではなく、特徴量データセットを学習・予測処理へ接続できることを確認するためのものです。
* 実務で修正優先度を判定するには、専門家レビューや業務上の影響度を反映した正解ラベルが必要です。

---

## 6. AI Readiness Scoreに関する制約

* `AIReadinessScore` はPoC用の簡易指標であり、実務上の正式なAI活用準備度基準ではありません。
* `AIReadinessScore = 100 - AIReadinessPenalty合計` という単純な減点方式で算出しています。
* `AIReadinessPenalty` はPoC用の仮設定です。
* 現時点では、Rule Master v003の3ルールのみを対象にしています。
* 現時点のデータでは、全25要素が `AIReadinessScore = 40`、`AIReadinessLevel = Low`、`HumanReviewRequired = True` になっています。
* この結果は、現時点の入力データが正式にAI活用不可であることを示すものではなく、属性情報、分類コード、命名規則を整備する必要があることを説明するためのPoC結果です。
* 実務適用する場合は、社内BIM標準、分類体系、プロジェクト要件、AI利用目的に応じて、評価項目や重み付けを調整する必要があります。

---

## 7. AI Context v002に関する制約

* `AI Context v002` は生成AIやRAGへ渡す前段階の構造化コンテキストであり、生成AI APIの呼び出しは未実装です。
* 現時点では、OpenAI API、Azure OpenAI、Azure AI Search、ローカルLLMなどとは接続していません。
* `ai_context_v002.json` と `ai_context_v002.md` は、AIに渡すための参照情報を整理したファイルです。
* 生成AIに自由判断させるのではなく、RuleId、品質チェック結果、QualityScore、FixPriority、AIReadinessScore、HumanReviewRequiredなどを明示的に渡す設計を重視しています。
* 現時点のContextはPoC用であり、実務利用にはプロンプト設計、セキュリティ、アクセス制御、データ秘匿、監査ログなどの検討が必要です。

---

## 8. Fix Guide Markdownに関する制約

* `Fix Guide Markdown` は生成AI APIではなく、RuleIdベースのテンプレート方式で生成しています。
* 出力される修正ガイドは、品質チェック結果とRule Master v003に基づく参考情報です。
* 実際のモデル修正、設計判断、施工判断を自動化するものではありません。
* 各ElementIdに対する修正方針は、人間のBIM担当者、設計者、管理者が確認する前提です。
* 現時点では、要素同士の関係、設計意図、プロジェクト条件、施工条件などは考慮していません。
* 実務利用する場合は、BIM標準、設計ルール、プロジェクト運用ルールに合わせてFixGuideの内容を調整する必要があります。

---

## 9. Streamlit画面に関する制約

* Streamlit画面はPoC説明用の簡易UIです。
* 本格的な業務アプリケーションではありません。
* 認証、権限管理、ユーザー管理、監査ログ、エラーハンドリングなどは実装していません。
* 現時点では、ローカル環境での確認を前提としています。
* 画面はやや縦長であり、今後タブ分けや表示整理を行う余地があります。
* 大規模データを前提としたパフォーマンス最適化は行っていません。

---

## 10. Power BIに関する制約

* Power BIは補助的な可視化手段として使用しています。
* `.pbix` ファイル本体は、容量・配布条件を考慮し、GitHub公開対象外としています。
* 現時点では、Power BIダッシュボードの再設計は第2段階の主対象ではありません。
* 第2段階では、Streamlitを主な確認画面として扱っています。

---

## 11. Revit API / pyRevitに関する制約

* Revit APIとの直接連携は未実装です。
* pyRevit連携は未実装です。
* Revitモデルから正式な内部ElementId、FamilyName、TypeName、Level、RoomNameなどを直接取得する処理は未実装です。
* Revitモデルへ修正内容を書き戻す処理は未実装です。
* Revitモデルの自動修正は対象外です。
* 将来的にRevit API / pyRevit連携を検討しますが、今回の第2段階では対象外とします。

---

## 12. 生成AI / RAGに関する制約

* 本格RAGは未実装です。
* Azure AI Search連携は未実装です。
* 生成AI API接続は未実装です。
* OpenAI API、Azure OpenAI、ローカルLLMなどへの接続は行っていません。
* ベクトル検索、Embedding、検索インデックス作成は未実装です。
* 本PoCでは、生成AIやRAGへ渡す前段階のデータ品質評価と構造化コンテキスト生成に集中しています。

---

## 13. テストに関する制約

* 現時点で実装済みのテストは、RuleIdベース品質チェックの最小テストです。
* `tests/test_quality_rules.py` で、R-001、R-002、R-003の基本動作を確認しています。
* AI Readiness Score計算のテストは未実装です。
* AI Readiness Level分類のテストは未実装です。
* Rule Master v003必須列確認のテストは未実装です。
* AI Context v002生成結果の基本確認テストは未実装です。
* Fix Guide Markdown生成結果の基本確認テストは未実装です。

---

## 14. GitHub公開に関する制約

* `.rvt` ファイル本体はGitHub公開対象外です。
* `.pbix` ファイル本体はGitHub公開対象外です。
* 実案件データ、社外秘データ、個人情報は使用しません。
* 旧試作コード、応募文面、面接メモ、個人作業メモは公開対象外です。
* GitHub公開前に、公開対象ファイルとREADME記載内容の整合性を確認する必要があります。

---

## 15. 今後の対応

今後の主な対応は以下です。

* AI Readiness Score計算のテスト追加
* AI Readiness Level分類のテスト追加
* Rule Master v003必須列確認のテスト追加
* AI Context v002生成結果の基本確認テスト追加
* Fix Guide Markdown生成結果の基本確認テスト追加
* READMEとdocsの整合性確認
* GitHub公開範囲の確認
* Streamlit画面スクリーンショットの保存
* 必要に応じたポートフォリオPDF v003化検討
* 将来的なRevit内部ElementId、FamilyName、TypeName、Level、RoomNameの正式取得検討
* 将来的なRevit API / pyRevit連携検討

---

## 16. まとめ

本PoCは、BIMデータをAI・機械学習・データ分析で扱うための前処理、ルールベース判定、品質メトリクス作成、特徴量設計、AI活用準備度評価、構造化コンテキスト生成、修正ガイド生成、簡易可視化までの一連の流れを検証するものです。

現時点では、Revit由来データの列マッピングや評価スコアはPoC用の仮設定を含みます。

そのため、本PoCの結果は正式な実務品質評価やAI活用可否判定ではなく、AI活用前にどのようなBIMデータ品質管理・構造化・人間確認が必要になるかを説明するための検証結果として扱います。
