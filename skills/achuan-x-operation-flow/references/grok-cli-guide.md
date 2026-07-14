# Grok CLI 账号检索

## 什么时候使用

用户要分析具体 X 账号、近期公开帖子、增长表现、可见度异常或收益风险时使用。用户只问一般方法、固定规则或直接入口时不需要调用。

## 开头先问

用小白能听懂的话收集：

1. 你的 X 账号 ID（`@名字`）或主页链接。
2. 现在大概多少粉丝。
3. 你最想解决什么问题。

风险和收益问题还要收集官方提示原文与发生时间。没问清楚前不调用、不路由、不猜原因。

## 安装与登录

Grok Build CLI 是可选能力。先检查：

```bash
command -v grok || test -x "$HOME/.grok/bin/grok"
grok --version
```

未安装时，先说明将安装官方 CLI，获得用户同意后运行：

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
```

未登录时运行：

```bash
grok login --oauth
```

CLI 仍处于快速更新阶段，订阅资格以登录页面实际提示为准。不能登录时转手动方案，不让整个问诊停住。

## 调用方式

优先使用随 skill 提供的脚本：

```bash
scripts/grok-x-research.sh @handle overview
scripts/grok-x-research.sh @handle growth
scripts/grok-x-research.sh @handle risk
scripts/grok-x-research.sh @handle monetization
```

脚本在临时空目录运行，并使用 `--verbatim --no-plan --no-memory --no-subagents`，减少本地项目和其他 agent 配置干扰。

## 如何使用结果

- 把 Grok 输出当成公开信息初筛，不当成 X 官方判定。
- 先区分“看得到的事实”“可能原因”“还缺的证据”。
- 账号风险和收益判断必须再结合用户收到的官方提示、时间和近期操作。
- Grok 看不到帖子或没有可靠链接时，明确写“无法确认”，不要补全或猜测。
- 给用户回答时只保留有用结论和步骤，不展示长来源清单。需要用户核对某条帖子时才给对应链接。

## 隐私边界

- 只发送公开账号 ID 和公开帖子检索任务。
- 不发送私信、邮件全文、证件、手机号、邮箱、支付资料、Stripe/Wise 信息或未公开截图。
- 不让 Grok 登录用户账号、删帖、发帖、申诉或修改设置。
- 删除或整改建议必须由 Codex 根据公开帖子、用户材料和平台提示综合判断。

## 失败时怎么做

如果 CLI 未安装、未登录、超时或无法搜索 X：

1. 请用户提供主页截图、最近 10-20 条帖子链接或 X Analytics 数据。
2. 继续做人工诊断，并标明哪些结论还不能确认。
3. 不反复要求安装，也不声称已经查过账号。
