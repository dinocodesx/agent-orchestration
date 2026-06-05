"""Researcher agent node."""

import logging

from google.genai import types

from schema import AgentState
from utils import get_client, get_model_name

logger = logging.getLogger(__name__)


def researcher_node(state: AgentState) -> dict:
    """Search for relevant facts using Gemini's built-in Google Search."""
    iteration = state.get("iteration", 0) + 1
    logger.info(f"Starting research iteration {iteration}...")
    client = get_client()
    model = get_model_name()

    # If we have feedback, use it to refine the search
    context = f"Research Plan: {state['research_plan']}\n"
    if state.get("feedback"):
        context += f"Previous Feedback: {state['feedback']}\n"

    prompt = f"{context}\nFind detailed facts for the next part of the research plan. Current iteration: {iteration}"

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            tools=[{"google_search": {}}],
        ),
    )

    new_research = list(state.get("raw_research", []))
    new_research.append(str(response.text))

    return {"raw_research": new_research, "iteration": iteration}
