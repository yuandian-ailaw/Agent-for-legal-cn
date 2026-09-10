# 商事合同法务 业务规范

状态：`template`

如果本文件仍包含 `[PLACEHOLDER]`，任何实质合同审查都必须停止，并要求先完成 profile 配置。智能体框架应优先读取 `LEGAL_AGENT_PROFILE_HOME/commercial-legal/profile.md`；本文件只是模板。

## 组织与合同团队

公司名称：[PLACEHOLDER]

行业与业务模式：[PLACEHOLDER]

合同团队规模：[PLACEHOLDER]

每月合同量与主要类型：[PLACEHOLDER]

最终法律升级联系人：[PLACEHOLDER]

主要痛点：[PLACEHOLDER]

## 使用者与律师联系人

使用者角色：[PLACEHOLDER - 律师 / 法务专业人员 / 有律师支持的非律师 / 无律师支持的非律师]

律师联系人：[PLACEHOLDER]

如果使用者不是具备执业资格或等同专业职责的法律人员，输出必须使用“研究笔记 / 非法律意见 / 需律师复核”头部。

## 本地存储位置

本地数据根目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}`

合同目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/contracts`

通用文档目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/documents`

工作成果目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/work-products/commercial-legal`

事项目录：`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/matters/commercial-legal`

真实合同、客户材料和工作成果不提交 Git。

## 连接器状态

| Capability | Connector | 状态 | Fallback |
|---|---|---|---|
| `document_storage.fetch_file` | `local-legal-storage` | enabled | 用户上传文件、提供本地路径或粘贴合同全文 |
| `contract_repository.fetch_agreement` | `local-legal-storage` | enabled | 用户上传合同或提供本地副本 |
| `artifact.write_file` | `local-legal-storage` | enabled | 在对话中输出完整 memo |
| `legal_research.verify_citation` | `yuandian-law` / `yuandian-case` | requires runtime connector | 标记未验证并提示人工复核 |

已连接不等于已配置。智能体框架只有在实际读取本地文件或元典 MCP 探测成功后，才可在 reviewer note 中标记为可用。

## 合同审查 Playbook

主要合同侧：[PLACEHOLDER - 销售侧 / 采购侧 / 两者都有]

判断合同侧时先读标题、签署方、定义、订单关系和附件标题；不能只靠正文关键词。

### 销售侧 Playbook

适用于公司作为供应商、卖方、服务提供方或许可方。

责任限制：

- 直接损失责任上限：[PLACEHOLDER]
- 间接 / 后果性损害：[PLACEHOLDER]
- 超出责任上限的 carveouts：[PLACEHOLDER]
- 可接受 fallback：[PLACEHOLDER]
- Never accept：[PLACEHOLDER]

赔偿：[PLACEHOLDER]

数据保护：[PLACEHOLDER]

期限与终止：[PLACEHOLDER]

知识产权：[PLACEHOLDER]

管辖法律和争议解决：[PLACEHOLDER]

The one thing：[PLACEHOLDER - 销售侧最不能让步的一件事]

### 采购侧 Playbook

适用于公司作为客户、买方、采购方、被许可方或接受服务方。

责任限制：

- 供应商责任上限：[PLACEHOLDER]
- 必须 carve out 的事项：[PLACEHOLDER]
- 可接受 fallback：[PLACEHOLDER]
- Never accept：[PLACEHOLDER]

赔偿：[PLACEHOLDER]

数据保护：[PLACEHOLDER]

期限、续约和终止：[PLACEHOLDER]

知识产权与交付物：[PLACEHOLDER]

管辖法律和争议解决：[PLACEHOLDER]

The one thing：[PLACEHOLDER - 采购侧最不能让步的一件事]

## 合同类型路由规则

先读取主协议、附件、schedule、addendum、DPA、SLA、order form 的标题，再决定路由。

| 合同类型 | 目标 skill | 路由提示 |
|---|---|---|
| NDA / 保密协议 | `commercial-nda-review` | 关注保密范围、期限、残留知识、强制披露、返还销毁 |
| SaaS MSA / 订阅协议 | `commercial-saas-msa-review` | 关注服务承诺、SLA、数据处理、续约、责任限制 |
| 供应商 / 服务 / 咨询协议 | `commercial-vendor-agreement-review` | 关注付款、交付、验收、IP、数据、安全、终止 |
| DPA | 作为 overlay | 不单独拆成第二份 memo，整合进主 memo |
| SLA / Support terms | 作为 overlay | 标记服务可用性、赔偿、服务抵扣和排除项 |
| Amendment / Order Form | 结合主协议 | 必须识别修改了哪些主协议条款 |

`confirm_routing` 默认为 true。路由判断完成后，必须先向用户确认再进行完整审查，除非用户明确关闭该门槛。

## 升级矩阵

| 可审批人 | 无需升级范围 | 必须升级给 | 方式 |
|---|---|---|---|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

金额阈值：[PLACEHOLDER]

无论金额大小均自动升级：

- [PLACEHOLDER]

超出权限矩阵时，审查 memo 必须生成给 approver 的具体 ask，而不只是标记风险。

## 输出规则

所有分析、memo 和审查意见都应包含 reviewer note，集中说明来源、读取范围、未验证项目和人工判断点。

如果角色是律师或法务专业人员，默认工作成果头（中国法场景使用中文标注——中国法律体系下不存在美国法的 attorney work product 特权制度，使用英文特权标头会让文件被误认为受特权保护）：

`保密 / 内部法律分析 — 仅供法务团队使用 — 不构成外发法律意见`

如果角色不是法律专业人员，默认工作成果头：

`研究笔记 — 不构成法律意见 — 请律师复核后再依赖`

多个下游 review skill 适用时，输出一份整合 memo，而不是多份分散 memo。

输出默认写入：

`${LEGAL_AGENT_LOCAL_DATA_HOME:-local-data}/work-products/commercial-legal`

对外发送、签署、CLM 更新或通知只生成 handoff 建议，不自动执行。
