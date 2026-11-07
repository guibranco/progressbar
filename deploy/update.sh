#!/usr/bin/env bash
#
# Redeploy ProgressBar: pull the branch, rebuild the image, restart the
# container and wait for /health. Safe to run repeatedly; this is what
# .github/workflows/deploy.yml runs over SSH.
#
# Run as the deploy user (owner of APP_DIR, member of the docker group).
#
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/progressbar/app}"
BRANCH="${BRANCH:-main}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:8099/health}"

cd "$APP_DIR"

echo "==> Pulling $BRANCH"
git fetch --prune origin "$BRANCH"
git pull --ff-only origin "$BRANCH"
echo "    now at $(git rev-parse --short HEAD): $(git log -1 --pretty=%s)"

echo "==> Rebuilding and restarting"
docker compose up -d --build --remove-orphans
docker image prune -f >/dev/null || true

echo "==> Waiting for $HEALTH_URL"
for _ in $(seq 1 20); do
  if curl -fsS --max-time 2 "$HEALTH_URL" >/dev/null 2>&1; then
    echo "    healthy"
    exit 0
  fi
  sleep 2
done

echo "!! health check failed; recent container logs:" >&2
docker compose logs --tail=50 >&2 || true
exit 1
