# 技能套件目录

本目录保存可安装的技能组合（技能套件）声明清单。技能套件描述一组技能、它们依赖的业务规范 / 工作流 / 能力，并提供导出 / 安装时的语义分组。

## 本插件的技能套件

| 技能套件 | 描述 |
|---|---|
| [regulatory-legal](regulatory-legal.bundle.json) | 监管合规法务集群完整套件 |

> 单 plugin 分发包内通常只有一个 bundle。可读元数据见仓库根 `BUNDLE.md`；机器可读源见同目录 `regulatory-legal.bundle.json` 与 `../catalog.json`。

## 字段含义（节选）

- `id`：技能套件唯一标识
- `title` / `description`：人类可读说明
- `practice_area`：所属实务领域
- `skills`：套件包含的技能 ID 列表，全部存在于 `../skills/` 与 `../catalog.json`
- `required_profiles` / `required_workflows`：依赖的业务规范与工作流
- `recommended_capabilities` / `minimum_capabilities`：能力要求
- `entry_skill` / `setup_skill`：套件入口与配置技能
