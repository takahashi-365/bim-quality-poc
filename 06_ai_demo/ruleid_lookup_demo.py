# このファイルの目的：
# RuleIdをもとに、該当するBIM品質ルールの内容を検索・表示するためのデモ。
#
# 主な処理フロー：
# 1. BIM品質ルールの一覧を読み込む
# 2. ユーザーが入力したRuleIdを受け取る
# 3. RuleIdに一致するルールを検索する
# 4. 該当するルール内容を表示する

import pandas as pd
from pathlib import Path


# =========================================
# Path settings
# =========================================

BASE_DIR = Path(__file__).resolve().parents[1]
RULE_MASTER_CSV = BASE_DIR / "02_rule_master" / "bim_rule_master_v001.csv"


# =========================================
# Functions
# =========================================

def load_rule_master() -> pd.DataFrame:
    """Load the RuleId master CSV."""
    if not RULE_MASTER_CSV.exists():
        raise FileNotFoundError(f"Rule master CSV not found: {RULE_MASTER_CSV}")

    return pd.read_csv(RULE_MASTER_CSV, encoding="utf-8-sig")


def search_rule(rule_master: pd.DataFrame, rule_id: str) -> pd.Series | None:
    """Search rule by RuleId."""
    rule_id = rule_id.strip().upper()
    matched = rule_master[rule_master["RuleId"].str.upper() == rule_id]

    if matched.empty:
        return None

    return matched.iloc[0]


def print_rule(rule: pd.Series) -> None:
    """Print rule details."""
    print("\n=========================================")
    print("RuleId検索結果")
    print("=========================================")
    print(f"RuleId        : {rule.get('RuleId', '')}")
    print(f"RuleName      : {rule.get('RuleName', '')}")
    print(f"Category      : {rule.get('Category', '')}")
    print(f"Severity      : {rule.get('Severity', '')}")
    print(f"TargetField   : {rule.get('TargetField', '')}")
    print(f"CheckLogic    : {rule.get('CheckLogic', '')}")
    print(f"BusinessImpact: {rule.get('BusinessImpact', '')}")
    print(f"AIUseImpact   : {rule.get('AIUseImpact', '')}")
    print(f"FixGuide      : {rule.get('FixGuide', '')}")
    print(f"Reference     : {rule.get('Reference', '')}")
    print("=========================================\n")


# =========================================
# Main process
# =========================================

def main() -> None:
    print("RuleId lookup demo started.")
    print(f"Rule master: {RULE_MASTER_CSV}")

    rule_master = load_rule_master()

    while True:
        rule_id = input("\n検索したいRuleIdを入力してください。終了する場合は q を入力してください: ")

        if rule_id.strip().lower() == "q":
            print("RuleId lookup demo finished.")
            break

        rule = search_rule(rule_master, rule_id)

        if rule is None:
            print(f"\n該当するRuleIdが見つかりません: {rule_id}")
            print("例：R-001, R-002, R-003")
        else:
            print_rule(rule)


if __name__ == "__main__":
    main()