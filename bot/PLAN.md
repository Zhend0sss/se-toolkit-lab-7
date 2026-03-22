# LMS Telegram Bot — Development Plan

This document outlines the approach for building a Telegram bot that lets users interact with the LMS backend through chat. The bot supports slash commands like `/health` and `/labs`, and uses an LLM to understand plain text questions.

## Task 1: Plan and Scaffold

**Goal:** Create project structure with testable handler architecture.

**Approach:**
- Create `bot/` directory with `bot.py` as entry point
- Implement `--test` mode that calls handlers directly without Telegram
- Separate handlers into `bot/handlers/` module (no Telegram dependency)
- Add `config.py` for environment variable loading from `.env.bot.secret`
- Create `pyproject.toml` with dependencies: `aiogram`, `httpx`, `python-dotenv`

**Key pattern:** Handlers are plain functions that take input and return text. Same function works from `--test` mode, unit tests, or Telegram. This is **separation of concerns**.

## Task 2: Backend Integration

**Goal:** Connect handlers to the LMS backend for real data.

**Approach:**
- Create `bot/services/lms_client.py` — HTTP client for the LMS API
- Implement Bearer token authentication using `LMS_API_KEY`
- Update handlers to call real endpoints:
  - `/health` → `GET /health` on backend
  - `/labs` → `GET /items` filtered by type
  - `/scores <lab>` → `GET /analytics/{lab_id}`
- Handle errors gracefully (backend down, auth failure, timeouts)

**Key pattern:** API client encapsulates HTTP details. Handlers call client methods, not raw HTTP. URLs and keys come from environment variables — never hardcoded.

## Task 3: Intent-Based Natural Language Routing

**Goal:** Let users ask questions in plain text, routed by an LLM.

**Approach:**
- Create `bot/services/llm_client.py` — client for LLM API (OpenRouter)
- Define tool descriptions for each backend endpoint
- Implement intent router: LLM receives user message + tool descriptions, returns which tool to call
- Add fallback: if LLM is unavailable, respond with friendly error
- Wire up: non-slash messages go through LLM, slash commands go to direct handlers

**Key pattern:** LLM tool use. The LLM reads tool descriptions to decide which to call. Description quality matters more than prompt engineering. This is the same pattern from Lab 6, but inside a Telegram bot.

## Task 4: Containerize and Deploy

**Goal:** Deploy bot alongside backend on the VM using Docker Compose.

**Approach:**
- Create `bot/Dockerfile` — Python base image, copy bot code, install dependencies
- Add bot service to `docker-compose.yml` with proper networking
- Configure environment variables via `.env.docker.secret`
- Document deployment in README
- Verify: bot responds in Telegram after deployment

**Key pattern:** Docker networking. Containers use service names (e.g., `backend`), not `localhost`. Environment variables inject secrets at runtime.

## Testing Strategy

- **Unit tests:** Test handlers in isolation (pytest)
- **Test mode:** `--test` flag for manual testing without Telegram
- **Integration tests:** Test API client against running backend
- **Manual testing:** Send commands in Telegram after deployment

## Git Workflow

For each task:
1. Create issue describing the work
2. Create branch: `task-N-short-description`
3. Implement, test, commit
4. Create PR with "Closes #..." in description
5. Partner review, then merge
