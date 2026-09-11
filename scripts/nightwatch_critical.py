#!/usr/bin/env python3
"""Night watchman: critical alerts only (deduped via state file).
Modes: critical | digest
Creds from environment (source monitoring.env first)."""
import os, ssl, json, sys, urllib.request
from datetime import datetime

TIMEOUT = 9
STATE_DIR = os.environ.get("STATE_DIR", "/var/lib/nightwatch")
ALARM_STATE = os.path.join(STATE_DIR, "alarms.json")
STORAGE_CRIT = float(os.environ.get("STORAGE_CRIT", 90.0))
UNIFI_DOWN = {"OFFLINE", "DISCONNECTED", "HEARTBEAT_MISSED"}

_CTX = ssl.create_default_context()
_CTX.check_hostname = False; _CTX.verify_mode = ssl.CERT_NONE

def http(url, headers=None, data=None, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, context=_CTX, timeout=timeout) as r:
        return r.status, r.read()

def poll_proxmox(full=False):
    """Poll all configured Proxmox nodes."""
    out = {}
    for tag in os.environ.get("PX_NODES", "NODE1,NODE2,NODE3").split(","):
        host = os.environ.get(f"PX_{tag}_HOST")
        tid = os.environ.get(f"PX_{tag}_TOKENID", "")
        tval = os.environ.get(f"PX_{tag}_TOKENVALUE", "")
        rec = {"host": host, "reachable": False}
        if not host: out[tag] = rec; continue
        hdr = {"Authorization": f"PVEAPIToken={tid}={tval}"}
        try:
            _, body = http(f"https://{host}:8006/api2/json/nodes", headers=hdr)
            rec["reachable"] = True
            rec["nodes"] = json.loads(body)["data"]
        except Exception as e:
            rec["error"] = repr(e)[:100]
        out[tag] = rec
    return out

def compute_alarms(px):
    a = {}
    for tag, rec in px.items():
        if not rec.get("reachable"):
            a[f"px:{tag}:down"] = f"Node {tag} unreachable ({rec.get('host')})"
            continue
        for node in rec.get("nodes", []):
            nm = node["node"]
            if node.get("status") != "online":
                a[f"px:{nm}:status"] = f"Node {nm} status: {node.get('status')}"
    return a

def load_state():
    try: return json.load(open(ALARM_STATE))
    except Exception: return {}

def save_state(d):
    os.makedirs(STATE_DIR, exist_ok=True)
    json.dump(d, open(ALARM_STATE, "w"))

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "critical"
    px = poll_proxmox()
    cur = compute_alarms(px)
    prev = load_state()
    save_state(cur)

    if mode == "critical":
        new = [k for k in cur if k not in prev]
        resolved = [k for k in prev if k not in cur]
        if not new and not resolved: return  # silent
        lines = []
        if new:
            lines.append(f"🔴 ALERT ({datetime.now():%H:%M})")
            lines += [f"🔴 {cur[k]}" for k in new]
        if resolved:
            lines.append(f"🟢 RESOLVED")
            lines += [f"🟢 {prev[k]}" for k in resolved]
        print("\n".join(lines))
    elif mode == "digest":
        print(f"🛡 Watchman summary — {datetime.now():%Y-%m-%d %H:%M}")
        if cur:
            print("⚠ Active alarms:")
            for v in cur.values(): print(f"  🔴 {v}")
        else:
            print("✅ All systems nominal")

if __name__ == "__main__":
    main()
