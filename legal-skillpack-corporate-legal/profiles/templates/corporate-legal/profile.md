# 公司法务业务规范

*由 cold-start-interview 访谈写入。如看到 `[PLACEHOLDER]`，请先运行 `/corporate-legal:cold-start-interview`。*

---

## 使用说明

本文件是 `corporate-legal` 插件的核心配置文件。所有 skill 在执行前读取此文件，以了解：
- 公司基础信息与法务团队组成
- 适用模块：并购、董事会与秘书、上市公司、主体管理（按需开启）
- 重要性阈值、问题备忘录格式、董事会会议纪要格式、披露清单格式等内部规范
- 升级链与权限矩阵
- 集成连接器状态

如本文件不存在或包含 `[PLACEHOLDER]`，以下 skill 将拒绝运行并提示先完成初始化：

- `/corporate-diligence-issue-extraction`
- `/corporate-material-contract-schedule`
- `/corporate-board-minutes`
- `/corporate-written-consent`
- `/corporate-entity-compliance`
- `/corporate-closing-checklist`
- `/corporate-integration-management`
- `/corporate-deal-team-summary`
- `/corporate-tabular-review`
- `/corporate-ai-tool-handoff`

`/corporate-matter-workspace` 与本配置并存——多交易工作区结构在 `$LEGAL_AGENT_PROFILE_HOME/corporate-legal/deals/<code>/` 下。

---

*激活的模块（Active modules）：* `[PLACEHOLDER —— 并购 | 董事会与秘书 | 上市公司 | 主体管理；可多选]`

---

## 公司简介

*以下内容由 `/corporate-legal:cold-start-interview` 访谈填写。*

- **公司名称：** `[PLACEHOLDER]`
- **所属行业：** `[PLACEHOLDER]`
- **公司性质：** `[私营 / 上市 / 上市公司子公司 —— PLACEHOLDER]`
- **主要注册地（管辖范围）：** `[PLACEHOLDER]`
- **法务团队规模：** `[一人 / N 人团队 —— PLACEHOLDER]`
- **执业环境：** `[公司内部律师 / 中大型律所 / 个人或小型律所 / 政府或法援机构 / 其他 —— PLACEHOLDER]`
- **升级：** `[需更高级别签字（重要性门槛决定、董事利益冲突、超权限决定等）时联系：姓名 / 角色（GC / 合伙人 / 交易负责人 / 自行决定） —— PLACEHOLDER]`

---

## 用户列表

- **使用者类型：** `[律师或法律专业人士 / 非律师但可咨询律师 / 非律师且无定期律师支持 —— PLACEHOLDER]`
- **日常使用者：** `[PLACEHOLDER]`
- **律师联系人（如非律师）：** `[PLACEHOLDER]`

非律师输出模式：输出标题为「研究笔记，需与律师审查」；涉及法律后果的步骤前 skill 会暂停并准备律师沟通简报。

---

## 可用集成

| 集成 | 状态 | 不可用时的回退 |
|---|---|---|
| 数据室（飞书 / 坚果云 / Box / SharePoint / VDR） | `[✓ / ⚪ / ✗ —— PLACEHOLDER]` | 用户手动粘贴文件路径或上传 |
| 董事会门户（飞书云文档 / 专用董事会管理系统） | `[✓ / ⚪ / ✗ —— PLACEHOLDER]` | 用户上传或粘贴会议材料 |
| 主体管理系统（企查查 / 天眼查 / 飞书多维表格 / 手工台账） | `[✓ / ⚪ / ✗ —— PLACEHOLDER]` | 手动维护实体清单 |
| 股权管理（Carta / Shareworks / Ledgr / 手工） | `[✓ / ⚪ / ✗ —— PLACEHOLDER]` | 手动维护股权结构表 |
| 元典法规库 | `[✓ / ⚪ / ✗ —— PLACEHOLDER]` | 引用标记 `[未核验]` |
| 元典案例库 | `[✓ / ⚪ / ✗ —— PLACEHOLDER]` | 引用标记 `[未核验]` |

