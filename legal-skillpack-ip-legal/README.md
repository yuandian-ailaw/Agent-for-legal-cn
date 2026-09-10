# 知识产权法务技能套件

知识产权法务技能套件（中国法本地化版 v0.18.0-cn）—— 12 个技能，覆盖知识产权全周期。FTO + 清查 / 发明披露 / 合同 IP 条款审查 / 维权（停止侵权函 + 下架通知）/ IP 组合管理 / 开源合规 / 多事项工作区。中国法依据：《专利法》（2020 修正）+ 《商标法》（2019 修正）+ 《著作权法》（2020 修正）+ 《反不正当竞争法》（2025 修正）+ 《电子商务法》第 42-45 条 + 《信息网络传播权保护条例》第 14-17/24 条 + 《律师法》（2026修正）第 41 条 + 专利代理条例第 17 条。

- 技能套件 ID：`ip-legal`
- 技能数量：12
- 入口技能：`ip-matter-workspace`（事项工作区）
- 配置技能：`ip-cold-start-interview`（冷启动访谈）

## 快速开始

```bash
# 检测环境（建议先执行）
python3 install.py --check-only

# 安装到平台默认目录
python3 install.py

# 或指定目录
python3 install.py --target ~/.agents/skills
```

> 本 Plugin 包含 1 个定时 Workflow（`ip-renewal-watcher`）。
> 如果您的平台不支持定时任务：Legal Gateway 尚未发布（规划中），当前请手动触发 Workflow，或使用平台自身的定时任务能力配置自动触发。
> 详细兼容性检查见 [CHECKPOINT.md](CHECKPOINT.md)。

## 包含的技能

- `ip-cease-desist`（停止侵权函）
- `ip-clause-review`（IP 条款审查）
- `ip-clearance`（商标清查）
- `ip-cold-start-interview`（冷启动访谈）
- `ip-customize`（个性化调整）
- `ip-fto-triage`（FTO 分流）
- `ip-infringement-triage`（侵权分流）
- `ip-invention-intake`（发明披露录入）
- `ip-matter-workspace`（事项工作区）
- `ip-oss-review`（开源合规审查）
- `ip-portfolio`（IP 组合管理）
- `ip-takedown`（下架通知）