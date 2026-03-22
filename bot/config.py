"""Configuration loader for the bot.

Reads environment variables from .env.bot.secret file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Find the .env.bot.secret file in the project root
ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR / ".env.bot.secret"

# Load environment variables from the file
load_dotenv(ENV_FILE)


class Config:
    """Bot configuration loaded from environment variables."""

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    LMS_API_URL: str = os.getenv("LMS_API_URL", "http://localhost:42002")
    LMS_API_KEY: str = os.getenv("LMS_API_KEY", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_API_BASE: str = os.getenv("LLM_API_BASE", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "")
