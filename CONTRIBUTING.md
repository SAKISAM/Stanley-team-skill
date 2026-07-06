# Contributing

Thanks for improving St-skill.

## Development Rules

- Keep each skill self-contained.
- Keep `SKILL.md` concise and procedural.
- Put detailed reusable knowledge in `references/*.md`.
- Do not add README, changelog, install guides, raw captures, reports, or source logs inside individual skill folders.
- Do not commit private Feishu/Lark links, local absolute paths, browser logs, account state files, CSV exports, tokens, or secrets.

## Skill Directory Shape

Each skill should use this shape:

```text
skills/st-example/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── optional-reference.md
```

## Before Opening a Pull Request

Run:

```bash
python3 scripts/validate-skills.py skills
```

Also test at least one realistic user prompt for every skill you changed.

## Pull Request Checklist

- Name the skill or references changed.
- Explain the user scenario improved.
- List any new external links.
- Confirm no private source material or local paths were added.
- Confirm `python3 scripts/validate-skills.py skills` passes.

## Safety Boundary

Contributions must not add instructions for platform enforcement evasion, fake identity verification, bulk registration, engagement manipulation, payout manipulation, or automated spam behavior.
