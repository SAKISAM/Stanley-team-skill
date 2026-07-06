# 工具与素材源地图

来源说明：本文件为开源版工具地图，不依赖本地素材库。工具可用性、价格、权限和页面状态变化快，使用前应现查。

## 工具分类

| 类别 | 工具/来源 | 用途 | 状态 |
|---|---|---|---|
| 爆款监测 | X Viral Monitor | views/hour、热帖排行、Markdown 复制、支持者图谱、Grok 回复草稿 | 已抓取公开商店页 |
| 影子封禁检测 | Shadowban Checker F：https://x-shadowban-checker.fia-s.com/ | 检查帖子是否被搜索排除、最近帖子是否隐藏 | 已抓取元信息 |
| P/P+ 教程 | snail_9106 P/P+ 通用教程：https://x.com/snail_9106/status/2023930594003177490 | 开 P、开 P+、Premium、Premium+、蓝 V 的流程线索 | 已抓取公开 X 帖 |
| 收益绑定教程 | Formulasearch 收益绑定 / Wise 开通：https://x.com/Formulasearch/status/2061726617899073633 | 绑定创作者收益、Wise 开通、收益收款的流程线索 | 已抓取公开 X 帖 |
| 新闻热点 | NewsNow | 实时新闻聚合阅读 | 已抓取元信息 |
| 热榜入口 | TopHub | 泛流量选题雷达 | 抓取时 503，待复抓 |
| 跨平台内容 | 新榜 | 榜单、热门内容、创作者工具、投放变现线索 | 已抓取公开页 |
| 官方规格 | X Help Profile / Posts / Articles / Replies / Lists | 核验主页规格、内容格式、回复可见性、互动名单 | 使用时现查 |
| 商单平台 | Tutti：https://tutti.so/join?ref=YLFW7F | 3000 粉以上尝试进入平台接单、浏览 campaign、提交内容、查看 tracking/payout | 已抓取公开页 |
| 商单规则 | X Paid Partnerships Policy / FTC Endorsements | 检查 Paid Partnership disclosure、material connection、禁投品类 | 使用时现查 |
| 打款规则 | Stripe Connect docs | 检查 onboarding、KYC、currently_due/past_due、payout 状态 | 使用时现查 |

## 公理

- 工具只提供信号，不替代判断。
- 爆款监测的作用是发现“正在起量的流量池”，不是复制原文。
- 热点源要经过账号方向过滤，不能所有热点都追。

## 使用流程

1. 先明确当前用途：找选题、找热帖回复、检测可见度、找对标、找变现渠道、查商单规则或查收款状态。
2. 选择对应工具。
3. 把工具发现的内容转成 Markdown 或记录到素材池。
4. 交给 `/st-content-system` 做选题重组，或交给 `/st-reply-growth` 做回复策略。

## 工具 SOP

| 用途 | SOP |
|---|---|
| 爆款监测 | 找正在起量的帖子，记录主题、钩子、证据、评论区需求；不要复制原文 |
| 影子封禁检测 | 先直接给链接 https://x-shadowban-checker.fia-s.com/；再用无痕 `from:handle`、精确句子和回复可见性测试交叉验证 |
| 开 P/P+ | 先直接给链接 https://x.com/snail_9106/status/2023930594003177490；再转 `/st-infra` 检查购买渠道、订阅档位、真实支付条件和账号是否受限 |
| 绑定收益/Wise | 先直接给链接 https://x.com/Formulasearch/status/2061726617899073633；再转 `/st-infra` 检查 Stripe/Wise、身份、地区和 Monetization 页面提示 |
| 热点素材 | 先用 NewsNow/TopHub/新榜找信号，再用官方/原始来源核验事实 |
| 互动名单 | 用 X Lists 分组大号、同行、潜在客户、素材源 |
| 官方规格 | 主页、handle、longer post、Article、reply/quote 等先查 X Help 最新说明 |
| 商单平台 | 3000 粉以上可看 Tutti 等平台；先检查领域、互动、披露和打款条款 |
| 商单合规 | 先查 X Paid Partnerships Policy 和 FTC endorsement guidance，再写内容 |
| Stripe/打款 | 查看平台 onboarding、currently_due、past_due、payout 状态，再转 `/st-infra` |

## 边界

- 不安装、登录或购买工具，除非用户明确要求并确认。
- 不使用工具做批量自动化互动。
- 涉及账号状态检测时，工具结果只作为线索，最终以平台提示和实际可见度为准。
- Shadowban Checker F 的结果要和无痕 `from:handle` 搜索、精确句子搜索、回复可见性测试交叉验证。
- X 帖教程只作为流程入口；涉及价格、地区、身份、支付、收款和 KYC 时，以官方页面当前提示为准。
