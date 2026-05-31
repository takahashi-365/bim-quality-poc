# Rule Specification

## BIM Data Quality Engineering & AI Analysis PoC

## この資料の目的

この資料は、`BIM Data Quality Engineering & AI Analysis PoC` で使用する RuleId ルールマスタの仕様を整理するための資料です。

RuleId は、BIM品質チェック、チェック結果CSV、Power BIによる補助的可視化、RuleId検索デモ、生成AI向け構造化コンテキスト生成を接続するための共通キーとして使用します。

この資料では、RuleIdルールマスタの各列の意味、初期ルールの内容、Severityの考え方、今後の拡張方針を整理します。

---

## 1. RuleIdルールマスタの位置づけ

RuleIdルールマスタは、BIM品質チェックに使用するルールを外部CSVとして管理するためのファイルです。

現時点では、以下のファイルをルールマスタとして使用しています。

`02_rule_master/bim_rule_master_v001.csv`

このルールマスタは、以下の処理で共通利用します。