# Flutter Web Chatbot

The Telegram bot works, but it lives inside Telegram — users need to install an app and find your bot. In this task, you build a web-based chatbot in Flutter that provides the same functionality, accessible directly from the LMS dashboard at the `/flutter` endpoint.

This is a replacement for the Telegram bot: same backend, same data, same LLM-powered intent routing — but as a web chat widget anyone can open in a browser.

## Requirements targeted

- **P4.1** Flutter web chatbot with a conversational UI
- **P4.2** Served through Caddy on `/flutter`
- **P4.3** Queries the LMS backend through the same endpoints
- **P4.4** LLM-powered intent routing (same as the Telegram bot)

## What you will build

A Flutter web app with a chat interface that connects to your LMS backend and LLM. Caddy serves the compiled Flutter build at `/flutter`, so users can open `http://<your-vm-ip-address>:42002/flutter` in a browser and start asking questions.

```
User opens /flutter in browser
  → types "which lab has the lowest pass rate?"
  → Flutter app sends message to LLM via /utils/qwen-code-api
  → LLM decides: call get_pass_rates for each lab
  → Flutter app calls backend endpoints directly
  → feeds results back to LLM
  → LLM summarizes
  → chat bubble with the answer appears
```

The chat UI should feel like a messaging app: message input at the bottom, conversation history scrolling up, user messages on one side, bot responses on the other.

## Commands and menu

The chatbot must support the same slash commands as the Telegram bot. When the user types a message starting with `/`, the app handles it directly — no LLM call needed:

| Command         | What it does                         |
| --------------- | ------------------------------------ |
| `/start`        | Welcome message with bot description |
| `/help`         | Lists all commands with descriptions |
| `/health`       | Calls backend, reports up/down       |
| `/labs`         | Lists available labs                 |
| `/scores <lab>` | Per-task pass rates for a lab        |

The app must show a **command menu** — a set of clickable buttons or chips visible in the UI so users can discover available actions without typing. For example, a row of buttons above the input field or a sidebar with common queries. Clicking a button sends the corresponding command or query into the chat.

Messages that don't start with `/` go through the LLM intent router, same as the Telegram bot.

## How it works

The Flutter chatbot runs entirely in the browser. It calls the backend API endpoints and the LLM proxy through Caddy — the same endpoints the Telegram bot uses, but from the client side:

| What             | Telegram bot                                              | Flutter chatbot                                       |
| ---------------- | --------------------------------------------------------- | ----------------------------------------------------- |
| Transport        | Telegram API                                              | Browser (Flutter web)                                 |
| Backend access   | `http://backend:8000` (Docker network)                    | `/items`, `/analytics/*` (via Caddy reverse proxy)    |
| LLM access       | `http://host.docker.internal:42005` (from Docker)         | `/utils/qwen-code-api` (via Caddy reverse proxy)      |
| Intent routing   | Server-side (bot calls LLM, executes tools, sends result) | Client-side (Flutter app calls LLM, executes tools)   |
| Hosting          | Docker container, always running                          | Static files served by Caddy, runs in user's browser  |

> [!NOTE]
> The LLM tool-calling loop runs in the Flutter app itself. The app sends the user's message and tool definitions to the LLM, receives tool call decisions, executes them against the backend API, feeds results back to the LLM, and displays the final answer. This is the same pattern as the Telegram bot's intent router — but implemented in Dart instead of Python.

## Backend endpoints

Same endpoints as the Telegram bot, all available through Caddy without the `Authorization` header (Caddy proxies to the backend directly):

| Endpoint                                         | Returns                        |
| ------------------------------------------------ | ------------------------------ |
| `GET /items/`                                    | Labs and tasks                 |
| `GET /learners/`                                 | Enrolled students              |
| `GET /analytics/scores?lab=lab-01`               | Score distribution (4 buckets) |
| `GET /analytics/pass-rates?lab=lab-01`           | Per-task averages              |
| `GET /analytics/timeline?lab=lab-01`             | Submissions per day            |
| `GET /analytics/groups?lab=lab-01`               | Per-group performance          |
| `GET /analytics/top-learners?lab=lab-01&limit=5` | Top N learners                 |
| `GET /analytics/completion-rate?lab=lab-01`      | Completion percentage          |
| `POST /pipeline/sync`                            | Trigger ETL sync               |

The LLM proxy is available at `/utils/qwen-code-api/v1/chat/completions` through Caddy. Use the same tool definitions and system prompt as the Telegram bot — the only difference is the HTTP client (Dart's `http` package instead of Python's `httpx`).

## Deliverables

### 1. Flutter web app (`flutter_chatbot/`)

A Flutter project inside the repo with a chat UI. The app must:

- Display a chat interface with message bubbles (user vs. bot)
- Show a command menu (buttons or chips) for quick access to common commands
- Handle `/start`, `/help`, `/health`, `/labs`, `/scores <lab>` directly (no LLM)
- Route plain text messages through the LLM with tool definitions
- Execute the LLM's tool calls against the backend API
- Feed tool results back to the LLM and display the final answer
- Handle errors gracefully (backend down, LLM errors)

