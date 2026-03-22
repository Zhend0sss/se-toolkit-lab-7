"""Telegram bot entry point with --test mode for offline testing.

Usage:
    uv run bot.py --test "/start"    # Test mode - prints response to stdout
    uv run bot.py                    # Normal mode - connects to Telegram
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)
from handlers.intent_router import handle_natural_language

# Telegram imports
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_handler(command: str):
    """Return the handler function for a given command."""
    handlers = {
        "/start": handle_start,
        "/help": handle_help,
        "/health": handle_health,
        "/labs": handle_labs,
        "/scores": handle_scores,
    }
    return handlers.get(command, handle_help)


def run_test_mode(command: str) -> None:
    """Run a command in test mode - print response to stdout."""
    # Parse command and extract arguments
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    # Check if it's a slash command or natural language
    if cmd.startswith("/"):
        handler = get_handler(cmd)
        if handler:
            response = handler(arg)
            print(response)
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)
    else:
        # Natural language query - use intent router
        full_message = f"{cmd} {arg}".strip()
        response = handle_natural_language(full_message)
        print(response)


async def start_command(message: types.Message) -> None:
    """Handle /start command from Telegram."""
    response = handle_start()
    
    # Create inline keyboard with common actions
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Check Health", callback_data="health")],
        [InlineKeyboardButton(text="📚 List Labs", callback_data="labs")],
        [InlineKeyboardButton(text="📈 Scores Lab 04", callback_data="scores_lab-04")],
        [InlineKeyboardButton(text="❓ Help", callback_data="help")],
    ])
    
    await message.answer(response, reply_markup=keyboard)


async def help_command(message: types.Message) -> None:
    """Handle /help command from Telegram."""
    response = handle_help()
    await message.answer(response)


async def health_command(message: types.Message) -> None:
    """Handle /health command from Telegram."""
    response = handle_health()
    await message.answer(response)


async def labs_command(message: types.Message) -> None:
    """Handle /labs command from Telegram."""
    response = handle_labs()
    await message.answer(response)


async def scores_command(message: types.Message) -> None:
    """Handle /scores command from Telegram."""
    # Extract lab name from command args
    lab_name = message.text.replace("/scores", "").strip()
    response = handle_scores(lab_name)
    await message.answer(response)


async def callback_query_handler(callback_query: types.CallbackQuery) -> None:
    """Handle inline keyboard button clicks."""
    data = callback_query.data
    
    if data == "health":
        response = handle_health()
    elif data == "labs":
        response = handle_labs()
    elif data.startswith("scores_"):
        lab = data.replace("scores_", "")
        response = handle_scores(lab)
    elif data == "help":
        response = handle_help()
    else:
        response = "Unknown action."
    
    await callback_query.message.answer(response)
    await callback_query.answer()


async def natural_language_handler(message: types.Message) -> None:
    """Handle natural language messages via LLM routing."""
    user_text = message.text or ""
    logger.info(f"Natural language query: {user_text}")
    
    try:
        response = handle_natural_language(user_text)
        await message.answer(response)
    except Exception as e:
        logger.error(f"Error in natural language handler: {e}")
        await message.answer("Sorry, I encountered an error processing your query. Please try again.")


async def echo_handler(message: types.Message) -> None:
    """Catch-all handler for unknown messages."""
    logger.info(f"Received message: {message.text}")
    await message.answer(f"Unknown command. Use /help for available commands.")


async def run_telegram_mode() -> None:
    """Run the bot in Telegram mode - connect to Telegram API."""
    if not Config.BOT_TOKEN:
        logger.error("BOT_TOKEN not found in .env.bot.secret")
        sys.exit(1)

    logger.info(f"Bot token configured: {bool(Config.BOT_TOKEN)}")
    logger.info(f"LMS API URL: {Config.LMS_API_URL}")

    # Initialize bot and dispatcher
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    # Register command handlers
    dp.message.register(start_command, CommandStart())
    dp.message.register(help_command, Command("help"))
    dp.message.register(health_command, Command("health"))
    dp.message.register(labs_command, Command("labs"))
    dp.message.register(scores_command, Command("scores"))
    # Callback query handler for inline buttons
    dp.callback_query.register(callback_query_handler)
    # Natural language handler (must be before catch-all)
    dp.message.register(natural_language_handler)
    # Catch-all handler for other messages
    dp.message.register(echo_handler)

    logger.info("Bot is starting...")
    await dp.start_polling(bot)


def main() -> None:
    """Main entry point."""
    import asyncio

    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        type=str,
        metavar="COMMAND",
        help="Test mode - run a command and print response to stdout"
    )

    args = parser.parse_args()

    if args.test:
        run_test_mode(args.test)
    else:
        asyncio.run(run_telegram_mode())


if __name__ == "__main__":
    main()
