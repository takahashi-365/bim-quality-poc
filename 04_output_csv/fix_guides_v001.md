# Fix Guide v001

## Summary

- Total target elements: 25
- Total violations: 100
- Average AI Readiness Score: 40.0
- Human Review Required Count: 25

## Input Files

- Check results CSV: `04_output_csv/check_results_revit_v002.csv`
- Rule master CSV: `02_rule_master/bim_rule_master_v003.csv`
- AI readiness CSV: `04_output_csv/ai_readiness_scores_v001.csv`

## AI Readiness Level Summary

| AIReadinessLevel | Count |
|---|---:|
| Low | 25 |

## Blocking Rule Summary

| RuleId | RuleName | Severity | AIReadinessImpact | ViolationCount |
|---|---|---|---|---:|
| R-001 | 必須パラメータ未入力 | High | High | 50 |
| R-002 | 分類コード未入力 | High | High | 25 |
| R-003 | ファミリ命名規則違反 | Medium | Medium | 25 |

## Element Fix Guide

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

### ElementId: 102

- Category: Doors
- FamilyName: SD
- TypeName: 外部階段 1F
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

### ElementId: 103

- Category: Doors
- FamilyName: SD
- TypeName: ごみ置き場
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

### ElementId: 104

- Category: Doors
- FamilyName: SD
- TypeName: PS
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

### ElementId: 105

- Category: Doors
- FamilyName: SD
- TypeName: ポンプ室
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

### ElementId: 106

- Category: Doors
- FamilyName: SD
- TypeName: EPS 1F
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

### ElementId: 107

- Category: Doors
- FamilyName: SD
- TypeName: 駐車場
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

### ElementId: 108

- Category: Doors
- FamilyName: SD
- TypeName: 電気室 1F
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

### ElementId: 109

- Category: Doors
- FamilyName: SD
- TypeName: 管理人室 清掃管理人室 倉庫
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

### ElementId: 110

- Category: Doors
- FamilyName: SD
- TypeName: 管理用出入口附室
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

### ElementId: 111

- Category: Doors
- FamilyName: SD
- TypeName: 店舗裏口
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

### ElementId: 201

- Category: Doors
- FamilyName: SD
- TypeName: 事務室
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

### ElementId: 202

- Category: Doors
- FamilyName: SD
- TypeName: 外部階段
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

### ElementId: 203

- Category: Doors
- FamilyName: SD
- TypeName: 設備バルコニー
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

### ElementId: 204

- Category: Doors
- FamilyName: SD
- TypeName: 階段室
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

### ElementId: 205

- Category: Doors
- FamilyName: SD
- TypeName: EPS
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

### ElementId: 206

- Category: Doors
- FamilyName: SD
- TypeName: EPS
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

### ElementId: 207

- Category: Doors
- FamilyName: SD
- TypeName: PS
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

### ElementId: 208

- Category: Doors
- FamilyName: SD
- TypeName: PS
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

### ElementId: 209

- Category: Doors
- FamilyName: SD
- TypeName: PS
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

### ElementId: 210

- Category: Doors
- FamilyName: SD
- TypeName: PS
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

### ElementId: 211

- Category: Doors
- FamilyName: SD
- TypeName: DS
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

### ElementId: 301

- Category: Doors
- FamilyName: SD
- TypeName: はと小屋
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

### ElementId: 401

- Category: Doors
- FamilyName: SD
- TypeName: 門扉南
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

### ElementId: 402

- Category: Doors
- FamilyName: SD
- TypeName: 門扉西
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

## Limitations

- This Fix Guide is generated by rule-based templates, not by a generative AI API.
- AIReadinessScore is a simple PoC metric, not an official AI readiness standard.
- Fix recommendations are intended to support human review, not automate BIM model correction.
- Final design, construction, and model correction decisions should be made by a human reviewer.
- Revit API and pyRevit integration are not implemented in this stage.
