# 公司法务技能套件

公司法务技能套件（中国法本地化版 v0.17.0-cn）—— 13 个技能，覆盖公司法务全周期：尽调、董事会纪要、书面决议、交割清单、主体合规、整合管理、重大合同清单、表格审查、多事项工作区。依《公司法》《企业信息公示暂行条例》《外商投资法》《民法典》合同编。

> 本技能套件中文化版本参考自 [陈石 claude-for-legal-ZH](https://github.com/CSlawyer1985/claude-for-legal-ZH)（Apache-2.0），元力工场团队进行了运行时中立适配。

- 技能套件 ID：`corporate-legal`
- 技能数量：13
- 入口技能：`corporate-matter-workspace`（事项工作区）
- 配置技能：`corporate-cold-start-interview`（冷启动访谈）

## 快速开始

```bash
# 检测环境（建议先执行）
python3 install.py --check-only

# 安装到平台默认目录
python3 install.py

# 或指定目录
python3 install.py --target ~/.agents/skills
```

> 本 Plugin 包含 1 个定时 Workflow（`corporate-dataroom-watcher`）。
> 如果您的平台不支持定时任务，建议安装 [Legal Gateway](https://github.com/yuandian-ailaw/Agent-for-legal-cn/tree/main/legal-gateway) 获得自动触发能力。
> 详细兼容性检查见 [CHECKPOINT.md](CHECKPOINT.md)。

## 包含的技能

- `corporate-ai-tool-handoff`（AI 工具交接）
- `corporate-board-minutes`（董事会纪要）
- `corporate-closing-checklist`（交割清单）
- `corporate-cold-start-interview`（冷启动访谈）
- `corporate-customize`（个性化调整）
- `corporate-deal-team-summary`（交易团队简报）
- `corporate-diligence-issue-extraction`（尽调问题提取）
- `corporate-entity-compliance`（主体合规）
- `corporate-integration-management`（整合管理）
- `corporate-material-contract-schedule`（重大合同清单）
- `corporate-matter-workspace`（事项工作区）
- `corporate-tabular-review`（表格审查）
- `corporate-written-consent`（书面决议）