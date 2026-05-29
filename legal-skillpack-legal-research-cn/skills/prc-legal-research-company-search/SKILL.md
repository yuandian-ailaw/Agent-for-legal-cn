---
name: prc-legal-research-company-search
description: >
  中国企业信息查询助手。用户需要查询某企业的工商信息、风险状况、诉讼记录、股权信息或
  知识产权时触发。适用场景：基本工商信息查询、风险摸排（失信 / 被执行 / 严重违法 /
  经营异常）、涉诉文书查询、股权冻结 / 出质查询、知识产权查询、企业投资 / 担保关系
  查询。本 skill **仅覆盖中国大陆注册企业**——外国企业不在覆盖范围。
argument-hint: "[企业名称 | 统一社会信用代码 18 位 | 描述查询意图]"
---

# 中国企业信息查询

## 适用范围（先读）

本 skill 通过 `company_data.*` capability 接入元典企业库（`yuandian-company` MCP），**仅中国大陆注册企业**。

**不要在以下场景使用本 skill：**

- **外国企业或非中国大陆注册企业** — 超出元典数据库覆盖范围。
- **港澳台地区企业** — 不在覆盖范围。
- **起草法律文件、表格或模板** — 超出本 skill 范围。
- **执行具体任务的指令** — 超出本 skill 范围。
- **需要查找法律条文** — 建议使用 `prc-legal-research-law-search`。
- **需要查找案例判决** — 建议使用 `prc-legal-research-case-search`。
- **需要综合分析法律问题、输出研究报告** — 建议使用 `prc-legal-research-deep-research`。

## 前置条件 / 连接器探测

`company_data.search_enterprise` / `company_data.fetch_aggregation` / `company_data.fetch_writ_list` / `company_data.fetch_risk_signals` 等 capability（实际由 `yuandian-company` MCP 提供）必须实际连通才能跑。

**严禁仅凭配置文件声明就认为连接器可用**——必须实际探测一次轻量级 capability 成功后才往下走。失败标 `[连接器未核验]` 并停止：

```text
元典企业信息工具未连接（或探测失败）。请确认对应的 MCP 服务器 API 凭据已配置、
网络可达，并在重启 agent 后重试。订阅与凭据问题联系数据源方（元典开放平台
https://open.chineselaw.com/，支持邮箱 yuandianzonghe@thunisoft.com）。
```

## 第一步：定位企业

**已知统一社会信用代码（18 位）或企业 ID**：直接进入第二步。

**已知企业名称（全称或关键词）**：

调用 `yuandian_rh_enterpriseSearch`，参数 `name="企业名称关键词"`。

若返回多家企业，**列出候选列表，请用户确认目标企业后再继续**，不擅自选择。这是消歧门，避免误查同名 / 类似名企业。

## 第二步：查询信息

### 可查询的信息类型与对应 MCP 工具

