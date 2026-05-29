# 法律学生助手 Plugin — 运行前检查

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
| 定时调度器（cron/scheduled tasks） | 待检测 | 本 Plugin 无 Workflow，不影响 |
| 审计写操作（attorney-gate） | 待检测 | 法律写操作无审计留痕，建议补足 |

## 2. 本 Plugin 包含的 Workflow

本 Plugin 不包含定时 Workflow，所有 13 个 Skill 均为手动触发使用。

## 3. 如果检测到缺口

**安装 Legal Gateway**（一键解决）：

```bash
pip install legal-gateway
legal-gateway init --skills ./skills
```

或访问完整指南：[github.com/yuandian-ailaw/Agent-for-legal-cn/tree/main/legal-gateway](https://github.com/yuandian-ailaw/Agent-for-legal-cn/tree/main/legal-gateway)

## 4. 环境检测

运行以下命令自动检测：

```bash
python3 install.py --check-only
```

---

本 Plugin 可在无 Gateway 环境下运行所有 Skill，无需定时调度或自动触发能力。