*重检：`corporate-cold-start-interview --check-integrations`*

---

## 输出

- **工作成果标题：** 律师 → 律师工作成果（含特权标记）；非律师 → 研究笔记（需律师审查）
- **法域：** `[PLACEHOLDER]`
- **披露清单 / 问题备忘录 / 会议纪要 / 同意书的内部格式：** 见各模块下方提取结果

---

## 并购（M&A）

*仅当「并购」模块激活时填写。*

### 交易立场（默认）

- **常见角色：** `[买方 / 卖方 / 两者皆有 —— PLACEHOLDER]`（每个交易的实际立场由 `--new-deal` 写入 `deal-context.md` 覆盖此默认值）
- **交易频率：** `[连续收购 / 偶发 —— PLACEHOLDER]`
- **交易负责部门：** `[企业发展 / 法务 / 外部律师牵头 / 组合 —— PLACEHOLDER]`

### 尽职调查结构

- **类别组织方式：** `[按职能 / 按文档类型 / 其他 —— PLACEHOLDER]`
- **合同审查重要性阈值：** `[全部 / 金额 ≥ X / 按收入排名前 N / 其他规则 —— PLACEHOLDER]`
- **常用 VDR：** `[PLACEHOLDER]`
- **AI 辅助审查工具：** `[PLACEHOLDER 或 无]`

### 问题备忘录格式（来自种子文件提取）

- **章节结构：** `[PLACEHOLDER]`
- **严重程度分级：** `[PLACEHOLDER]`
- **调查结果模板：** `[PLACEHOLDER]`
- **撰写深度：** `[PLACEHOLDER]`

### 卖方具体情况（如卖方业务激活）

- **数据室准备协调人：** `[PLACEHOLDER]`
- **披露备忘录 / 问题日志：** `[是 / 否 —— PLACEHOLDER]`

### 交割清单 与 交易团队简报

- **交割清单存放位置：** `[PLACEHOLDER]`
- **更新责任人：** `[PLACEHOLDER]`
- **简报节奏：** `[每日 / 每周 / 按里程碑 —— PLACEHOLDER]`
- **简报方式：** `[邮件 / Slack / 电话 / 文档 —— PLACEHOLDER]`

---

## 董事会与秘书

*仅当「董事会与秘书」模块激活时填写。*

### 角色与结构

- **职务：** `[公司秘书 / 助理秘书 / 顾问无正式头衔 —— PLACEHOLDER]`
- **董事会规模与组成：** `[PLACEHOLDER]`
- **董事会委员会：** `[审计 / 薪酬 / 提名治理 / 战略 / 其他 —— PLACEHOLDER]`
- **管理工具：** `[飞书云文档 / 专用董事会系统 / 邮件 / 无 —— PLACEHOLDER]`
- **年度例行会议次数与月份：** `[PLACEHOLDER]`

### 会议纪要模板（Minutes template）

*由 corporate-board-minutes 使用——从种子会议纪要提取的内部格式。*

- **整体结构与章节顺序：** `[PLACEHOLDER]`
- **标题格式：** `[公司名称、会议类型、日期、地点 —— PLACEHOLDER]`
- **出席记录格式：** `[PLACEHOLDER]`
- **讨论深度：** `[长篇叙述 / 行动纪要 / 混合 —— PLACEHOLDER]`
- **决议措辞：** `[「决议如下」 / 「兹决议」 / 其他 —— PLACEHOLDER]`
- **附件引用规范：** `[PLACEHOLDER]`
- **签名栏格式：** `[PLACEHOLDER]`
- **标准开场白 / 模板：** `[PLACEHOLDER 或 无]`

### 书面决议

- **常规使用：** `[是 / 否 —— PLACEHOLDER]`
- **典型使用场景：** `[常规高管任免 / 股权授予 / 年度行动 / 更广泛 —— PLACEHOLDER]`
- **决议批准的章程或议事规则限制：** `[PLACEHOLDER 或 无]`

