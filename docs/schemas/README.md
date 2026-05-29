# 标准 Schemas

本目录定义本项目的运行时中立数据结构。它们是后续转换脚本、校验脚本和 MCP 网关共同使用的合同。

这些 schema 不绑定 Codex、腾讯 WorkBuddy、OpenCode、OpenClaw、Kimi Code 或 Claude Code。运行时专属清单、安装目录、zip 包或 marketplace 元数据只能从标准 `skillpack/` 派生。

## 文件

| 文件 | 作用 |
|---|---|
| `skillpack.schema.json` | 标准法律技能包总清单，记录 package、paths、skills、profiles、connector registry 和 workflows。 |
| `catalog.schema.json` | 机器可读 skill 索引（`skillpack/catalog.json`）。给 MCP gateway `legal_skill_list`、导出生成器和 bundle 校验使用。 |
| `bundle.schema.json` | 可安装的 skill 组合（`skillpack/bundles/*.bundle.json`），声明一组 skill、依赖的 profile / workflow / capability 与最低执行要求。 |
| `profile.schema.json` | 中立 profile manifest，描述 company/practice/matter/user profile 的解析规则、必填区块、占位符、连接器状态和法律安全边界。 |
| `connector-registry.schema.json` | 中立连接器能力注册表。Skill 只依赖 capability，例如 `document_storage.fetch_file`，不依赖某个运行时 tool 名称。MCP header 只允许使用环境变量占位符，不写明文密钥。 |
| `workflow.schema.json` | 中立 workflow manifest，用于 watcher、monitor、scheduled agent 和 managed-agent cookbook 的迁移。 |
| `migration-report.schema.json` | 转换报告 schema，记录每个上游文件如何迁移、哪些内容被改写、哪些 capability 被映射、哪里需要人工复核。 |
| `behavior-contract.schema.json` | 转换前行为契约，记录关键 invariants、fixture、静态检查和验收条件。 |

补充说明：`evals/golden/*.golden.json` 当前由 `src/validate/run_behavior_fixtures.py` 直接校验，尚未单独抽成 JSON Schema。等 golden 格式稳定后再补 `golden-fixture.schema.json`。

## 设计原则

- `skillpack/` 是权威源。
- `SKILL.md` 仍是技能正文的权威文件，`skillpack.schema.json` 只索引和约束它们。
- Profile 路径必须通过 `LEGAL_AGENT_PROFILE_HOME` 等中立变量解析，不写 `~/.claude/...`。
- Connector 以 capability 为中心，不以产品名或 MCP tool 名为中心。
- Workflow 描述触发、输入、步骤、能力、产物和人工审核闸门，不描述具体运行时调度 API。
- Migration report 必须可审计，方便我们知道每个上游文件是直接迁移、改写、workflow 化、connector 化还是仅保留参考。

## 当前版本

当前 schema 版本为 `0.1.0`。这是迁移 MVP 的起点，后续在第一批 skill 转换时可以小版本迭代。
