"""Shared factory for Gemini LLMs."""

from __future__ import annotations

import logging
from typing import Any, Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from packages.infrastructure.config.config import get_settings
from google import genai
from google.genai import types


_LOGGER = logging.getLogger(__name__)


def _build_api_version_kwargs() -> Dict[str, Any]:
    settings = get_settings()
    api_version = getattr(settings, "google_api_version", None)
    if not api_version:
        return {}

    fields = getattr(ChatGoogleGenerativeAI, "model_fields", {}) or {}
    if "client" in fields:
        client = genai.Client(
            api_key=settings.google_api_key,
            http_options=types.HttpOptions(api_version=api_version),
        )
        return {"client": client}
    if "google_api_version" in fields:
        return {"google_api_version": api_version}
    if "api_version" in fields:
        return {"api_version": api_version}

    _LOGGER.warning(
        "GOOGLE_API_VERSION is set but not supported by langchain_google_genai; ignoring."
    )
    return {}


def create_gemini_llm(
    *,
    temperature: float,
    max_output_tokens: int,
    **kwargs: Any,
) -> ChatGoogleGenerativeAI:
    """Create a Gemini LLM with shared settings and optional API versioning."""
    settings = get_settings()
    init_kwargs: Dict[str, Any] = {
        "model": settings.gemini_model,
        "api_key": settings.google_api_key,
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }
    init_kwargs.update(kwargs)

    init_kwargs.update(_build_api_version_kwargs())
    return ChatGoogleGenerativeAI(**init_kwargs)
