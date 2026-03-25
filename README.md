# refbotka

Telegram bot for [refinance](https://github.com/F0RTHSP4CE/refinance).

## Commands

| Command | Description |
|---|---|
| `/transfer @user 100 GEL [comment]` | Send money (creates a draft you confirm) |
| `/request @user 50 GEL [comment]` | Request money from someone |
| `/balance [@user]` | Show balance and pending invoices |
| `/deposit 10 GEL` | Top up via Keepz |
| `/transactions` | Last 10 transactions |
| `/split 150 GEL @user [comment]` | Create an expense split |
| `/split_join [id] [amount]` | Join a split (reply to card or provide id) |
| `/split_add [id] @user [amount]` | Add someone to a split |
| `/split_leave [id] [@user]` | Leave a split |
| `/splits` | List open splits |

## Setup

```bash
cp .env.example .env
# fill in .env
uv sync
uv run refbotka
```

## Configuration

| Variable | Description |
|---|---|
| `REFBOTKA_BOT_TOKEN` | Telegram bot token |
| `REFBOTKA_REFINANCE_API_URL` | Refinance API base URL |
| `REFBOTKA_REFINANCE_SECRET_KEY` | Shared secret for JWT auth with refinance API |
| `REFBOTKA_REFINANCE_BOT_ENTITY_ID` | Refinance entity ID for the bot |
| `REFBOTKA_DATABASE_URL` | SQLite (default) or PostgreSQL |
| `REFBOTKA_BOOTSTRAP_RESIDENT_IDS` | Comma-separated Telegram IDs granted resident tier |

## Docker

```bash
docker build -t refbotka .
docker run --env-file .env -v /data:/data refbotka
```

## How it works

Refbotka imports its finance handlers directly from [botka](https://github.com/mintyleaf/botka) (`python-version-splits` branch) — no code is duplicated. All finance state lives in the refinance API; the local SQLite DB only stores the user registry for `@username` → entity resolution.
