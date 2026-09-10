# Skillpack 管理 / Hub 技能套件

平台元技能集群——管理其他法律技能集群的工具。10 个技能：冷启动 / 配置定制 / 技能仓库浏览（法律元力 + 静态 yaml + GitHub 三级 fallback）/ 技能安装器（双通道：API zip + GitHub raw）/ QA 设计框架审查 / 自动更新检测 / 相关技能推荐 / 禁用 / 卸载 / 管理路由。受保护列表：cn-localized 8 法律技能集群 + hub 自身。对应 Anthropic legal-builder-hub v1.0.2 上游。

- 技能套件 ID：`legal-builder-hub`
- 技能数量：10
- 入口技能：`legal-builder-hub-cold-start-interview`（冷启动访谈）
- 配置技能：`legal-builder-hub-cold-start-interview`（冷启动访谈）

## 快速开始

```bash
# 检测环境（建议先执行）
python3 install.py --check-only

# 安装到平台默认目录
python3 install.py

# 或指定目录
python3 install.py --target ~/.agents/skills
```

> 本 Plugin 包含 1 个定时 Workflow（`skillpack-management-registry-sync`）。
> 如果您的平台不支持定时任务：Legal Gateway 尚未发布（规划中），当前请手动触发 Workflow，或使用平台自身的定时任务能力配置自动触发。
> 详细兼容性检查见 [CHECKPOINT.md](CHECKPOINT.md)。

## 包含的技能

- `legal-builder-hub-auto-updater`（自动更新检测）
- `legal-builder-hub-cold-start-interview`（冷启动访谈）
- `legal-builder-hub-customize`（个性化调整）
- `legal-builder-hub-disable`（禁用）
- `legal-builder-hub-registry-browser`（仓库浏览）
- `legal-builder-hub-related-skills-surfacer`（相关技能推荐）
- `legal-builder-hub-skill-installer`（技能安装器）
- `legal-builder-hub-skill-manager`（技能管理）
- `legal-builder-hub-skills-qa`（技能 QA 审查）
- `legal-builder-hub-uninstall`（卸载）