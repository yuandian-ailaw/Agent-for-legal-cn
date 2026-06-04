<!--
配置位置（版本无关，插件更新不覆盖）

用户配置写入：
  $LEGAL_AGENT_PROFILE_HOME/legal-builder-hub/profile.md

规则：
1. 所有 skill / agent 从上述路径读取配置，不读本模板文件。
2. 若 profile.md 不存在或仍含 [PLACEHOLDER]，除 `legal-builder-hub-cold-start-interview` 与 `--check-integrations` 外，停止实质性工作并提示先完成冷启动。
3. 冷启动与 customize 写入 profile.md；首次运行可从旧 Claude 插件缓存路径迁移。
4. 本文件为模板，随包更新；勿写入用户数据。

共享公司层：$LEGAL_AGENT_PROFILE_HOME/company-profile.md（各 practice area 共用）。
-->

# Legal Builder Hub 管理配置（profile）

*由冷启动于 [DATE] 填写。*

---

## 使用角色

**角色：** [PLACEHOLDER — 律师/法务 | 非律师（有律师支持）| 非律师（无固定律师）]
**律师联系人：** [PLACEHOLDER]

---

## 可用集成

| 集成 | 状态 | 不可用时的回退 |
|---|---|---|
| 办公通讯（飞书 / 企业微信 / 钉钉；海外可选 Slack） | [✓ / ✗] | 新 skill / 更新通知在下次 `legal-builder-hub-registry-browser` 或 `legal-builder-hub-auto-updater` 时展示 |
| 本地 digest | [✓] | `$LEGAL_AGENT_PROFILE_HOME/legal-builder-hub/digests/registry-sync-latest.md` |

*重检：`legal-builder-hub-cold-start-interview --check-integrations`*

---

## 输出

本插件不产出实体法工作成果，负责发现、install、QA 社区 skill。已安装 skill 自带输出头；hub 不覆盖。

**管辖权与保密头（QA 时检查）。** 社区 skill 常带美国 attorney work product 表述；中国法场景应使用 `plugin/shared/header-by-role.md` 与 `disclaimer-cn.md`。

**非律师输出模式。** 当角色为非律师时，hub 面向用户的输出须含律师简报段与通俗说明。

---

## 共享护栏

- **三值规则（禁止静默补全）：** 带 flag 补充 / 停止索要原文 / 仅提示疑点 `[model knowledge — verify]`
- **用户陈述法条须核验**后再展开分析
- **目的地检查**：对外发送前确认是否应带保密标记
- **显式批准**：安装、更新、卸载须用户明确 yes

---

## 法律元力（yuanli）

| 项 | 值 |
|---|---|
| **base_url** | `https://yuanli.ailaw.cn`（[法律元力](https://yuanli.ailaw.cn/)，无尾斜杠；冷启动默认；可用 customize 修改） |
| **api 参考** | `references/yuanli-api.md`（各 hub skill 目录内） |

有 `base_url` 时：`registry-browser` / `skill-installer` / `auto-updater` / `registry-sync` **优先调公开 REST API**（`{BASE}/api/...`）；API 失败或未配置时回退 `references/yuanli-toolkits.yaml`。

## 监视的 registry

由冷启动写入；默认见 `references/registries.yaml`（**yuanli-cn 优先**，其次 GitHub）。

## Allowlist

`$LEGAL_AGENT_PROFILE_HOME/legal-builder-hub/allowlist.yaml` — 默认自 `references/allowlist-default.yaml` 复制。

## 已安装 skill

`$LEGAL_AGENT_PROFILE_HOME/legal-builder-hub/install-log.yaml`

---

## 中国法 入门包 映射（冷启动推荐）

| 实践侧重 | 法律元力 toolkit_id |
|----------|----------------------|
| 法律研究 | legal-skillpack-legal-research-cn |
| 商事合同 | legal-skillpack-commercial-legal |
| 公司法务 | legal-skillpack-corporate-legal |
| 监管合规 | legal-skillpack-regulatory-legal |
| 诉讼 | legal-skillpack-litigation-legal |
| AI 治理 | legal-skillpack-ai-governance-legal |
| 法学学习/法考 | legal-skillpack-law-student |

