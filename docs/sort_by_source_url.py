#!/usr/bin/env python3
"""Reorganize CSV: Source Url first column, rows grouped by Source Url."""
import csv

INPUT = "behavioral-health-state-boards-subset.csv"
OUTPUT = "behavioral-health-state-boards-subset.csv"

with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)
    old_fieldnames = list(reader.fieldnames)

# New column order: Source Url first, then everything else except Source Url
source_url_key = "Source Url"
other_keys = [k for k in old_fieldnames if k != source_url_key]
fieldnames = [source_url_key] + other_keys

# Group rows by Source Url (same URL together; empty last)
def sort_key(row):
    url = (row.get(source_url_key) or "").strip()
    return (url == "", url.lower())

rows.sort(key=sort_key)

# Write with Source Url first
with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print(f"Reorganized {len(rows)} rows: Source Url first, grouped by Source Url. Wrote {OUTPUT}")
