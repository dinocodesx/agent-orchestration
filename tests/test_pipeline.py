"""Integration coverage for the orchestration pipeline."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from main import create_orchestrator, AgentState

@pytest.fixture
def mock_gemini_client():
    with patch("main.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        yield mock_client

def test_pipeline_runs_with_mocked_gemini(tmp_path: Path, mock_gemini_client) -> None:
    output_path = tmp_path / "report.md"

    # Setup the mock responses for the 3 phases
    research_response = MagicMock()
    research_response.text = "LangChain supports agents and chains. Source: https://python.langchain.com/docs/"
    
    summarize_response = MagicMock()
    summarize_response.text = "- LangChain provides agent and chain abstractions.\n- Source: https://python.langchain.com/docs/"
    
    report_response = MagicMock()
    report_response.text = "\n".join([
        "# LangChain Agent Frameworks",
        "",
        "## Key Findings",
        "- LangChain provides agent and chain abstractions.",
        "",
        "## Conclusion",
        "LangChain can orchestrate multi-step agent workflows.",
        "",
        "## Sources",
        "- https://python.langchain.com/docs/",
        "",
    ])

    # Ensure the mock returns these responses in sequence for the 3 calls
    mock_gemini_client.models.generate_content.side_effect = [
        research_response,
        summarize_response,
        report_response
    ]

    orchestrator = create_orchestrator()

    initial_state: AgentState = {
        "query": "What are agent frameworks?",
        "raw_research": "",
        "summary": "",
        "final_report": "",
        "report_path": str(output_path),
    }

    result = orchestrator.invoke(initial_state)

    assert "LangChain Agent Frameworks" in result["final_report"]
    assert Path(result["report_path"]).read_text(encoding="utf-8").startswith(
        "# LangChain Agent Frameworks"
    )
    
    assert mock_gemini_client.models.generate_content.call_count == 3
