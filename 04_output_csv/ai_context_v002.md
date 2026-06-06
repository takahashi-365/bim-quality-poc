# AI Context v002

## Project

- Name: BIM Data Quality & AI Readiness Assessment PoC
- Previous Name: BIM Data Quality Engineering & AI Analysis PoC
- Purpose: Prepare BIM quality check results and AI readiness scores as structured context for future generative AI or RAG usage.
- Note: This context is generated for PoC purposes. It is not a production AI system.

## Input Files

- Check results CSV: `04_output_csv/check_results_revit_v002.csv`
- Features CSV: `04_output_csv/bim_features_v001.csv`
- AI readiness CSV: `04_output_csv/ai_readiness_scores_v001.csv`

## Summary

- Total violations: 100
- Total elements: 25
- Average AI Readiness Score: 40.0
- Human Review Required Count: 25

## Rule Summary

| RuleId | RuleName | Severity | ViolationCount |
|---|---|---|---:|
| R-001 | 必須パラメータ未入力 | High | 50 |
| R-002 | 分類コード未入力 | High | 25 |
| R-003 | ファミリ命名規則違反 | Medium | 25 |

## FixPriority Summary

| FixPriority | Count |
|---|---:|
| High | 25 |

## AI Readiness Level Summary

| AIReadinessLevel | Count |
|---|---:|
| Low | 25 |

## Sample Element Context

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

### ElementId: 102

- Category: Doors
- FamilyName: SD
- TypeName: 外部階段 1F
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

### ElementId: 103

- Category: Doors
- FamilyName: SD
- TypeName: ごみ置き場
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

## Limitations

- QualityScore is a simple PoC metric, not an official business quality standard.
- AIReadinessScore is a simple PoC metric, not an official AI readiness standard.
- FixPriority is a provisional label, not a verified business ground truth.
- The generated context is intended to support human review, not automate BIM model correction.
- Generative AI API integration is not implemented in this stage.
- Revit API and pyRevit integration are not implemented in this stage.