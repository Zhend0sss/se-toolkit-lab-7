# `Telegram` bot

<h2>Table of contents</h2>

- [About `Telegram` bots](#about-telegram-bots)
- [Create a `Telegram` bot](#create-a-telegram-bot)
- [Set up the bot environment](#set-up-the-bot-environment)

## About `Telegram` bots

A [`Telegram` bot](https://core.telegram.org/bots) is an automated program that runs inside the [`Telegram`](https://telegram.org/) messaging app.
Bots can respond to messages, answer queries, and interact with external services.

In this project, you build a `Telegram` bot that connects to the [LMS API](./lms-api.md#about-the-lms-api) to provide analytics and answer questions about the course data.

Docs:

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather](https://core.telegram.org/bots#botfather)

## Create a `Telegram` bot

> [!NOTE]
> You need a [`Telegram`](https://telegram.org/) account to create a bot.

1. Open `Telegram` and search for [`@BotFather`](https://t.me/BotFather).

2. Send `/newbot`.

3. Choose a **name** for your bot (e.g., `My LMS Bot`).

4. Choose a **username** for your bot.

   The username must end in `bot` (e.g., `my_lms_bot`).

5. `BotFather` will reply with a token like:

   ```text
   123456789:ABCdefGhIJKlmNoPQRsTUVwxyz
   ```

6. Save this token — you will need it for the [bot environment file](./dotenv-bot-secret.md#bot_token).

## Set up the bot environment

1. [Connect to the VM as the user `admin`](./vm-access.md#connect-to-the-vm-as-the-user-user-local).

2. Go to the project directory:

   ```terminal
   cd ~/se-toolkit-lab-7
   ```

3. Create the bot environment file:

   ```terminal
   cp .env.bot.example .env.bot.secret
   ```

4. Open the file for editing:

   ```terminal
   nano .env.bot.secret
   ```

5. Set the values.

   See [`.env.bot.secret`](./dotenv-bot-secret.md#about-envbotsecret) for a description of each variable.

   - [`BOT_TOKEN`](./dotenv-bot-secret.md#bot_token) — the token from [`@BotFather`](#create-a-telegram-bot).
   - [`LMS_API_URL`](./dotenv-bot-secret.md#lms_api_url) — the base URL of the [LMS API](./lms-api.md#about-the-lms-api).
   - [`LMS_API_KEY`](./dotenv-bot-secret.md#lms_api_key) — must match the value in [`.env.docker.secret`](./dotenv-docker-secret.md#lms_api_key).
   - [`LLM_API_KEY`](./dotenv-bot-secret.md#llm_api_key) — the key for your [LLM provider API](./llm.md#llm-provider-api).
   - [`LLM_API_BASE_URL`](./dotenv-bot-secret.md#llm_api_base_url) — the LLM API endpoint.
   - [`LLM_API_MODEL`](./dotenv-bot-secret.md#llm_api_model) — the model name.

6. Save and close the file.
