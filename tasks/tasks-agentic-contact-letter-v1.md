# Tasks: Agentic Contact Letter (v1)

Generated from PRD: `prd/prd-agentic-contact-letter.md`  
Scope: Contact discovery, letter content, and outreach. No codebase yet; no feature branch. Use AWS managed services where possible.

---

## Relevant Files

- `research/behavioral-health-state-boards-subset.csv` – Input board list (Board Name, Source Url, Confluence Link).
- `research/contact-master.csv` (or S3 object) – Output contact master; structured contact data per board.
- `docs/letter-spec.md` – Letter specification (required clauses, signatory, refresh process).
- `docs/letter-template.md` – Letter template (Markdown) for outreach body/attachment.
- `docs/outreach-playbook.md` or generated artifact – Playbook derived from contact master + letter spec.
- `code/contact_discovery/` – Contact Discovery logic (e.g. Lambda + Bedrock or script).
- `code/letter_content/` – Letter spec and template generation (e.g. Lambda + Bedrock or script).
- `code/outreach/` – Outreach Agent: playbook derivation, template fill, draft/send (e.g. Lambda + Bedrock, optional SES).
- `infra/` or `iac/` – AWS infrastructure (S3, Lambda, Step Functions, IAM) e.g. CDK, Terraform, or SAM.
- `docs/board-base-url-derivation.md` – Document how board base URL is derived from Source Url.

### Notes

- No existing codebase; paths above are targets for v1. Unit/integration tests can be added alongside modules (e.g. `code/contact_discovery/..._test.py`).
- Prefer AWS managed services: S3 (artifacts), Lambda (agents), Step Functions (orchestration), Bedrock (LLM), SES (optional send), DynamoDB or S3 for outreach state.

---

## Instructions for Completing Tasks

**IMPORTANT:** As you complete each task, check it off in this file by changing `- [ ]` to `- [x]`. Update after each sub-task, not only after a full parent task.

---

## Tasks

### 1.0 Project foundation and data schema

- [ ] 1.1 Define repo layout for v1: `research/` (board list, contact master), `docs/` (letter spec, template, playbook), `code/` (discovery, letter, outreach), and `infra/` or `iac/` for AWS.
- [ ] 1.2 Define and document the **contact master** schema (CSV or equivalent): Board Name, Board Base URL, Contact Email(s), Contact Role/Title, Phone, Contact Form URL, Source of truth, Confluence Link; allow future columns (e.g. last_contacted_date, letter_received) without breaking readers.
- [ ] 1.3 Document **board base URL** derivation from Source Url (e.g. origin only, or known parent path for state DOPL); add `docs/board-base-url-derivation.md`.
- [ ] 1.4 Confirm input board list location and columns (e.g. `research/behavioral-health-state-boards-subset.csv` with Board Name, Source Url, Confluence Link); add placeholder or sample if missing.

---

### 2.0 Contact Discovery

- [ ] 2.1 Implement **board base URL** derivation from each board’s Source Url using the documented rule (e.g. Python/Node helper or Lambda).
- [ ] 2.2 Implement logic to fetch and parse board contact pages (contact, about, or staff) from the board’s website; use HTTP client and HTML/text parsing (e.g. AWS Lambda + Bedrock for extraction, or deterministic parser).
- [ ] 2.3 Extract and normalize per board: at least one contact email or contact form URL; when available: phone, mailing address, role/title (e.g. “Executive Director,” “License Verification”).
- [ ] 2.4 Record **source** of contact info per board (e.g. “board website”; “Confluence” if integrated later).
- [ ] 2.5 Output a **contact master** in the defined schema (CSV or equivalent); support writing to local file and/or S3 (AWS managed).
- [ ] 2.6 Flag boards for which no contact info could be found (e.g. dedicated column or separate list) for manual handling.
- [ ] 2.7 Support human review and correction of contact master (e.g. editable CSV in repo or S3, with a simple validation step before outreach).

---

### 3.0 Letter spec and template

