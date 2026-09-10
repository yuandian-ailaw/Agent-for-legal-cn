# AI 治理合规 套件

- 套件 ID: `ai-governance-legal`
- Skill 数量: 9
- 入口 skill: `ai-governance-use-case-triage`

## 简介

中国 AI 治理合规 skill 集群——基于《生成式 AI 暂行办法》《算法推荐管理规定》《深度合成管理规定》《PIPL》《数据安全法》《网安法 2025 修正》《网络数据安全管理条例》《人脸识别办法》《内容标识办法》《伦理审查办法》11 部现行法规为依据。9 个 skill 形成「冷启动配置 → profile 单点调整 → 用例分类 → 影响评估 → 供应商审查 → 法规差距 → 政策监控 → 政策起草 → 系统清单」全闭环。Provider / Deployer 角色二分，L1-L4 合规等级，备案触发（算法 / 生成式 AI / 人脸信息）三类专项追踪。

## 包含的 skill

- `ai-governance-aia-generation`
- `ai-governance-cold-start-interview`
- `ai-governance-customize`
- `ai-governance-inventory`
- `ai-governance-policy-monitor`
- `ai-governance-policy-starter`
- `ai-governance-reg-gap-analysis`
- `ai-governance-use-case-triage`
- `ai-governance-vendor-ai-review`

## 套件说明

- Cluster 入口：`ai-governance-use-case-triage`——对拟议 AI 用例做合规分类（审批通过 / 有条件审批 / 不审批）。任何业务 skill 在 profile 未完成时一律重定向到 `ai-governance-cold-start-interview`。
- **仅中国大陆 AI 治理法规**。其他法域（EU AI Act / NIST AI RMF / 美国行政命令等）请使用对应区域工具或当地律所。
- Provider vs Deployer 角色二分：同一公司对不同 AI 系统可能承担不同角色，必须 per-system 判断，不可整体打标。
- 11 部 AI 法规中 4 部 2025 年新生效、1 部 2026 年生效、1 部 2026-07-15 施行施行（拟人化互动办法，现行有效）；未施行结论必须标 `[尚未施行 - 复核于施行后]`。
- 备案触发：算法备案（《算法推荐管理规定》第 24 条）/ 生成式 AI 服务备案（《生成式 AI 暂行办法》第 17 条）/ 人脸信息备案（《人脸识别办法》第 15 条，存储 ≥ 10 万人触发）三类专项追踪；插件识别触发，不代替办理。
- AICA（AI Compliance Assessment）替代原版 EU AIA/FRIA：8 大监管框架逐法规分析 + L1-L4 合规等级 + 行动计划 P0/P1/P2。
- 来源标签三级分级：`[国家法律法规数据库]` / `[元典检索 YYYY-MM-DD]` / `[references/ 已下载法规]` / `[最高人民法院]` / `[监管机构官网]` / `[地方人大]` / `[律所文章]`（参考级来源，仅作框架对照）/ `[需核验]` / `[模型知识 — 需核验]`。
- 交接路径：vendor-ai-review 发现合规风险 → commercial-escalation-flagger（上报到 GC）；aia-generation 涉及个人信息 → privacy-pia-generation；reg-gap-analysis 识别新法规 gap → regulatory-policy-diff（监管集群）。
