# FixPriority教師データ設計の制約

## 目的

このドキュメントでは、第3段階E：FixPriority教師データ設計における制約、注意点、対象外事項を整理する。

第3段階Eは、`FixPriority` を将来的に教師データとして扱えるようにするための設計段階である。

本段階では、機械学習モデルの作成、モデル学習、精度評価、自動優先度判定は行わない。

---

## 第3段階Eの位置づけ

第3段階Eは、新規PoCではなく、既存の `BIM Data Quality & AI Readiness Assessment PoC` の第3段階拡張である。

目的は、既存PoCで扱っている以下の情報をもとに、将来的な教師データ設計を整理することである。

```text id="smp7t7"
RuleId
Severity
QualityScore
AI Readiness Score
HumanReviewRequired
Fix Guide
ElementId / UniqueId
Door / Roomカテゴリ
CurrentFixPriority
```

ただし、この段階では、これらの情報から正式な修正優先度を自動決定しない。

---

## 主な制約

### 1. サンプル教師データは学習用ではない

`07_fixpriority_training/fixpriority_training_samples_v001.csv` は、モデル学習用データではない。

このCSVは、以下を確認するための小規模サンプルである。

```text id="1y4482"
列設計
ラベル候補
LabelReasonの扱い
Reviewラベルの扱い
Door / Roomカテゴリの扱い
CSV品質検証
```

そのため、このサンプル件数や内容をもとに、機械学習モデルの性能や有効性を評価しない。

---

### 2. FixPriorityは正式な優先度基準ではない

FixPriorityは、BIMデータ品質上の問題に対して、どの修正を優先的に確認すべきかを整理するためのPoC用指標である。

FixPriorityは、最終判断ではない。

最終的な対応順序は、BIM担当者が以下を踏まえて判断する。

```text id="j4ac8l"
プロジェクト状況
設計意図
納品要件
データ利用目的
BIM運用ルール
後工程への影響
```

---

### 3. ProposedFixPriorityLabelは教師データ候補である

`ProposedFixPriorityLabel` は、将来的な教師ラベル候補である。

これは、AIやスクリプトが確定した正解ラベルではない。

初期MVPでは、以下の位置づけとする。

```text id="8jksfz"
ルールベースの初期案
人による確認を前提としたラベル
将来的な分析・学習のための候補値
```

---

### 4. Reviewは低優先度ではない

`Review` は、High / Medium / Low のいずれかに機械的に分類できない場合に使う。

重要な点：

```text id="67yfs5"
Review は優先度が低いという意味ではない
Review は人による判断が必要という意味である
Review の行では LabelReason に判断保留の理由を必ず記録する
```

---

### 5. LabelReasonが空欄のデータは不完全

`LabelReason` は必須列である。

理由：

```text id="hqdxmz"
ラベル付けの判断根拠を後から確認するため
BIM担当者が妥当性を確認するため
CurrentFixPriority と ProposedFixPriorityLabel が異なる場合の理由を残すため
Reviewラベルの判断保留理由を明確にするため
```

LabelReasonが空欄の教師データは、初期MVPでは不完全なデータとして扱う。

---

### 6. HumanReviewRequired=Trueは自動判断しない

`HumanReviewRequired=True` の行は、人による確認が必要である。

方針：

```text id="tl0bl6"
HumanReviewRequired=True の行では、FixPriorityを完全自動決定しない
Reviewラベルの候補とする
SeverityがHighの場合はHigh候補にもなり得る
LabelReasonに人間確認が必要な理由を記録する
```

---

### 7. Severityだけで優先度を決めない

`Severity` は重要な参考情報であるが、FixPriorityの正式な優先度を単独で決めるものではない。

判断時には以下を組み合わせる。

```text id="9o98le"
RuleId
Category
AI Readiness Score
HumanReviewRequired
Fix Guide
IssueSummary
プロジェクト条件
```

---

### 8. AI Readiness Scoreだけで優先度を決めない

