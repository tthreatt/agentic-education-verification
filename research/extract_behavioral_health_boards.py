#!/usr/bin/env python3
"""
Filter Data (1).csv to state-issued behavioral health licenses (NUCC),
extract unique boards from Confluence Link, and write subset + board list to docs/.
"""
import csv
import re
from pathlib import Path
from urllib.parse import unquote

US_STATES = {
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming",
}

# Phrases that indicate NUCC behavioral health (avoid single words that match non-BH licenses)
BEHAVIORAL_HEALTH_KEYWORDS = [
    "Counselor", "LPC", "LCPC", "LMHC", "LPCC", "LCSW", "LICSW", "LBSW", "LMSW", "LISW", "LISWCP", "LAPSW",
    "Social Worker", "Clinical Social Worker", "Master Social Worker", "Baccalaureate Social Worker",
    "Advanced Practice Social Worker", "Licensed Clinical Social Worker", "Licensed Master Social Worker",
    "Licensed Baccalaureate Social Worker", "Licensed Advanced Practice Social Worker",
    "LMFT", "LAMFT", "MFT", "Marriage and Family Therapist", "Marital and Family Therapist",
    "Marriage & Family Therapist", "Family Therapist", "Licensed Marriage and Family Therapist",
    "Licensed Associate Marriage and Family Therapist",
    "Psychologist", "Psychology",
    "Alcohol & Drug", "Alcohol and Drug", "Alcohol & Drug Counselor", "Alcohol and Drug Counselor",
    "Substance Abuse", "Substance Abuse Counselor", "Addiction Counselor", "Chemical Dependency",
    "Licensed Chemical Dependency Counselor", "Licensed Associate Substance Abuse Counselor",
    "Licensed Independent Substance Abuse Counselor", "Licensed Addiction Counselor",
    "Behavior Analyst", "Behavioral Analyst", "LBA", "LABA", "Licensed Behavior Analyst",
    "Licensed Assistant Behavior Analyst",
    "Professional Counselor", "Associate Licensed Counselor", "Associate Counselor",
    "Licensed Professional Counselor", "Licensed Professional Counselor Associate", "LPCA",
    "Licensed Associate Counselor", "ALC", "Mental Health Service Provider",
    "Clinical Pastoral Counselor", "Pastoral Counselor",
]

EXCLUDE_PHRASES = ("Controlled Substance", "Genetic Counselor")

# License type substrings that indicate NON-behavioral-health (exclude these rows)
NON_BH_INDICATORS = (
    "Nurse", "Nursing", "CRNA", "CRNP", "ARNP", "CNA", "LPN", "RN ", "Dentist", "Dental",
    "Dietitian", "Nutrition", "Athletic Trainer", "Audiologist", "Speech Pathology", "Audiology",
    "Chiropractic", "Chiropractor", "EMT", "Paramedic", "Emergency Medical",
    "Medical Examiner", "Osteopathy", "Physician", "Doctor of ", "Anesthesiologist Assistant",
    "Optometry", "Optometrist", "Pharmacy", "Pharmacist", "Physical Therapy", "PT ", "Massage",
    "Podiatry", "Assisted Living Administrator", "Nursing Home Administrator",
    "Occupational Therapy", "Respiratory Therapy", "EMS Management", "Dietetics",
    "General Anesthesia Permit", "Medical Doctor", "Medication Aide", "Limited Purpose Schedule",
    "LPSP", "Occupational Therapist",
    "Speech Language Pathologist", "Respiratory Therapist", "Respiratory Care",
    "Physical Therapist", "Podiatrist", "Oral Conscious Sedation",
    "Specialty Care Assisted Living", "Special Purpose",
)

def is_behavioral_health(concatenated: str, license_type: str, aliases: str) -> bool:
    """True if row is behavioral health per NUCC and not excluded."""
    text = f"{concatenated or ''} {license_type or ''} {aliases or ''}"
    text_lower = text.lower()
    for exc in EXCLUDE_PHRASES:
        if exc.lower() in text_lower:
            return False
    for exc in NON_BH_INDICATORS:
        if exc.lower() in text_lower:
            return False
    for kw in BEHAVIORAL_HEALTH_KEYWORDS:
        if kw in text or kw.lower() in text_lower:
            return True
    return False

def board_name_from_confluence_link(url: str) -> str:
    """Extract board/regulator name from Confluence Link. e.g. /pages/123/Board+Name+Here -> Board Name Here"""
    if not url:
        return ""
    m = re.search(r"/pages/\d+/([^#\s]+)", url)
    if not m:
        return ""
    slug = m.group(1)
    decoded = unquote(slug.replace("+", " "))
    return decoded.strip()

