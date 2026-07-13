# Achuan-X-OperationFlow

Achuan-X-OperationFlow 是一组面向 Codex 的 X/Twitter 起号与增长技能。它不是单个重型 skill，而是一套轻量、可路由、可继续扩展的 skill 群。

它覆盖主页搭建、发推节奏、内容系统、回复增长、增长诊断、账号风险恢复、创作者收益检查、基础设施、平台外变现、工具导航和状态保存等流程。

## 这是什么

- 一组位于 `skills/achuan-x-*` 下的本地 Codex skills。
- 一套用于 X/Twitter 成长的策略、诊断、规划、模板和检查清单。
- 一个自包含的开源发布包，不依赖私有飞书/Lark 文档、原始抓取材料、浏览器日志或本地绝对路径。

## 这不是什么

- 不会登录或代操作你的 X/Twitter 账号。
- 不会自动发帖、关注、取关、回复或刷互动。
- 不提供规避平台风控、虚假身份验证、批量注册、操纵互动、操纵收益或绕过平台规则的方法。
- 不承诺创作者收益、账号恢复、身份验证、打款或涨粉结果。

## 包含的 Skill

| Skill | 用途 |
|---|---|
| `achuan-x-operation-flow` | Achuan-X-OperationFlow 技能群主入口和路由器 |
| `achuan-x-profile` | 主页搭建：头像、header、ID、bio、置顶帖 |
| `achuan-x-content-rhythm` | 发推节奏、短推/长文比例、阶段计划 |
| `achuan-x-content-system` | 内容栏目、选题池、短推/长文/回复/引用分工 |
| `achuan-x-reply-growth` | 回复策略、互动频率、评论区涨粉 |
| `achuan-x-growth-diagnosis` | 低曝光、低互动、涨粉慢等增长诊断 |
| `achuan-x-risk-recovery` | 冻结、锁定、受限、影子封禁、账号异常 |
| `achuan-x-monetization-check` | 创作者收益资格、自查、暂停和申诉准备 |
| `achuan-x-infra` | Premium/P+、Wise、Stripe、eSIM、支付、身份验证 |
| `achuan-x-monetization-path` | 平台外变现：咨询、社群、课程、服务、商单 |
| `achuan-x-toolkit` | 工具入口、爆款监测、影子封禁查询、P/P+ 和 Wise 教程 |
| `achuan-x-save` | 保存账号状态、阶段判断和下一步动作 |
| `achuan-x-positioning` | 早期“账号方向”说法的兼容入口 |

## 安装

把 `skills/` 下的 skill 目录复制到你的 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R skills/achuan-x-* ~/.codex/skills/
```

如果 Codex 没有立刻显示新 skill，重启 Codex。

## 更新

用最新版替换本地已安装的 `achuan-x-*` 目录：

```bash
rm -rf ~/.codex/skills/achuan-x-*
cp -R skills/achuan-x-* ~/.codex/skills/
```

## 使用示例

- “Use achuan-x-operation-flow：推特新号从 0 到 1 怎么开始？”
- “Use achuan-x-toolkit：怎么检测自己有没有影子封禁？”
- “Use achuan-x-infra：怎么开 P+？”
- “Use achuan-x-monetization-check：创作者收益暂停怎么申诉？”
- “Use achuan-x-growth-diagnosis：为什么我发了很多但不涨粉？”

## 仓库结构

```text
.
├── skills/
│   ├── achuan-x-operation-flow/
│   ├── achuan-x-profile/
│   └── ...
├── scripts/
│   └── validate-skills.py
└── .github/
    ├── workflows/
    └── ISSUE_TEMPLATE/
```

每个 skill 目录只应该包含：

- `SKILL.md`
- `agents/openai.yaml`
- 可选的 `references/*.md`

不要在单个 skill 目录里添加 README、更新日志、安装指南、原始素材、本地报告或抓取记录。

## 校验

提交 PR 前运行自包含校验脚本：

```bash
python3 scripts/validate-skills.py skills
```

校验脚本会检查：

- 每个 `achuan-x-*` 目录只有一个根级 `SKILL.md`。
- skill frontmatter 里有合法的 `name` 和 `description`。
- `agents/openai.yaml` 存在，并包含必要的 UI 字段。
- skill 目录没有嵌套 `SKILL.md` 或辅助文档。
- 发布包不包含常见私有路径、原始抓取目录、`.DS_Store`、`.env` 或疑似密钥。

## 安全边界

Achuan-X-OperationFlow 可以提供策略、诊断、规划、检查清单、模板和本地状态结构。不要用它来规避平台风控、伪造身份、操纵互动、批量注册账号或操纵收益。

平台规则、支付支持、创作者收益条件和身份验证流程会变化。外部链接和教程只能作为流程参考，执行前请核验官方当前状态。

## 许可证

MIT。详见 [LICENSE](LICENSE)。
