# Bot Dockerfile
# Uses uv for dependency management (not pip/requirements.txt)

FROM python:3.14-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy pyproject.toml for dependency installation
COPY pyproject.toml ./

# Install dependencies using uv sync (generates lock if needed)
RUN uv sync --no-dev

# Copy the rest of the bot code
COPY . .

# Run the bot
CMD ["uv", "run", "python", "bot.py"]
