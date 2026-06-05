"""Command-line entry point for the LangGraph agent orchestration demo using Gemini API."""

import argparse
import logging
import os
from pathlib import Path
from typing import TypedDict
from dotenv import load_dotenv

from google import genai
from google.genai import types
from langgraph.graph import StateGraph, END

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    """The state of the research and reporting pipeline."""
    query: str
    raw_research: str
    summary: str
    final_report: str
    report_path: str

def get_client() -> genai.Client:
    """Initialize the Gemini client."""
    if not os.getenv("GEMINI_API_KEY") and os.getenv("GOOGLE_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]
    return genai.Client()

def research_node(state: AgentState) -> dict:
    """Search for relevant facts using Gemini's built-in Google Search."""
    logger.info("Starting research phase...")
    client = get_client()
    model = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    
    prompt = f"Research the following query and provide detailed facts, including sources:\n\nQuery: {state['query']}"
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            tools=[{"google_search": {}}],
        )
    )
    
    logger.info("Research complete.")
    return {"raw_research": str(response.text)}

def summarize_node(state: AgentState) -> dict:
    """Condense the raw facts into concise bullets."""
    logger.info("Starting summary phase...")
    client = get_client()
    model = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    
    prompt = f"User Query: {state['query']}\n\nRaw Research:\n{state['raw_research']}\n\nCondense this research into concise bullet points. Remove duplicates and preserve any source URLs."
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        )
    )
    
    logger.info("Summary complete.")
    return {"summary": str(response.text)}

def report_node(state: AgentState) -> dict:
    """Structure the bullets into a final Markdown report."""
    logger.info("Starting reporting phase...")
    client = get_client()
    model = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    
    prompt = f"User Query: {state['query']}\n\nSummary:\n{state['summary']}\n\nCreate a well-structured Markdown report based on the summary. Include a Title, Key Findings, Conclusion, and Sources."
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        )
    )
    
    final_report = str(response.text)
    report_path = state.get("report_path", "output/report.md")
    
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(final_report, encoding="utf-8")
    
    logger.info(f"Report saved to {report_path}")
    return {"final_report": final_report}

def create_orchestrator():
    """Create a LangGraph StateGraph that runs research, summary, and report steps."""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("researcher", research_node)
    workflow.add_node("summarizer", summarize_node)
    workflow.add_node("reporter", report_node)
    
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "summarizer")
    workflow.add_edge("summarizer", "reporter")
    workflow.add_edge("reporter", END)
    
    return workflow.compile()

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
        "raw_research": "",
        "summary": "",
        "final_report": "",
        "report_path": args.output,
    }
    
    logger.info(f"Starting pipeline for query: '{args.query}'")
    result = orchestrator.invoke(initial_state)
    
    print("\n" + "="*40 + "\nFINAL REPORT\n" + "="*40)
    print(result["final_report"])

if __name__ == "__main__":
    main()
