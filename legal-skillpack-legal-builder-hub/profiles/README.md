# 管理配置模板

本目录保存智能体框架中立的业务规范定义。Profile 用来替代上游 `CLAUDE.md` 中的用户配置，但不保留 Claude 专属路径。

## 解析规则

智能体框架按以下顺序解析 profile：

1. 智能体框架显式传入的 profile。
2. `LEGAL_AGENT_PROFILE_HOME/<practice>/profile.md`。
3. 当前工作区中的 profile。
4. `skillpack/profiles/templates/<practice>/profile.md` 模板。

如果 profile 仍包含 `[PLACEHOLDER]`，涉及实质法律分析的 skill 或 workflow 必须停止并要求先完成配置。

## 跨集群 共享层：`company-profile.md`

**单文件，全 cluster 共享**——存放与具体 cluster 无关的事实（公司名 / 行业 / 规模 / 法域 / 监管足迹 / 风险偏好 / 升级链）。

```text
$LEGAL_AGENT_PROFILE_HOME/company-profile.md   ← 跨集群 共享层
$LEGAL_AGENT_PROFILE_HOME/<practice>/profile.md ← 每 cluster 各自的 profile（playbook / 风格 / 案件工作区）
```

**Canonical 模板**：[`templates/company-profile.md`](templates/company-profile.md)（中文化适配中国监管语境，32+ 行，含跨集群 字段影响表）

**架构特征**：
- 当前 **7 cluster / 12 SKILL.md** 引用本文件：commercial / privacy / regulatory / employment / ai-governance / litigation 都读写；law-student / prc-legal-research 不读取
- **6 个 cold-start-interview 都可写入它**（第一个跑的 cluster 创建，其余 cluster 读取）
- **任何 cluster 的 customize 都可更新它**，但必须按以下纪律：
  1. 明示跨集群 影响（diff 中列出受影响 集群）
  2. 法定下限拒绝降低（风险 / 升级链字段）
  3. 重大变更需用户显式确认（如 `主要法域` / `执业场景` / `规模`）

**profile.json 中的 `source: "company"` 标记**：表示该 section 来自共享层（如 `ai-governance-legal.profile.json` 的 `company-basics` section / `litigation-legal.profile.json` 的 `company-basics`）。本机解析时该 section 从 `$LEGAL_AGENT_PROFILE_HOME/company-profile.md` 提取，而非 `<practice>/profile.md`。

**与上游对应关系**：上游 `claude-for-legal/references/company-profile-template.md` 是原型（32 行英文）；本 skillpack 的中文化版做了 4 项增强：
1. 中国监管语境（国家网信办 / 证监会 / 市监局 / 公安部 / 工信部 / 国家数据局 / 知识产权局）
2. 跨集群 字段影响表（哪个字段影响哪个 cluster 的哪个 skill）
3. 不读取本文件的 cluster 显式列出（law-student / prc-legal-research）
4. 更新协议明示（customize 纪律 + 跨集群 变更确认门）

## 已落地模板

| Practice | Manifest | Template |
|---|---|---|
| 商事合同法务 | `commercial-legal.profile.json` | `templates/commercial-legal/profile.md` |
| 数据隐私与个人信息保护法务 | `privacy-legal.profile.json` | `templates/privacy-legal/profile.md` |
| 监管合规法务 | `regulatory-legal.profile.json` | `templates/regulatory-legal/profile.md` |
| 劳动用工法务 | `employment-legal.profile.json` | `templates/employment-legal/profile.md` |
| 中国法法律研究 | `legal-research-cn.profile.json` | `templates/legal-research-cn/profile.md` |
| AI 治理合规 | `ai-governance-legal.profile.json` | `templates/ai-governance-legal/profile.md` |
| 诉讼业务管理 | `litigation-legal.profile.json` | `templates/litigation-legal/profile.md` |

中国法法律研究 profile 为 placeholder——它的实际配置由所属 MCP（元典 + Tavily）管理，本仓库只占位说明边界。

AI 治理合规 profile 9 大节：公司基础信息 / AI 活动角色 / 监管足迹 / 红线 / 用例注册表 / 供应商立场 / 政策承诺 / 备案状态 / 集成状态——基于 11 部中国 AI 法规重写自上游。

诉讼业务管理 profile 9 大节：公司概况 / 使用者 / 执业角色（法务 / 律所律师 / 独立执业）/ 立场（原告 / 被告 / 混合）/ 风险校准 / 执业背景 / 文书风格 / 案件工作区 / 集成状态——基于 10 部中国诉讼法规翻译 + 9 个 cn-law-overlay 重写自上游。

## 与 connector 的关系

- 存储、合同库和工作成果使用本地目录 connector（`local-legal-storage`）。
- 中国法律法规查询使用元典法律法规 MCP（`yuandian-law`）。
- 中国案例查询使用元典案例 MCP（`yuandian-case`）。
- 中国企业信息查询使用元典企业 MCP（`yuandian-company`）。
- 中国法二手文献使用 Tavily MCP（`tavily`，含 14 律所 + 10 政府 + 10 学术 include_domains 白名单）。
- 美国法等非中国大陆法实质研究**不在本 skillpack 覆盖范围**——请走当地商业法律研究服务（Westlaw / LexisNexis / CoCounsel 等）或当地律所。
- 对外发送不自动执行，走 `runtime-notification` 的 `notification.preview_and_send`，逐次预览 + 用户确认。
