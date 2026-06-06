"""Researcher agent node - Iterative Deep Research."""

import logging

from google.genai import types

from schema import AgentState
from utils import get_client, get_model_name

logger = logging.getLogger(__name__)


def researcher_node(state: AgentState) -> dict:
    """Search for relevant facts with iterative refinement and deep-dive capabilities."""
    iteration = state.get("iteration", 0) + 1
    logger.info(f"Starting research iteration {iteration}...")
    client = get_client()
    model = get_model_name()

    # Context-aware prompting (Industry Trend: Chain-of-Thought Research)
    context = f"Research Plan: {state['research_plan']}\n"
    if state.get("feedback"):
        context += f"PREVIOUS EVALUATION FEEDBACK: {state['feedback']}\n"

    prompt = f"""
    {context}

    Your goal is to find high-quality, factual information to fulfill the research plan.
    If you have previous feedback, prioritize addressing those specific gaps.
    Look for recent data (2025-2026) and ensure you capture source names for citations.

    Current iteration: {iteration}
    """

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            tools=[{"google_search": {}}],
            # Industry Trend: System instructions or specific search configurations
        ),
    )

    new_research = list(state.get("raw_research", []))
    new_research.append(str(response.text))

    return {"raw_research": new_research, "iteration": iteration}