def main():
    base = Path(__file__).resolve().parent
    csv_path = base / "Data (1).csv"
    docs = base.parent / "docs"
    docs.mkdir(exist_ok=True)

    # Try encodings
    for encoding in ("utf-8-sig", "utf-8", "utf-16", "utf-16-le"):
        try:
            with open(csv_path, "r", encoding=encoding, newline="") as f:
                reader = csv.reader(f, delimiter="\t")
                headers = next(reader)
                rows = list(reader)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        raise SystemExit("Could not read CSV with any supported encoding.")

    # Column indices
    col_concatenated = headers.index("License Issuer - License Type (Concatenated)") if "License Issuer - License Type (Concatenated)" in headers else 0
    col_issuer = headers.index("Issuer")
    col_license_type = headers.index("License Type")
    col_aliases = headers.index("License Type Aliases")
    col_category = headers.index("License Category")
    col_atypical = headers.index("Atypical Verification")
    col_confluence = headers.index("Confluence Link")
    col_source_url = headers.index("Source Url")
    col_scraper_status = headers.index("Scraper Status")
    col_automated = headers.index("Automated")
    col_captcha = headers.index("Captcha")
    col_mapping = headers.index("Mapping Location")
    col_scraper_id = headers.index("Scraper Id") if "Scraper Id" in headers else None
    col_lic_format = headers.index("Lic Number Format") if "Lic Number Format" in headers else None

    subset = []
    board_to_info = {}  # board_name -> one row's Confluence + Source Url for reference

    for row in rows:
        if len(row) <= max(col_confluence, col_source_url):
            continue
        issuer = (row[col_issuer] or "").strip()
        if issuer not in US_STATES:
            continue
        concat = row[col_concatenated] if col_concatenated < len(row) else ""
        ltype = row[col_license_type] if col_license_type < len(row) else ""
        aliases = row[col_aliases] if col_aliases < len(row) else ""
        if not is_behavioral_health(concat, ltype, aliases):
            continue
        confluence = row[col_confluence] if col_confluence < len(row) else ""
        source_url = row[col_source_url] if col_source_url < len(row) else ""
        board_name = board_name_from_confluence_link(confluence)
        if board_name and board_name not in board_to_info:
            board_to_info[board_name] = {"confluence": confluence, "source_url": source_url}
        subset.append({
            "License Issuer - License Type (Concatenated)": concat,
            "Issuer": issuer,
            "License Type": ltype,
            "License Type Aliases": aliases,
            "License Category": row[col_category] if col_category < len(row) else "",
            "Atypical Verification": row[col_atypical] if col_atypical < len(row) else "",
            "Confluence Link": confluence,
            "Source Url": source_url,
            "Scraper Status": row[col_scraper_status] if col_scraper_status < len(row) else "",
            "Automated": row[col_automated] if col_automated < len(row) else "",
            "Captcha": row[col_captcha] if col_captcha < len(row) else "",
            "Mapping Location": row[col_mapping] if col_mapping < len(row) else "",
            "Scraper Id": row[col_scraper_id] if col_scraper_id is not None and col_scraper_id < len(row) else "",
            "Lic Number Format": row[col_lic_format] if col_lic_format is not None and col_lic_format < len(row) else "",
            "Board Name": board_name,
        })

    unique_boards = sorted(set(r["Board Name"] for r in subset if r["Board Name"]))

    # Write subset CSV
    subset_path = docs / "behavioral-health-state-boards-subset.csv"
    if subset:
        subset_headers = list(subset[0].keys())
        with open(subset_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=subset_headers, delimiter="\t")
            w.writeheader()
            w.writerows(subset)

    # Write markdown: summary, unique boards with URLs, then full subset table
    md_path = docs / "behavioral-health-state-boards.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Behavioral Health State Boards (NUCC-Aligned)\n\n")
        f.write("Subset of `research/Data (1).csv`: **Issuer** = one of 50 US states, **License Type** = behavioral health per NUCC taxonomy (Counselor, LPC, LCSW, Social Worker, LMFT, Psychologist, Behavior Analyst, Alcohol & Drug, Substance Abuse). Excludes \"Controlled Substance\" rows.\n\n")
        f.write(f"- **Total subset rows:** {len(subset)}\n")
        f.write(f"- **Unique boards/regulators (from Confluence Link):** {len(unique_boards)}\n\n")
        f.write("---\n\n")
        f.write("## Unique boards to contact (with screenshot URL and metadata)\n\n")
        f.write("| # | Board / Regulator Name | Confluence Link | Source Url (screenshot/verification) |\n")
        f.write("|---|------------------------|-----------------|--------------------------------------|\n")
        for i, board in enumerate(unique_boards, 1):
            info = board_to_info.get(board, {})
            conf = info.get("confluence", "")
            src = info.get("source_url", "")
            f.write(f"| {i} | {board} | {conf} | {src} |\n")
        f.write("\n---\n\n")
        f.write("## Full subset (State, License Type, Source Url, metadata)\n\n")
        f.write("| State | License Type | Source Url (screenshot) | Confluence Link | Scraper Status | Automated | Captcha | Board Name |\n")
        f.write("|-------|--------------|-------------------------|-----------------|----------------|-----------|---------|------------|\n")
        for r in subset:
            issuer = r["Issuer"]
            ltype = r["License Type"]
            src = r["Source Url"]
            conf = r["Confluence Link"]
            status = r["Scraper Status"]
            auto = r["Automated"]
            cap = r["Captcha"]
            board = r["Board Name"]
            f.write(f"| {issuer} | {ltype} | {src} | {conf} | {status} | {auto} | {cap} | {board} |\n")

    print(f"Wrote {subset_path} ({len(subset)} rows)")
    print(f"Wrote {md_path}")
    print(f"Unique boards: {len(unique_boards)}")

if __name__ == "__main__":
    main()