| 查询类型 | MCP 工具 | 说明 |
|----------|---------|------|
| **基本工商信息** | `yuandian_rh_enterpriseBaseInfo` | 注册资本、法人、地址、股东、核心成员等 |
| **快速风险总览** | `yuandian_rh_enterpriseAggregationSummary` | 18 类信息统计概览（**推荐首选**） |
| **涉诉统计** | `yuandian_rh_enterpriseWritAgg` | 涉诉案件数量分布 |
| **涉诉文书列表** | `yuandian_rh_enterpriseWritList` | 裁判文书列表（分页，每页约 30 条） |
| **开庭公告** | `yuandian_rh_enterpriseCourtSessionNotice` | 即将 / 近期开庭信息 |
| **法院公告** | `yuandian_rh_enterpriseCourtNotice` | 法院发布的公告 |
| **失信被执行人** | `yuandian_rh_enterpriseExecutions` | 老赖名单记录 |
| **被执行人** | `yuandian_rh_enterpriseExecutedPerson` | 被执行人信息 |
| **严重违法** | `yuandian_rh_enterpriseSeriousIllegal` | 严重违法记录 |
| **经营异常** | `yuandian_rh_enterpriseAbnormalOperation` | 经营异常情形 |
| **欠税公告** | `yuandian_rh_enterpriseCorporateTax` | 欠税公告记录 |
| **股权冻结** | `yuandian_rh_enterpriseFrozenEquity` | 股权冻结情况 |
| **股权出质** | `yuandian_rh_enterprisePledge` | 股权出质情况 |
| **对外投资** | `yuandian_rh_enterpriseOutInvest` | 投资标的企业 |
| **对外担保** | `yuandian_rh_enterpriseGuaranty` | 担保承诺信息 |
| **商标信息** | `yuandian_rh_enterpriseBrand` | 商标注册情况 |
| **专利信息** | `yuandian_rh_enterprisePatent` | 专利列表 |
| **软件著作权** | `yuandian_rh_enterpriseSoftRight` | 软著列表 |
| **作品著作权** | `yuandian_rh_enterpriseWorksRight` | 版权列表 |
| **网站备案** | `yuandian_rh_enterpriseIcp` | ICP 备案信息 |
| **变更记录** | `yuandian_rh_enterpriseChangeInfo` | 工商变更历史 |
| **行政处罚** | `yuandian_rh_enterprisePunishment` | 行政处罚记录 |

所有工具均接受 `id`（企业 ID）或 `tyshxydm`（统一社会信用代码）作为主要参数；列表类工具额外支持 `pageNo`（页码，默认 1）。

### 查询策略

**用户未明确指定查询类型时**：
1. 先调用 `yuandian_rh_enterpriseBaseInfo` 获取基本工商信息。
2. 再调用 `yuandian_rh_enterpriseAggregationSummary` 获取风险总览。
3. 根据总览中有数量的类别，提示用户可深入查询。

**用户明确指定查询类型时**：直接调用对应 MCP 工具。

### 关键区分：统计 vs 明细（硬性纪律）

| 用户意图 | 应调用工具 |
|----------|-----------|
| "有多少案件"、"涉诉概览"、"风险摸排" | `yuandian_rh_enterpriseAggregationSummary`（汇总统计） |
| "列出案件"、"涉诉文书列表"、"看案件明细"、"具体案号" | `yuandian_rh_enterpriseWritList`（分页文书列表） |
| "股权冻结情况"、"冻结明细"、"每条冻结记录"、"冻结金额" | `yuandian_rh_enterpriseFrozenEquity`（冻结明细） |
| "股权出质明细"、"出质记录" | `yuandian_rh_enterprisePledge`（出质明细） |

`yuandian_rh_enterpriseAggregationSummary` 只返回各类数量统计，**不包含 per-record 字段**（案号、案由、金额等）。需要记录级别数据时，必须调用对应的专项接口——**不允许**用 aggregation 接口的统计数充当明细。

## 第三步：输出结果

以清晰格式在对话中直接呈现，**无需保存文件**。

### 基本工商信息格式

```
【{企业全称}】

统一社会信用代码：{代码}
注册资本：{金额}         成立日期：{YYYY-MM-DD}
登记状态：{存续 / 注销 / 吊销 / 迁出}
法定代表人：{姓名}       注册地址：{地址}
营业期限：{起始日期} 至 {截止日期}

经营范围：
{前 200 字，超出时截取并标注"...（已截取）"}
```

### 风险总览格式（聚合接口）

```
【{企业名称}】风险摸排概览

司法风险：
- 涉诉文书：{X} 件  |  失信被执行：{X} 条  |  被执行人：{X} 条
- 开庭公告：{X} 条  |  法院公告：{X} 条

经营风险：
- 严重违法：{X} 条  |  经营异常：{X} 条  |  欠税公告：{X} 条  |  行政处罚：{X} 条

股权信息：
- 股权冻结：{X} 条  |  股权出质：{X} 条  |  对外担保：{X} 条

知识产权：
- 商标：{X} 件  |  专利：{X} 件  |  软著：{X} 件  |  作品版权：{X} 件

如需查看详情，请告知需要深入哪一类信息。
```

