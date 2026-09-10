# Legal Agent Skillpack — 通用安装说明

> **便携式分发包**：同一份 install.py 适用于 Cursor、Codex、Claude Code / MyAgents、OpenCode、OpenClaw、Kimi Code、WorkBuddy 等。
> installer 会自动扫描您机器上已装的智能体框架，并装到对应的默认目录。

## 1. 一行命令安装

```bash
python3 install.py
```

installer 会：

1. 扫描 `~/.claude` / `~/.codex` / `~/.workbuddy` / `~/.kimi` / `~/.config/opencode` / `~/.openclaw` / 当前目录 `.cursor` 等位置；
2. 检测到的第一个智能体框架作为默认安装目标，并提示其他检测到的平台；
3. 把全部 skill 复制到对应的 `skills/` 目录。

需要 **Python 3.9+**（仅标准库）。

## 2. 各平台默认目录对照

| 智能体框架 | 默认 skill 目录 |
|----------|---------------|
| MyAgents / Claude Code | `~/.claude/skills` |
| Codex（专用目录） | `~/.codex/skills` |
| 腾讯 WorkBuddy | `~/.workbuddy/skills` |
| Kimi Code | `~/.kimi/skills` |
| OpenCode | `~/.config/opencode/skills` |
| OpenClaw | `~/.openclaw/skills` |
| Cursor IDE | `./.cursor/skills`（项目级） |
| 通用 Agents | `~/.agents/skills`（未检测到任何已知框架时的 fallback）|

## 3. 想装到指定目录 / 指定平台

```bash
# 指定一个目录（强制覆盖自动检测）
python3 install.py --target ~/.claude/skills

# 想同时装到多个平台：逐个 --target 重跑
python3 install.py --target ~/.codex/skills
```

或者用软链复用一份本体：

```bash
python3 install.py --target ~/.agents/skills
ln -snf ~/.agents/skills ~/.claude/skills
ln -snf ~/.agents/skills ~/.codex/skills
```

Cursor 用户：在用户项目根目录执行；安装后 Cmd+Shift+P → **Developer: Reload Window**。

## 4. 先查环境再决定

```bash
python3 install.py --check-only
```

只检测、不安装，输出：

- 当前机器检测到哪些智能体框架
- 是否有定时调度能力
- 推荐走「路径 A 原生 Skill 发现」还是「路径 B MCP Gateway」

平台兼容性详情见同目录 `CHECKPOINT.md`。

## 5. 常用维护命令

```bash
python3 install.py --list         # 列出每个 skill 的安装状态
python3 install.py --uninstall    # 卸载本包标记管理的 skill
python3 install.py --dry-run      # 只打印动作，不写文件
python3 install.py --force        # 升级时覆盖已装版本（仅限本包管理）
```

## 6. 包内文件

```text
INSTALL.md              本文件
CHECKPOINT.md           运行前兼容性检查
README.md               本 Plugin 简介
install.py              通用安装脚本（自动检测平台）
EXPORT-MANIFEST.json    构建元信息（bundle_id 等）
BUNDLE.md / bundle.json 本包 skill 组合
skills/                 SKILL.md 目录
profiles/ connectors/ workflows/ jurisdictions/ bundles/
```

## 7. MCP 与连接器

研究类 skill 需元典 MCP（及 deep-research 的 Tavily）。配置见 `connectors/registry.json`。
Gateway 接入说明：见仓库根 `docs/gateway.md`。
> ⚠️ Legal Gateway 尚未发布（规划中，本版本不含）；`pip install legal-gateway` 不可用，
> 定时 Workflow 发布前需手动触发或在平台定时任务能力中配置。

## 8. Agent 自服务安装提示

若您是自动化 Agent 正在为用户安装本包：

1. 直接执行 `python3 install.py`，installer 会自检并选目标；
2. 若用户要求装到特定平台或目录，加 `--target <path>`；
3. 安装前可先 `python3 install.py --check-only` 获取环境摘要；
4. 反馈问题时请附带 `EXPORT-MANIFEST.json` 中的 `bundle_id` 与 `source_commit`。
