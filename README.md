# Agent-for-legal-cn —— 中国法律实务智能体技能套装

> 将 Anthropic `claude-for-legal` 进行中国法本地化，面向中国律师、法务和法律工作者。

## 关于我们

我们是**元力工场团队**，专注于让智能体在中国法律事务场景中真实落地。我们引进和原创的 Skill 与仓库都开放在 **[法律元力平台 yuanli.ailaw.cn](https://yuanli.ailaw.cn)**，欢迎前往浏览、下载、安装。

## 为什么开源这个仓库

Anthropic 的 `claude-for-legal` 是一套非常优秀的法律智能体框架，但它原生面向美国法实务与 Claude Code 环境。要让它在中国法律场景里真正可用，至少要解决两个核心问题：

1. **智能体框架的通用适配** —— 让 Skill 不再绑定 Claude Code 单一运行时，能在 Codex / Cursor / WorkBuddy / Kimi Code / OpenCode / OpenClaw / MyAgents 等任何支持 Skill 或 MCP 的平台上工作。
2. **中国法实务的适配** —— 用《民法典》《公司法》《民事诉讼法》《PIPL》《生成式 AI 暂行办法》等现行法律法规与监管文件，替换原版以英美法/普通法为前提的工作流；接入元典 MCP（法规 / 案例 / 企业三类检索）作为中国法事实底座；调整文书体例与论证范式（IRAC + 三段论 + 鉴定式分析法）。

开源出来一是希望让中国法律行业的同仁能够直接用、直接改；二是让上下游的智能体开发者看到「跨框架适配 + 行业本地化」是怎么落地的，少踩同样的坑。

## 核心适配原理：本地 MCP 统一接入

我们解决「跨智能体框架」问题的核心机制是：**让 Skill 本体保持运行时中立，把平台差异交给本地 MCP Gateway 兜底**。

```text
路径 A：原生 Skill 发现
   ~/.claude/skills/、~/.codex/skills/、./.cursor/skills/ 等
   ↓
   运行时直接读 SKILL.md → 加载

路径 B：本地 MCP Gateway 统一接入
   Skill 本体不变，由本地 Gateway 暴露统一 MCP 接口
   ↓
   任何支持 MCP 的运行时（含 Cursor、Claude Desktop 等）
   都可通过 MCP 调用同一份 Skill
```

具体设计：

- **SKILL.md 运行时中立** —— 不写死 `~/.claude/` 路径，统一用 `$LEGAL_AGENT_PROFILE_HOME` 等环境变量，配置、产出、审计在不同平台都能落到正确位置。
- **`install.py` 自动检测部署** —— 不需要用户指定平台，扫描 `~/.claude` / `~/.codex` / `~/.workbuddy` / `~/.kimi` / `~/.config/opencode` / `~/.openclaw` / `.cursor` 等已装平台目录，自动安装到对应位置。
- **Legal Gateway（规划中，本版本未包含）** —— 设计目标是对不支持原生 Skill 发现，或需要定时调度、审计写操作（attorney-gate）的运行时，提供一个本地 MCP 服务，把 14 个核心能力（list/get/install/workflow/scheduler/...）以统一接口暴露出来。**该组件尚未交付**：当前版本不含 `legal-gateway/` 目录，`pip install legal-gateway` 不可用；含定时 Workflow 的 plugin 在其发布前需手动触发，或在平台自身的定时任务能力中配置。

这样一份 Skill 内容，可以同时服务原生 Skill 平台与纯 MCP 平台，**插件运行、配置、审计的整体机制由本地 MCP 兜底**，不再需要为每个新平台手写 adapter。

## 致谢与共建邀请

这是一份**志愿、公益**的研发工作，肯定还有很多问题和不足。**欢迎更多伙伴参与共建** —— 提 Issue、提 PR、贡献新 Skill、做更深的法条本地化，都非常欢迎。

特别致谢 **[陈石律师](https://github.com/CSlawyer1985/claude-for-legal-ZH)** —— 我们部分组件（特别是商事合同、公司法务、部分诉讼法务）的研发主要参考了他在 `claude-for-legal-ZH` 中文化版本中的成果，他的开源工作让我们少走了很多弯路。

---

## 包含的 Plugin（9 个业务领域）

| Plugin | Skill 数量 | 说明 |
|--------|-----------|------|
| [商事合同法务](legal-skillpack-commercial-legal/) | 12 | 合同审查、谈判、续约管理 |
| [公司法务](legal-skillpack-corporate-legal/) | 13 | 并购、合规、董事会 |
| [知识产权法务](legal-skillpack-ip-legal/) | 12 | 专利、商标、著作权 |
| [诉讼法务](legal-skillpack-litigation-legal/) | 19 | 争议解决、证据、出庭 |
| [监管合规法务](legal-skillpack-regulatory-legal/) | 10 | 监管动态、合规 gap |
| [AI 治理合规](legal-skillpack-ai-governance-legal/) | 9 | AI 审计、政策监控 |
| [法律学生助手](legal-skillpack-law-student/) | 13 | 学习、备考、写作 |
| [中国法法律研究](legal-skillpack-legal-research-cn/) | 4 | 元典法条/案例/企业检索 |
| [Legal Builder Hub](legal-skillpack-legal-builder-hub/) | 10 | Skill 发现、安装、管理 |

每个 Plugin 可独立安装运行。详见各目录下的 `README.md`。

## 快速开始

```bash
# 进入任意 plugin 目录
cd legal-skillpack-commercial-legal

# 检测环境
python3 install.py --check-only

# 安装到平台默认目录
python3 install.py
```

## 架构说明

- **独立 Plugin**：每个文件夹自包含 skills、profiles、connectors，可单独使用
- **通用安装器**：`install.py` 支持 Codex / WorkBuddy / OpenCode / OpenClaw / Kimi Code / MyAgents / Cursor
- **MCP Gateway（规划中）**：Legal Gateway 尚未发布，当前版本不包含该组件；非原生 Skill 平台暂无法通过 Gateway 接入，进度见 `docs/gateway.md`

## 上游归属

本项目主要基于 [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal)（Apache-2.0）的 skill 框架，由元力工场团队进行中国法本地化与原创扩展。

其中：

- **commercial-legal**（商事合同）、**corporate-legal**（公司法务）及 **litigation-legal**（诉讼法务）中事项管理类技能，参考了 [CSlawyer1985/claude-for-legal-ZH](https://github.com/CSlawyer1985/claude-for-legal-ZH)（陈石律师，Apache-2.0）的中文化版本。
- **ai-governance-legal**（AI 治理）、**ip-legal**（知识产权）、**law-student**（法学学生）、**legal-builder-hub**（Hub 元 cluster）、**regulatory-legal**（监管合规）由元力工场团队基于上游英文版独立完成中国法适配。
- **legal-research-cn**（中国法法律研究）为元力工场自研，集成元典 MCP（北京华宇元典）法规 / 案例 / 企业三类检索能力。

## License

Apache-2.0，详见 [LICENSE](LICENSE)。
