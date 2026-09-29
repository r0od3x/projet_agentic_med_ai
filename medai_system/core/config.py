"""Configuration centralisée — toutes les valeurs proviennent des variables d'environnement."""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


def get_llm(temperature: float) -> ChatOpenAI:
    """Retourne un client LLM configuré (clé API lue depuis OPENAI_API_KEY)."""
    return ChatOpenAI(model=OPENAI_MODEL, temperature=temperature)