### 决议存储库

- **存储位置：** `[文件夹路径 / 云文档目录 / 飞书目录 / 无集中存储 —— PLACEHOLDER]`

### 决议格式（来自种子决议提取）

- **内部决议措辞：** `[PLACEHOLDER]`
- **鉴于部分结构：** `[PLACEHOLDER]`
- **授权语言：** `[PLACEHOLDER]`
- **副本与电子签名语言：** `[PLACEHOLDER]`
- **签署栏格式：** `[PLACEHOLDER]`

### 年度公司治理常规事项

- `[PLACEHOLDER —— 例：董事选举 / 审计师聘任 / 股权激励计划审批 / 年度董事会自评 等]`

---

## 上市公司

*仅当「上市公司」模块激活时填写。*

- **上市交易所：** `[上交所 / 深交所 / 北交所 / 港交所 / 其他 —— PLACEHOLDER]`
- **财政年度结束日期：** `[PLACEHOLDER]`
- **申报状态：** `[大型加速申报 / 加速申报 / 非加速申报 —— PLACEHOLDER]`

### 信息披露委员会

- **是否设立：** `[是 / 否 —— PLACEHOLDER]`
- **成员构成：** `[CFO / CAO / IR / 法务 / 其他 —— PLACEHOLDER]`
- **会议节奏：** `[季度 / 按需 —— PLACEHOLDER]`

### 内幕交易政策

- **交易窗口（相对财报）：** `[PLACEHOLDER]`
- **预审范围：** `[全部高管和董事 / 更广泛名单 —— PLACEHOLDER]`
- **信息封锁豁免流程：** `[PLACEHOLDER]`

### 业绩说明会

- **法务角色：** `[审讲稿 / 备问答 / 其他 / 不参与 —— PLACEHOLDER]`
- **介入时点：** `[会议前 X 天 —— PLACEHOLDER]`

---

## 主体管理

*仅当「主体管理」模块激活时填写。*

- **活跃实体数量（估计）：** `[PLACEHOLDER]`
- **关键注册地：** `[PLACEHOLDER]`
- **工商登记代办机构：** `[外部代理 / 内部 / 各地不同 —— PLACEHOLDER]`
- **主体管理系统：** `[企查查 / 天眼查 / 飞书多维表格 / 手工台账 —— PLACEHOLDER]`
- **股权结构表工具：** `[Carta / Shareworks / Ledgr / 手工 / N/A —— PLACEHOLDER]`
- **日常申报责任人：** `[PLACEHOLDER]`
- **子公司治理：** `[各自独立治理 / 休眠控股公司 / 混合 —— PLACEHOLDER]`
- **公司间协议：** `[服务协议 / 知识产权许可 / 贷款 / 其他 —— PLACEHOLDER 或 无]`

### 实体清单（来自上传或访谈）

| 实体名称 | 实体类型 | 成立地法域 | 所有权链与股权比例 | 状态 |
|---|---|---|---|---|
| `[PLACEHOLDER]` | `[公司 / 有限责任公司 / 有限公司 / 分支机构 / 其他]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[活跃 / 休眠 / 不活跃]` |

---

## 升级与权限矩阵

*由「公司简介」中的升级问题与（如有）授权委托文件填写。*

| 事项类型 | 自决权限 | 升级阈值 | 上报对象 |
|---|---|---|---|
| `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` |

---

## 法规与白名单时效说明

本配置引用的法规以以下为准：《公司法》《企业信息公示暂行条例》《外商投资法》《证券法》《民法典》合同编。法规以**国家法律法规数据库**最新版本为准；引用前如时效不确定，标 `[未核验]`。

---

## 修订记录

| 日期 | 章节 | 操作 | 备注 |
|---|---|---|---|
| `[YYYY-MM-DD]` | 全部 | 初始化 | `cold-start-interview` 写入 |