- [ ] 3.1 Produce a **letter specification** document: required clauses (e.g. attestation of primary source verification of education), scope (license types), effective date, signatory (authorized board representative), and how to request re-sign/refresh; store in repo (e.g. `docs/letter-spec.md`).
- [ ] 3.2 Produce a **letter template** (Markdown preferred for v1) that implements the spec; include addressee (our organization), board name, statement of verification practice, scope of license types, effective date, signatory and signature/date block; store in repo (e.g. `docs/letter-template.md`).
- [ ] 3.3 Ensure letter template and spec are versioned and loadable by the Outreach Agent (e.g. from repo or from S3 if using AWS).
- [ ] 3.4 (Optional) If NCQA/CAQH references are available, add mapping of template clauses to those standards and flag gaps; otherwise skip for v1.

---

### 4.0 Outreach playbook and Outreach Agent

- [ ] 4.1 Implement **outreach playbook** generation: derive from contact master + letter spec (e.g. one row per board with contact email, channel, template version); output as structured file or S3 object.
- [ ] 4.2 Implement **Outreach Agent** (or deterministic template engine): read contact master and letter template; for each board (or filtered list) generate a **draft** outreach (email body or form payload) using the template; support variable substitution (e.g. board name, contact name) and optional LLM (Bedrock) for agentic phrasing.
- [ ] 4.3 Support **draft-only mode** by default: no automatic sending; output drafts for human review and manual send.
- [ ] 4.4 Support **filtering** of boards for outreach (e.g. by state, license type, or “no letter on file”) so not all boards are included in a single run.
- [ ] 4.5 (Optional) If “send” mode is enabled: record per-board outreach state (e.g. “request sent,” “reminder sent,” “letter received”) and retain a copy of sent content for audit; use DynamoDB or S3 + metadata as store.

---

### 5.0 AWS infrastructure and storage (managed services)

- [ ] 5.1 Define **S3** buckets/prefixes for: contact master, letter spec, letter template, playbook, and (if send mode) sent content and audit copies; document paths and naming.
- [ ] 5.2 Implement **Lambda** (or equivalent) for Contact Discovery, Letter Content (if automated), and Outreach Agent; use **Bedrock** for LLM where agentic behavior is required; keep IAM least-privilege.
- [ ] 5.3 (Optional) Use **Step Functions** to orchestrate: load board list → Contact Discovery → write contact master → (Letter Content if needed) → generate playbook → Outreach Agent drafts; or run as separate invocations for v1.
- [ ] 5.4 If send mode is implemented: use **Amazon SES** for sending email and store outreach state in **DynamoDB** or S3 object metadata; retain sent body for audit.
- [ ] 5.5 Provide a way to run the pipeline (e.g. CLI script invoking Lambda, or Step Functions execution) and to load inputs from repo or S3.

---

### 6.0 Integration, docs, and handoff

- [ ] 6.1 Ensure contact master, letter spec, and letter template are in **known locations** (repo paths and/or S3) and documented so agents and humans can read and update them.
- [ ] 6.2 Add a short **runbook** or README: how to run Contact Discovery, how to regenerate playbook and drafts, how to filter boards, and where to find drafts for human review.
- [ ] 6.3 Validate end-to-end for a small subset (e.g. 5–10 boards): contact discovery → contact master → playbook → draft outreach; confirm traceability (board, template version, contact source).
- [ ] 6.4 Document open decisions from PRD (e.g. draft-only vs send in v1, contact master file location, letter approver) in `docs/` or as comments in this task file.

---

## Summary

| Parent      | Focus                                      |
|------------|---------------------------------------------|
| 1.0        | Repo layout, contact master schema, base URL rule, board list |
| 2.0        | Contact Discovery: fetch, parse, extract, contact master output, flags, review |
| 3.0        | Letter spec + template in repo, versioned, loadable |
| 4.0        | Playbook derivation, Outreach Agent (draft-only default), filtering, optional send/state |
| 5.0        | AWS: S3, Lambda, Bedrock, optional Step Functions, SES, DynamoDB |
| 6.0        | Locations, runbook, E2E validation, open-questions doc |
