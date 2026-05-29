# 商事合同法务技能套件

商事合同法务技能套件（中国法本地化版 v0.17.0-cn）—— 12 个技能，依《民法典》合同编 / 《个人信息保护法》/ 《劳动合同法》竞业限制 / 《律师法》第 38 条保密义务。新增 customize + matter-workspace + review (router入口)。

> 本技能套件中文化版本参考自 [陈石 claude-for-legal-ZH](https://github.com/CSlawyer1985/claude-for-legal-ZH)（Apache-2.0），元力工场团队进行了运行时中立适配。

- 技能套件 ID：`commercial-legal`
- 技能数量：12
- 入口技能：`commercial-review`（合同审查路由入口）
- 配置技能：`commercial-cold-start-interview`（冷启动访谈）

## 快速开始

```bash
# 检测环境（建议先执行）
python3 install.py --check-only

# 安装到平台默认目录
python3 install.py

# 或指定目录
python3 install.py --target ~/.agents/skills
```

> 本 Plugin 包含 3 个定时 Workflow（`commercial-deal-debrief`、`commercial-playbook-monitor`、`commercial-renewal-watcher`）。
> 如果您的平台不支持定时任务，建议安装 [Legal Gateway](https://github.com/yuandian-ailaw/Agent-for-legal-cn/tree/main/legal-gateway) 获得自动触发能力。
> 详细兼容性检查见 [CHECKPOINT.md](CHECKPOINT.md)。

## 包含的技能

- `commercial-amendment-history`（修订历史追踪）
- `commercial-cold-start-interview`（冷启动访谈）
- `commercial-customize`（个性化调整）
- `commercial-escalation-flagger`（升级路由）
- `commercial-matter-workspace`（事项工作区）
- `commercial-nda-review`（保密协议审查）
- `commercial-renewal-tracker`（续约跟踪）
- `commercial-review`（合同审查路由入口）
- `commercial-review-proposals`（审查建议处理）
- `commercial-saas-msa-review`（SaaS/MSA 审查）
- `commercial-stakeholder-summary`（业务方简报）
- `commercial-vendor-agreement-review`（供应商协议审查）