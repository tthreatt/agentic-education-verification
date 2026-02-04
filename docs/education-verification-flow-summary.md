# Education Verification Flow — Summary

Summary of the architecture shown in *Screenshot 2026-02-04 at 10.48.15 AM.png*.

## Overview

The diagram describes an **event-driven, AI-powered education verification system** on AWS. It is triggered by email or other events, uses an AI agent (Strands SDK + Bedrock) to perform verification, then either notifies the client by email or stores the result.

## Flow

### 1. Initiation

- **Client email:** The client sends an email → **AWS SES (Inbound)** receives it → request is passed to the **Orchestrator Lambda**.
- **Other triggers:** Additional event sources (“Other Triggers?”) can also invoke the **Orchestrator Lambda** directly.

### 2. Orchestration and AI

- **Orchestrator Lambda** is the single entry point. It receives the request and **spawns an AI agent** using the **Strands SDK** on **AWS Bedrock**.
- The agent runs the **education verification** logic.

### 3. Decision

After the agent runs, the flow branches on:

**“Education verification is satisfactory?”**

### 4. If No (unsatisfactory)

- Flow uses the **Send Email MCP Tool**.
- That tool calls **AWS SES (Outbound)** to send an email.
- The **client** receives the notification (e.g., that verification was not satisfactory or what to do next).

### 5. If Yes (satisfactory)

- Flow uses the **Store Results MCP Tool**.
- That tool writes to the **Education Verification Store** (persistent store for successful verifications).

## Components

| Component | Role |
|----------|------|
| Client | Initiates via email (or other triggers) |
| AWS SES (Inbound) | Receives client email, forwards to Orchestrator |
| Other Triggers? | Alternative event sources for the flow |
| Orchestrator Lambda | Entry point; spawns and drives the agent |
| Strands SDK + AWS Bedrock | AI agent that performs education verification |
| Send Email MCP Tool | Sends outbound email when verification is unsatisfactory |
| Store Results MCP Tool | Persists results when verification is satisfactory |
| AWS SES (Outbound) | Sends email to the client |
| Education Verification Store | Database/storage for successful verification results |

## Summary

**Trigger** (email or other) → **Orchestrator Lambda** → **Agent** (Strands + Bedrock) performs verification → **Branch:** unsatisfactory → Send Email MCP → SES Outbound → **Client**; satisfactory → Store Results MCP → **Education Verification Store**.
