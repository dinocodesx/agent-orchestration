"""Summarizer agent node."""

import logging

from google.genai import types

from schema import AgentState
from utils import get_client, get_model_name

logger = logging.getLogger(__name__)


def summarizer_node(state: AgentState) -> dict:
    """Condense the raw facts into concise bullets."""
    logger.info("Starting summary phase...")
    client = get_client()
    model = get_model_name()

    all_research = "\n---\n".join(state["raw_research"])
    prompt = f"User Query: {state['query']}\n\nResearch Data:\n{all_research}\n\nSummarize the key findings into a comprehensive list of bullet points. Keep it concise to save tokens."

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1),
    )

    return {"summary": str(response.text)}
