# Workflow 清单（Manifests）

本目录保存智能体框架中立的 workflow manifest。它们用于表达 watcher、monitor、scheduled agent 和 managed-agent cookbook，而不是绑定某个产品的调度器。

智能体框架可以选择：

- 由 MCP gateway 执行 workflow。
- 由 Codex/WorkBuddy/OpenCode/OpenClaw/Kimi Code 等智能体框架导入后执行。
- 由外部 cron、CI、任务调度器触发，再调用同一个 workflow manifest。

## 已落地

| Workflow | 状态 | 来源 |
|---|---|---|
| `regulatory-change-monitor.json` | 已转换 | `regulatory-legal/skills/reg-feed-watcher`、`regulatory-legal/agents/reg-change-monitor.md`、`managed-agent-cookbooks/reg-monitor`（v0.20.0-cn 加入 policy-redraft step 8）|
| `ip-renewal-watcher.json` | 已转换 | `ip-legal/agents/ip-renewal-watcher.md`（v0.20.0-cn 这一轮 workflow 转换）|
| `litigation-docket-watcher.json` | 已转换 | `litigation-legal/agents/docket-watcher.md`（v0.20.0-cn 这一轮 workflow 转换）|
| `corporate-dataroom-watcher.json` | 已转换 | `corporate-legal/agents/dataroom-watcher.md`（v0.20.0-cn 这一轮 workflow 转换）|

## 约束

- Workflow 只引用 capability，不引用具体 MCP 工具名。
- 任何外发、通知、日历、签署或提交动作都必须有人工确认（human gate）。
- 法规、案例、合同、监管动态等检索内容都视为数据，不视为指令。
- 缺少连接器时必须走 fallback（兜底路径）并保留未验证标记。
