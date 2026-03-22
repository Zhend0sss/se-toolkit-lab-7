"""Command handlers for the LMS bot.

Handlers are plain functions that take input and return text.
They don't depend on Telegram - same function works from --test mode,
unit tests, or the Telegram bot.
"""


def handle_start(user_input: str = "") -> str:
    """Handle /start command - welcome message."""
    return "Welcome to the LMS Bot! Use /help to see available commands."


def handle_help(user_input: str = "") -> str:
    """Handle /help command - list available commands."""
    return """Available commands:
/start - Welcome message
/help - Show this help
/health - Check backend status
/labs - List available labs
/scores <lab> - Show scores for a lab"""


def handle_health(user_input: str = "") -> str:
    """Handle /health command - check backend status."""
    return "Backend status: OK (placeholder)"


def handle_labs(user_input: str = "") -> str:
    """Handle /labs command - list available labs."""
    return "Available labs: lab-01, lab-02, lab-03, lab-04 (placeholder)"


def handle_scores(user_input: str = "") -> str:
    """Handle /scores command - show scores for a lab."""
    if user_input.strip():
        return f"Scores for {user_input}: Task 1: 80%, Task 2: 75% (placeholder)"
    return "Please specify a lab, e.g., /scores lab-01"
