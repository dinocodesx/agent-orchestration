"""Command-line entry point for the LangGraph agent orchestration demo."""

import argparse
import logging

from dotenv import load_dotenv

from graph import create_orchestrator
from schema import AgentState

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Run the Research & Reporting Assistant pipeline."
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Research question to send through the multi-agent pipeline.",
    )
    parser.add_argument(
        "--output",
        default="output/report.md",
        help="Optional markdown report path. Defaults to output/report.md.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the full pipeline from a query string."""
    load_dotenv()
    args = parse_args()

    orchestrator = create_orchestrator()

    initial_state: AgentState = {
        "query": args.query,
        "research_plan": "",
        "raw_research": [],
        "summary": "",
        "final_report": "",
        "report_path": args.output,
        "iteration": 0,
        "feedback": "",
    }

    logger.info(f"Starting pipeline for query: '{args.query}'")
    result = orchestrator.invoke(initial_state)

    print("\n" + "=" * 40 + "\nFINAL REPORT\n" + "=" * 40)
    print(result.get("final_report", "No report generated."))


if __name__ == "__main__":
    main()
