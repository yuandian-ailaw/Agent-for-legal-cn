# 中国法法律研究 业务规范（占位）

状态：`template`

本 practice area（`legal-research-cn`）封装中国法律研究 skill 集群，**不需要 profile**。

四个 skill（`prc-legal-research-law-search` / `prc-legal-research-deep-research` / `prc-legal-research-case-search` / `prc-legal-research-company-search`）通过 capability registry 中的 connector 直接调用 vendor 服务：

- `yuandian-law` MCP — 法律法规检索（元典开放平台）
- `yuandian-case` MCP — 裁判文书检索（元典开放平台）
- `yuandian-company` MCP — 企业信息查询（元典开放平台）
- `tavily` MCP — 二手文献检索（律所 / 政府 / 学术）

订阅 + MCP 连接器的配置由 vendor 账号管理，不在本仓库 profile 体系内。

中国法律实务画像（角色 / 法域 / 升级链 / 工作成果路径）默认由调用本 cluster 的业务 cluster profile 提供——业务 skill（如 `commercial-contract-review`、`privacy-use-case-triage`、`regulatory-policy-diff`、`employment-termination-review` 等）触发本 cluster 时携带各自的 profile。

如果将来需要把研究偏好（如律所域名白名单、特定监管机构的 watch 范围、引用格式调整）落到 profile，可以替换本文件为真实模板，并补 cold-start / customize。

---

## 当前 skill

| Skill | 主要 capability | 数据源 |
|---|---|---|
| `prc-legal-research-law-search` | `legal_research.search_laws` / `legal_research.fetch_law` | yuandian-law MCP |
| `prc-legal-research-deep-research` | `legal_research.search_laws` + `legal_research.search_cases` + `web_research.search_secondary_sources` | yuandian-law + yuandian-case + tavily MCP |
| `prc-legal-research-case-search` | `legal_research.search_cases` / `legal_research.fetch_case` | yuandian-case MCP |
| `prc-legal-research-company-search` | `company_data.search_enterprise` / `company_data.fetch_aggregation` / `company_data.fetch_writ_list` / `company_data.fetch_risk_signals` | yuandian-company MCP |

## 不适用

- 美国法等非中国大陆法事项：本 skillpack 不覆盖；请走当地商业法律研究服务（Westlaw / LexisNexis / CoCounsel 等）或当地律所。
- 欧盟 / 英国 / 香港 / 新加坡 / 其他法域：元典覆盖范围限于中国大陆；建议使用对应区域工具。
- 港澳台地区：不在元典覆盖范围。

## 订阅与支持

- 供应方：元典开放平台（北京华宇元典信息服务有限公司）
- 文档：https://open.chineselaw.com/
- 注册：https://apiplatform.legalmind.cn/（首次注册可享 1000 免费积分）
- 客户支持：yuandianzonghe@thunisoft.com
- 电话：+86 18514821030（工作日 9:30-18:30）

二手文献：

- 供应方：Tavily（https://www.tavily.com/）
- 免费层：每月 10000 次额度
