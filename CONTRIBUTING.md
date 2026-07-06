# 贡献指南

感谢你改进 St-skill。

## 开发规则

- 每个 skill 必须保持自包含。
- `SKILL.md` 要简洁、流程化，避免写成长篇文章。
- 详细且可复用的知识放进 `references/*.md`。
- 不要在单个 skill 目录里添加 README、更新日志、安装指南、原始抓取材料、报告或来源日志。
- 不要提交私有飞书/Lark 链接、本地绝对路径、浏览器日志、账号状态文件、CSV 导出、token 或密钥。

## Skill 目录结构

每个 skill 使用这个结构：

```text
skills/st-example/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── optional-reference.md
```

## 提交 PR 前

运行：

```bash
python3 scripts/validate-skills.py skills
```

并且为你改过的每个 skill 至少测试 1 条真实用户提问。

## PR 检查清单

- 说明修改了哪个 skill 或 reference。
- 说明改善了哪个用户场景。
- 列出新增的外部链接。
- 确认没有加入私有素材、本地路径或敏感数据。
- 确认 `python3 scripts/validate-skills.py skills` 通过。

## 安全边界

贡献内容不得加入规避平台风控、虚假身份验证、批量注册、操纵互动、操纵收益或自动化垃圾行为的说明。
