# `Telegram` bot

<h2>Table of contents</h2>

- [About `Telegram` bots](#about-telegram-bots)
- [Bot username](#bot-username)
- [Your bot username](#your-bot-username)
  - [`<your-bot-username>` placeholder](#your-bot-username-placeholder)
- [Create a `Telegram` bot](#create-a-telegram-bot)
- [Deploy the bot on the VM](#deploy-the-bot-on-the-vm)
  - [Enter the repository directory (REMOTE)](#enter-the-repository-directory-remote)
  - [Configure the environment (REMOTE)](#configure-the-environment-remote)
  - [Start the bot](#start-the-bot)
    - [Start the bot via `uv run python`](#start-the-bot-via-uv-run-python)
    - [Start the bot via `uv run poe`](#start-the-bot-via-uv-run-poe)
    - [Start the bot via `Docker Compose`](#start-the-bot-via-docker-compose)
  - [Check the bot](#check-the-bot)
    - [Check the bot via `uv run python`](#check-the-bot-via-uv-run-python)
    - [Check the bot via `uv run poe`](#check-the-bot-via-uv-run-poe)
    - [Check the bot in `Telegram`](#check-the-bot-in-telegram)

## About `Telegram` bots

A [`Telegram` bot](https://core.telegram.org/bots) is an automated program that runs inside the [`Telegram`](https://telegram.org/) messaging app.
Bots can respond to messages, answer queries, and interact with external services.

In this project, you build a `Telegram` bot that connects to the [LMS API](./lms-api.md#about-the-lms-api) to provide analytics and answer questions about the course data.

Docs:

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather](https://core.telegram.org/bots#botfather)

## Bot username

A unique name of the bot on `Telegram`.

Example: `@BotFather`

## Your bot username

The [username](#bot-username) of your bot.

### `<your-bot-username>` placeholder

[Your bot username](#your-bot-username) (without `<` and `>`).

## Create a `Telegram` bot

> [!NOTE]
> You need a [`Telegram`](https://telegram.org/) account to create a bot.

1. Open `Telegram` and search for [`@BotFather`](https://t.me/BotFather).

2. Send `/newbot`.

3. Choose a **name** for your bot (e.g., `My LMS Bot`).

4. Choose a [username for your bot](#your-bot-username).

   The username must end in `bot` (e.g., `my_lms_bot`).

5. `BotFather` will reply with a token like:

   ```text
   123456789:ABCdefGhIJKlmNoPQRsTUVwxyz
   ```

6. Save this token — you will need it for the [bot environment file](./dotenv-bot-secret.md#bot_token).

## Deploy the bot on the VM

1. [Connect to the VM as the user `admin` (LOCAL)](./vm-access.md#connect-to-the-vm-as-the-user-user-local).
2. [Install `uv` (REMOTE)](./python.md#install-uv).
3. [Enter the repository directory (REMOTE)](#enter-the-repository-directory-remote).
4. [Configure the environment (REMOTE)](#configure-the-environment-remote).
5. [Start the bot (REMOTE)](#start-the-bot).
6. [Check the bot (REMOTE)](#check-the-bot-via-uv-run-poe).
7. [Check the bot in `Telegram`](#check-the-bot-in-telegram).

### Enter the repository directory (REMOTE)

1. To enter the repository directory,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   cd ~/se-toolkit-lab-7
   ```

### Configure the environment (REMOTE)

1. To open [`.env.docker.secret`](./dotenv-bot-secret.md#about-envbotsecret) for editing,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   nano .env.bot.secret
   ```

2. [Set the variables in `.env.bot.secret`](./environments.md#set-the-variable-to-value-in-the-env-file-at-file-path):

   - [`BOT_TOKEN`](./dotenv-bot-secret.md#bot_token)
   - [`LMS_API_BASE_URL`](./dotenv-bot-secret.md#LMS_API_BASE_URL)
   - [`LMS_API_KEY`](./dotenv-bot-secret.md#lms_api_key)
   - [`LLM_API_KEY`](./dotenv-bot-secret.md#llm_api_key)
   - [`LLM_API_BASE_URL`](./dotenv-bot-secret.md#llm_api_base_url)
   - [`LLM_API_MODEL`](./dotenv-bot-secret.md#llm_api_model)

3. Save and close the file.

### Start the bot

<!-- no toc -->
- Method 1: [Start the bot via `uv run python`](#start-the-bot-via-uv-run-python)
- Method 2: [Start the bot via `uv run poe`](#start-the-bot-via-uv-run-poe)
- Method 3: [Start the bot via `Docker Compose`](#start-the-bot-via-docker-compose)

#### Start the bot via `uv run python`

1. To start the bot,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run --env-file .env.bot.secret python bot/bot.py
   ```

   See [`.env.bot.secret`](./dotenv-bot-secret.md).

#### Start the bot via `uv run poe`

1. To start the bot,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe bot
   ```

   This loads the environment variables from [`.env.bot.secret`](./dotenv-bot-secret.md) automatically.

#### Start the bot via `Docker Compose`

1. To start the bot,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   docker compose up --env-file .env.docker.secret bot --build -d
   ```

### Check the bot

- Method 1: [Check the bot via `uv run python`](#check-the-bot-via-uv-run-python)
- Method 2: [Check the bot via `uv run poe`](#check-the-bot-via-uv-run-poe)
- Method 3: [Check the bot in `Telegram`](#check-the-bot-in-telegram)

#### Check the bot via `uv run python`

1. To check that the bot is working,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run --env-file .env.bot.secret python bot/bot.py --test "/health"
   ```

   You should see a response from the bot.

#### Check the bot via `uv run poe`

1. To check that the bot is working,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   uv run poe bot-test "/health"
   ```

   This loads the environment variables from [`.env.bot.secret`](./dotenv-bot-secret.md) automatically.

   You should see a response from the bot.

#### Check the bot in `Telegram`

1. Open `Telegram`.

2. Find your bot by [your bot username](#your-bot-username).

3. Send `/health`.

   You should see a response from your bot.
