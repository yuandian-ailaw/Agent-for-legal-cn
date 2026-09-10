# 监管栏目页参考清单

> 最后人工可达性核验：2026-09-09。**仅作搜索验证的起点**，不直接用于轮询；以下站点多数有反爬机制（flk.npc.gov.cn 403、gsxt.gov.cn 521 属正常），脚本探测失败不代表页面失效——以浏览器人工访问为准。

## 全国人大 / 法律数据库

- 国家法律法规数据库：https://flk.npc.gov.cn/ （法律、行政法规、司法解释权威文本；反爬严格，人工访问）
- 全国人大网-法律草案征求意见：http://www.npc.gov.cn/npc/c2/c30834/ （立法动态与征求意见稿）

## 市场监管 / 反垄断

- 市场监管总局-政策文件：https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/fgs/
- 市场监管总局-反垄断指南：https://www.samr.gov.cn/xw/zj/（反垄断执法动态按栏目检索）

## 网信 / 数据

- 网信办-政策文件：https://www.cac.gov.cn/zwgk/
- 全国网信系统-执法督查：https://www.cac.gov.cn/ztzl/zhengcefagui/

## 金融 / 证券

- 证监会-规章与规范性文件：http://www.csrc.gov.cn/csrc/c101954/zfxxgk_zdgk.shtml
- 金融监管总局-政策法规：https://www.nfra.gov.cn/

## 工业与信息化

- 工信部-政策文件：https://www.miit.gov.cn/jgsj/zbes/zhengcefagui/index.html

## 使用方式

1. 轮询策略：优先各站官方 RSS / 政策文件栏目 API；无 RSS 的站点以站内搜索关键词触发（法规名 + "征求意见" / "修订" / "施行"）。
2. 命中后到国家法律法规数据库或元典 MCP 核验时效性（sxx 字段），再登记进 profile 的 watch 清单。
3. 栏目改版会导致 URL 失效——发现 404 时先站内搜索替代入口，再更新本清单并记录日期。
