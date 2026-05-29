# AI 治理合规技能套件

中国 AI 治理合规技能集群——基于《生成式 AI 暂行办法》《算法推荐管理规定》《深度合成管理规定》《PIPL》《数据安全法》《网安法 2025 修正》《网络数据安全管理条例》《人脸识别办法》《内容标识办法》《伦理审查办法》11 部现行法规为依据。9 个技能形成「冷启动配置 → profile 单点调整 → 用例分类 → 影响评估 → 供应商审查 → 法规差距 → 政策监控 → 政策起草 → 系统清单」全闭环。Provider / Deployer 角色二分，L1-L4 合规等级，备案触发（算法 / 生成式 AI / 人脸信息）三类专项追踪。

- 技能套件 ID：`ai-governance-legal`
- 技能数量：9
- 入口技能：`ai-governance-use-case-triage`（用例分类）
- 配置技能：`ai-governance-cold-start-interview`（冷启动访谈）

## 快速开始

```bash
# 检测环境（建议先执行）
python3 install.py --check-only

# 安装到平台默认目录
python3 install.py

# 或指定目录
python3 install.py --target ~/.agents/skills
```

> 本 Plugin 不包含定时 Workflow，所有 Skill 可直接在平台内手动使用。
> 详细兼容性检查见 [CHECKPOINT.md](CHECKPOINT.md)。

## 包含的技能

- `ai-governance-aia-generation`（AI 影响评估）
- `ai-governance-cold-start-interview`（冷启动访谈）
- `ai-governance-customize`（个性化调整）
- `ai-governance-inventory`（AI 系统清单）
- `ai-governance-policy-monitor`（政策监控）
- `ai-governance-policy-starter`（政策起草）
- `ai-governance-reg-gap-analysis`（法规差距分析）
- `ai-governance-use-case-triage`（用例分类）
- `ai-governance-vendor-ai-review`（供应商 AI 审查）