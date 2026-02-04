# Agentic Contact Letter — ER and Flow Diagrams

From [prd-agentic-contact-letter.md](./prd-agentic-contact-letter.md).

---

## 1. Entity-Relationship Diagram

Entities and relationships for contact discovery, letter content, and outreach.

Source: [prd-agentic-contact-letter-er.mmd](./prd-agentic-contact-letter-er.mmd)

```mermaid
erDiagram
    BoardList ||--o{ Board : "contains"
    Board ||--o| ContactMaster : "has one row"
    LetterSpec ||--|| LetterTemplate : "implements"
    ContactMaster }o--o{ LetterTemplate : "used with"
    OutreachPlaybook ||--o{ PlaybookEntry : "contains"
    Board ||--o| OutreachState : "has status"
    ContactMaster ||--o| OutreachState : "used for"

    BoardList {
        string source_file "e.g. behavioral-health-state-boards-subset.csv"
    }

    Board {
        string board_name PK
        string source_url
        string confluence_link "optional"
        string base_url "derived from source_url"
    }

    ContactMaster {
        string board_name PK,FK
        string contact_emails
        string contact_role_title "optional"
        string phone "optional"
        string contact_form_url "optional"
        string mailing_address "optional"
        string source_of_truth "board website | Confluence"
        string confluence_link "optional"
    }

    LetterSpec {
        string id PK
        string required_clauses "e.g. attestation of PSV"
        string scope_license_types
        string effective_date
        string signatory "authorized board representative"
        string refresh_process "how to request re-sign"
    }

    LetterTemplate {
        string id PK
        string spec_id FK
        string addressee "our organization"
        string statement_of_verification
        string scope_block
        string signatory_block "signature/date"
    }

    OutreachPlaybook {
        string id PK
        string generated_at
        string filter_criteria "state, license type, no letter on file"
    }

    PlaybookEntry {
        string playbook_id FK
        string board_name FK
        string contact_method "email | form | mail"
        string template_id FK
        string who_to_contact "from contact master"
    }

    OutreachState {
        string board_name PK,FK
        string status "draft | request_sent | reminder_sent | letter_received"
        datetime last_contacted "optional"
        string sent_content_copy "audit copy, optional"
    }
```

---

## 2. System Flow Diagram

End-to-end flow: inputs → agents → artifacts → outreach.

Source: [prd-agentic-contact-letter-flow.mmd](./prd-agentic-contact-letter-flow.mmd)

```mermaid
flowchart TB
    subgraph inputs["Inputs"]
        BoardCSV["Board list CSV\n(board name, source URL, Confluence link)"]
        Docs["Docs / refs\n(meeting notes, scope, NCQA/CAQH optional)"]
    end

    subgraph contact_discovery["Contact Discovery"]
        CD_Agent["Contact Discovery Agent\n(HTTP, browser, parsing)"]
        CD_Agent --> DeriveBaseURL["Derive base URL\nfrom source URL"]
        DeriveBaseURL --> Scrape["Scrape board site\n(contact, about, staff)"]
        Scrape --> OptionalConfluence["Optional: Confluence\n(enrich contact)"]
        OptionalConfluence --> ContactMaster["Contact Master\n(structured CSV)"]
        ContactMaster --> HumanReviewContact["Human review & correct\ncontact master"]
    end

    subgraph letter_content["Letter Content"]
        LC_Agent["Letter Content Agent\n(prompt + retrieval over docs)"]
        LC_Agent --> LetterSpec["Letter Spec\n(required clauses, signatory, refresh)"]
        LetterSpec --> LetterTemplate["Letter Template\n(Word/Markdown, implements spec)"]
        LetterTemplate --> StoreInRepo["Store in repo\n(docs/ or research/)"]
    end

    subgraph outreach["Outreach"]
        Filter["Filter boards\n(state, license type, no letter)"]
        PlaybookGen["Generate Outreach Playbook\n(per board: who, how, which template)"]
        OA["Outreach Agent\n(read contact master + template)"]
        Draft["Draft per-board outreach\n(email body or form payload)"]
        HumanReviewDraft["Human review draft\n(optional)"]
        SendOptional["Optional: send\n(record state + audit copy)"]
        Track["Track status\n(sent, reminder, letter received)"]
    end

    BoardCSV --> CD_Agent
    Docs --> LC_Agent

    HumanReviewContact --> ContactMasterFinal["Contact Master (approved)"]
    StoreInRepo --> LetterTemplatePath["Letter template path"]

    ContactMasterFinal --> Filter
    LetterTemplatePath --> Filter
    Filter --> PlaybookGen
    PlaybookGen --> OA
    OA --> Draft
    Draft --> HumanReviewDraft
    HumanReviewDraft --> SendOptional
    SendOptional --> Track

    style inputs fill:#e8f4f8
    style contact_discovery fill:#fff4e6
    style letter_content fill:#f0f8e8
    style outreach fill:#f5e6ff
```

---

### Flow summary

