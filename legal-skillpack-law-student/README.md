# 法学学习与法考备考技能套件

中国法学学习技能集群——以 13 个技能覆盖法学院学习场景（本科 / 法硕 / 法学硕士 / 法学博士）和国家统一法律职业资格考试（法考）备考。基于 8 部中国法律 / 司法解释 / 监管文件（《律师法》《国家统一法律职业资格考试实施办法》《最高人民法院关于案例指导工作的规定》《最高人民法院关于统一法律适用加强类案检索的指导意见》《立法法（2023 修正）》《民事诉讼法》《行政诉讼法》/ GB/T 7714-2015）+ 元典 API 平台（yuandian-law / yuandian-case）作为检索支撑。13 个技能中 1 个为翻译（customize）+ 12 个为中国法 overlay（覆盖 MBE/UBE/NextGen → 法考 / 判例法 → 成文法 / 1L-3L → 本科-硕士-博士 / Bluebook → GB/T 7714 / Westlaw + CourtListener → 元典 / IRAC → IRAC + 鉴定式分析法 + 三段论 / attorney-client privilege → 《律师法》第 38 条保密义务）。

- 技能套件 ID：`law-student`
- 技能数量：13
- 入口技能：`law-student-session`（学习会话）
- 配置技能：`law-student-cold-start-interview`（冷启动访谈）

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

- `law-student-bar-prep-questions`（法考练习题）
- `law-student-case-brief`（案例摘要）
- `law-student-cold-call-prep`（课堂提问准备）
- `law-student-cold-start-interview`（冷启动访谈）
- `law-student-customize`（个性化调整）
- `law-student-exam-forecast`（考点预测）
- `law-student-flashcards`（记忆卡片）
- `law-student-irac-practice`（IRAC 练习）
- `law-student-legal-writing`（法律写作）
- `law-student-outline-builder`（课程大纲）
- `law-student-session`（学习会话）
- `law-student-socratic-drill`（苏格拉底问答）
- `law-student-study-plan`（学习计划）