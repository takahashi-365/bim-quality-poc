# tests/test_quality_rules.py

"""
RuleIdベース品質チェックの最小テスト。

現時点では、08_python/check_bim_quality.py が試作コードのため、
本テストでは品質チェックルールの期待動作を確認する。

今後、src/check_bim_quality.py へ本実装を移行した後、
このテストを本実装関数に接続する。
"""


def is_blank(value):
    """空欄、None、空文字、スペースのみを未入力として扱う。"""
    if value is None:
        return True
    if str(value).strip() == "":
        return True
    return False


def check_required_parameters(row):
    """
    R-001：必須パラメータ未入力チェック。
    BIM_ModelRole と BIM_Zone が空欄の場合、R-001を返す。
    """
    results = []

    for field in ["BIM_ModelRole", "BIM_Zone"]:
        if is_blank(row.get(field)):
            results.append(
                {
                    "RuleId": "R-001",
                    "ParameterName": field,
                    "Status": "NG",
                }
            )

    return results


def check_classification_code(row):
    """
    R-002：分類コード未入力チェック。
    BIM_ClassificationCode が空欄の場合、R-002を返す。
    """
    if is_blank(row.get("BIM_ClassificationCode")):
        return [
            {
                "RuleId": "R-002",
                "ParameterName": "BIM_ClassificationCode",
                "Status": "NG",
            }
        ]

    return []


def check_family_naming(row):
    """
    R-003：ファミリ命名規則違反チェック。
    Categoryごとの想定接頭辞に合わない場合、R-003を返す。
    """
    category_prefix_map = {
        "Doors": "DR_",
        "Rooms": "RM_",
        "Walls": "WAL_",
    }

    category = row.get("Category")
    family_name = row.get("FamilyName")

    expected_prefix = category_prefix_map.get(category)

    if expected_prefix is None:
        return []

    if is_blank(family_name) or not str(family_name).startswith(expected_prefix):
        return [
            {
                "RuleId": "R-003",
                "ParameterName": "FamilyName",
                "Status": "NG",
            }
        ]

    return []


def test_r001_required_parameters_detects_blank_fields():
    row = {
        "BIM_ModelRole": "",
        "BIM_Zone": "",
    }

    results = check_required_parameters(row)

    assert len(results) == 2
    assert results[0]["RuleId"] == "R-001"
    assert results[1]["RuleId"] == "R-001"


def test_r002_classification_code_detects_blank_field():
    row = {
        "BIM_ClassificationCode": "",
    }

    results = check_classification_code(row)

    assert len(results) == 1
    assert results[0]["RuleId"] == "R-002"
    assert results[0]["ParameterName"] == "BIM_ClassificationCode"


def test_r003_family_naming_detects_invalid_door_family_name():
    row = {
        "Category": "Doors",
        "FamilyName": "SD",
    }

    results = check_family_naming(row)

    assert len(results) == 1
    assert results[0]["RuleId"] == "R-003"
    assert results[0]["ParameterName"] == "FamilyName"


def test_r003_family_naming_passes_valid_door_family_name():
    row = {
        "Category": "Doors",
        "FamilyName": "DR_SingleDoor",
    }

    results = check_family_naming(row)

    assert len(results) == 0


def test_all_rules_detect_expected_violations():
    row = {
        "Category": "Doors",
        "FamilyName": "SD",
        "BIM_ClassificationCode": "",
        "BIM_ModelRole": "",
        "BIM_Zone": "",
    }

    results = []
    results.extend(check_required_parameters(row))
    results.extend(check_classification_code(row))
    results.extend(check_family_naming(row))

    rule_ids = [result["RuleId"] for result in results]

    assert rule_ids.count("R-001") == 2
    assert rule_ids.count("R-002") == 1
    assert rule_ids.count("R-003") == 1
    assert len(results) == 4