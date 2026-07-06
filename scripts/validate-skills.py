#!/usr/bin/env python3
"""Validate St-skill release folders without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
FORBIDDEN_SKILL_DOCS = {
    "README.md",
    "CHANGELOG.md",
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
}
FORBIDDEN_NAMES = {
    ".DS_Store",
    ".env",
    "01-raw-md",
    "01-raw",
    "browser-logs",
    "captures",
    "logs",
    "sessions",
    "reports",
}
SENSITIVE_PATTERNS = [
    (re.compile("/" + "Users" + r"/[A-Za-z0-9._-]+"), "local absolute path"),
    (re.compile("Content" + "System" + r"/06-"), "private local project path"),
    (re.compile(r"https?://[^\s)\]]*feishu\.cn", re.IGNORECASE), "private Feishu URL"),
    (re.compile(r"https?://[^\s)\]]*larksuite\.com", re.IGNORECASE), "private Lark URL"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"), "secret-like value"),
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError(f"{path}: file is not valid UTF-8")


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    content = read_text(skill_md)
    if not content.startswith("---\n"):
        raise ValueError(f"{skill_md}: missing YAML frontmatter")
    end = content.find("\n---", 4)
    if end == -1:
        raise ValueError(f"{skill_md}: invalid frontmatter delimiter")

    frontmatter = content[4:end]
    keys: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            raise ValueError(f"{skill_md}: unsupported frontmatter line: {line}")
        keys[match.group(1)] = match.group(2).strip()
    return keys


def validate_frontmatter(skill_dir: Path, skill_md: Path) -> list[str]:
    errors: list[str] = []
    try:
        frontmatter = parse_frontmatter(skill_md)
    except ValueError as exc:
        return [str(exc)]

    extra = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if extra:
        errors.append(f"{skill_md}: unexpected frontmatter keys: {', '.join(sorted(extra))}")

    name = frontmatter.get("name", "").strip().strip("'\"")
    if not name:
        errors.append(f"{skill_md}: missing name")
    elif not re.match(r"^[a-z0-9-]+$", name):
        errors.append(f"{skill_md}: name must be kebab-case")
    elif name != skill_dir.name:
        errors.append(f"{skill_md}: name {name!r} does not match directory {skill_dir.name!r}")

    if "description" not in frontmatter:
        errors.append(f"{skill_md}: missing description")

    return errors


def validate_agent_metadata(skill_dir: Path) -> list[str]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return [f"{path}: missing agents/openai.yaml"]
    content = read_text(path)
    required = ["interface:", "display_name:", "short_description:", "default_prompt:"]
    return [f"{path}: missing {field}" for field in required if field not in content]


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    skill_files = [
        path
        for path in skill_dir.rglob("SKILL.md")
        if "__pycache__" not in path.parts and "node_modules" not in path.parts
    ]
    if len(skill_files) != 1:
        extras = ", ".join(str(path.relative_to(skill_dir)) for path in skill_files)
        errors.append(f"{skill_dir}: expected exactly one SKILL.md, found {len(skill_files)}: {extras}")

    for name in FORBIDDEN_SKILL_DOCS:
        found = list(skill_dir.rglob(name))
        if found:
            errors.extend(f"{path}: auxiliary docs belong at repository root, not inside skills" for path in found)

    errors.extend(validate_frontmatter(skill_dir, skill_md))
    errors.extend(validate_agent_metadata(skill_dir))
    return errors


def scan_sensitive_material(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in {".git", "__pycache__"} for part in rel.parts):
            continue
        if path.name in FORBIDDEN_NAMES:
            errors.append(f"{rel}: forbidden release file or directory name")
        if not path.is_file():
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            content = read_text(path)
        except ValueError as exc:
            if path.name == ".DS_Store":
                errors.append(f"{rel}: forbidden .DS_Store file")
            else:
                errors.append(str(exc))
            continue
        for pattern, label in SENSITIVE_PATTERNS:
            if pattern.search(content):
                errors.append(f"{rel}: contains {label}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: scripts/validate-skills.py <skills-directory>")
        return 2

    skills_root = Path(argv[1]).resolve()
    if not skills_root.exists() or not skills_root.is_dir():
        fail(f"{skills_root}: skills directory not found")
        return 1

    repo_root = skills_root.parent
    errors: list[str] = []
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir() and path.name.startswith("st-"))
    if not skill_dirs:
        errors.append(f"{skills_root}: no st-* skill directories found")

    for skill_dir in skill_dirs:
        errors.extend(validate_skill_dir(skill_dir))

    unexpected = sorted(path.name for path in skills_root.iterdir() if path.is_dir() and not path.name.startswith("st-"))
    if unexpected:
        errors.append(f"{skills_root}: unexpected non-st skill directories: {', '.join(unexpected)}")

    errors.extend(scan_sensitive_material(repo_root))

    if errors:
        for error in errors:
            fail(error)
        print(f"\nValidation failed with {len(errors)} issue(s).")
        return 1

    print(f"Validated {len(skill_dirs)} skill(s). No release issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
