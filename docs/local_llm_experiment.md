# Local LLM Experiment

## Purpose

このドキュメントは、第3段階A：Local LLM Explanation Demo の実験記録である。

本実験では、第2段階PoCで生成した `AI Context v002` と `Fix Guide Markdown` をローカルLLMに入力し、BIM担当者向けの説明文を生成できるかを確認する。

目的は、LLMの性能比較ではなく、`AI Context v002` が説明生成用の構造化コンテキストとして利用できるかを検証することである。

LLMの回答は参考情報として扱い、最終判断はBIM担当者または人間のレビュー担当者が行う。

---

## Experiment Environment

| 項目      | 内容                                                    |
| ------- | ----------------------------------------------------- |
| 実行日     | 2026-06-13                                            |
| 実行環境    | LM Studio                                             |
| 実行区分    | Formal experiment                                     |
| OS      | Windows 11 Home                                       |
| CPU     | Core i7-12700                                         |
| RAM     | 64GB                                                  |
| GPU     | ZOTAC GAMING GeForce RTX 5060 Ti 16GB                 |
| VRAM    | 16GB                                                  |
| SSD     | Nextorage 2TB M.2 NVMe Gen4                           |
| LAN     | 10GBASE-T                                             |
| 電源      | 850W                                                  |
| モデル名    | Gemma 4 E4B                                           |
| 量子化形式   | LM Studio上で取得したモデル設定に従う                               |
| コンテキスト長 | LM Studio上の既定設定                                       |
| 入力ファイル  | `06_local_llm/local_llm_prompt_input_sample_v001.md`  |
| 出力記録    | `06_local_llm/local_llm_explanation_examples_v001.md` |
| 備考      | ノートPCで事前確認後、AIデスクトップPCで正式実験を実施                        |

---

## Pre-check

正式実験の前に、ノートPCでLM Studioの起動確認と簡単な日本語応答確認を行った。

| 項目   | 内容               |
| ---- | ---------------- |
| 実行区分 | Pre-check        |
| 実行環境 | ノートPC            |
| 実行環境 | LM Studio        |
| モデル名 | Gemma 4 E4B      |
| 確認内容 | 短い日本語プロンプトへの応答確認 |
| 結果   | 日本語応答を確認         |

このPre-checkは、正式なRaw LLM Outputとしては扱わない。
正式な出力記録には、AIデスクトップPCで実行した結果を使用する。

---

## Input

今回の入力は、`AI Context v002` 全文ではなく、ElementId 1件分に限定した。

| 項目                  | 内容                                                   |
| ------------------- | ---------------------------------------------------- |
| 対象ElementId         | 101                                                  |
| Category            | Doors                                                |
| RuleIds             | R-001, R-002, R-003                                  |
| AI Readiness Score  | 40                                                   |
| AI Readiness Level  | Low                                                  |
| HumanReviewRequired | True                                                 |
| Prompt Input        | `06_local_llm/local_llm_prompt_input_sample_v001.md` |

入力は以下の方針に基づいて作成した。

```text
ElementId 1件分のAI Context
+ 該当RuleIdのFix Guide
```

---

## Output

LM Studio上で、`Gemma 4 E4B` に対してPrompt Inputを入力し、BIM担当者向け説明文を生成した。

生成結果はRaw LLM Outputとして、以下に記録した。

```text
06_local_llm/local_llm_explanation_examples_v001.md
```

---

## Evaluation Result

| 評価項目                         | 結果      | コメント                                           |
| ---------------------------- | ------- | ---------------------------------------------- |
| RuleIdに沿って説明できているか           | OK      | R-001、R-002、R-003を拾えている。                       |
| Severityを誤解していないか            | OK      | R-001、R-002を優先度高として扱えている。                      |
| AI Readiness Scoreを正しく扱えているか | OK      | AI Readiness Score 40 / Low として説明できている。        |
| HumanReviewRequiredを明記できているか | OK      | 人間による再確認が必要であることを明記している。                       |
| FixGuideを自然文に変換できているか        | OK      | 必須パラメータ入力、分類コード入力、ファミリ名修正を自然文で説明できている。         |
| 根拠として参照した情報を明示できているか         | OK      | RuleId、Severity、AI Readiness Scoreを根拠として示している。 |
| 余計な設計判断をしていないか               | Partial | 最終判断はBIM担当者と明記しているが、「設計判断」という表現が含まれているため注意が必要。 |
| 存在しない情報を推測していないか             | Partial | 「フロア平面との関連付け」やファミリー名修正例など、入力にない補足が一部含まれている。    |
| BIM担当者向けに分かりやすいか             | OK      | 見出し構成が明確で、BIM担当者向けの説明として読みやすい。                 |
| 最終判断はBIM担当者が行うと明記できているか      | OK      | 最後に、最終的なモデル修正や判断はBIM担当者が行うと明記している。             |

---

## Findings

### 良かった点

* ElementId 101 の品質課題を、BIM担当者向けに分かりやすい文章へ変換できた。
* R-001、R-002、R-003 の各RuleIdを説明に反映できた。
* AI Readiness Score 40 / Low を説明に含めることができた。
* HumanReviewRequired が True であることを明記できた。
* 修正方針を「案」として表現できた。
* 最終判断はBIM担当者が行うという注意を含めることができた。

### 課題

* 入力情報にない具体例が一部追加された。
* 「AIシステムによる自動判定結果」という表現は、Local LLM説明生成デモとしてはやや強い。
* 「設計判断」という表現は、今回の目的であるBIMデータ品質確認から少し広がって見える可能性がある。
* FixGuideにはない具体的な命名例が追加された。

### 今後の改善点

* プロンプトに「入力にない具体例を追加しない」と明記する。
* 「設計判断」ではなく「BIMデータ品質確認・モデル修正方針の確認」と表現させる。
* 「AIシステムによる自動判定結果」ではなく、「既存PoCのルールベース品質チェック結果をもとにした説明」と表現させる。
* Raw OutputとHuman Reviewを分け、LLM出力をそのまま採用しない運用を継続する。
* 必要に応じて、プロンプトテンプレートを改善し、同じElementIdで再実行する。

---

## Handling of Imperfect Outputs

生成結果に誤解、過剰推測、設計判断に近い表現、入力にない情報の補完が含まれた場合も、MVPとしては失敗とは扱わない。

その場合は、以下の改善点として記録する。

* AI Context v002 の情報不足
* Fix Guide の粒度不足
* プロンプトの制約不足
* 入力範囲の切り出し方法
* LLM出力の評価観点
* HumanReviewRequired の表現方法
* 「入力情報からは判断できません」と言わせる制約の不足
* 最終判断はBIM担当者が行うことの明示不足

---

## Result

今回の実験では、`AI Context v002` と `Fix Guide Markdown` をElementId 1件単位でローカルLLMに入力し、BIM担当者向けの説明文を生成できることを確認した。

生成結果には一部改善点があったが、Raw LLM OutputとHuman Reviewを分けて記録することで、LLM出力をそのまま採用せず、人間が評価する運用を示すことができた。

したがって、第3段階AのMVPとしては、`AI Context v002` が説明生成用の構造化コンテキストとして利用可能であることを小さく確認できた。
