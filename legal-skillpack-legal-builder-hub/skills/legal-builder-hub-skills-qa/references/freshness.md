# Skill 时效四字段格式定义

> 最后核验：2026-09-09

legal-builder-hub 对"skill 内容是否过期"的机读约定。绑定时效管理的 skill，其 SKILL.md frontmatter 声明以下四字段：

```yaml
last_verified: 2026-09-09      # 最近一次人工/活库核验日期（ISO 8601）
freshness_window: 90d          # 时效窗口：90d / 180d / 1y（按内容漂移风险定级）
freshness_category: law-citation   # 类别见下表
verified_against: yuandian         # 核验数据源标识
```

## freshness_category 取值

| 类别 | 含义 | 建议 window |
|---|---|---|
| law-citation | 内含法条引用，法规可能修订/废止 | 90d |
| regulator-feed | 监控监管动态的清单类内容 | 90d |
| platform-api | 依赖外部 API/接口契约（元典 MCP、yuanli API） | 180d |
| template-output | 文书/表格模板，法条以变量方式引入 | 180d |
| process-only | 纯流程说明，无外部事实依赖 | 1y |

## QA 判定规则（legal-builder-hub-skills-qa 使用）

1. `last_verified` 缺失或超出 `freshness_window` → 时效档降一级（可安装→有顾虑）。
2. `freshness_category: law-citation` 的 skill 未通过 `tools/verify_citations.py` → 重大顾虑。
3. `verified_against` 应指向可复核的数据源（yuandian / npc / 官网清单）；缺核验源 = 未核验。
4. 超窗skill 的修复路径：活库核验 → 更新 last_verified → 登记到 docs/legal-citations/registry.yaml。
