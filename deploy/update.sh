#!/usr/bin/env bash
#
# Redeploy ProgressBar: fetch the branch (or an exact commit), rebuild the
# image, restart the container and wait for /health. If the new container
# never becomes healthy, the previous image is restored. Safe to run
# repeatedly; this is what .github/workflows/deploy.yml runs over SSH.
#
# Run as the deploy user (owner of APP_DIR, member of the docker group).
#
# Environment:
#   APP_DIR     checkout directory              (default /opt/progressbar/app)
#   BRANCH      branch to deploy                (default main)
#   DEPLOY_SHA  optional exact commit to deploy; must be on origin/BRANCH
#   HEALTH_URL  liveness URL                    (default http://127.0.0.1:8099/health)
#
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/progressbar/app}"
BRANCH="${BRANCH:-main}"
DEPLOY_SHA="${DEPLOY_SHA:-}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:8099/health}"
IMAGE="progressbar:local"
PREVIOUS_IMAGE="progressbar:previous"

cd "$APP_DIR"

echo "==> Fetching origin/$BRANCH"
git fetch --prune origin "$BRANCH"
target="origin/$BRANCH"
if [[ -n "$DEPLOY_SHA" ]]; then
  git merge-base --is-ancestor "$DEPLOY_SHA" "origin/$BRANCH" \
    || { echo "!! $DEPLOY_SHA is not on origin/$BRANCH; refusing to deploy" >&2; exit 1; }
  target="$DEPLOY_SHA"
fi
git checkout -q "$BRANCH"
git reset -q --hard "$target"
echo "    now at $(git rev-parse --short HEAD): $(git log -1 --pretty=%s)"

healthy_now() {
  curl -fsS --max-time 2 "$HEALTH_URL" >/dev/null 2>&1
}

wait_healthy() {
  for _ in $(seq 1 20); do
    if healthy_now; then
      return 0
    fi
    sleep 2
  done
  return 1
}

# Restore the previous image (if there is one) and recreate the container.
rollback() {
  if ! docker image inspect "$PREVIOUS_IMAGE" >/dev/null 2>&1; then
    echo "!! no previous image to roll back to" >&2
    return 1
  fi
  echo "==> Rolling back to the previous image" >&2
  docker tag "$PREVIOUS_IMAGE" "$IMAGE"
  docker compose up -d --no-build --force-recreate --remove-orphans >&2 || true
  if wait_healthy; then
    echo "    rollback healthy (deployment of $(git rev-parse --short HEAD) FAILED)" >&2
  else
    echo "!! rollback is not healthy either" >&2
  fi
}

if docker image inspect "$IMAGE" >/dev/null 2>&1; then
  docker tag "$IMAGE" "$PREVIOUS_IMAGE"
fi

echo "==> Rebuilding and restarting"
if ! docker compose up -d --build --remove-orphans; then
  echo "!! docker compose up failed" >&2
  if healthy_now; then
    # The build failed before anything was replaced: the previous container is
    # still serving, so leave it alone.
    echo "    the previous container is still serving; nothing was replaced" >&2
  else
    # Compose already removed the old container but could not start the new
    # one: put the previous image back.
    rollback || true
  fi
  exit 1
fi

echo "==> Waiting for $HEALTH_URL"
if wait_healthy; then
  echo "    healthy"
  docker image prune -f >/dev/null || true
  exit 0
fi

echo "!! health check failed; recent container logs:" >&2
docker compose logs --tail=50 >&2 || true
rollback || true
exit 1
