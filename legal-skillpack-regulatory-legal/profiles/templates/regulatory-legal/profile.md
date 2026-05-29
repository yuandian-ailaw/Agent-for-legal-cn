# 监管合规法务业务规范

状态：`template`

如果本文件仍包含 `[PLACEHOLDER]`，任何实质监管动态监测、政策比对或内规差异判断都必须停止，并要求先完成业务规范配置。智能体框架应优先读取 `LEGAL_AGENT_PROFILE_HOME/regulatory-legal/profile.md`；本文件只是模板。

## 监管关注清单

| 监管机构 / 主题 | 地域 | 为什么关注 | 优先级 | 元典检索关键词 |
|---|---|---|---|---|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

关注清单决定监管动态监测的范围。没有关注清单时，不得静默检索泛化新闻或模型记忆。

## 使用者与律师联系人

使用者角色：[PLACEHOLDER - 律师 / 法务专业人员 / 有律师支持的非律师 / 无律师支持的非律师]

律师联系人：[PLACEHOLDER]

监管内规差异最终判断人：[PLACEHOLDER]

## 本地存储位置

本地数据根目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}`

政策库目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/documents/regulatory-legal/policies`

监管动态输入目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/documents/regulatory-legal/feeds`

工作成果目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/work-products/regulatory-legal`

评议期台账：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/matters/regulatory-legal/comment-tracker.yaml`

内规差异台账：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/matters/regulatory-legal/gap-tracker.yaml`

核验日志：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/matters/regulatory-legal/verification-log.md`

真实政策、监管材料、客户信息和工作成果不提交 Git。

## 连接器状态

| 能力 | 连接器 | 状态 | 兜底 |
|---|---|---|---|
| `regulatory_feed.fetch_updates` | `yuandian-law` + 本地信息源目录 | 需运行时连接器 | 只处理用户粘贴或本地目录中的监管动态，并标记覆盖缺口 |
| `legal_research.search_laws` | `yuandian-law` | 需运行时连接器 | 标记未核验，不得声称已核验 |
| `legal_research.verify_authority` | `yuandian-law` | 需运行时连接器 | 保留未核验标记并要求人工核对 |
| `legal_research.search_cases` | `yuandian-case` | 需运行时连接器 | 案例部分标记未核验 |
| `legal_research.verify_citation` | `yuandian-law` / `yuandian-case` | 需运行时连接器 | 引用标记未核验 |
| `artifact.write_file` | `local-legal-storage` | 已启用 | 在对话中输出完整简报 |
| `notification.send_digest` | `local-legal-storage` | 已启用 | 只生成本地简报和移交文本，不自动外发 |
| `notification.preview_and_send` | `runtime-notification` | 需运行时连接器 | 只生成可复制通知文本；外发前必须预览并等待确认 |

只有实际探测成功的连接器才能在复核提示中标记为可用。

## 政策库

| 政策 / 制度 | 本地文件 | 最近更新 | 负责人 | 适用主题 |
|---|---|---|---|---|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

政策库用于政策比对和内规差异呈现。没有政策文件时，只能输出监管变化摘要和建议的人工比对路径。

## 重要性阈值

始终重要，必须立即评估：

- [PLACEHOLDER]

值得复核，需要评估后决定：

- [PLACEHOLDER]

仅供参考，只记录不行动：

- [PLACEHOLDER]

跳过，默认过滤：

- [PLACEHOLDER]

征求意见稿、立法预公告、信息征询等预规则材料不能直接当作合规内规差异；应作为方向信号和评议期事项处理。

## 监管动态源配置

检查频率：[PLACEHOLDER - 每日 / 每周 / 自定义]

默认起始日期策略：[PLACEHOLDER - 上次成功检查时间 / 固定回看天数]

元典法律法规关键词：

- [PLACEHOLDER]

本地信息源目录：`skillpack/references/regulatory-source-catalog.md`

手工输入路径：

- 用户粘贴监管动态
- `${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/documents/regulatory-legal/feeds`

覆盖缺口处理：

- 如果关注清单关注的地域或主题没有对应信息源，简报顶部必须提示一次覆盖缺口。
- 如果用户明确选择暂不覆盖某类来源，应记录原因和日期，避免重复打扰。

## 内规差异响应流程

监管变化初筛负责人：[PLACEHOLDER]

政策更新负责人：[PLACEHOLDER]

评议期决策负责人：[PLACEHOLDER]

升级路径：[PLACEHOLDER]

内规差异台账位置：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/matters/regulatory-legal/gap-tracker.yaml`

评议台账位置：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/matters/regulatory-legal/comment-tracker.yaml`

## 输出规则

所有简报、政策比对、内规差异报告都必须包含复核提示，集中说明：

- 实际使用了哪些来源和连接器
- 读取范围
- 覆盖缺口
- 哪些引用已由元典 MCP 核验
- 哪些项目仍需人工核对

如果角色是律师或法务专业人员，默认工作成果头：

`律师工作材料 — 涉密 — 在律师指挥下制作`

如果角色不是法律专业人员，默认工作成果头：

`研究笔记 — 非法律意见 — 行动前请由持证律师复核`

来源标签规则：

- `[元典法规]` 仅用于本次运行中确实由元典法律法规 MCP 返回的法规或规范性文件。
- `[元典案例]` 仅用于本次运行中确实由元典案例 MCP 返回的案例。
- `[用户提供]` 用于用户粘贴或本地提供的材料。
- `[模型知识 — 需核验]` 用于未检索、未核验的模型知识。
- `[二级来源 — 需核验]` 用于二级来源，应追溯到一手出处。

输出默认写入：

`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/work-products/regulatory-legal/digests`

对外通知只生成移交文本，不自动发送。
