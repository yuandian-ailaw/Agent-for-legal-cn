# 安装指南

## 环境要求

- Python 3.9+
- 支持的智能体平台之一：Codex、WorkBuddy、OpenCode、OpenClaw、Kimi Code、MyAgents、Cursor

## 安装单个 Plugin

```bash
cd legal-skillpack-commercial-legal

# 1. 检测环境（推荐先执行）
python3 install.py --check-only

# 2. 安装到平台默认目录
python3 install.py

# 3. 或指定目录
python3 install.py --target ~/.agents/skills
```

## 各平台默认安装路径

| 平台 | 默认路径 |
|------|---------|
| Codex | `~/.codex/skills` |
| WorkBuddy | `~/.codebuddy/skills` |
| OpenCode | `~/.config/opencode/skills` |
| OpenClaw | `~/.openclaw/skills` |
| Kimi Code | `~/.kimi/skills` |
| MyAgents / Claude Code | `~/.claude/skills` |
| Cursor | `./.cursor/skills`（项目级） |

## 手动安装（不用 install.py）

直接将 `skills/` 目录下的文件夹复制到平台的 Skill 目录即可。

## 安装问题排查

见各 Plugin 目录下的 `CHECKPOINT.md`。如果平台不支持原生 Skill 发现或定时任务，建议安装 Legal Gateway。
