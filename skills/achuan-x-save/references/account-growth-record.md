# 账号成长档案格式

来源说明：本文件为开源版状态格式，蒸馏自数据作战计划的“本地 JSON 记忆”思想；不依赖服务器、数据库、私有路径或特定品牌。

## 设计原则

- 一个账号一个成长档案，用户自己保存。
- 成长档案用于跨会话对比：首次基准、7 天复盘、季度复盘。
- 成长档案只保存事实、判断和下一步假设，不保存未授权隐私材料。
- Markdown 存档适合人读；JSON 成长档案适合下次复盘时机器读取。

## 文件命名

```text
{handle}_achuan_x_growth_record.json
```

如果没有 handle，用项目名：

```text
{project}_achuan_x_growth_record.json
```

## 最小字段

```json
{
  "version": "1.0",
  "handle": "@example",
  "nickname": "",
  "bio": "",
  "directions": [],
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "last_analysis_date": "YYYY-MM-DDTHH:MM:SS",
  "total_analyses": 1,
  "current_stage": "",
  "baseline": {
    "date": "YYYY-MM-DD",
    "followers": 0,
    "avg_impressions": 0,
    "new_follows": 0,
    "reply_ratio": 0,
    "top_content_type": "",
    "viral_formula": ""
  },
  "analyses": [],
  "execution_history": [],
  "viral_patterns": {
    "confirmed": [],
    "emerging": [],
    "fatigue_signals": []
  },
  "growth_milestones": [],
  "next_skill": "",
  "confidence": "",
  "evidence_sources": [],
  "privacy_status": "redacted",
  "next_review_at": "",
  "notes": []
}
```

## 单次分析记录

每次数据复盘后，在 `analyses` 里追加：

```json
{
  "id": "YYYY-MM-DD",
  "date": "YYYY-MM-DD",
  "mode": "FIRST_TIME | WEEKLY | QUARTERLY",
  "data_period": "",
  "followers_at_time": 0,
  "stats": {
    "total_posts": 0,
    "total_impressions": 0,
    "avg_impressions": 0,
    "max_impressions": 0,
    "new_follows_period": 0,
    "reply_ratio": 0,
    "type_breakdown": {}
  },
  "findings": [],
  "plan": {
    "start_date": "",
    "end_date": "",
    "kpi_targets": {},
    "content_ratio": {},
    "top_hypotheses": []
  },
  "evidence": {
    "csv_summary": "",
    "official_links": [],
    "user_provided_context": [],
    "excluded_causes": []
  },
  "self_reported_execution": "",
  "execution_score": ""
}
```

## 执行历史

当用户做 7 天或季度复盘时，在 `execution_history` 里保存：

```json
{
  "date": "YYYY-MM-DD",
  "previous_plan_id": "YYYY-MM-DD",
  "execution_score": "A | B | C | D",
  "execution_rate": 0,
  "kpi_achievements": {},
  "what_worked": [],
  "what_to_reduce": [],
  "next_adjustment": []
}
```

## 保存规则

- 不保存原始 CSV 全文，只保存聚合结果和 TOP 帖摘要。
- TOP 帖摘要最多保留前 80-120 字，避免把成长档案变成全文搬运库。
- 保存“已排除方向”，例如不是风险异常、不是主页承接、不是收益问题。
- 如果用户没有授权，不保存邮箱、证件、支付、手机号等敏感信息。
- 如果涉及收益暂停、风险恢复或身份验证，只保存状态摘要和下一步 skill，不保存完整私密材料。
- 如果涉及商单/赞助，保存品牌类别、披露状态、交付指标和付款状态摘要，不保存合同全文或付款账号。

## 开源迁移规则

- 存档路径只能使用 `~/.achuan-x-operation-flow`、`${ACHUAN_X_HOME}` 或用户指定目录。
- reference 只保存公开来源 URL 或来源 ID，不保存私有飞书、浏览器 cookie、抓取日志。
- 每次保存都写入 `schema_version`，由 `achuan-x-save` 在恢复或生成报告时按版本读取。
- `privacy_status` 默认为 `redacted`；如果用户要求保存敏感摘要，标为 `contains-sensitive-summary`。

## 下次使用

- 有成长档案 + 新 CSV：进入 7 天/季度复盘。
- 无成长档案 + 新 CSV：进入首次基准。
- 有成长档案但无新 CSV：只能做历史状态恢复，不能编造新数据。