### 列表类信息格式

```
【{企业名称}】{信息类型}（共 {X} 条，第 {N} 页）

1. {关键字段 1}：{值}  {关键字段 2}：{值}  {关键字段 3}：{值}
   {补充信息}

2. ...

{如有更多页：还有 {N} 页数据，如需查看请告知页码。}
```

## 来源标签

- `[元典企业数据]`：本会话内通过 `company_data.*` capability 实际返回的数据。默认标签。
- `[verify - 重大决策建议对照官方工商系统]`：API 数据存在一定时间延迟，重大决策（投融资 / 收购 / 重大合同签订）前建议以国家企业信用信息公示系统等官方源为准。
- `[模型知识 — 需核验]`：未经 MCP 核验、来自模型记忆的内容。**仅在 MCP 不可用时使用**。

## 工作约束

- **不编造数据**：所有信息必须来自 MCP 工具实际返回，未检索到时如实告知 `[模型知识 — 需核验]`。
- **消歧确认**：名称检索返回多家企业时，必须让用户确认目标企业，不擅自选择。
- **数量提示**：列表数据 > 5 条时，提示总数并告知可翻页查看。
- **状态说明**：若企业登记状态为注销 / 吊销 / 迁出，在基本信息输出时**突出标注**（建议用 ⚠️ 或加粗）。
- **数据时效**：API 数据存在一定时间延迟，重要决策前以官方工商系统为准。
- **统计 vs 明细**：严格按"关键区分"表选用接口，不混用。
- **来源标签**：所有数据按上述三级标注。

## 工作成果头部

按 profile 中角色 + 法域决定：

- 律师 + 中国法：`保密 / 内部法律分析 — 仅供法务团队使用 — 不构成外发法律意见`
- 非律师：`研究笔记 / 内部记录 — 不构成法律意见 — 请律师复核后再依赖`

外发给业务方 / 客户的版本去工作成果头。

## 非律师门

企业信息查询本身是事实查询。但当用户**基于本 skill 查询结果做具体决策**（合同主体审核、KYC / 反洗钱、投融资 due diligence、监管报送等）时，先 surface：

```text
本 skill 返回的企业数据是研究材料——汇集了元典企业库的命中。
数据存在 API 延迟，且不替代官方工商系统的实时核验。

如果计划基于这些数据做具体决策（合同主体审核、KYC / 反洗钱、投融资 DD、监管报送），
是否已与律师 / 有执业资格的法律人员复核过？
- 是：明确确认后继续；建议同步以官方工商系统（国家企业信用信息公示系统等）核验关键字段
- 否：建议先与律师复核数据在你具体场景下的可依赖性，并对照官方源核验
```

## 交接

- 涉诉文书 → `prc-legal-research-case-search`（用案号查全文）。
- 案件涉及的法律问题 → `prc-legal-research-deep-research`。
- 案件援引的法律条文 → `prc-legal-research-law-search`。
- 业务场景关联：
  - 合同主体审核 → `commercial-contract-review` / `commercial-vendor-agreement-review`。
  - 数据合规 KYC → `privacy-use-case-triage` / `privacy-dpa-review`。
  - 监管报送 → `regulatory-policy-diff` / `regulatory-gap-surfacer`。
  - 雇主资质核查 → `employment-cold-start-interview` 等。

## 本 skill 不做的事

- 不对外国企业 / 港澳台企业查询。
- 不在 capability 不可达时尝试用模型知识"模拟"查询。
- 不编造企业数据、不虚构案号 / 案由 / 金额、不伪造登记状态。
- 不替代律师做具体事实下的法律判断。
- 不替代官方工商系统的实时核验。
- 不保留 Claude 专属配置路径。
- 不要求用户调用 Claude slash command。

## 数据来源

- MCP server：`yuandian-company`（http stream，订阅管理）
- 数据来源：元典开放平台（北京华宇元典信息服务有限公司）
- API 文档：https://open.chineselaw.com/
- 支持邮箱：yuandianzonghe@thunisoft.com
