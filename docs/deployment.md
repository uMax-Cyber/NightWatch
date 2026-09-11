# Night Watchman Deployment

## Cron Setup

```bash
# Critical watcher (every 5 minutes)
*/5 * * * * /opt/nightwatch/scripts/nightwatch_critical.sh 2>/dev/null

# Daily digest (08:00)
0 8 * * * /opt/nightwatch/scripts/nightwatch_digest.sh 2>/dev/null

# Weekly security audit (Monday 09:00)
0 9 * * 1 /opt/nightwatch/scripts/secaudit.sh 2>/dev/null
```

## Wrapper Script Pattern

```bash
#!/usr/bin/env bash
# nightwatch_critical.sh — wrapper that sources creds and pipes to alerting
set -a
. /etc/nightwatch/monitoring.env
set +a
exec python3 /opt/nightwatch/scripts/nightwatch_critical.py critical
```

The wrapper sources credentials from a separate env file (600 permissions),
then execs the Python poller. Cron delivers stdout to your alerting channel
(Telegram via agent gateway, email, Slack webhook — your choice).

## State File
The dedup state file (`alarms.json`) tracks active alarm keys. Each run:
- New keys → 🔴 alert
- Gone keys → 🟢 resolved
- Unchanged keys → silent

This prevents alert fatigue while ensuring state transitions are always reported.
