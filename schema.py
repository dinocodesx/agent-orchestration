"""State and schema definitions for the research pipeline."""

from typing import List, TypedDict


class AgentState(TypedDict):
    """The state of the research and reporting pipeline."""

    query: str
    research_plan: str
    raw_research: List[str]
    summary: str
    final_report: str
    report_path: str
    iteration: int
    feedback: str
