"""Utility functions for the research pipeline."""

import os

from google import genai


def get_client() -> genai.Client:
    """Initialize the Gemini client."""
    if not os.getenv("GEMINI_API_KEY") and os.getenv("GOOGLE_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]
    return genai.Client()


def get_model_name() -> str:
    """Get the model name from environment variables."""
    return os.getenv("MODEL_NAME", "gemini-2.5-flash")
