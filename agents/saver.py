"""Saver agent node."""

import logging
from pathlib import Path

from schema import AgentState

logger = logging.getLogger(__name__)


def save_report_node(state: AgentState) -> dict:
    """Save the final report to disk."""
    report_path = state.get("report_path", "output/report.md")
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(state["final_report"], encoding="utf-8")
    logger.info(f"Final report saved to {report_path}")
    return {}
