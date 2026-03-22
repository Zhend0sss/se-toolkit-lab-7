"""Command handlers for the LMS bot.

Handlers use the LMS client to fetch real data from the backend.
"""

from services.lms_client import LMSClient
from config import Config


def get_lms_client() -> LMSClient:
    """Create LMS client from config."""
    return LMSClient(
        base_url=Config.LMS_API_URL,
        api_key=Config.LMS_API_KEY,
    )


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
    client = get_lms_client()
    result = client.health_check()
    client.close()
    return result["message"]


def handle_labs(user_input: str = "") -> str:
    """Handle /labs command - list available labs."""
    client = get_lms_client()
    labs = client.get_labs()
    client.close()
    
    if not labs:
        return "No labs available or backend is unreachable."
    
    lines = ["Available labs:"]
    for lab in labs:
        title = lab.get("title", "Unknown")
        lines.append(f"- {title}")
    
    return "\n".join(lines)


def handle_scores(user_input: str = "") -> str:
    """Handle /scores command - show scores for a lab."""
    if not user_input.strip():
        return "Please specify a lab, e.g., /scores lab-04"
    
    client = get_lms_client()
    result = client.get_pass_rates(user_input.strip())
    client.close()
    
    if not result["success"]:
        return f"Error: {result['error']}"
    
    data = result.get("data", [])
    if not data:
        return f"No pass rate data available for {user_input}."
    
    lines = [f"Pass rates for {user_input}:"]
    for item in data:
        task_name = item.get("task_title", item.get("title", "Unknown"))
        rate = item.get("pass_rate", 0)
        attempts = item.get("attempts", 0)
        lines.append(f"- {task_name}: {rate:.1f}% ({attempts} attempts)")
    
    return "\n".join(lines)
