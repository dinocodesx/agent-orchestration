"""Reviewer agent node."""

import logging

from google.genai import types

from schema import AgentState
from utils import get_client, get_model_name

logger = logging.getLogger(__name__)


def reviewer_node(state: AgentState) -> dict:
    """Review the report and provide feedback or approve."""
    logger.info("Reviewing report...")
    client = get_client()
    model = get_model_name()

    prompt = f"User Query: {state['query']}\n\nReport:\n{state['final_report']}\n\nReview this report for accuracy, completeness, and citations. If it is excellent, write 'APPROVED'. Otherwise, provide specific constructive feedback for improvement."

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1),
    )

    feedback = str(response.text)
    return {"feedback": feedback}
