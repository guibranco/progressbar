"""Gunicorn configuration for self-hosted deployments (Docker or bare metal)."""

# Vercel ignores this file: there the app is served by the @vercel/python
# runtime. Every value can be overridden with an environment variable so the
# same image/unit works on a 1 vCPU / 1 GB VM and on something bigger.
#
# Usage:
#     gunicorn -c gunicorn.conf.py app:app

import os


def _env_int(name, default):
  raw = os.environ.get(name)
  if raw is None or raw.strip() == "":
    return default
  try:
    return int(raw)
  except ValueError:
    return default


# Bind to loopback by default: a reverse proxy (NGINX) terminates TLS and
# caches responses in front of gunicorn. Docker overrides this to 0.0.0.0.
bind = os.environ.get("PROGRESSBAR_BIND", "127.0.0.1:8099")

# Threaded workers: /dynamic/json/ performs outbound HTTP fetches (up to 8s),
# and with plain sync workers a handful of slow upstreams would block the
# cheap /<n>/ route as well. 2 workers x 8 threads is plenty for a small VM
# (~45 MB RSS per worker).
workers = _env_int("PROGRESSBAR_WORKERS", 2)
worker_class = "gthread"
threads = _env_int("PROGRESSBAR_THREADS", 8)

# Longer than the 8s JSON fetch timeout plus rendering, shorter than the
# NGINX proxy_read_timeout (15s) so the proxy sees a clean error, not a hang.
timeout = _env_int("PROGRESSBAR_TIMEOUT", 12)
graceful_timeout = 10
keepalive = 5

# Recycle workers periodically to keep memory flat on long-running hosts.
max_requests = 5000
max_requests_jitter = 500

# NGINX (or the platform) already writes an access log; keep gunicorn quiet
# unless explicitly asked for (PROGRESSBAR_ACCESS_LOG=- logs to stdout).
accesslog = os.environ.get("PROGRESSBAR_ACCESS_LOG") or None
errorlog = "-"
loglevel = os.environ.get("PROGRESSBAR_LOG_LEVEL", "warning")

# Trust X-Forwarded-* only from the local reverse proxy / docker network.
forwarded_allow_ips = os.environ.get("PROGRESSBAR_FORWARDED_ALLOW_IPS", "127.0.0.1")
