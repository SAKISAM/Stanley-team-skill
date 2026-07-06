# St-skill

St-skill is a Codex skill group for X/Twitter account growth from 0 to 1.

It focuses on practical routing and workflows for profile setup, content rhythm, content systems, reply growth, growth diagnosis, account risk recovery, creator monetization checks, infrastructure, monetization paths, tools, and state saving.

## What This Is

- A group of local Codex skills under `skills/st-*`.
- A strategy, diagnosis, planning, and template system for X/Twitter growth.
- A self-contained release package that does not depend on private Feishu/Lark documents, raw captures, browser logs, or local absolute paths.

## What This Is Not

- It does not log in to X/Twitter or operate accounts for you.
- It does not automate posting, following, replying, or engagement.
- It does not provide evasion, fake identity verification, bulk registration, engagement manipulation, payout manipulation, or platform enforcement bypass methods.
- It does not guarantee creator revenue, account recovery, verification, payouts, or growth outcomes.

## Included Skills

| Skill | Purpose |
|---|---|
| `st-skill` | Main router for the St-skill group |
| `st-profile` | Profile setup: avatar, header, ID, bio, pinned post |
| `st-content-rhythm` | Posting rhythm, short/long post ratio, stage plans |
| `st-content-system` | Content pillars, topic pool, post/reply/quote roles |
| `st-reply-growth` | Reply strategy, interaction frequency, comment-section growth |
| `st-growth-diagnosis` | Low exposure, low engagement, slow growth diagnosis |
| `st-risk-recovery` | Account freeze, lock, restriction, shadowban, abnormal status |
| `st-monetization-check` | Creator revenue eligibility, suspension, appeal preparation |
| `st-infra` | Premium/P+, Wise, Stripe, eSIM, payment, identity verification |
| `st-monetization-path` | Off-platform monetization: consulting, community, courses, services, deals |
| `st-toolkit` | Tool links, viral monitoring, shadowban checker, P/P+ and Wise tutorials |
| `st-save` | Save account state, stage judgment, and next actions |
| `st-positioning` | Compatibility entry for early account direction language |

## Install

Copy the skill folders into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/st-* ~/.codex/skills/
```

Restart Codex if the new skills do not appear immediately.

## Update

Replace the installed `st-*` folders with the latest release:

```bash
rm -rf ~/.codex/skills/st-*
cp -R skills/st-* ~/.codex/skills/
```

## Usage Examples

- "Use st-skill: how should I start a new X account from 0 to 1?"
- "Use st-toolkit: how do I check whether I am shadowbanned?"
- "Use st-infra: how do I open P+?"
- "Use st-monetization-check: how do I appeal creator revenue suspension?"
- "Use st-growth-diagnosis: why am I posting a lot but not gaining followers?"

## Repository Layout

```text
.
├── skills/
│   ├── st-skill/
│   ├── st-profile/
│   └── ...
├── scripts/
│   └── validate-skills.py
└── .github/
    ├── workflows/
    └── ISSUE_TEMPLATE/
```

Each skill directory should contain only:

- `SKILL.md`
- `agents/openai.yaml`
- optional `references/*.md`

Do not add README, changelog, install guide, raw source material, or local reports inside individual skill directories.

## Validation

Run the self-contained validator before opening a pull request:

```bash
python3 scripts/validate-skills.py skills
```

The validator checks:

- each `st-*` directory has one root `SKILL.md`;
- skill frontmatter has valid `name` and `description`;
- `agents/openai.yaml` exists and has required UI fields;
- skill folders do not contain nested `SKILL.md` files or auxiliary docs;
- release files do not include common private paths, raw capture folders, `.DS_Store`, `.env`, or obvious secret-like values.

## Safety

St-skill can provide strategy, diagnosis, planning, checklists, templates, and local state structures. It should not be used to evade platform enforcement, fake identity checks, manipulate engagement, mass-register accounts, or manipulate payouts.

Platform rules, payment support, creator revenue requirements, and verification flows change over time. Treat external links and tutorials as workflow references, then verify current official status before acting.

## License

MIT. See [LICENSE](LICENSE).
