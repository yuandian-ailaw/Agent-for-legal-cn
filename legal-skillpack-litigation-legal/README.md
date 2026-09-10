# 诉讼业务管理技能套件

中国诉讼业务管理技能集群——以 19 个技能覆盖案件组合管理、催告函体系、证据 / 时间线 / 要件分析、调查令分流、庭审准备、外聘律师协调和文书起草。基于《民事诉讼法（2023 修正）》《最高人民法院民事诉讼证据规定（2019 修正）》《民法典》《民诉法解释（2022 修正）》《个人信息保护法》《律师法》《专利法》《劳动合同法》《保险法》《会计档案管理办法》等 10 部现行法律法规，对 catalog 中已有技能集群形成「诉讼前 (demand-* / matter-intake / legal-hold) → 诉讼中 (chronology / claim-chart / deposition-prep / brief-section-drafter / subpoena-triage) → 调度 (matter-update / matter-briefing / oc-status / portfolio-status / privilege-log-review) → 结案 (matter-close)」全闭环。原告 / 被告立场二分，法务 / 律所律师 / 独立执业角色三分，必须 per-case 判断。19 个技能中 10 个为翻译等价迁移、9 个为中国法 overlay（demand-* / chronology / claim-chart / deposition-prep / legal-hold / subpoena-triage / brief-section-drafter）。

> 本技能套件中事项管理类技能参考自 [陈石 claude-for-legal-ZH](https://github.com/CSlawyer1985/claude-for-legal-ZH)（Apache-2.0），诉讼业务核心技能由元力工场团队基于上游英文版原创适配。

- 技能套件 ID：`litigation-legal`
- 技能数量：19
- 入口技能：`litigation-matter-intake`（案件录入）
- 配置技能：`litigation-cold-start-interview`（冷启动访谈）

## 快速开始

```bash
# 检测环境（建议先执行）
python3 install.py --check-only

# 安装到平台默认目录
python3 install.py

# 或指定目录
python3 install.py --target ~/.agents/skills
```

> 本 Plugin 包含 1 个定时 Workflow（`litigation-docket-watcher`）。
> 如果您的平台不支持定时任务：Legal Gateway 尚未发布（规划中），当前请手动触发 Workflow，或使用平台自身的定时任务能力配置自动触发。
> 详细兼容性检查见 [CHECKPOINT.md](CHECKPOINT.md)。

## 包含的技能

- `litigation-brief-section-drafter`（文书章节起草）
- `litigation-chronology`（时间线）
- `litigation-claim-chart`（要件分析表）
- `litigation-cn-evidence-review`（证据审查）
- `litigation-cold-start-interview`（冷启动访谈）
- `litigation-customize`（个性化调整）
- `litigation-demand-draft`（催告函起草）
- `litigation-demand-intake`（催告函录入）
- `litigation-demand-received`（收到催告函处理）
- `litigation-deposition-prep`（庭前询问准备）
- `litigation-legal-hold`（法律保全）
- `litigation-matter-briefing`（事项简报）
- `litigation-matter-close`（结案）
- `litigation-matter-intake`（案件录入）
- `litigation-matter-update`（案件更新）
- `litigation-matter-workspace`（事项工作区）
- `litigation-oc-status`（外聘律师状态）
- `litigation-portfolio-status`（案件组合状态）
- `litigation-subpoena-triage`（调查令分流）