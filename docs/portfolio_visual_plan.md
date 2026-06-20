# Portfolio Visual Plan

## 目的

このドキュメントでは、`BIM Data Quality & AI Readiness Assessment PoC` を完成成果物として見せるための図解方針を整理する。

対象は、README、Portfolio PDF、説明資料で使用する図解である。

本ドキュメントでは、まず図に何を含めるかを決める。
実際の画像作成、PDF反映、README反映は後続作業とする。

---

## 図解作成の目的

このPoCは、BIMデータ品質チェックだけでなく、AI Readiness、AI Context、Fix Guide、Local LLM、Roomカテゴリ、pyRevit Metadata、RAG設計、FixPriority教師データ設計まで拡張している。

そのため、文章だけでは全体像が伝わりにくい。

図解では、以下を分かりやすく示す。

```text
このPoCが何を入力としているか
どのように品質チェックしているか
AI活用前に何を評価しているか
第3段階A〜Eで何を拡張したか
何を実装済みで、何を設計段階に留めているか
```

---

## 作成する図

初期版では、以下の2種類を作成する。

```text
図1：PoC全体フロー図
図2：第3段階A〜E拡張図
```

この2枚を、READMEとPortfolio PDFの両方で使えるようにする。

---

# 図1：PoC全体フロー図

## 目的

PoC全体フロー図では、Revit ScheduleやpyRevit Metadataから、品質チェック、AI Readiness、AI Context、Fix Guide、RAG設計、FixPriority教師データ設計へつながる流れを示す。

---

## 図1に含める要素

```text
Revit Schedule TXT
pyRevit Metadata CSV
CSV変換
データクリーニング
品質チェック
Rule Master
QualityScore
FixPriority prototype
AI Readiness Score
HumanReviewRequired
AI Context
Fix Guide
Local LLM Explanation Demo
RAG / Azure AI Search Design
FixPriority Training Data Design
```

---

## 図1の推奨構成

```text
[Revit Schedule TXT]
        ↓
[CSV変換]
        ↓
[データクリーニング]
        ↓
[品質チェック] ← [Rule Master]
        ↓
[QualityScore]
        ↓
[FixPriority prototype]
        ↓
[AI Readiness Score] → [HumanReviewRequired]
        ↓
[AI Context] + [Fix Guide]
        ↓
[Local LLM Explanation Demo]
[ RAG / Azure AI Search Design ]
[ FixPriority Training Data Design ]

[pyRevit Metadata CSV] → [ElementId / UniqueId] → [AI Context / RAG Metadata候補]
```

---

## 図1で伝えたいこと

図1では、以下を伝える。

```text
BIMデータをAIで使う前に、品質・AI利用準備度・修正方針を整理している
AI ContextとFix GuideをLLMやRAGの入力候補として設計している
pyRevit Metadataにより、Revit内部識別子との接続を検討している
FixPriorityを将来的な教師データ候補として整理している
```

---

## 図1で強調するポイント

```text
AIが自動判断するPoCではない
Revitモデルを自動修正するPoCではない
BIM担当者の確認を支援するPoCである
AI活用前のデータ品質評価・整備支援が目的である
```

---

# 図2：第3段階A〜E拡張図

## 目的

第3段階A〜E拡張図では、既存PoCに対して第3段階で何を追加・整理したかを示す。

---

## 図2に含める要素

```text
既存PoC Core
A：Local LLM Explanation Demo
B：Roomカテゴリ追加
C：pyRevit ElementId / UniqueId取得PoC
D：RAG / Azure AI Search構成検討
E：FixPriority教師データ設計
```

---

## 図2の推奨構成

```text
                   ┌──────────────────────────────┐
                   │ Existing PoC Core             │
                   │ - Quality Check               │
                   │ - QualityScore                │
                   │ - AI Readiness Score          │
                   │ - AI Context                  │
                   │ - Fix Guide                   │
                   └──────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
┌───────▼────────┐       ┌────────▼───────┐       ┌────────▼────────┐
│ Phase 3A        │       │ Phase 3B       │       │ Phase 3C         │
│ Local LLM       │       │ Room Category  │       │ pyRevit Metadata │
│ Explanation     │       │ Extension      │       │ ElementId/UniqueId│
└────────────────┘       └────────────────┘       └─────────────────┘

        ┌─────────────────────────┼─────────────────────────┐
        │                         │
┌───────▼────────┐       ┌────────▼────────┐
│ Phase 3D        │       │ Phase 3E         │
│ RAG / Azure AI  │       │ FixPriority      │
│ Search Design   │       │ Training Design  │
└────────────────┘       └─────────────────┘
```

---

## 図2で伝えたいこと

図2では、以下を伝える。

```text
第3段階は新規PoCではなく、既存PoCの拡張である
A〜Eはそれぞれ独立しつつ、AI活用前処理という目的でつながっている
LLM、Room、pyRevit、RAG、教師データ設計を一通り検討した
各テーマは本格実装ではなく、PoCとしてのMVPまたは設計整理である
```

---

# READMEでの使い方

READMEでは、図は多すぎない方がよい。

READMEに掲載する図は、初期版では以下の1〜2枚とする。

```text
PoC全体フロー図
第3段階A〜E拡張図
```

READMEでは図の下に、短い説明文を付ける。

例：

```text
This PoC evaluates BIM data quality and AI readiness before using BIM data for LLM, RAG, BI, or future machine learning workflows.
```

---

# Portfolio PDFでの使い方

Portfolio PDFでは、READMEよりも図を大きく使う。

推奨掲載箇所：

```text
PoC全体フロー図：PoC概要ページ
第3段階A〜E拡張図：Phase 3説明ページ
```

PDFでは、図だけでなく以下の補足を添える。

```text
目的
入力データ
処理内容
成果物
制約
今後の展開
```

---

# 図に入れない情報

図には、以下を入れない。

```text
実案件名
顧客名
個人名
社内固有の分類コード
実モデル由来のUniqueId
実モデル由来のElementId
ローカルパス
APIキー
Azureリソース名
接続文字列
```

---

# 図の形式候補

図の形式候補は以下。

```text
Mermaid
draw.io
PowerPoint図形
PNG画像
PDF内図版
```

初期案では、まずMermaidまたはPowerPoint図形で作成する。

GitHub READMEに載せる場合は、MermaidまたはPNGが扱いやすい。
Portfolio PDFに載せる場合は、PowerPoint図形またはPNGが扱いやすい。

---

# 推奨方針

初期版は以下の方針とする。

```text
README用：MermaidまたはPNG
Portfolio PDF用：PowerPoint図形またはPNG
まずはMermaidで構造を確定する
その後、見た目を整える場合はPowerPointまたはdraw.ioで図化する
```

---

# 完了条件

この図解計画は、以下を満たした時点で完了とする。

```text
PoC全体フロー図に入れる要素を整理した
第3段階A〜E拡張図に入れる要素を整理した
READMEでの使い方を整理した
Portfolio PDFでの使い方を整理した
図に入れない情報を整理した
図の形式候補を整理した
```

---

# 次の作業

次の作業は以下。

```text
1. PoC全体フロー図のMermaid案を作成する
2. 第3段階A〜E拡張図のMermaid案を作成する
3. READMEに載せるか、画像化してPortfolio PDFに使うかを判断する
```
