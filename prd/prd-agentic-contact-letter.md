# Product Requirements Document: Agentic Contact Discovery, Letter Content, and Outreach

## 1. Introduction / Overview

Education verification today relies on knowing **where** to look up credentials (state board license lookup URLs are documented), but we do **not** have structured answers for: (1) where to get **contact information** for each verification source, (2) **who** to contact and **how** (email, form, mail), or (3) **what the letter** requesting proxy verification should say. This PRD defines an agentic system that fills those three gaps so we can systematically request and maintain signed letters from boards stating they perform primary source verification (PSV) of education, building a "proxy eligible" list and reducing manual verification.

**Problem:** We cannot reliably contact the right person at each board or send a standardized request because contact data and letter content are undefined.

**Goal:** Deliver a system of agents and artifacts that discover contact info per board, define and draft the letter content, and run (or prepare) outreach so we know who to contact, how to contact them, and what to ask for.

---

## 2. Goals

- **Contact discovery:** Produce a single, structured **contact master** (per board) that answers: where we got the contact info, who to contact (role/title if available), and how to contact (email, contact form URL, or mail).
- **Letter clarity:** Produce a **letter template** and **letter spec** (required clauses, signatory, refresh process) so outreach requests are consistent and aligned with “highest level of education verification” / compliance requirements.
- **Outreach execution:** Produce an **outreach playbook** and an **Outreach Agent** that uses the contact master and letter template to prepare (and optionally send) per-board requests and track status.
- **Integration with existing scope:** Align with the existing Discovery + Outreach (top-of-tree) scope and with the existing board list (e.g. behavioral health state boards CSV and docs).

---

## 3. User Stories

- **As a** credentialing operator, **I want** a list of boards with contact email or form and preferred contact role **so that** I know who to reach out to without manual searching.
- **As a** credentialing operator, **I want** a standard letter template and a short spec of what must be in the letter **so that** every board receives the same ask and we can get legal/compliance sign-off once.
- **As a** credentialing operator, **I want** the system to draft (or send) outreach for each board using that template and contact info **so that** we can scale letter requests and track sent/pending/received.
- **As a** developer, **I want** contact data and letter assets stored in versioned, explicit formats (e.g. CSV, Markdown) **so that** agents and humans can read and update them without hidden state.

---

## 4. Functional Requirements

### 4.1 Contact Discovery

1. The system must accept as input the list of boards (e.g. from `research/behavioral-health-state-boards-subset.csv` or a derived unique-board list), including at least: Board Name, Source Url, and Confluence Link (if present).
2. The system must derive a board “base URL” from each board’s Source Url (e.g. license lookup URL) for use in finding contact pages.
3. The system must attempt to find contact information from (a) the board’s website (contact, about, or staff pages), and optionally (b) Confluence when an integration is available.
4. The system must extract and store, per board: at least one contact email or contact form URL, and when available: phone, mailing address, and role/title (e.g. “Executive Director,” “License Verification”).
5. The system must record the **source** of the contact info (e.g. “board website,” “Confluence”) per board.
6. The system must output a **contact master** in a structured format (e.g. CSV or equivalent) with columns: Board Name, Board Base URL, Contact Email(s), Contact Role/Title (if found), Phone, Contact Form URL (if used), Source of truth, Confluence Link.
7. The system must support human review and correction of contact master rows before the data is used for outreach.
8. The system must flag boards for which no contact info could be found so they can be handled manually.

### 4.2 Letter Content

9. The system must produce a **letter specification** document that states: required clauses (e.g. attestation of primary source verification of education), scope (license types), effective date, signatory (authorized board representative), and how to request re-sign/refresh.
10. The system must produce a **letter template** (e.g. Word or Markdown) that implements the spec and can be used as the body or attachment of outreach requests.
11. The letter template must include: addressee (our organization), board name, statement of verification practice, scope of license types, effective date, signatory and signature/date block.
12. If NCQA/CAQH references are provided, the system may map template clauses to those standards and flag gaps; this is optional and depends on input availability.

### 4.3 Outreach

13. The system must produce an **outreach playbook** that, for each board (or a filtered subset), states: who to contact (from contact master), how to contact (email vs. form vs. mail), and which letter template to use.
14. The system must include an **Outreach Agent** that: reads the contact master and letter template, and for each board (or filtered list) generates a draft outreach (e.g. email body or form payload) using the template.
15. The Outreach Agent must support a mode where it only **drafts** outreach for human review and send (no automatic sending) when so configured.
16. If an optional “send” mode is enabled, the system must record per-board outreach state (e.g. “request sent,” “reminder sent,” “letter received”) and retain a copy of sent content (e.g. email) for audit.
17. The system must allow filtering the set of boards for outreach (e.g. by state, license type, or “no letter on file”) so that not all boards are contacted in a single run.

### 4.4 Data and Artifacts

18. The letter template and letter spec must be stored in the repository (e.g. under `docs/` or `research/`) and versioned so the Outreach Agent can load them explicitly.
19. The contact master must be stored in a known location and format so that both humans and the Outreach Agent can read and, where allowed, update it.

---

## 5. Non-Goals (Out of Scope)

