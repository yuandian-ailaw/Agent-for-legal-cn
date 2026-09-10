# 法学学习与法考备考 套件

- 套件 ID: `law-student`
- Skill 数量: 13
- 入口 skill: `law-student-session`

## 简介

中国法学学习 skill 集群——以 13 个 skill 覆盖法学院学习场景（本科 / 法硕 / 法学硕士 / 法学博士）和国家统一法律职业资格考试（法考）备考。基于 8 部中国法律 / 司法解释 / 监管文件（《律师法》《国家统一法律职业资格考试实施办法》《最高人民法院关于案例指导工作的规定》《最高人民法院关于统一法律适用加强类案检索的指导意见》《立法法（2023 修正）》《民事诉讼法》《行政诉讼法》/ GB/T 7714-2015）+ 元典 API 平台（yuandian-law / yuandian-case）作为检索支撑。13 skill 中 1 个为翻译（customize）+ 12 个为中国法 overlay（覆盖 MBE/UBE/NextGen → 法考 / 判例法 → 成文法 / 1L-3L → 本科-硕士-博士 / Bluebook → GB/T 7714 / Westlaw + CourtListener → 元典 / IRAC → IRAC + 鉴定式分析法 + 三段论 / attorney-client privilege → 《律师法》（2026修正）第 41 条保密义务）。

## 包含的 skill

- `law-student-bar-prep-questions`
- `law-student-case-brief`
- `law-student-cold-call-prep`
- `law-student-cold-start-interview`
- `law-student-customize`
- `law-student-exam-forecast`
- `law-student-flashcards`
- `law-student-irac-practice`
- `law-student-legal-writing`
- `law-student-outline-builder`
- `law-student-session`
- `law-student-socratic-drill`
- `law-student-study-plan`

## 套件说明

- Cluster 入口：`law-student-session`——单次集中学习会话（N 道题 / N 张记忆卡片，按科目）。首次使用需先跑 `law-student-cold-start-interview` 填 profile。
- **学习工具，不是法律咨询**——本 cluster 仅供法学院学生学习和法考备考。所有 skill 输出标 `学习笔记 — 不构成法律意见`。真实当事人事项触发即暂停并重定向。学术诚信：插件输出不得作为评分作业提交。
- **仅中国大陆法学体系**——其他法域（美国法 J.D. / 英国法 LLM / 欧盟法）请走当地法学院学习工具或教师辅导。
- 13 个 skill 涵盖：1) **学习准备**（cold-start-interview / customize）；2) **题目练习**（bar-prep-questions / socratic-drill / session）；3) **写作反馈**（case-brief / irac-practice / legal-writing / outline-builder）；4) **课堂准备**（cold-call-prep）；5) **应试规划**（study-plan / exam-forecast / flashcards）。
- **核心法律差异**：（1）考试体系——MBE / UBE / NextGen → 法考客观题 + 主观题，去掉管辖权分流（中国法考是统一考试）；（2）案例体系——判例法案例摘要 → 中国案例体系（指导性 / 典型 / 公报 / 普通），**法条优先级高于判例**；（3）法学教育体系——1L / 2L / 3L → 中国本科 / 法硕 / 法学硕士 / 法学博士；（4）写作框架——保留 IRAC 同时新增**鉴定式分析法**（中国民法教学法）和**三段论**；（5）保密制度——attorney-client privilege → 《律师法》（2026修正）第 41 条保密义务（不构成 work product doctrine）；（6）引用规范——Bluebook → GB/T 7714-2015 国家标准 + 《法学引注手册》。
- **法考核心**：客观题（单选 / 多选 / 不定项）+ 主观题（案例分析 / 法律文书 / 论述）。study-plan / bar-prep-questions / exam-forecast 三个 skill 共同支撑长期备考节奏。客观题日期 / 主观题日期由 profile.bar-prep 节捕获。
- **Socratic / 讲解型双模式**：socratic-drill / case-brief / cold-call-prep / irac-practice / legal-writing 都按 profile.learning-style 分流——追问型先要求学生陈述，讲解型先讲解再测试。
- **绝不代写**——所有 skill 提供脚手架 / 反馈 / 追问，不生成最终大纲 / 论文 / 案例分析答卷。学生自己写，插件标记问题。
- 来源标签：`[元典 API]` / `[裁判文书网]` / `[人民法院案例库]` / `[国家法律法规数据库]` / `[国家标准]` / `[用户提供]` / `[模型知识 — 需验证]` / `[已确认 — 最后确认 YYYY-MM-DD]`。
- 交接路径：study-plan + exam-forecast 输出加权科目 → 进 bar-prep-questions / session 做练习；case-brief / outline-builder 输出 → 进 socratic-drill 测试掌握；legal-writing / irac-practice 反馈 → 学生修改后重试。
- Known gaps（按 notes.md gap-01..03）：法考历年真题无专门 API（gap-01，medium）/ 元典 API 三个 MCP Server 尚未实际跑通（gap-02，low）/《法学引注手册》最新版本未核实（gap-03，low）——后续版本逐项补全。
