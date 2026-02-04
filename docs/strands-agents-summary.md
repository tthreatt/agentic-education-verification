### Strands Agents – Summary

**Source**: [Introducing Strands Agents, an Open Source AI Agents SDK](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/)

### Overview
- **Strands Agents** is an open source SDK from AWS for building and running AI agents with a **model‑driven** approach.
- It focuses on letting modern LLMs handle planning, tool use, and reasoning, instead of relying on heavy, predefined orchestration workflows.
- It’s already used in production at AWS (for example, **Amazon Q Developer**, **AWS Glue**, and **VPC Reachability Analyzer**).

### Core concepts
Strands defines an agent as three things:
- **Model**: Any tool‑using, streaming LLM (for example, Amazon Bedrock models, Anthropic Claude via Anthropic API, Llama via Llama API, Ollama, others via LiteLLM, or custom providers).
- **Tools**: Functions or services the agent can invoke (Python functions via an `@tool` decorator, MCP servers, built‑in utilities for HTTP, files, AWS APIs, and more).
- **Prompt**: System and user prompts that define the agent’s behavior and task.

Agents run in an **agentic loop**:
- The SDK calls the LLM with the prompt, context, and tool descriptions.
- The model may respond with natural language, choose tools, plan, or reflect.
- Strands executes tools and feeds back results until the task is complete.

### Example: naming agent
- The blog walks through a **naming assistant** that suggests names for an open source project.
- It uses:
  - A **system prompt** focused on naming.
  - An MCP server (`fastdomaincheck-mcp-server`) to check domain availability.
  - A Strands **HTTP request tool** to check GitHub organization name availability.
- Running the agent (after installing `strands-agents` and `strands-agents-tools` and configuring Bedrock plus a GitHub token) produces name suggestions plus available domains and GitHub orgs.

### Tools and patterns
Strands includes higher‑level tools to support complex behaviors:
- **Retrieve tool**: Semantic search over knowledge bases (for example, to select a small subset of relevant tools from thousands).
- **Thinking tool**: Encourages deep, multi‑step reasoning and self‑reflection when needed.
- **Multi‑agent tools** (workflow, graph, swarm): Enable structured collaboration across multiple sub‑agents, modeled as tools so the main agent can decide when to use them.

### Deployment architectures
Strands is designed for **production** from the start, with multiple reference architectures:
- **Local client**: Entire agent and tools run on a user’s machine (for example, a CLI assistant).
- **Backend API**: Agent and tools deployed behind an API (for example, via AWS Lambda, Fargate, or EC2).
- **Separated agent and tools**: Agent runs in one environment, tools in another (for example, agent in Fargate, tools as Lambda functions).
- **Return‑of‑control / hybrid tools**: Some tools run locally in the client, others in the backend.

### Observability and telemetry
- Strands emits **OpenTelemetry (OTEL)** traces and metrics for agent trajectories, enabling:
  - End‑to‑end request tracing across components.
  - Visualization and troubleshooting.
  - Evaluation of agent performance in production.

### Community and licensing
- Strands Agents is **open source**, **Apache 2.0‑licensed**.
- AWS is building it in the open and collaborating with partners such as **Accenture, Anthropic, Langfuse, mem0.ai, Meta, PwC, Ragas.io, and Tavily**.
- Contributions are welcome for new model providers, tools, features, and documentation.
