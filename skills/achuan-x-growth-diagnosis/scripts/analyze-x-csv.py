#!/usr/bin/env python3
"""Summarize an X Analytics CSV with deterministic, dependency-free metrics."""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path


ALIASES = {
    "post_text": ["post text", "post", "tweet text", "text", "帖文内容", "推文内容", "内容"],
    "impressions": ["impressions", "impression", "展示次数", "曝光", "曝光量"],
    "likes": ["likes", "like", "点赞数", "点赞"],
    "engagements": ["engagements", "engagement", "互动次数", "互动"],
    "bookmarks": ["bookmarks", "bookmark", "收藏数", "收藏"],
    "shares": ["shares", "reposts", "repost", "retweets", "转发数", "转发"],
    "new_follows": ["new follows", "follows", "new followers", "新增关注", "新增粉丝"],
    "replies": ["replies", "reply", "回复数", "回复"],
    "date": ["date", "time", "created at", "发布时间", "日期", "时间"],
    "post_type": ["post type", "tweet type", "type", "内容类型", "帖子类型"],
}


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", value.lower()).strip()


def map_columns(fieldnames: list[str]) -> dict[str, str]:
    normalized = {normalize(name): name for name in fieldnames}
    mapping: dict[str, str] = {}
    for standard, aliases in ALIASES.items():
        for alias in aliases:
            if normalize(alias) in normalized:
                mapping[standard] = normalized[normalize(alias)]
                break
    return mapping


def number(value: str | None) -> float:
    if value is None:
        return 0.0
    cleaned = value.strip().replace(",", "").replace("%", "")
    if not cleaned or cleaned.lower() in {"n/a", "na", "null", "-"}:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def content_type(row: dict[str, str], mapping: dict[str, str]) -> str:
    explicit = row.get(mapping.get("post_type", ""), "").strip().lower()
    if explicit:
        if "repl" in explicit or "回复" in explicit:
            return "reply"
        if "quote" in explicit or "引用" in explicit:
            return "quote"
        if "repost" in explicit or "retweet" in explicit or "转发" in explicit:
            return "repost"

    text = row.get(mapping.get("post_text", ""), "").strip()
    if text.startswith("@"):
        return "reply"
    if re.search(r"https?://(?:www\.)?(?:x|twitter)\.com/[^/]+/status/", text):
        return "quote_or_link"
    if len(text) > 280:
        return "long_post"
    if "http://" in text or "https://" in text:
        return "link_post"
    return "short_post"


def rounded(value: float | None) -> float | None:
    return None if value is None else round(value, 4)


def analyze(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(8192)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(handle, dialect=dialect)
        fieldnames = reader.fieldnames or []
        mapping = map_columns(fieldnames)
        rows = list(reader)

    missing_required = [field for field in ["post_text", "impressions"] if field not in mapping]
    if missing_required:
        return {
            "status": "needs_column_mapping",
            "available_columns": fieldnames,
            "recognized_columns": mapping,
            "missing_required": missing_required,
            "message": "无法确认帖子内容或曝光列，请用户指定对应列名后再分析。",
        }

    metrics = ["impressions", "likes", "engagements", "bookmarks", "shares", "new_follows", "replies"]
    prepared: list[dict[str, object]] = []
    by_type: dict[str, list[dict[str, object]]] = defaultdict(list)

    for row in rows:
        item: dict[str, object] = {
            "text": row.get(mapping["post_text"], "").strip(),
            "date": row.get(mapping.get("date", ""), "").strip(),
            "type": content_type(row, mapping),
        }
        for metric in metrics:
            item[metric] = number(row.get(mapping[metric])) if metric in mapping else None
        prepared.append(item)
        by_type[str(item["type"])].append(item)

    impressions = [float(item["impressions"] or 0) for item in prepared]
    total_impressions = sum(impressions)
    total_follows = sum(float(item["new_follows"] or 0) for item in prepared) if "new_follows" in mapping else None
    total_engagements = sum(float(item["engagements"] or 0) for item in prepared) if "engagements" in mapping else None
    reply_count = sum(1 for item in prepared if item["type"] == "reply")
    top = sorted(prepared, key=lambda item: float(item["impressions"] or 0), reverse=True)[:10]

    type_summary: dict[str, object] = {}
    for kind, items in sorted(by_type.items()):
        kind_impressions = sum(float(item["impressions"] or 0) for item in items)
        kind_follows = sum(float(item["new_follows"] or 0) for item in items) if "new_follows" in mapping else None
        type_summary[kind] = {
            "posts": len(items),
            "total_impressions": rounded(kind_impressions),
            "average_impressions": rounded(kind_impressions / len(items) if items else 0),
            "new_follows": rounded(kind_follows),
            "follows_per_10k_impressions": rounded(
                (kind_follows * 10000 / kind_impressions) if kind_follows is not None and kind_impressions else None
            ),
        }

    return {
        "status": "ok",
        "source_file": path.name,
        "recognized_columns": mapping,
        "missing_optional_columns": [metric for metric in metrics + ["date", "post_type"] if metric not in mapping],
        "summary": {
            "posts": len(prepared),
            "total_impressions": rounded(total_impressions),
            "average_impressions": rounded(statistics.mean(impressions) if impressions else 0),
            "median_impressions": rounded(statistics.median(impressions) if impressions else 0),
            "max_impressions": rounded(max(impressions) if impressions else 0),
            "new_follows": rounded(total_follows),
            "engagements": rounded(total_engagements),
            "reply_share": rounded(reply_count / len(prepared) if prepared else 0),
            "top_10_impression_share": rounded(
                sum(float(item["impressions"] or 0) for item in top) / total_impressions if total_impressions else 0
            ),
        },
        "content_types": type_summary,
        "top_posts": [
            {
                "date": item["date"],
                "type": item["type"],
                "text": str(item["text"])[:180],
                "impressions": item["impressions"],
                "new_follows": item["new_follows"],
                "engagements": item["engagements"],
            }
            for item in top
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze an X Analytics CSV without changing the source file.")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    if not args.csv_path.is_file():
        print(json.dumps({"status": "error", "message": "CSV file not found."}, ensure_ascii=False))
        return 2

    try:
        result = analyze(args.csv_path)
    except (OSError, csv.Error) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "ok" else 3


if __name__ == "__main__":
    raise SystemExit(main())
