#!/usr/bin/env python3
"""Build behavioral-health-source-url-summary.md from the subset CSV."""
import csv
from collections import defaultdict

INPUT = "behavioral-health-state-boards-subset.csv"
OUTPUT = "behavioral-health-source-url-summary.md"

LICENSE_COL = "License Issuer - License Type (Concatenated)"
SOURCE_COL = "Source Url"

with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    by_url = defaultdict(list)
    for row in reader:
        url = (row.get(SOURCE_COL) or "").strip()
        label = (row.get(LICENSE_COL) or "").strip()
        if label:
            by_url[url].append(label)

# Empty URL last; otherwise sort by URL
def sort_key(item):
    url = item[0]
    return (url == "", url.lower())

lines = [
    "# Behavioral health state boards: source URL summary",
    "",
    "Source verification URLs with all License Issuer – License Type (concatenated) values that use them. Generated from `behavioral-health-state-boards-subset.csv`.",
    "",
]

for url, labels in sorted(by_url.items(), key=sort_key):
    display_url = url if url else "(no Source URL)"
    lines.append(f"## {display_url}")
    lines.append("")
    for label in labels:
        lines.append(f"- {label}")
    lines.append("")

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUTPUT} with {len(by_url)} source URLs")