AI Readiness Scoreは、AI活用準備度を示す参考指標である。

ただし、AI Readiness ScoreだけでFixPriorityを決定しない。

判断時には以下を組み合わせる。

```text id="ksnxgh"
RuleId
Severity
Category
HumanReviewRequired
Fix Guide
IssueSummary
```

---

### 9. Fix Guideは修正命令ではない

Fix Guideは、修正方針を説明するための参考情報である。

Fix Guideは、BIM担当者への修正提案であり、最終判断ではない。

```text id="vedz7s"
Fix Guideを根拠にしてAIが自動修正しない
Fix Guideを修正命令として扱わない
BIM担当者が内容を確認して判断する
```

---

### 10. Door / Roomカテゴリで優先度は変わり得る

同じSeverityでも、DoorとRoomでは優先度が異なる可能性がある。

理由：

```text id="9u4ed4"
Doorでは分類コード、建具番号、ファミリ名などが重要
Roomでは部屋名、部屋番号、面積、階、分類コードなどが重要
カテゴリごとにAI ContextやRAG検索への影響が異なる
```

そのため、`Category` を必須列とし、RuleIdと組み合わせて判断する。

---

## 対象外

第3段階Eでは、以下を行わない。

```text id="89p09x"
本格的な機械学習モデル作成
モデル学習
モデル精度評価
ファインチューニング
深層学習
自動ラベル付けの本格実装
FixPriorityの完全自動判定
設計判断・施工判断の自動化
法規適合性の自動判断
Revitモデル自動修正
実案件データを使った教師データ作成
大量データ収集
本番運用設計
```

---

## GitHub公開上の制約

GitHubに含めてよいもの：

```text id="v3hf14"
公開可能なPoC用サンプル
匿名化したサンプル教師データ
ラベル付け方針
列設計
サンプルCSV
サンプルMarkdown
制約ドキュメント
```

GitHubに含めないもの：

```text id="m90h8i"
実案件データ
社外秘モデル由来の情報
顧客名
プロジェクト名
個人名
担当者名
実際のレビュー者名
社内固有の分類コード
機密性の高い仕様情報
APIキー
接続文字列
Azureリソース名
```

公開用サンプルでは、`ReviewedBy` は空欄または匿名値とする。

---

## サンプルデータの制約

`07_fixpriority_training/fixpriority_training_samples_v001.csv` には、以下の制約がある。

```text id="wv9hq6"
8件のみの小規模サンプルである
Door / Roomカテゴリを説明用に混在させている
High / Medium / Low / Review を説明用に含めている
実案件データではない
モデル学習用データではない
統計分析に使える件数ではない
精度評価に使えるデータではない
```

---

## 将来拡張時の注意点

将来的にFixPriorityを学習・分析に使う場合は、以下が必要になる。

```text id="si1vgq"
実務レビュー結果の蓄積
BIM担当者によるラベル確認
ActualFixPriorityの追加
修正工数の記録
手戻り有無の記録
後工程影響の記録
プロジェクト条件の記録
データ利用目的の記録
ラベル付け者間の判断差の整理
公開不可データの分離
```

ただし、これらは第3段階Eの範囲外である。

---

## 完了条件

このドキュメントは、以下を満たした時点で完了とする。

```text id="tmawaq"
サンプル教師データが学習用ではないことを明記した
FixPriorityが正式な優先度基準ではないことを明記した
ProposedFixPriorityLabelが教師データ候補であることを明記した
Reviewが低優先度ではないことを明記した
LabelReasonが必須であることを明記した
HumanReviewRequired=Trueでは自動判断しないことを明記した
Severityだけで優先度を決めないことを明記した
AI Readiness Scoreだけで優先度を決めないことを明記した
Fix Guideが修正命令ではないことを明記した
Door / Roomカテゴリで判断が変わり得ることを明記した
対象外を整理した
GitHub公開上の制約を整理した
将来拡張時の注意点を整理した
```
