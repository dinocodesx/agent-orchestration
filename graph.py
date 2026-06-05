"""Workflow graph definition."""

import logging

from langgraph.graph import END, StateGraph

from agents.planner import planner_node
from agents.reporter import reporter_node
from agents.researcher import researcher_node
from agents.reviewer import reviewer_node
from agents.saver import save_report_node
from agents.summarizer import summarizer_node
from schema import AgentState

logger = logging.getLogger(__name__)


def should_continue(state: AgentState):
    """Determine if we should continue researching or approve the report."""
    if "APPROVED" in state.get("feedback", ""):
        return "end"
    if state.get("iteration", 0) >= 3:
        logger.warning("Max iterations reached. Ending pipeline.")
        return "end"
    return "continue"


def create_orchestrator():
    """Create a LangGraph StateGraph with advanced orchestration."""
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("reporter", reporter_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("saver", save_report_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "summarizer")
    workflow.add_edge("summarizer", "reporter")
    workflow.add_edge("reporter", "reviewer")

    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "continue": "researcher",
            "end": "saver",
        },
    )

    workflow.add_edge("saver", END)

    return workflow.compile()
