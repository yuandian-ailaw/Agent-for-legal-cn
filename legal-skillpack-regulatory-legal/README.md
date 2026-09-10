# 监管合规法务技能套件

监管合规法务技能套件（中国法本地化版 v0.17.0-cn）—— 10 个技能，依托国家法律法规数据库 + 国务院政策文件库 + 政府网 + 元典 API + 飞书 / 钉钉 / 企业微信。新增"监管来函"（6 分法分类处置）+ "内规差异跟踪"（全周期）+ "事项工作区" + "政策修订红线"等，并将原 `feed-watcher` 重命名为 `reg-feed-watcher`。

- 技能套件 ID：`regulatory-legal`
- 技能数量：10
- 入口技能：`regulatory-reg-feed-watcher`（监管动态监测）
- 配置技能：`regulatory-cold-start-interview`（冷启动访谈）

## 快速开始

```bash
# 检测环境（建议先执行）
python3 install.py --check-only

# 安装到平台默认目录
python3 install.py

# 或指定目录
python3 install.py --target ~/.agents/skills
```

> 本 Plugin 包含 1 个定时 Workflow（`regulatory-change-monitor`）。
> 如果您的平台不支持定时任务：Legal Gateway 尚未发布（规划中），当前请手动触发 Workflow，或使用平台自身的定时任务能力配置自动触发。
> 详细兼容性检查见 [CHECKPOINT.md](CHECKPOINT.md)。

## 包含的技能

- `regulatory-cold-start-interview`（冷启动访谈）
- `regulatory-comments`（评议管理）
- `regulatory-customize`（个性化调整）
- `regulatory-gap-surfacer`（内规差异呈现）
- `regulatory-gaps`（内规差异跟踪）
- `regulatory-incoming-letter`（监管来函处置）
- `regulatory-matter-workspace`（事项工作区）
- `regulatory-policy-diff`（政策比对）
- `regulatory-policy-redraft`（政策修订红线）
- `regulatory-reg-feed-watcher`（监管动态监测）
