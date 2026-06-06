"""Utility functions for the research pipeline."""

import logging
import os

from google import genai

logger = logging.getLogger(__name__)


def setup_observability():
    """Enable LangSmith tracing if API key is present."""
    if os.getenv("LANGSMITH_API_KEY"):
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_PROJECT"] = os.getenv(
            "LANGCHAIN_PROJECT", "agent-orchestration"
        )
        logger.info("LangSmith observability enabled.")


def get_client() -> genai.Client:
    """Initialize the Gemini client."""
    setup_observability()
    if not os.getenv("GEMINI_API_KEY") and os.getenv("GOOGLE_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]
    return genai.Client()


def get_model_name() -> str:
    """Get the model name from environment variables."""
    return os.getenv("MODEL_NAME", "gemini-2.5-flash")
