"""Planner agent node."""

import logging

from google.genai import types

from schema import AgentState
from utils import get_client, get_model_name

logger = logging.getLogger(__name__)


def planner_node(state: AgentState) -> dict:
    """Create a research plan based on the query."""
    logger.info("Planning research...")
    client = get_client()
    model = get_model_name()

    prompt = f"User Query: {state['query']}\n\nCreate a concise research plan with 3-5 specific questions to answer. Focus on factual accuracy and depth."

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1),
    )

    return {"research_plan": str(response.text), "iteration": 0, "raw_research": []}