The project structure:

```
se-toolkit-lab-7/
├── flutter_chatbot/         ← NEW
│   ├── lib/
│   │   ├── main.dart        ← entry point
│   │   ├── chat_screen.dart ← chat UI
│   │   ├── llm_service.dart ← LLM API client + tool calling loop
│   │   └── lms_service.dart ← backend API client
│   ├── web/                 ← Flutter web assets
│   ├── pubspec.yaml         ← dependencies
│   └── ...
├── bot/                     ← existing Telegram bot
├── backend/                 ← existing
└── docker-compose.yml       ← existing
```

> [!TIP]
> Use your coding agent to scaffold the Flutter project. Give it the tool definitions from the Telegram bot and ask it to implement the same intent routing pattern in Dart.

### 2. Compiled web build

Build the Flutter app for web and place the output where Caddy can serve it:

```terminal
cd flutter_chatbot
flutter build web --base-href /flutter/
```

The build output goes to `flutter_chatbot/build/web/`. Caddy serves these static files at `/flutter`.

### 3. Caddy configuration (`caddy/Caddyfile`)

Add a route to serve the Flutter build at `/flutter`:

```
handle_path /flutter* {
    root * /srv/flutter
    try_files {path} /index.html
    file_server
}
```

### 4. Docker integration

Update the Caddy service in `docker-compose.yml` to mount the Flutter build directory:

```yaml
caddy:
  volumes:
    - ./caddy/Caddyfile:/etc/caddy/Caddyfile
    - ./flutter_chatbot/build/web:/srv/flutter  # ← NEW
```

Alternatively, add a build stage to the Caddy Dockerfile that compiles Flutter and copies the output. Either approach works — the result must be that `/flutter` serves the app.

## Verify

### Build the Flutter app

On your VM (or locally), install Flutter and build:

```terminal
cd ~/se-toolkit-lab-7/flutter_chatbot
flutter build web --base-href /flutter/
```

If you don't have Flutter installed on the VM, build locally and commit the `build/web/` output, or add a Docker build stage.

### Update Caddy and restart

```terminal
cd ~/se-toolkit-lab-7
docker compose --env-file .env.docker.secret up --build -d
```

### Verify in the browser

Open `http://<your-vm-ip-address>:42002/flutter` in your browser. You should see the chat interface.

**What to check:**

1. The page loads without errors (no blank screen, no 404)
2. A command menu is visible (buttons or chips for common actions)
3. Click a menu button — the corresponding command runs and a response appears
4. Type `/health` — the bot reports backend status
5. Type `/labs` — the bot lists available labs
6. Type `/scores lab-04` — the bot shows per-task pass rates
7. Type "what labs are available?" — the LLM routes the query and responds with lab data
8. Type "which lab has the lowest pass rate?" — the bot chains multiple API calls and names a specific lab
9. Type "hello" — the bot responds with a greeting, not an error

### Common problems

| Symptom                           | Likely cause                                                                                                                                                               |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 404 at `/flutter`                 | Caddy route missing or Flutter build not mounted. Check `Caddyfile` and `docker-compose.yml` volumes.                                                                      |
| Blank page, console errors        | `--base-href` not set to `/flutter/` during build. Rebuild with `flutter build web --base-href /flutter/`.                                                                 |
| CORS errors in browser console    | Backend or LLM proxy rejecting cross-origin requests. Since everything goes through Caddy, this shouldn't happen — check that you're using relative URLs, not `localhost`. |
| LLM calls fail                    | Check that `/utils/qwen-code-api` is proxied in `Caddyfile`. The Flutter app must call this path, not `localhost:42005`.                                                   |
| "XMLHttpRequest error" in Flutter | Flutter web uses `dart:html` for HTTP. Make sure you're using the `http` package, not `dart:io`.                                                                           |

## Acceptance criteria

### On `GitHub`

- [ ] [`Git workflow`](../../../wiki/git-workflow.md) followed (issue, branch, PR, review, merge).

### On `GitHub` on the `main` branch

- [ ] `flutter_chatbot/` directory with a Flutter project exists.
- [ ] `flutter_chatbot/pubspec.yaml` exists.
- [ ] `caddy/Caddyfile` includes a `/flutter` route.
- [ ] Source code contains LLM tool definitions (at least 5 tool schemas).
- [ ] Source code contains a command menu (buttons, chips, or equivalent UI element).

### On the VM (REMOTE)

- [ ] `curl -sf http://localhost:42002/flutter/ | head -c 100` returns HTML (Flutter app loads).
- [ ] Backend still healthy (`curl -sf http://localhost:42002/docs` returns 200).
- [ ] Chat interface loads in browser at `http://<your-vm-ip-address>:42002/flutter`.
- [ ] Command menu is visible with clickable actions.
- [ ] `/health` returns backend status.
- [ ] `/labs` lists available labs.
- [ ] `/scores lab-04` shows per-task pass rates.
- [ ] Typing a natural language question returns a data-backed answer (TA-verified).
