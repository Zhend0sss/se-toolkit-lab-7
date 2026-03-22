# `.env.bot.secret`

<h2>Table of contents</h2>

- [About `.env.bot.secret`](#about-envbotsecret)
- [`BOT_TOKEN`](#bot_token)
- [LMS backend connection](#lms-backend-connection)
  - [`LMS_API_BASE_URL`](#lms_api_base_url)
  - [`LMS_API_KEY`](#lms_api_key)
- [LLM API](#llm-api)
  - [`LLM_API_KEY`](#llm_api_key)
  - [`LLM_API_BASE_URL`](#llm_api_base_url)
  - [`LLM_API_MODEL`](#llm_api_model)

## About `.env.bot.secret`

`.env.bot.secret` is a [`.env` file](./environments.md#env-file) that stores [environment variables](./environments.md#environment-variable) for the Telegram bot.

The values configure the bot token, the [LMS API](./lms-api.md#about-the-lms-api) connection, and the [LLM](./llm.md) that powers the bot.

Default values: [`.env.bot.example`](../.env.bot.example)

> [!NOTE]
> `.env.bot.secret` was added to [`.gitignore`](./git.md#gitignore) because you may specify there
> [secrets](./environments.md#secrets) such as the [`BOT_TOKEN`](#bot_token) or the [`LLM_API_KEY`](#llm_api_key).

## `BOT_TOKEN`

The Telegram bot token obtained from [`@BotFather`](https://core.telegram.org/bots#botfather).

Default: `<bot-token>`

## LMS backend connection

The bot calls these endpoints to communicate with the [LMS API](./lms-api.md#about-the-lms-api).

### `LMS_API_BASE_URL`

The [LMS API base URL](./lms-api.md#lms-api-base-url).

Default: `<lms-api-base-url>`

### `LMS_API_KEY`

The [LMS API key](./lms-api.md#lms-api-key).

Its value must match the value of [`LMS_API_KEY`](./dotenv-docker-secret.md#lms_api_key) in [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret) used for deployment.

Default: `my-secret-api-key`

## LLM API

Variables for the [LLM API](./llm-api.md#about-llm-api) that powers the bot.

### `LLM_API_KEY`

The [LLM API key](./llm-api.md#llm-api-key).

Default: `<llm-api-key>`

### `LLM_API_BASE_URL`

The [LLM API base URL](./llm-api.md#llm-api-base-url).

Default: `<llm-api-base-url>`

### `LLM_API_MODEL`

The [LLM API model](./llm-api.md#llm-api-model).

Default: `coder-model`
