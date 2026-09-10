# 诉讼法务 Plugin — 运行前检查

## 快速开始

```bash
# 方式1：安装到平台默认目录
python3 install.py

# 方式2：安装到指定目录
python3 install.py --target ~/.agents/skills

# 方式3：手动复制 skills/ 到平台 Skill 目录
```

---

## 1. 平台兼容性检查

| 能力 | 您的平台是否支持 | 不满足时的影响 |
|------|----------------|---------------|
| 原生 Skill 发现（`SKILL.md`） | 待检测 | 无法自动识别 Skill，需手动加载 |
| MCP 客户端 | 待检测 | 无法通过 Gateway 调用 |
| 定时调度器（cron/scheduled tasks） | 待检测 | Workflow 不会自动触发，需手动执行 |
| 审计写操作（attorney-gate） | 待检测 | 法律写操作无审计留痕，建议补足 |

## 2. 本 Plugin 包含的 Workflow

| Workflow | 触发条件 | 是否需要 Gateway |
|----------|---------|-----------------|
| `litigation-docket-watcher` | 案件排期/状态变更监控 | 是（定时触发）|

> 如果您的平台**不支持定时任务**，以上 Workflow 不会自动运行。您可以：
> - 手动定期执行对应 Skill
> - Gateway 发布前：手动触发 Workflow，或用平台自身定时任务能力配置触发（Gateway 规划中，见下文）

## 3. 如果检测到缺口

**关于 Legal Gateway（2026-09-09 状态更新）**：Legal Gateway（MCP 统一接入层）尚在规划中、
**未随本版本发布**——`pip install legal-gateway` 当前不可用，"一键安装"暂无法执行。
在 Gateway 发布前：定时 Workflow 请手动触发，或使用平台自身的定时任务能力
（如 MyAgents Task、cron）配置触发；审计写操作依赖各 skill 内建的确认与留痕步骤
（见各 SKILL.md）。Gateway 发布后，本节将恢复安装指引。

## 4. 环境检测

运行以下命令自动检测：

```bash
python3 install.py --check-only
```

---

本 Plugin 可在无 Gateway 环境下运行基础 Skill；Workflow 自动触发和集中审计写操作依赖规划中的 Legal Gateway（未发布），当前请按上文替代方案操作。