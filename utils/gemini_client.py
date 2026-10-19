"""
Core Gemini API client module for DevHelper AI.
Uses the official google-genai Python SDK with robust error handling,
API key management, and token-efficient generation configs.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()

# We import google.genai inside functions or wrap in try/except
# so that if dependencies aren't yet installed, the module still imports cleanly.
try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    APIError = Exception  # Fallback for type annotation

from utils.prompts import (
    SYSTEM_ERROR_EXPLAINER,
    SYSTEM_COMMIT_GENERATOR,
    SYSTEM_REGEX_EXPLAINER,
    SYSTEM_SQL_EXPLAINER,
    format_error_prompt,
    format_commit_prompt,
    format_regex_prompt,
    format_sql_prompt,
)

# Recommended fast, cost-effective model
DEFAULT_MODEL = "gemini-3.8-flash"


class GeminiClientError(Exception):
    """Custom exception class for user-friendly error reporting."""
    pass


def get_active_api_key(explicit_key: Optional[str] = None) -> str:
    """
    Resolves the API key with priority:
    1. Explicit key passed from UI sidebar input
    2. GEMINI_API_KEY from environment variables (.env or OS)
    """
    key = explicit_key.strip() if explicit_key else ""
    if not key:
        key = os.getenv("GEMINI_API_KEY", "").strip()
    return key


def get_gemini_client(api_key: Optional[str] = None):
    """
    Initializes and returns an official Google GenAI client instance.
    Raises GeminiClientError if SDK is missing or key is not provided.
    """
    if not GENAI_AVAILABLE:
        raise GeminiClientError(
            "The `google-genai` package is not installed. "
            "Please run `pip install -r requirements.txt` to install dependencies."
        )

    resolved_key = get_active_api_key(api_key)
    if not resolved_key:
        raise GeminiClientError(
            "Gemini API Key is missing! Please enter your API key in the sidebar "
            "or set `GEMINI_API_KEY` in your `.env` file."
        )

    try:
        return genai.Client(api_key=resolved_key)
    except Exception as e:
        raise GeminiClientError(f"Failed to initialize Gemini Client: {str(e)}")


def generate_content(
    prompt: str,
    system_instruction: str,
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
) -> str:
    """
    Executes a structured, token-efficient completion request to the Gemini API.
    Handles quota limits, invalid keys, and network timeouts gracefully.
    """
    client = get_gemini_client(api_key)

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )

        if not response or not response.text:
            return "No response received from the Gemini model. Please check your input and try again."

        return response.text

    except APIError as api_err:
        err_msg = str(api_err)
        if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg:
            raise GeminiClientError("Rate limit / Quota exceeded. Please wait a moment before trying again.")
        elif "API_KEY_INVALID" in err_msg or "400" in err_msg and "key" in err_msg.lower():
            raise GeminiClientError("The provided Gemini API Key is invalid. Please verify it in Google AI Studio.")
        else:
            raise GeminiClientError(f"Gemini API Error: {err_msg}")
    except Exception as e:
        raise GeminiClientError(f"Unexpected error while communicating with Gemini API: {str(e)}")


# -------------------------------------------------------------
# Tool-Specific Helper Functions
# -------------------------------------------------------------

def explain_python_error(
    traceback_text: str,
    code_snippet: str = "",
    api_key: Optional[str] = None,
) -> str:
    """Generates plain-English explanation and code fix for Python errors."""
    prompt = format_error_prompt(traceback_text, code_snippet)
    return generate_content(
        prompt=prompt,
        system_instruction=SYSTEM_ERROR_EXPLAINER,
        api_key=api_key,
        temperature=0.2,
    )


def generate_git_commit(
    description: str,
    scope: str = "",
    api_key: Optional[str] = None,
) -> str:
    """Generates standard Conventional Commit messages from casual descriptions."""
    prompt = format_commit_prompt(description, scope)
    return generate_content(
        prompt=prompt,
        system_instruction=SYSTEM_COMMIT_GENERATOR,
        api_key=api_key,
        temperature=0.3,
    )


def explain_regex_pattern(
    regex_pattern: str,
    flags: str = "",
    api_key: Optional[str] = None,
) -> str:
    """Explains a regular expression token-by-token with test cases."""
    prompt = format_regex_prompt(regex_pattern, flags)
    return generate_content(
        prompt=prompt,
        system_instruction=SYSTEM_REGEX_EXPLAINER,
        api_key=api_key,
        temperature=0.1,
    )


def explain_sql_query(
    sql_query: str,
    dialect: str = "Standard SQL",
    api_key: Optional[str] = None,
) -> str:
    """Explains a SQL query in plain English with clause breakdowns."""
    prompt = format_sql_prompt(sql_query, dialect)
    return generate_content(
        prompt=prompt,
        system_instruction=SYSTEM_SQL_EXPLAINER,
        api_key=api_key,
        temperature=0.2,
    )
