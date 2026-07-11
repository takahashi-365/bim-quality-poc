
  README.md:9:This portfolio demonstrates how BIM implementation support experience can be extended into construction AI / data utilization support by preparing Revit-derived BIM data for BI, RAG, and human-reviewed AI assistance.
  README.md:10:
> README.md:11:Revit集計表から書き出したTXT、Room Schedule TXT、pyRevitで取得した選択要素メタデータCSVをPythonで処理し、RuleIdベースの品質チェック、QualityScore算出、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlitによる簡易可視化、ローカルLLMによる説明文生成デモ、RAG / Azure AI Search構成検討、FixPriority教師データ設計までを扱っています。
  README.md:12:
  README.md:13:本PoCの目的は、AIに設計判断・施工判断・法規判断をさせることではありません。
  README.md:34:AI Context JSON / Markdown生成
  README.md:35:Fix Guide Markdown生成
> README.md:36:Streamlitによる簡易可視化
  README.md:37:ローカルLLMによる説明文生成デモ
  README.md:38:pyRevitによるElementId / UniqueId取得MVP
  README.md:39:RAG / Azure AI Search向けの構成検討
  README.md:40:FixPriority教師データの列設計・ラベル方針整理
> README.md:41:pytestによる主要ロジックの検証
  README.md:42:```
  README.md:43:
  README.md:127:* RAG / Azure AI Searchを想定したチャンク設計・メタデータ設計を行うこと
  README.md:128:* FixPriorityを将来的な教師データ候補として扱うための列設計・ラベル方針を整理すること
> README.md:129:* pytestで主要ロジックを検証すること
  README.md:130:
  README.md:131:---
  README.md:290:## Demo Screenshots
  README.md:291:
> README.md:292:### Streamlit - AI Readiness Assessment
  README.md:293:
  README.md:294:AI Readiness Score、AI Readiness Level、HumanReviewRequired、ElementId別スコアを確認できる画面です。
  README.md:295:
> README.md:296:![Streamlit AI Readiness Assessment](07_portfolio/screenshots/streamlit_ai_readiness_overview_v001.png)
  README.md:297:
> README.md:298:### Streamlit - AI Context v002 Preview
  README.md:299:
  README.md:300:品質チェック結果、特徴量データセット、AI Readiness Scoreをもとに生成した、AI向け構造化コンテキストを確認できる画面です。
  README.md:301:
> README.md:302:![Streamlit AI Context v002 Preview](07_portfolio/screenshots/streamlit_ai_context_preview_v001.png)
  README.md:303:
> README.md:304:### Streamlit - Fix Guide Preview
  README.md:305:
  README.md:306:RuleId、Severity、AIReadinessImpact、HumanReviewRequiredをもとに生成した、人間確認向けの修正ガイドを確認できる画面です。
  README.md:307:
> README.md:308:![Streamlit Fix Guide Preview](07_portfolio/screenshots/streamlit_fix_guide_preview_v001.png)
  README.md:309:
  README.md:310:### Revit Sample Model
  README.md:317:### Revit Schedule Used
  README.md:318:
> README.md:319:本PoCでは、Revit集計表 `20 ドア 建具表 SD` をTXTとして書き出し、Python処理の入力データとして使用しています。
  README.md:320:
  README.md:321:![Revit door schedule](07_portfolio/screenshots/revit_door_schedule_view.png)
  README.md:387:## Tests
  README.md:388:
> README.md:389:pytestで主要ロジックの最小テストを作成しています。
  README.md:390:
  README.md:391:主なテスト：
  README.md:399:```
  README.md:400:
> README.md:401:実行：
  README.md:402:
  README.md:403:```powershell
> README.md:404:$env:PYTHONPATH = "."
> README.md:405:pytest -q
  README.md:406:```
  README.md:407:
  README.md:421:
  README.md:422:```text
> README.md:423:Python
  README.md:424:pandas
> README.md:425:pytest
> README.md:426:Streamlit
  README.md:427:Markdown
  README.md:428:CSV
  README.md:541:## Summary
  README.md:542:
> README.md:543:本PoCでは、Revit / BIMデータを対象に、Pythonによるデータ変換、データクレンジング、RuleIdベース品質チェック、QualityScore算出、AI Readiness Score算出、生成AI向け構造化コンテキスト生成、Fix Guide Markdown生成、Streamlit簡易可視化、Local LLM説明文生成デモ、pyRevitメタデータ取得、RAG構成検討、FixPriority教師データ設計、pytestによる最小テストまでを整理しました。
  README.md:544:
  README.md:545:目的は、AIモデルそのものを作ることではなく、BIMデータをBI、データ分析、将来的な機械学習、生成AI、RAGで安全に活用するための前処理、品質評価、構造化、修正ガイド生成、人間レビュー設計の流れを示すことです。


