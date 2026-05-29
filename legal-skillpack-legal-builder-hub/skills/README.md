# 技能目录

本目录保存 **Skillpack 管理 / Hub** 集群的所有技能（Agent Skills），每个技能为一个独立子目录，含 `SKILL.md` 主文件与可选的 `references/` 资料。

权威清单见 [`../catalog.json`](../catalog.json)（机器可读）。

## 本插件包含的技能（10 个）

- `legal-builder-hub-auto-updater`
- `legal-builder-hub-cold-start-interview`
- `legal-builder-hub-customize`
- `legal-builder-hub-disable`
- `legal-builder-hub-registry-browser`
- `legal-builder-hub-related-skills-surfacer`
- `legal-builder-hub-skill-installer`
- `legal-builder-hub-skill-manager`
- `legal-builder-hub-skills-qa`
- `legal-builder-hub-uninstall`

## 技能结构约定

- 每个 `<skill-id>/SKILL.md` 是技能本体，含 YAML frontmatter（`name` / `description` / `argument-hint` 等）+ 中文正文
- 可选 `<skill-id>/references/` 存放该技能的参考资料、模板与示例
- 技能运行时中立——不绑定单一智能体框架；通过 `$LEGAL_AGENT_PROFILE_HOME` 等环境变量与本地 MCP Gateway 兜底实现跨平台
