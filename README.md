# AI Research & Reporting Orchestrator

A modular, multi-agent orchestration pipeline built with **LangGraph** and **Gemini 2.5 Flash**. It uses iterative research with Google Search and self-correction to produce high-quality Markdown reports.

## Prerequisites

- Python 3.11+
- A Gemini API Key (get one at [aistudio.google.com](https://aistudio.google.com/))

## Setup

1. **Clone and enter the directory**:

   ```bash
   cd agent-orchestration
   ```

2. **Install dependencies**:
   Using [uv](https://docs.astral.sh/uv/):

   ```bash
   uv sync --all-extras
   ```

3. **Configure environment variables**:
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and add your `GEMINI_API_KEY`.

## Usage

Run the orchestrator by providing a research query using `uv run`:

```bash
uv run main.py --query "What are the latest breakthroughs in fusion energy?"
```

### Options

- `--query`: (Required) The topic you want the agents to research.
- `--output`: (Optional) Path to save the Markdown report. Defaults to `output/report.md`.

## Architecture (Modern AI Features)

The pipeline now includes industry-standard "Agentic" patterns:
1. **Planner**: Creates a research plan.
2. **Human-in-the-Loop (HITL)**: The system **pauses** after planning. You can approve, reject, or edit the plan before research begins.
3. **Researcher**: Iterative deep research with Google Search.
4. **Summarizer**: Condenses findings.
5. **Reporter**: Generates a professional Markdown report.
6. **LLM-as-a-Judge (Reviewer)**: Evaluates the report using structured metrics (Faithfulness, Relevancy, Structure). It loops back for more research if the score is low.
7. **Observability**: Supports **LangSmith** tracing (if `LANGSMITH_API_KEY` is in `.env`).
8. **Saver**: Persists the final approved report.


## Testing

Run the integration tests to verify the workflow:

```bash
uv run pytest
```