- **Validation Agent and per-provider verification:** This PRD does not cover the Validation Agent (checking a clinician’s board status against the proxy list) or outreach to education institutions for one-off verification. Those remain in scope for a later phase.
- **Discovery Agent implementation:** The existing “Discovery Agent” (analyzing bylaws for PSV) is referenced as an upstream input (list of boards that need a letter) but is not specified in detail here; this PRD focuses on contact discovery, letter content, and outreach.
- **Confluence integration:** If Confluence is not available via API to the agent environment, contact discovery may rely only on board websites; Confluence can be integrated later or used manually to enrich the contact master.
- **Legal/compliance final sign-off:** The system produces a draft letter template and spec; final approval of wording and signatory requirements remains with legal/compliance.
- **Full production hardening:** This PRD supports a prototype / first-run capability; security hardening, rate limiting, and full production deployment are out of scope unless explicitly added later.

---

## 6. Design Considerations

- **Contact master schema:** Design the CSV (or equivalent) so a junior developer can add columns later (e.g. “last_contacted_date,” “letter_received”) without breaking existing readers.
- **Playbook as derived artifact:** The outreach playbook can be generated from the contact master + letter spec (e.g. one row per board with “contact email,” “channel,” “template version”) so it stays in sync with data.
- **Human-in-the-loop:** Contact Discovery and Outreach should assume a human reviews contact data and optionally each draft before send; the UI can be “file in repo + script output” for the prototype.

### 6.1 Outreach: when agentic vs. deterministic

Outreach does **not** have to be agentic. The same flow can be implemented with Filter → Playbook derivation → template fill → human review → optional send → track, using a template engine (e.g. Jinja or simple variable substitution) and no LLM.

**Agentic design is preferred when:**

- You need **per-board judgment**: e.g. adapt tone (formal vs. brief), choose channel (email vs. form) when multiple exist, or handle missing/incomplete contact data with fallback wording.
- You want one component to own "read contact + template → produce draft" so it can **reason over edge cases** (e.g. "contact form only" vs. "email + form") and keep wording consistent with the letter spec.
- Playbook generation should **recommend strategy** (who to contact first, how to phrase the ask) rather than only joining static fields.

**A non-agentic (deterministic) design is preferable when:**

- The task is **fully templated**: same letter body, only board name and contact name substituted; no need to adapt phrasing or channel.
- You want **low cost and simple ops**: a template engine + Filter + Playbook (as a derived table) is easier to debug and run than an LLM.
- **Compliance or audit** requires every board to receive byte-for-byte identical text; then a fixed template + variable substitution is safer than an agent-generated draft.

For "draft per-board outreach (email body or form payload)" with optional human review, the **Outreach Agent** is the core agentic piece when chosen; the **Playbook** can stay derived (non-agentic) unless you explicitly want per-board strategy from an LLM. See [prd-agentic-contact-letter-diagrams.md](./prd-agentic-contact-letter-diagrams.md) (Outreach Architecture Diagram) for the component breakdown.

---

## 7. Technical Considerations

- **Strands Agents:** Per `docs/strands-agents-summary.md`, each agent is model + tools + prompt. Contact Discovery needs HTTP/browser and parsing tools; Letter Content can use prompt + retrieval over docs; Outreach needs read access to contact master and letter template and optional send tool.
- **Inputs:** Contact Discovery Agent inputs: Board Name, Source Url, Confluence Link (optional). Letter Content Agent inputs: `docs/current_conversation.md`, `docs/260203_meeting-notes.md`, `docs/two-week-prototype-scope-decision.md`, and optionally NCQA/CAQH references. Outreach Agent inputs: contact master path, letter template path, optional filter parameters.
- **Outputs:** Contact master (file), letter spec (document), letter template (document), outreach playbook (generated), per-board outreach status (if sending is implemented).
- **Board base URL:** Derive from Source Url by taking the origin (scheme + host) or a known parent path (e.g. state DOPL site); document the derivation rule so it can be adjusted per board type.

---

## 8. Success Metrics

- **Contact coverage:** Percentage of boards in the input list for which the contact master has at least one contact method (email or contact form URL). Target: high coverage with clear flags for “no contact found.”
- **Letter spec and template:** One approved letter spec and one template in repo, loadable by the Outreach Agent.
- **Outreach readiness:** For a chosen subset of boards (e.g. 5–10), the system produces a playbook and draft outreach (email or form text) that a human can send with minimal edits.
- **Traceability:** Each outreach draft or sent item can be tied to a board, a template version, and a contact source.

---

## 9. Open Questions

- Should the first release support **sending** outreach (e.g. via email API) or only **drafting** for human send?
- What is the exact **contact master** file location and schema (CSV column set) for the repo?
- Who approves the **letter template** (legal, compliance, or product) and where is that approval recorded?
- Should the **Discovery Agent** (bylaws/PSV analysis) be implemented first so that Contact Discovery and Outreach only run for boards that “need a letter,” or should Contact Discovery run for all boards in the CSV initially?
- Are **NCQA/CAQH** documents available in a form the Letter Content Agent can use (e.g. URLs or uploaded text), and is mapping to those standards required for v1?
