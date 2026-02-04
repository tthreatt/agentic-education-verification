# Two-Week Education Verification Prototype: Scope & Decision Summary

**Goal:** Prototype something in two weeks and bring back learnings, successes, and failures. Scoping is critical.

---

## 1. What We're Trying to Accomplish

- **Reduce or eliminate manual clinician education verification** by:
  - Using **board certification and other trusted sources** as "proxy" primary source verification (PSV) where allowed (state boards, ABMS, AOA, AMA, NSC, etc.).
  - Designing an **agentic workflow** (e.g., Strands Agents) with Discovery, Outreach, and Validation agents that orchestrate this logic and build internal agentic AI capability.

- **Decision-tree logic:** Once any source in the tree stands in for education verification, we're done. The open question is **which part of the tree** we automate agentically first.

---

## 2. Scope Decisions We Need to Make

### 2.1 Provider type (who)

| Option | Pros | Cons |
|--------|------|------|
| **MD/DO first** | Clearer path; existing integrations (ABMS, AOA); faster win; establishes pattern | Doesn't prove approach for harder cases |
| **Behavioral health first** | Proves approach where it's hardest; NCQA calls out full credentialing/education for this group | Messier tree and sources; higher risk of little to show in 2 weeks |

**Decision needed:** MD/DO first vs. behavioral health first for this 2-week prototype.

---

### 2.2 Part of the tree (what)

| Option | Description | Trigger | Agents in play |
|--------|-------------|---------|----------------|
| **Top of tree** | Get and maintain **letters/agreements from boards and authorities** so we have a "proxy eligible" list and can use board cert (etc.) as proof | **Date-based** (e.g., "we need updated letters by date X") | Discovery Agent, Outreach Agent |
| **Bottom of tree** | **Per-provider institutional verification** when no proxy applies—reach out to schools one-off | **Request-based** ("we need institutional verification for this provider") | Validation Agent (and possibly a fourth agent for institution outreach) |

**Decision needed:** Top (letters) vs. bottom (institutional verification) for the first 2-week prototype. This also sets whether the first trigger is **date-based** or **provider-based**.

---

## 3. How It Fits Together

- **Mechanisms:** Each source can use any mechanism (API, batch, email, portal, etc.). We support whatever fits per source; no single global mechanism.
- **API Intelligence POC:** Queries the **profile database** (RAG-structured): "What do we already have?" That's the **read/query layer**. Agentic education verification is the **execution layer** that uses that state to decide and act (get letters vs. get institutional verification). Complementary.
- **Strands Agents:** Chosen as the SDK for building and running agents (model + tools + prompt; agentic loop). Reference: `docs/strands-agents-summary.md`.

---

## 4. Two-Week Constraint

- **Not all possible in two weeks.** Discovery + outreach (top of tree) was discussed as the initial scope.
- Success = **clear learnings, successes, and failures**—not necessarily a production-ready system. Scoping tightly is essential.

---

## 5. Decision Checklist

Use this to lock the 2-week scope:

- [ ] **Provider type:** MD/DO **or** behavioral health (pick one for this prototype).
- [ ] **Tree segment:** Top (letters / Discovery + Outreach) **or** bottom (institutional verification / Validation) (pick one for this prototype).
- [ ] **Trigger type:** Date-based (top) or provider-based (bottom)—follows from tree segment.
- [ ] **Concrete 2-week outcome:** e.g., "Discovery agent run on N boards + one Outreach flow" or "Validation agent run on M test providers with one institution type."

---

## 6. References

- Meeting takeaways and agent concepts: `docs/260203_meeting-notes.md`
- Context and API Intelligence link: `docs/current_conversation.md`
- Strands Agents overview: `docs/strands-agents-summary.md`
