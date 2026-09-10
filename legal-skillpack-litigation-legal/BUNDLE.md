# 诉讼业务管理 套件

- 套件 ID: `litigation-legal`
- Skill 数量: 19
- 入口 skill: `litigation-matter-intake`

## 简介

中国诉讼业务管理 skill 集群——以 19 个 skill 覆盖案件组合管理、催告函体系、证据 / 时间线 / 要件分析、调查令分流、庭审准备、外聘律师协调和文书起草。基于《民事诉讼法（2023 修正）》《最高人民法院民事诉讼证据规定（2019 修正）》《民法典》《民诉法解释（2022 修正）》《个人信息保护法》《律师法》《专利法》《劳动合同法》《保险法》《会计档案管理办法》等 10 部现行法律法规，对 catalog 中已有 cluster 形成「诉讼前 (demand-* / matter-intake / legal-hold) → 诉讼中 (chronology / claim-chart / deposition-prep / brief-section-drafter / subpoena-triage) → 调度 (matter-update / matter-briefing / oc-status / portfolio-status / privilege-log-review) → 结案 (matter-close)」全闭环。原告 / 被告立场二分，法务 / 律所律师 / 独立执业角色三分，必须 per-case 判断。19 skill 中 10 个为翻译等价迁移、9 个为中国法 overlay（demand-* / chronology / claim-chart / deposition-prep / legal-hold / subpoena-triage / brief-section-drafter）。

## 包含的 skill

- `litigation-brief-section-drafter`
- `litigation-chronology`
- `litigation-claim-chart`
- `litigation-cn-evidence-review`
- `litigation-cold-start-interview`
- `litigation-customize`
- `litigation-demand-draft`
- `litigation-demand-intake`
- `litigation-demand-received`
- `litigation-deposition-prep`
- `litigation-legal-hold`
- `litigation-matter-briefing`
- `litigation-matter-close`
- `litigation-matter-intake`
- `litigation-matter-update`
- `litigation-matter-workspace`
- `litigation-oc-status`
- `litigation-portfolio-status`
- `litigation-subpoena-triage`

## 套件说明

- Cluster 入口：`litigation-matter-intake`——新案件登记 + 利益冲突门控；若是收到催告函则改走 `litigation-demand-received`。任何业务 skill 在 profile 未完成时一律重定向到 `litigation-cold-start-interview`。
- **仅中国大陆诉讼法规**。涉外 / 跨境诉讼请使用对应区域工具或当地律所；FRCP / Federal Rules of Evidence / Zubulake / IPR 等美国法概念不适用。
- 原告 vs 被告立场二分：同一公司在不同案件可承担不同立场，必须 per-case 判断；demand-draft / demand-received / chronology / claim-chart 都按立场分流。
- 9 个翻译等价 skill（cold-start-interview / customize / matter-* × 5 / oc-status / portfolio-status）保留原版行为契约；10 个中国法 overlay skill（brief-section-drafter / chronology / claim-chart / demand-* × 3 / deposition-prep / legal-hold / subpoena-triage / privilege-log-review）有实质法律逻辑重写。（注：privilege-log-review 原 intake 标为翻译版，实际为「证据三性审查」cn-law-overlay，本项目已更正分类）
- **核心法律差异**：（1）和解通讯保护——《民诉法解释》第 107 条仅覆盖诉讼中，诉前催告函不自动受保护；（2）保密制度——《律师法》（2026修正）第 41 条是义务而非权利，无 attorney-client privilege / work product doctrine；（3）专利无效程序——拆分为 `--invalidity-cnipa`（国知局行政程序）和 `--invalidity-court`（法院诉讼无效抗辩）；（4）调查令——5 类（法院调查令 / 律师调查令 / 行政协查 / 证人出庭 / 监察委-刑事侦查）；（5）证据保存义务——非法定 legal hold，定性为企业内部最佳实践；（6）无 Rule 30(b)(6) 代表性证人制度。
- PIPL 第 41 条跨境提供禁止：境外司法 / 执法机构要求提供境内个人信息须经主管机关批准（subpoena-triage 必检风险点）。
- 律师调查令各省差异：无上位法统一规范，subpoena-triage 附录 B-2 列出广东 / 上海 / 北京参考；其他省份标 `[模型知识——需验证]`，使用时通过元典确认当地现行规定。
- 来源标签：`[国家法律法规数据库]` / `[最高人民法院]` / `[元典]` / `[裁判文书网]` / `[人民法院案例库]` / `[威科先行]` / `[北大法宝]` / `[法律法规官网]` / `[用户提供]` / `[模型知识——需验证]` / `[已核实——最后确认 YYYY-MM-DD]`。
- 交接路径：demand-received 上报到刑事/监察 → commercial-escalation-flagger；chronology / claim-chart 涉及个人信息 → privacy-pia-generation；subpoena-triage 触发跨境数据 → privacy-cross-border；matter-* 涉及合同审查 → commercial-contract-review。
- Known gaps（按 notes.md gap-01..04）：律师调查令各省规定（gap-01，medium）/ chronology 特权表述（gap-02，medium）/ ~~privilege-log-review 翻译版残留特权概念（gap-03，low）~~——已核查 gap-03 与实际不符：实为「证据三性审查」cn-law-overlay / 仲裁机构程序对比（gap-04，low）。其余后续版本逐项补全。
- `litigation-customize` 由研究员直接翻译，保留原版行为；矩阵参考 commercial-customize / privacy-customize / ai-governance-customize。
