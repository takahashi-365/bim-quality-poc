# このファイルの目的：
# RuleIdに紐づくBIM品質ルールをもとに、
# 生成AIへ渡すためのプロンプト文を作成するデモ。
#
# 主な処理フロー：
# 1. BIM品質ルールマスターを読み込む
# 2. ユーザーが入力したRuleIdを受け取る
# 3. RuleIdに対応するルール情報を取得する
# 4. 生成AI向けのプロンプト文を作成する
# 5. 作成したプロンプトを表示する
# 6. 必要に応じてtxtファイルとして保存する

from pathlib import Path
from datetime import datetime

import pandas as pd


# =========================================
# Path settings
# =========================================

BASE_DIR = Path(__file__).resolve().parents[1]
RULE_MASTER_CSV = BASE_DIR / "02_rule_master" / "bim_rule_master_v001.csv"
OUTPUT_DIR = BASE_DIR / "06_ai_demo" / "generated_prompts"


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


def build_ai_prompt(rule: pd.Series) -> str:
    """Build a prompt for generative AI using only the selected rule."""

    prompt = f"""
あなたは建設業界のBIM標準化・BIMデータ品質管理を支援するアシスタントです。

以下のBIM品質ルールだけを参照して回答してください。
資料にない内容は断定せず、「追加確認が必要」と表現してください。
設計判断・施工判断・モデル修正の最終判断は、人間のBIM担当者または責任者が行う前提で回答してください。

# 参照ルール

RuleId: {rule.get("RuleId", "")}
RuleName: {rule.get("RuleName", "")}
Category: {rule.get("Category", "")}
Severity: {rule.get("Severity", "")}
TargetField: {rule.get("TargetField", "")}
CheckLogic: {rule.get("CheckLogic", "")}
BusinessImpact: {rule.get("BusinessImpact", "")}
AIUseImpact: {rule.get("AIUseImpact", "")}
FixGuide: {rule.get("FixGuide", "")}
Reference: {rule.get("Reference", "")}

# 回答してほしい内容

1. このルールの内容
2. 違反が発生した場合の業務影響
3. 修正方法
4. AI活用時に注意すべき点
5. 人間が最終確認すべき点
6. 参照元RuleId

# 回答条件

- 参照ルールに書かれている内容を優先する
- 参照元RuleIdを必ず明記する
- 資料にない内容は断定しない
- 自動修正を前提にしない
- BIMマネージャーやRevit運用支援担当に説明する想定で、簡潔に整理する
""".strip()

    return prompt


def save_prompt(rule_id: str, prompt: str) -> Path:
    """Save generated prompt as txt file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"prompt_{rule_id}_{timestamp}.txt"

    output_file.write_text(prompt, encoding="utf-8")

    return output_file


def print_rule_summary(rule: pd.Series) -> None:
    """Print selected rule summary."""
    print("\n=========================================")
    print("選択されたRuleId")
    print("=========================================")
    print(f"RuleId   : {rule.get('RuleId', '')}")
    print(f"RuleName : {rule.get('RuleName', '')}")
    print(f"Severity : {rule.get('Severity', '')}")
    print(f"FixGuide : {rule.get('FixGuide', '')}")
    print("=========================================\n")


# =========================================
# Main process
# =========================================

def main() -> None:
    print("RuleId prompt generator demo started.")
    print(f"Rule master: {RULE_MASTER_CSV}")

    rule_master = load_rule_master()

    while True:
        rule_id = input("\nプロンプトを作成したいRuleIdを入力してください。終了する場合は q を入力してください: ")

        if rule_id.strip().lower() == "q":
            print("RuleId prompt generator demo finished.")
            break

        rule = search_rule(rule_master, rule_id)

        if rule is None:
            print(f"\n該当するRuleIdが見つかりません: {rule_id}")
            print("例：R-001, R-002, R-003")
            continue

        rule_id_normalized = rule.get("RuleId", "")
        print_rule_summary(rule)

        prompt = build_ai_prompt(rule)

        print("=========================================")
        print("生成AIに渡すプロンプト")
        print("=========================================")
        print(prompt)
        print("=========================================\n")

        save_answer = input("このプロンプトをtxtファイルとして保存しますか？ y/n: ")

        if save_answer.strip().lower() == "y":
            output_file = save_prompt(rule_id_normalized, prompt)
            print(f"\nプロンプトを保存しました: {output_file}")
        else:
            print("\nプロンプトは保存しませんでした。")


if __name__ == "__main__":
    main()