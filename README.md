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

## Architecture

The pipeline consists of several specialized agents:
1. **Planner**: Breaks the query into a multi-step research plan.
2. **Researcher**: Uses Gemini's Google Search tool to find facts (iterative).
3. **Summarizer**: Condenses raw findings into concise bullet points.
4. **Reporter**: Synthesizes the summary into a professional Markdown report.
5. **Reviewer**: Evaluates the report and provides feedback or approval.
6. **Saver**: Persists the final approved report to disk.

## Testing

Run the integration tests to verify the workflow:

```bash
pytest
```
ovides feedback or approval.
6. **Saver**: Persists the final approved report to disk.

## Testing

Run the integration tests to verify the workflow:

```bash
uv run pytest
```
