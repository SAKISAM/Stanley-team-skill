#!/usr/bin/env python3
"""Check behavior contracts that structural skill validation cannot catch."""

from __future__ import annotations

import re
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(relative: str, snippets: list[str], errors: list[str]) -> None:
    content = read(relative)
    for snippet in snippets:
        if snippet not in content:
            errors.append(f"{relative}: missing behavior contract {snippet!r}")


def main() -> int:
    errors: list[str] = []

    require(
        "skills/achuan-x-operation-flow/SKILL.md",
        [
            "没问清楚时不提 skill 名称",
            "一次只问最关键的 1-3 个问题",
            "完整读取并继续执行",
            "scripts/grok-x-research.sh @handle overview",
        ],
        errors,
    )

    follower_contracts = [
        "achuan-x-profile",
        "achuan-x-content-rhythm",
        "achuan-x-content-system",
        "achuan-x-reply-growth",
        "achuan-x-growth-diagnosis",
        "achuan-x-monetization-path",
        "achuan-x-monetization-check",
    ]
    for name in follower_contracts:
        content = read(f"skills/{name}/SKILL.md")
        if "粉丝数" not in content:
            errors.append(f"skills/{name}/SKILL.md: missing follower-count intake")

    for name in [path.name for path in SKILLS.glob("achuan-x-*") if path.is_dir()]:
        skill_md = read(f"skills/{name}/SKILL.md")
        if "## 回答方式" not in skill_md and name != "achuan-x-operation-flow":
            errors.append(f"skills/{name}/SKILL.md: missing beginner-facing response rules")
        agent_yaml = read(f"skills/{name}/agents/openai.yaml")
        short_line = next((line for line in agent_yaml.splitlines() if "short_description:" in line), "")
        if not re.search(r"[\u4e00-\u9fff]", short_line):
            errors.append(f"skills/{name}/agents/openai.yaml: short description is not Chinese")

    require(
        "skills/achuan-x-risk-recovery/SKILL.md",
        ["https://x-shadowban-checker.fia-s.com/", "grok-x-research.sh @handle risk"],
        errors,
    )
    require(
        "skills/achuan-x-monetization-check/SKILL.md",
        [
            "X 账号 ID",
            "当前粉丝数",
            "官方通知内容",
            "暂停/移除时间",
            "grok-x-research.sh @handle monetization",
            "不发送官方邮件",
            "中英双语申诉信模板",
            "请求人工复核",
            "https://help.x.com/en/forms/appeal-suspended-revenue-sharing/redirect",
        ],
        errors,
    )
    require(
        "skills/achuan-x-infra/SKILL.md",
        [
            "https://x.com/snail_9106/status/2023930594003177490",
            "https://x.com/Formulasearch/status/2061726617899073633",
            "https://help.x.com/en/using-x/x-premium",
            "https://x.com/settings/monetization",
        ],
        errors,
    )

    grok_script = SKILLS / "achuan-x-operation-flow" / "scripts" / "grok-x-research.sh"
    if not grok_script.exists():
        errors.append("missing Grok account research script")
    else:
        if not grok_script.stat().st_mode & 0o111:
            errors.append("Grok account research script is not executable")
        grok_content = grok_script.read_text(encoding="utf-8")
        for flag in ["--verbatim", "--no-plan", "--no-memory", "--no-subagents"]:
            if flag not in grok_content:
                errors.append(f"Grok account research script: missing isolation flag {flag}")

    csv_script = SKILLS / "achuan-x-growth-diagnosis" / "scripts" / "analyze-x-csv.py"
    if not csv_script.exists():
        errors.append("missing deterministic X Analytics CSV script")
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            sample = Path(temp_dir) / "sample.csv"
            sample.write_text(
                "Post text,Impressions,Engagements,New follows,Date\n"
                "A useful checklist,1000,50,2,2026-07-01\n"
                "@someone A specific reply,2000,80,1,2026-07-02\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(csv_script), str(sample)],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                errors.append(f"CSV analyzer self-test failed: {result.stderr or result.stdout}")
            else:
                payload = json.loads(result.stdout)
                summary = payload.get("summary", {})
                if summary.get("total_impressions") != 3000.0 or summary.get("reply_share") != 0.5:
                    errors.append("CSV analyzer self-test returned incorrect metrics")

    existing = {path.name for path in SKILLS.glob("achuan-x-*") if path.is_dir()}
    route_pattern = re.compile(r"/((?:achuan-x-)[a-z-]+)")
    for path in SKILLS.glob("achuan-x-*/SKILL.md"):
        for route in route_pattern.findall(path.read_text(encoding="utf-8")):
            if route not in existing:
                errors.append(f"{path.relative_to(ROOT)}: route points to missing skill {route}")

    banned_user_terms = ["# X 回复增长 routine", "## Organic 内容检查", "## 最大断点"]
    all_skill_text = "\n".join(path.read_text(encoding="utf-8") for path in SKILLS.glob("achuan-x-*/SKILL.md"))
    for term in banned_user_terms:
        if term in all_skill_text:
            errors.append(f"user-facing jargon remains: {term}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"\nBehavior contract checks failed with {len(errors)} issue(s).")
        return 1

    print(f"Behavior contracts passed for {len(existing)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
