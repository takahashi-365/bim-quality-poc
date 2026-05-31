# AI Context v001

## Project

- Name: BIM Data Quality Engineering & AI Analysis PoC
- Purpose: Prepare BIM quality check results as structured context for generative AI usage.
- Note: This context is generated for PoC purposes. It is not a production AI system.

## Input Files

- Check results CSV: `04_output_csv\check_results_revit_v002.csv`
- Features CSV: `04_output_csv\bim_features_v001.csv`

## Summary

- Total violations: 100
- Total elements: 25

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

## Sample Element Context

### ElementId: 101.0

- Category: Doors
- FamilyName: SD
- TypeName: 管理用出入口
- QualityScore: 65
- FixPriority: High
- RuleViolationCount: 4

| RuleId | RuleName | Severity | ParameterName | FixGuide |
|---|---|---|---|---|
| R-001 | 必須パラメータ未入力 | High | BIM_ModelRole | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-001 | 必須パラメータ未入力 | High | BIM_Zone | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-002 | 分類コード未入力 | High | BIM_ClassificationCode | 分類コード表に従い、BIM_ClassificationCode を入力する |
| R-003 | ファミリ命名規則違反 | Medium | FamilyName | 命名規則に従い、カテゴリ・用途・識別情報が分かるファミリ名へ修正する |

### ElementId: 102.0

- Category: Doors
- FamilyName: SD
- TypeName: 外部階段 1F
- QualityScore: 65
- FixPriority: High
- RuleViolationCount: 4

| RuleId | RuleName | Severity | ParameterName | FixGuide |
|---|---|---|---|---|
| R-001 | 必須パラメータ未入力 | High | BIM_ModelRole | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-001 | 必須パラメータ未入力 | High | BIM_Zone | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-002 | 分類コード未入力 | High | BIM_ClassificationCode | 分類コード表に従い、BIM_ClassificationCode を入力する |
| R-003 | ファミリ命名規則違反 | Medium | FamilyName | 命名規則に従い、カテゴリ・用途・識別情報が分かるファミリ名へ修正する |

### ElementId: 103.0

- Category: Doors
- FamilyName: SD
- TypeName: ごみ置き場
- QualityScore: 65
- FixPriority: High
- RuleViolationCount: 4

| RuleId | RuleName | Severity | ParameterName | FixGuide |
|---|---|---|---|---|
| R-001 | 必須パラメータ未入力 | High | BIM_ModelRole | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-001 | 必須パラメータ未入力 | High | BIM_Zone | 該当要素に必要な BIM_ModelRole または BIM_Zone を入力する |
| R-002 | 分類コード未入力 | High | BIM_ClassificationCode | 分類コード表に従い、BIM_ClassificationCode を入力する |
| R-003 | ファミリ命名規則違反 | Medium | FamilyName | 命名規則に従い、カテゴリ・用途・識別情報が分かるファミリ名へ修正する |

## Limitations

- QualityScore is a simple PoC metric, not an official business quality standard.
- FixPriority is a provisional label, not a verified business ground truth.
- The generated context is intended to support human review, not automate BIM model correction.
- Revit API and pyRevit integration are not implemented in this stage.