# Legal Gateway — 统一 MCP 接入层

## 是什么

Legal Gateway 是法律 Skillpack 的 **MCP 统一接入层**。

设计原则：**一个兼容层，不为每个运行时写手写 adapter**。

实现路径有两条：

```text
路径 A：运行时原生从 ~/.agents/skills/ 等目录加载 SKILL.md
        → Codex / WorkBuddy / OpenCode / OpenClaw / Kimi Code / Claude Code 均支持

路径 B：运行时通过 MCP 调用统一 Gateway
        → 适用于任何支持 MCP 的运行时，一套代码覆盖全部平台
```

两条路径并存，数据源是同一份 `skillpack/`。用户选 A 或 B 都可以。

## 什么时候装

| 场景 | 说明 |
|------|------|
| 想统一配置、不关心各平台 skills 目录差异 | 通过 Gateway 一处配置，多平台共用 |
| 需要 Workflow 自动触发（定时调度） | Gateway daemon 提供 cron 式调度 |
| 使用 Cursor 等仅支持 MCP 的平台 | 通过 MCP 接入 Skill |
| 不需要 MCP | 直接用 `install.py` 复制 skills 到平台目录即可，无需 Gateway |

## 安装

```bash
# 1. 安装 Gateway
pip install legal-gateway

# 2. 初始化（指向 plugin 的 skills 目录）
legal-gateway init --skills ./skills

# 3. 验证
legal-gateway --probe
# → Gateway v3 ready: 14 tools, daemon disabled

# 4. 如需定时 Workflow 自动触发，启用 daemon
legal-gateway daemon --enable
```

## Gateway 暴露的工具（14 个）

### 只读（6 个）
- `legal_skill_list` — 列出所有 skill
- `legal_skill_get` — 获取单个 skill 详情
- `legal_profile_resolve` — 解析法务画像配置
- `legal_connector_list` — 列出能力连接器
- `legal_workflow_list` — 列出工作流定义
- `legal_workflow_get` — 获取工作流详情

### 写操作（4 个，含 attorney-gate + audit-log）
- `legal_workflow_start` — 启动交互式工作流
- `legal_workflow_step_report` — 推进工作流步骤
- `legal_artifact_write` — 写入工作产物（审计）
- `legal_notification_preview` — 渲染通知预览（不发送）

### Daemon 模式（4 个，需启用）
- `legal_scheduler_list` — 列出已注册定时任务
- `legal_scheduler_enable` — 注册定时任务
- `legal_scheduler_disable` — 停用定时任务
- `legal_scheduler_status` — daemon 状态摘要

## 安全设计

### Attorney-gate（律师权限闸门）

| 角色 | 内部写操作 | 外部写操作 | 发送/签署 |
|------|----------|----------|----------|
| 律师 | 自动放行+留痕 | 自动放行+留痕 | 拒绝（Gateway 不处理外部发送） |
| 非律师（有授权） | 自动放行+留痕 | 需二次确认 | 拒绝 |
| 非律师（无授权） | 留痕+提醒 | 拒绝 | 拒绝 |

### Audit-log（审计日志）

所有写操作（workflow_start、artifact_write、notification_preview）均写入 append-only 审计日志。

## 源码

[github.com/yuandian-ailaw/Agent-for-legal-cn/tree/main/legal-gateway](https://github.com/yuandian-ailaw/Agent-for-legal-cn/tree/main/legal-gateway)

## 各平台 MCP 配置

在任意支持 MCP 的平台的 `.mcp.json` 或 MCP 配置中：

```json
{
  "mcpServers": {
    "legal-gateway": {
      "command": "python3",
      "args": ["-m", "src.gateway.server"],
      "cwd": "/path/to/legal-gateway"
    }
  }
}
```

适用：Claude Code / Claude Desktop / Codex / WorkBuddy / Cursor / OpenCode 等所有支持 MCP 的平台。