# AI Night Watchman
[![CI](https://github.com/uMax-Cyber/NightWatch/actions/workflows/ci.yml/badge.svg)](https://github.com/uMax-Cyber/NightWatch/actions/workflows/ci.yml)

Deterministic (no-LLM) infrastructure monitoring daemon: Proxmox nodes, network controllers, firewalls, and services. Critical alerts within 5 minutes, daily digest, weekly security audit. Runs as cron jobs — survives AI model outages.

## Why Deterministic?

AI agents are powerful but unreliable when the LLM provider is down or hallucinating. The Night Watchman is **pure Python, stdlib only** — it monitors even when the AI is offline. It's the safety net beneath the AI layer.

## Monitors

| Check | Interval | Alert Condition |
|-------|----------|----------------|
| Node reachability | 5 min | API timeout or status ≠ online |
| Storage usage | 5 min | > 90% used |
| Device states (network) | 5 min | Any device offline/disconnected |
| Gateway liveness | 5 min | API unreachable or auth failure |
| SSH brute-force | weekly | > 20 failed attempts/week |
| Package updates | weekly | > 100 pending |
| Backup freshness | weekly | No recent backup files |
| Port anomalies | weekly | Listening port count changed |

## Architecture

```
┌────────────┐    5 min    ┌──────────────┐    Telegram
│   cron     │──▶│ nightwatch.py│────────▶ │  alerts  │
└────────────┘             └──────────────┘           │
┌────────────┐   weekly    ┌──────────────┐           │
│   cron     │──▶│  secaudit.py │────────▶ │  report │
└────────────┘             └──────────────┘           ▼
```

## Key Design Decisions

1. **Stdlib only** — no pip dependencies, runs on any Python 3.10+
2. **State file for dedup** — alerts fire once on state change, not every poll
3. **Two output modes**: `critical` (only new/resolved alerts) and `digest` (full summary)
4. **Cron + --no-agent** — script stdout goes directly to Telegram, no LLM in the loop

## Usage

```bash
# Critical alerts (every 5 minutes via cron)
./scripts/nightwatch.py critical

# Daily digest (08:00 via cron)
./scripts/nightwatch.py digest

# Weekly security audit (Monday 09:00)
./scripts/secaudit.py
```

## License
MIT
