# 连接器配置

本目录是智能体框架中立的 connector registry。标准 skill 和 workflow 只依赖 capability，不直接依赖 Codex、WorkBuddy、OpenCode、OpenClaw、Kimi Code 或 Claude 的私有 tool 名。

## 当前决策

1. 存储相关能力使用本地目录实现（`local-legal-storage`）。
2. 中国法律法规查询使用元典法律法规 MCP（`yuandian-law`）。
3. 中国案例查询使用元典案例 MCP（`yuandian-case`）。
4. 中国企业 / 涉诉 / 风险信息查询使用元典企业 MCP（`yuandian-company`）。
5. 中国法二手文献检索使用 Tavily MCP（`tavily`，include_domains 白名单：14 律所 + 10 政府 + 10 学术）。
6. 外发动作走智能体框架原生通知 capability（`runtime-notification`），所有外发都先预览再由用户逐次确认。
7. 美国法等非中国大陆法实质研究**不在本 skillpack 覆盖范围**——请走当地商业法律研究服务（Westlaw / LexisNexis / CoCounsel 等）或当地律所。
8. 密钥不得写入仓库，统一用环境变量或智能体框架 secret store 注入。

## 本地目录

默认本地数据目录：

```text
local-data/
  documents/
  contracts/
  matters/
  profiles/
  work-products/
```

运行时可以通过环境变量覆盖：

```bash
export LEGAL_AGENT_LOCAL_DATA_HOME=/path/to/legal-agent-data
```

实际合同、客户材料、证据、工作成果都不应提交 Git。仓库只保留目录说明。

## 外部 MCP 鉴权

示例配置见 `yuandian.mcp.example.json`。使用前按所需 connector 设置环境变量：

```bash
export YUANDIAN_MCP_API_KEY=<your-yuandian-api-key>           # yuandian-law / yuandian-case / yuandian-company 共用
export TAVILY_API_KEY=<your-tavily-api-key>                    # tavily（白名单二手文献）
```

实际运行时应把 `${ENV_VAR}` 占位符交给智能体框架 secret store 注入。不要把 Bearer token 写入 `registry.json`、`.mcp.json`、README 或提交历史。

## 能力映射

| 目标 | capability | connector |
|---|---|---|
| 合同文件读取 | `document_storage.fetch_file` | `local-legal-storage` |
| 合同库读取 | `contract_repository.fetch_agreement` | `local-legal-storage` |
| 审查结果写入 | `artifact.write_file` | `local-legal-storage` |
| 中国法律法规检索 | `legal_research.search_laws` | `yuandian-law` |
| 中国法律依据核验 | `legal_research.verify_authority` | `yuandian-law` |
| 中国案例检索 | `legal_research.search_cases` | `yuandian-case` |
| 中国引用核验 | `legal_research.verify_citation` | `yuandian-law` / `yuandian-case` |
| 监管动态线索 | `regulatory_feed.fetch_updates` | `yuandian-law` + 本地 source catalog |
| 中国企业基础信息检索 | `company_data.search_enterprise` | `yuandian-company` |
| 中国企业统计聚合查询 | `company_data.fetch_aggregation` | `yuandian-company` |
| 中国企业涉诉文书明细 | `company_data.fetch_writ_list` | `yuandian-company` |
| 中国企业风险信号 | `company_data.fetch_risk_signals` | `yuandian-company` |
| 中国法二手文献检索 | `web_research.search_secondary_sources` | `tavily`（include_domains 白名单） |
| 外发预览 + 用户确认 | `notification.preview_and_send` | `runtime-notification` |
