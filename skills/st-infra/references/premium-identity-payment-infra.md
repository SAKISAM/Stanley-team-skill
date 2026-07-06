# Premium、身份验证与收款基础设施

来源说明：本文件为开源版蒸馏规则，不依赖本地素材库。涉及平台规则、地区支持、支付和身份验证时，使用前必须核验最新官方状态。

## 公理

- 基础设施是起号和收益的前置条件，不是增长策略本身。
- 支付、身份认证、地区支持和收款规则变化快，执行前必须核验最新官方状态。
- 任何教程都只能作为经验线索；不能把虚假身份、虚假地址、规避地区写成操作方案。

## 检查对象

| 目标 | 需要确认 |
|---|---|
| Premium / P+ | 当前套餐、价格、地区、支付方式、是否真的需要 P+ |
| Apple 订阅 | Apple ID 地区、支付方式、订阅管理入口 |
| 身份认证 | 真实证件、账号入口、手机语言/环境、失败提示 |
| 收款绑定 | X 收益入口、Stripe/Wise 支持、真实身份和税务/地区材料 |
| 支付失败 | 卡组织、账单信息、地区、风控提示、是否有订阅冲突 |

## 官方依据

| 事项 | 关键点 |
|---|---|
| Premium | X Premium 有 Basic、Premium、Premium+；功能、地区和平台可用性会变化 |
| Web vs App | 官方 FAQ 提到移动端价格可能因应用商店费用不同；通常先比较 web 价格 |
| Premium 权益缺失 | 先比对当前订阅档位和功能，再按官方 troubleshooting / Support 处理 |
| 手机号失败 | 常见原因包括同一手机号绑定超过限制、绑定过 30 天内删除账号、绑定 suspended account |
| 身份验证 | 收益相关项目可能要求 ID verification，以提高真实性并反欺诈 |
| 收款 | Creator Subscriptions / Creator Revenue 相关 payout 通过 Stripe；Stripe 根据创作者所在地判断 payout eligibility 和 methods |
| 税务 | 课程、数字内容、学习产品等销售可能涉及地区、产品形式、平台/市场差异带来的税务责任 |
| Stripe onboarding | Stripe-hosted onboarding 会根据 country、capabilities、business type 动态收集身份和业务信息 |
| Stripe KYC | 验证要求随国家、能力、业务类型、结构和风险水平变化，可能要求真实证件、地址或补充材料 |
| Stripe requirements | currently_due 到期未补齐会变成 past_due，并可能导致 charges 或 payouts 暂停 |
| 商单平台 | 平台可能代做 tracking/payout，但仍要核验平台条款、税务、提现、争议和身份材料 |

## 直达教程入口

| 用户问法 | 先给入口 | 后续检查 | 边界 |
|---|---|---|---|
| 怎么开 P、开 P+、Premium、Premium+、蓝 V | P/P+ 通用教程：https://x.com/snail_9106/status/2023930594003177490 | 购买渠道、订阅档位、真实地区、支付方式、账号是否受限、是否真的需要 P+ | 教程只作流程线索；不复述虚假地址、地区伪装、规避支付或风控的步骤 |
| 怎么绑定创作者收益、Wise 开通、收益收款、Stripe/Wise 打款 | 绑定创作者收益 / Wise 教程：https://x.com/Formulasearch/status/2061726617899073633 | Premium、身份验证、Stripe/Wise 支持、真实身份和税务材料、X Monetization 页面提示 | 不承诺通过；不提供虚假身份、虚假地区、规避 KYC 或绕过平台限制的方法 |

## 可照做输出格式

链接型问题先给入口，再给 3-7 步短清单：

1. 打开直达教程或官方入口。
2. 核对当前账号是否登录正确。
3. 准备真实身份、支付或收款材料。
4. 按页面提示走到失败点或完成点。
5. 截取/复制官方提示原文。
6. 如果卡住，把提示原文、购买渠道、地区和账号状态发回来分诊。

不要把背景写成长段方法论；需要解释时放在“风险提醒”里，用 1-3 条即可。

## 失败分诊

| 现象 | 优先检查 | 路由 |
|---|---|---|
| 买了 Premium 没权益 | 订阅档位、购买平台、是否延迟生效、账号是否受限 | 继续 infra |
| iOS/Android 价格贵 | 对比 web 价格和订阅渠道 | 继续 infra |
| 不能绑定手机号 | 号码是否绑定过多账号、是否关联删除/暂停账号、是否拦截短信 | 继续 infra 或 risk |
| 身份验证失败 | 真实证件、姓名一致性、入口、失败提示 | infra + monetization-check |
| Stripe/Wise/收款失败 | 地区支持、真实身份、税务/收款主体、平台提示 | monetization-check |
| Tutti/商单平台打款失败 | 平台 onboarding、Stripe/KYC、payout 状态、最低提现或争议状态 | infra + monetization-path |
| 支付后账号异常 | 账号提示、登录环境、支付风控 | risk-recovery |

## Stripe / 商单平台分诊

| 提示 | 判断 | 下一步 |
|---|---|---|
| currently_due | 还有当前必须补的字段 | 按平台/Stripe 页面逐项补真实材料 |
| past_due | 已超过截止时间或功能受限 | 先补材料，再观察 charges/payouts 是否恢复 |
| payouts disabled/paused | 打款暂停 | 查身份、地址、税务、银行账户、平台争议 |
| bank account ownership verification | 银行账户归属验证 | 使用平台/Stripe 官方流程验证，不手工暴露敏感账户信息 |
| account country/capability mismatch | 地区或能力不匹配 | 使用真实所在地和真实主体，不做地区伪装 |

## 处理规则

- 新人不默认建议 Premium+，先低成本验证账号方向和执行能力。
- 如果目标是收益验证，先确认 Premium、身份认证、收款主体和地区支持。
- 如果教程出现“生成地址”“地区伪装或异常 IP 操作”等内容，只记录为风险点，不输出为步骤。
- 如果用户问具体开通路径，先让用户描述真实地区、真实证件、支付方式和目标功能。
- 不把 eSIM、港卡、Apple ID 当作规避身份或地区规则的方案；只能作为真实用户的登录、支付和通信条件排查。
- 涉及价格、地区、身份验证入口和 Stripe 支持时，必须提示使用时核验官方最新状态。
- 涉及商单平台时，必须提醒用户核验平台服务条款、付款周期、结算币种、最低提现、争议处理和税务责任。

## 路由

- 目标是创作者收益：转 `/st-monetization-check`。
- 支付或验证导致账号异常：转 `/st-risk-recovery`。
- 基础设施已具备，想变现：转 `/st-monetization-path`。
