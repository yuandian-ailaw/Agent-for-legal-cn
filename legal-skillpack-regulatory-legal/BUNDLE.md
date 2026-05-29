# 技能套件：监管合规法务

- 技能套件 ID：`regulatory-legal`
- 技能数量：10
- 入口技能：`regulatory-reg-feed-watcher`（监管动态监测）

## 简介

监管合规法务技能套件（中国法本地化版 v0.17.0-cn）—— 10 个技能，依托国家法律法规数据库 + 国务院政策文件库 + 政府网 + 元典 API + 飞书 / 钉钉 / 企业微信。新增"监管来函"（6 分法分类处置）+ "内规差异跟踪"（全周期）+ "事项工作区" + "政策修订红线"等，并将原 `feed-watcher` 重命名为 `reg-feed-watcher`。

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

## 技能套件说明

- 集群入口：`regulatory-reg-feed-watcher`——监管动态监测；同时被 `regulatory-incoming-letter` / `regulatory-policy-diff` 等下游技能引用。
- **中国法本地化 v0.17.0-cn**：原 6 个英文上游技能替换为 10 个中国法版。新增 4 个技能：`regulatory-gaps`（内规差异全周期跟踪）/ `regulatory-incoming-letter`（监管来函 6 分法分类与处置）/ `regulatory-matter-workspace`（多事项工作区）/ `regulatory-policy-redraft`（政策修订红线）。1 个重命名：`feed-watcher` → `reg-feed-watcher`。
- 监管来函 6 分法：行政处罚 / 行政监管措施 / 监管谈话 / 程序性通知 / 专项自查 / 监管问询，覆盖监管文件下发到企业的全套处置链路。
- **已知缺口**：原版 `reg-change-monitor` 每周定时巡检任务未迁移（合入决策：由宿主端定时任务能力替代）；`lib/` 目录下 Python 适配层（`yuandian_api` / `yuandian_mcp_wrapper` / `webdav_adapter` / `feishu_*`）未入仓（合入决策：作为外部依赖，运行时按需 `pip install`）。
- 流转路径：`regulatory-reg-feed-watcher` 触发 → `regulatory-policy-diff`（比对分析）→ `regulatory-policy-redraft`（起草修订）→ `regulatory-gaps`（跟踪）；`regulatory-incoming-letter` → `regulatory-matter-workspace`（建事项）→ `regulatory-comments`（回应）；与"AI 治理 / 隐私"等相邻技能集群在数据 / AI 监管事项上交叉引用。
