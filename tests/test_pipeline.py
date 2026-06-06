"""Integration coverage for the orchestration pipeline."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from langchain_core.runnables import RunnableConfig

from graph import create_orchestrator
from schema import AgentState


@pytest.fixture
def mock_gemini_client():
    # Patch google.genai.Client directly so that any call to it returns our mock
    with patch("google.genai.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        yield mock_client


def test_pipeline_runs_with_mocked_gemini(tmp_path: Path, mock_gemini_client) -> None:
    output_path = tmp_path / "report.md"

    # Setup the mock responses for the phases
    planner_response = MagicMock()
    planner_response.text = "Plan: 1. Research framework A. 2. Research framework B."

    research_response = MagicMock()
    research_response.text = "Research: Framework A is good. Framework B is also good."

    summarize_response = MagicMock()
    summarize_response.text = "- Framework A is good.\n- Framework B is also good."

    report_response = MagicMock()
    report_response.text = "# Framework Report\n\nFramework A and B are both good."

    reviewer_response = MagicMock()
    reviewer_response.text = "APPROVED"

    # Ensure the mock returns these responses in sequence
    mock_gemini_client.models.generate_content.side_effect = [
        planner_response,
        research_response,
        summarize_response,
        report_response,
        reviewer_response,
    ]

    orchestrator = create_orchestrator()
    config: RunnableConfig = {"configurable": {"thread_id": "test_thread"}}

    initial_state: AgentState = {
        "query": "What are agent frameworks?",
        "research_plan": "",
        "raw_research": [],
        "summary": "",
        "final_report": "",
        "report_path": str(output_path),
        "iteration": 0,
        "feedback": "",
    }

    # First call: runs up to the interrupt (before researcher)
    result = orchestrator.invoke(initial_state, config=config)
    assert result["research_plan"] != ""
    assert result["final_report"] == ""

    # Second call: resumes from the interrupt
    result = orchestrator.invoke(None, config=config)

    assert "# Framework Report" in result["final_report"]
    assert Path(result["report_path"]).exists()
    # Call count: 1 (planner) + 4 (researcher, summarizer, reporter, reviewer) = 5
    assert mock_gemini_client.models.generate_content.call_count == 5
