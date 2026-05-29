# 中国法法律研究技能套件

中国法律研究技能集群——通过元典 MCP（法规 / 案例 / 企业）+ Tavily MCP（二手文献）做精确法条检索、综合法律研究、裁判文书检索和企业信息查询。四个技能形成「按需精细查 + 综合研究备忘录」的研究闭环，可被 commercial / privacy / regulatory / employment 四大业务技能集群在需要中国法 grounding 时调用。

- 技能套件 ID：`legal-research-cn`
- 技能数量：4
- 入口技能：`prc-legal-research-deep-research`（综合法律研究）

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

- `prc-legal-research-law-search`（法条精确检索）
- `prc-legal-research-deep-research`（综合法律研究）
- `prc-legal-research-case-search`（裁判文书检索）
- `prc-legal-research-company-search`（企业信息查询）