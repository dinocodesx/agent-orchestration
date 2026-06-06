"""Reviewer agent node - LLM-as-a-Judge."""

import logging

from google.genai import types

from schema import AgentState
from utils import get_client, get_model_name

logger = logging.getLogger(__name__)


def reviewer_node(state: AgentState) -> dict:
    """Review the report using structured evaluation metrics."""
    logger.info("Evaluating report quality (LLM-as-a-Judge)...")
    client = get_client()
    model = get_model_name()

    prompt = f"""
    User Query: {state["query"]}
    Report:
    {state["final_report"]}

    Evaluate the report based on these 3 industry-standard metrics:
    1. FAITHFULNESS: Are all claims backed by the research summary?
    2. RELEVANCY: Does it directly answer the user's query?
    3. STRUCTURE: Is the Markdown professional and well-cited?

    Provide a score (1-5) for each.
    If the total score is 13/15 or higher, start your response with 'APPROVED'.
    Otherwise, provide specific instructions for the Researcher to find missing information.
    """

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1),
    )

    feedback = str(response.text)
    return {"feedback": feedback}
