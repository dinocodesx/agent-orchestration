"""Reporter agent node."""

import logging

from google.genai import types

from schema import AgentState
from utils import get_client, get_model_name

logger = logging.getLogger(__name__)


def reporter_node(state: AgentState) -> dict:
    """Structure the bullets into a final Markdown report."""
    logger.info("Starting reporting phase...")
    client = get_client()
    model = get_model_name()

    prompt = f"User Query: {state['query']}\n\nSummary:\n{state['summary']}\n\nCreate a professional Markdown report. Use headers, bold text, and lists. Ensure all sources from the research are cited."

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1),
    )

    return {"final_report": str(response.text)}
