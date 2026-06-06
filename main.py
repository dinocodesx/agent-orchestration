"""Command-line entry point with Human-in-the-Loop support."""

import argparse
import logging
import uuid
from typing import cast

from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig

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
    """Run the full pipeline with HITL support."""
    load_dotenv()
    args = parse_args()

    orchestrator = create_orchestrator()
    thread_id = str(uuid.uuid4())
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    current_state: AgentState = {
        "query": args.query,
        "research_plan": "",
        "raw_research": [],
        "summary": "",
        "final_report": "",
        "report_path": args.output,
        "iteration": 0,
        "feedback": "",
    }

    logger.info(f"Starting pipeline [Thread: {thread_id}]")

    # Run until first interrupt or end
    for event in orchestrator.stream(current_state, config, stream_mode="values"):
        current_state = cast(AgentState, event)
    # Check if we are at an interrupt point
    snapshot = orchestrator.get_state(config)
    if snapshot.next:
        print("\n" + "!" * 40)
        print("HUMAN-IN-THE-LOOP: Plan Approval Required")
        print("!" * 40)
        print(f"\nPROPOSED PLAN:\n{snapshot.values.get('research_plan')}")

        user_input = (
            input("\nDo you approve this plan? (yes/no/edit): ").strip().lower()
        )

        if user_input == "no":
            logger.info("Plan rejected. Ending.")
            return
        elif user_input == "edit":
            new_plan = input("Enter the revised plan: ")
            orchestrator.update_state(config, {"research_plan": new_plan})

        logger.info("Resuming pipeline...")
        # Resume execution
        for event in orchestrator.stream(None, config, stream_mode="values"):
            current_state = cast(AgentState, event)

    print("\n" + "=" * 40 + "\nFINAL REPORT\n" + "=" * 40)
    print(current_state.get("final_report", "No report generated."))


if __name__ == "__main__":
    main()