| Phase | Input | Agent / step | Output |
|-------|--------|---------------|--------|
| Contact Discovery | Board list CSV | Contact Discovery Agent (scrape + optional Confluence) | Contact Master → human review |
| Letter Content | Docs, meeting notes, scope | Letter Content Agent | Letter Spec + Letter Template (in repo) |
| Outreach | Contact Master, Letter Template, filter | Playbook gen → Outreach Agent | Draft (or send) per board → track status |

---

## 3. Outreach Architecture Diagram

How the outreach subsystem fits together: inputs, agents, deterministic services, and human-in-the-loop.

Source: [prd-agentic-contact-letter-outreach-architecture.mmd](./prd-agentic-contact-letter-outreach-architecture.mmd)

```mermaid
flowchart TB
    subgraph inputs["Outreach inputs"]
        CM["Contact Master\n(approved CSV)"]
        LT["Letter Template\n(path in repo)"]
        LetterSpec["Letter Spec\n(optional ref)"]
        FilterParams["Filter params\n(state, license type, no letter)"]
    end

    subgraph deterministic["Deterministic / rules"]
        Filter["Filter service\n(apply state, license, no-letter)"]
        PlaybookDerive["Playbook derivation\n(join: board → who, how, which template)"]
    end

    subgraph agents["Agents"]
        PlaybookAgent["Playbook Generator Agent\n(optional: decide channel/tone per board)"]
        OA["Outreach Agent\n(model + tools + prompt)"]
    end

    subgraph oa_tools["Outreach Agent tools"]
        ReadContact["Read contact master"]
        ReadTemplate["Read letter template"]
        ComposeDraft["Compose draft\n(email body or form payload)"]
        OptionalSend["Optional: send tool\n(email API, form submit)"]
    end

    subgraph human_and_automation["Human & automation"]
        HumanReview["Human review draft\n(approve / edit)"]
        SendOptional["Optional: send\n(record state + audit copy)"]
        Track["Track status\n(sent, reminder, letter received)"]
    end

    subgraph stores["Stores"]
        PlaybookStore["Outreach Playbook\n(per-board: who, how, template)"]
        StateStore["Outreach state\n(per board status, audit copy)"]
    end

    CM --> Filter
    LT --> Filter
    FilterParams --> Filter
    Filter --> PlaybookDerive
    CM --> PlaybookDerive
    LT --> PlaybookDerive
    LetterSpec --> PlaybookDerive

    PlaybookDerive --> PlaybookStore
    PlaybookDerive -.->|"optional"| PlaybookAgent
    PlaybookAgent --> PlaybookStore

    PlaybookStore --> OA
    CM --> OA
    LT --> OA
    OA --> ReadContact
    OA --> ReadTemplate
    OA --> ComposeDraft
    ComposeDraft --> HumanReview
    HumanReview --> SendOptional
    SendOptional --> OptionalSend
    SendOptional --> StateStore
    Track --> StateStore

    style inputs fill:#e8f4f8
    style agents fill:#ffd6d6
    style deterministic fill:#e8f0e8
    style human_and_automation fill:#f5e6ff
    style stores fill:#f0f0f0
```

### Outreach component roles

| Component | Role | Agentic? |
|-----------|------|----------|
| **Filter** | Apply state, license type, “no letter on file” to board list. | No — rules/query. |
| **Playbook derivation** | Build playbook from contact master + letter spec (who, how, which template per board). | No — join/derivation. Can be replaced or augmented by Playbook Generator Agent. |
| **Playbook Generator Agent** | Optional: per-board judgment on channel (email vs form vs mail), tone, or edge cases. | Yes — model + tools + prompt. |
| **Outreach Agent** | Read contact master + template; for each board (or playbook entry), produce draft outreach (email body or form payload). | Yes — model + tools + prompt. |
| **Human review** | Approve or edit draft before send. | Human-in-the-loop. |
| **Send / Track** | Record state, optional audit copy, status (sent, reminder, letter received). | No — automation + state store. |

---

### When agentic outreach is preferred vs. not

**Agentic design is preferred when:**

- You need **per-board judgment**: e.g. adapt tone (formal vs. brief), choose channel (email vs. form) when multiple exist, or handle missing/incomplete contact data with fallback wording.
- You want **one agent** to own “read contact + template → produce draft” so it can reason over edge cases (e.g. “contact form only” vs. “email + form”) and keep wording consistent with the letter spec.
- Playbook generation should **recommend strategy** (who to contact first, how to phrase the ask) rather than only joining static fields.

**A non-agentic (deterministic) design is preferable when:**

- The task is **fully templated**: same letter body, only board name and contact name substituted; no need to adapt phrasing or channel.
- You want **low cost and simple ops**: a template engine + Filter + Playbook (as a derived table) is easier to debug and run than an LLM.
- **Compliance or audit** requires every board to receive byte-for-byte identical text; then a fixed template + variable substitution is safer than an agent-generated draft.

For the PRD’s “draft per-board outreach (email body or form payload)” with optional human review, the **Outreach Agent** is the core agentic piece; **Playbook** can stay derived (non-agentic) unless you explicitly want per-board strategy from an LLM.
