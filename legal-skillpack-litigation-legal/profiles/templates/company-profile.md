# 公司画像（跨集群 共享）

*所有 cluster 共享此文件。第一个跑 cold-start-interview 的 cluster 写入它；其它 cluster 读取它。运行任何 cluster 的 cold-start-interview 或 customize 都可更新本文件，但请阅读下方「跨集群 共享字段」段——某些字段改动会传播到多个 cluster 的下游 skill。*

---

**执业场景：** [独立执业 / 小所 | 中大型律所 | 企业内法务 | 政府 / 法律援助 / 学校诊所]
**机构 / 实体名称：** [公司或律所名称]
**行业 / 主营业务：** [公司所做的事 / 律所的主要执业领域]
**对外提供：** [产品 / 服务 / 服务对象，或律所写「不适用」]
**规模：** [员工 / 律师 / 相关人数]

## 地域与监管足迹

**业务覆盖法域：** [如 中国大陆（上海 / 北京 / 深圳 / 杭州）/ 香港 / 新加坡 / 欧盟 / 美国]
**主要法域：** [大部分工作发生在哪里]
**适用监管：** [国家网信办 / 证监会 / 市监局 / 公安部 / 工信部 / 国家数据局 / 知识产权局 / 国家安全部 / 海关总署 / EDPB / OAIC 等——只填实际适用的]
**当前监管事项：** [立案调查 / 监管问询 / 备案窗口，或填「无」]

## 风险姿态

**总体风险偏好：** [保守 / 中间 / 激进]
**最让团队睡不着的事：** [那个一旦发生就是灾难日的事项]
**领导层最常问的问题：** [或「未确定」]

## 关键人员

**法务总监 / 总法律顾问：** [姓名]
**升级链：** [姓名 → 姓名 → 姓名，或「每个 cluster 单独设置」]

---

## 跨集群 共享字段说明

本文件的字段会被多个 cluster 的 skill 读取，影响范围：

| 字段 | 影响 cluster | 具体下游 skill |
|---|---|---|
| `执业场景` | 全部业务 cluster | commercial-contract-review / employment-* / litigation-* 按法务 / 律所 / 独立执业分流默认工作流 |
| `行业 / 主营业务` | 商事 / 隐私 / AI 治理 | commercial 选行业 playbook；privacy / ai-governance 判定监管适用范围 |
| `规模` | 隐私 / 监管 / AI 治理 | PIPL 100 万人门槛 / 监管 CIIO 判定 / AI 治理算法备案 100 万用户门槛 |
| `业务覆盖法域` | 全部业务 cluster | 商事跨境合同 / 隐私 PIPL 第 38-40 出境机制 / 劳动用工地方法规 / 诉讼跨境调查令 PIPL 第 41 条 / AI 治理跨境算法 |
| `主要法域` | 全部业务 cluster | 决定默认引用的法条体系（中国大陆为主） |
| `适用监管` | 监管 / AI 治理 / 隐私 | feed-watcher / policy-monitor / use-case-triage 过滤监管渠道 |
| `当前监管事项` | 监管 / 商事升级 | regulatory-feed-watcher / commercial-escalation-flagger 优先级排序 |
| `风险偏好` | 全部业务 cluster | 影响 demand-draft / vendor 审查门槛 / AI 治理立场（严格 / 标准 / 基准）/ NDA RED/YELLOW/GREEN 阈值 |
| `升级链` | 全部业务 cluster | escalation-flagger / 任何 attorney-gate 都按此处定义路由 |

**不读取本文件的 cluster**：
- `law-student`：学生场景，读取学校 / 法考 / 学习风格字段（在 `$LEGAL_AGENT_PROFILE_HOME/law-student/profile.md`），不读取本文件
- `prc-legal-research`：研究工具 cluster，profile 由 vendor MCP 管理，不读取本文件

## 更新协议

**任何 cluster 的 customize 都可以更新本文件**，但必须按以下纪律：

1. **明示跨集群 影响**：customize 在写入前的 diff 中标注「此变更将影响 X 个 cluster 的下游 skill 输出」，列出受影响 cluster 列表
2. **法定下限拒绝降低**：风险偏好 / 升级链等关键字段，customize 在写入前先检查是否符合 profile manifest 的 `guardrails.attorney_contact_required` 等约束
3. **重大跨集群 变更需用户显式确认**：如 `主要法域` / `执业场景` / `规模` 改变时，customize 提示「请确认你了解此变更会触发 X 个 cluster 重新评估」，等用户输入「确认」后才写入

---

*每个 cluster 的业务规范（playbook / 审查框架 / 文书风格 / 案件工作区）存在各自的 profile 文件中（`$LEGAL_AGENT_PROFILE_HOME/<practice>/profile.md`），跟本文件并存。本文件存放与具体 cluster 无关的事实。*

*智能体框架解析顺序：runtime_provided > `$LEGAL_AGENT_PROFILE_HOME/company-profile.md`（本模板）> 工作区中的 profile > 模板兜底*

*技术细节见：[`skillpack/profiles/README.md`](../README.md) 跨集群 共享层章节。*
