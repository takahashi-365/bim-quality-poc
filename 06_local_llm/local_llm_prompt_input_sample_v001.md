# Local LLM Prompt Input Sample v001

## Purpose

このファイルは、第3段階A：Local LLM Explanation Demo で使用する入力サンプルを記録する。

本サンプルは、`AI Context v002` 全文をLLMに渡すのではなく、ElementId 1件分のAI Contextと、該当RuleIdのFix Guideだけを切り出して使用する。

---

## Source Files

| 種類 | ファイル |
|---|---|
| AI Context | `04_output_csv/ai_context_v002.md` |
| Fix Guide | `04_output_csv/fix_guides_v001.md` |
| Prompt Template | `docs/local_llm_prompt_template.md` |

---

## Target Element

| 項目 | 内容 |
|---|---|
| ElementId | 101 |
| Category | Doors |
| RuleIds | R-001, R-002, R-003 |
| AI Readiness Score | 40 |
| AI Readiness Level | Low |
| HumanReviewRequired | True |

---

## Prompt Input

```text
あなたはBIMデータ品質確認を補助するアシスタントです。

以下の AI Context と Fix Guide をもとに、BIM担当者向けの説明文を作成してください。

重要な前提：
- 設計判断、施工判断、モデル修正の最終判断は行わないでください。
- 入力情報に基づいて説明してください。
- 入力に含まれない情報は「入力情報からは判断できません」と表現してください。
- 不明な内容を推測しすぎないでください。
- HumanReviewRequired が True の場合は、人間確認が必要であることを明記してください。
- 修正方針は「案」として表現してください。
- 回答の根拠として参照した RuleId、Severity、AI Readiness Score、FixGuide を明記してください。
- 出力の最後に、LLM回答は参考情報であり、最終判断はBIM担当者が行うことを明記してください。
- 出力はBIM担当者が確認しやすい日本語にしてください。

出力形式：
1. 対象要素の概要
2. 検出された問題
3. AI活用上の影響
4. 修正優先度と理由
5. 人間が確認すべき項目
6. 修正方針案
7. 根拠として参照した情報
8. 注意点

AI Context：

### ElementId: 101

- Category: Doors
- FamilyName: SD
- TypeName: 管理用出入口
- QualityScore: 65
- FixPriority: High
- RuleViolationCount: 4
- AIReadinessScore: 40
- AIReadinessLevel: Low
- AIReadinessPenaltyTotal: 60
- BlockingRuleIds: R-001, R-002, R-003
- HumanReviewRequired: True

| RuleId | RuleName | Severity | ParameterName | FixGuide |
|---|---|---|---|---|
| R-001 | 必須パラメータ未入力 | High | BIM_ModelRole | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-001 | 必須パラメータ未入力 | High | BIM_Zone | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-002 | 分類コード未入力 | High | BIM_ClassificationCode | 分類コード表に従い、BIM_ClassificationCode を入力する |
| R-003 | ファミリ命名規則違反 | Medium | FamilyName | 命名規則に従い、カテゴリ・用途・識別情報が分かるファミリ名へ修正する |

Fix Guide：

### ElementId: 101

- Category: Doors
- FamilyName: SD
- TypeName: 管理用出入口
- AI Readiness Score: 40
- AI Readiness Level: Low
- AI Readiness Penalty Total: 60
- Blocking RuleIds: R-001, R-002, R-003
- Human Review Required: True

Recommended fix approach:

- Review the listed RuleId violations before using this BIM data for AI, BI, or analytics.
- Prioritize High severity and High AIReadinessImpact issues.
- Confirm final model correction decisions with a human BIM reviewer.

| RuleId | RuleName | Severity | ParameterName | CurrentValue | AIReadinessImpact | AIReadinessPenalty | FixGuide |
|---|---|---|---|---|---|---:|---|
| R-001 | 必須パラメータ未入力 | High | BIM_ModelRole |  | High | 15 | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-001 | 必須パラメータ未入力 | High | BIM_Zone |  | High | 15 | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-002 | 分類コード未入力 | High | BIM_ClassificationCode |  | High | 20 | 分類コード表に従い、BIM_ClassificationCode を入力する |
| R-003 | ファミリ命名規則違反 | Medium | FamilyName | SD | Medium | 10 | 命名規則に従い、カテゴリ・用途・識別情報が分かるファミリ名へ修正する |

```