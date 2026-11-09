#!/usr/bin/env bash
#
# First-time setup of ProgressBar on a VM (tested on Ubuntu 24.04).
# Prerequisites: git, docker (+ compose plugin) and nginx already installed.
#
#   curl -fsSLO https://raw.githubusercontent.com/guibranco/progressbar/main/deploy/install.sh
#   less install.sh          # review what will run as root
#   sudo bash install.sh
#   # or, from a checkout:  sudo deploy/install.sh
#
# Environment overrides:
#   APP_DIR   where the repository is checked out   (default /opt/progressbar/app)
#   REPO_URL  git remote                            (default this repository)
#   BRANCH    branch to deploy                      (default main)
#   DOMAIN    public hostname for the NGINX vhost   (default progress-bar.xyz)
#   DEPLOY_USER  owner of APP_DIR, used by deploy/update.sh and CI (default: the sudo caller)
#
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/progressbar/app}"
REPO_URL="${REPO_URL:-https://github.com/guibranco/progressbar.git}"
BRANCH="${BRANCH:-main}"
DOMAIN="${DOMAIN:-progress-bar.xyz}"
DEPLOY_USER="${DEPLOY_USER:-${SUDO_USER:-root}}"

log() { printf '\n==> %s\n' "$*"; }
need() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || { echo "missing required command: $cmd" >&2; exit 1; }
}

[[ "$(id -u)" -eq 0 ]] || { echo "run as root (sudo)" >&2; exit 1; }
[[ "$DOMAIN" =~ ^[A-Za-z0-9.-]+$ ]] || { echo "invalid DOMAIN: $DOMAIN" >&2; exit 1; }
[[ "$APP_DIR" =~ ^/[A-Za-z0-9._/-]+$ ]] || { echo "invalid APP_DIR: $APP_DIR" >&2; exit 1; }
need git; need docker; need nginx; need curl
docker compose version >/dev/null 2>&1 || { echo "missing: docker compose plugin" >&2; exit 1; }

log "Checking out $REPO_URL ($BRANCH) into $APP_DIR"
if [[ ! -d "$APP_DIR/.git" ]]; then
  mkdir -p "$(dirname "$APP_DIR")"
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi
cd "$APP_DIR"
# On a re-run the checkout already belongs to DEPLOY_USER; trust it before
# root touches it, or git refuses with "dubious ownership".
git config --global --add safe.directory "$APP_DIR" >/dev/null 2>&1 || true
git pull --ff-only origin "$BRANCH"
[[ -f deploy/env ]] || cp deploy/env.example deploy/env
chown -R "$DEPLOY_USER": "$APP_DIR"

log "Installing NGINX vhost for $DOMAIN"
install -m 0644 deploy/nginx/progressbar-cache.conf /etc/nginx/conf.d/progressbar-cache.conf
sed "s/progress-bar\.xyz/$DOMAIN/g" deploy/nginx/progress-bar.xyz.conf > "/etc/nginx/sites-available/$DOMAIN"
ln -sfn "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"
# The proxy_cache_path directory is created (and chowned to the worker user)
# by the NGINX master process on `nginx -t` / reload; no mkdir needed here.
nginx -t
systemctl reload nginx

log "Building and starting the container"
docker compose up -d --build --remove-orphans

log "Registering the systemd unit"
sed "s#/opt/progressbar/app#$APP_DIR#g" deploy/systemd/progressbar.service > /etc/systemd/system/progressbar.service
chmod 0644 /etc/systemd/system/progressbar.service
systemctl daemon-reload
systemctl enable --now progressbar.service

log "Smoke test"
for _ in $(seq 1 15); do
  if curl -fsS --max-time 2 http://127.0.0.1:8099/health >/dev/null; then break; fi
  sleep 2
done
curl -fsS --max-time 2 http://127.0.0.1:8099/health; echo
curl -fsS --max-time 5 -o /dev/null -w 'badge via nginx: HTTP %{http_code}\n' \
  -H "Host: $DOMAIN" "http://127.0.0.1/58/?title=installed"

cat <<EOF

Done. Next steps:
  1. TLS:  certbot --nginx -d $DOMAIN
  2. DNS:  point $DOMAIN at this host (ideally through a CDN/proxy such as Cloudflare)
  3. CI:   add the DEPLOY_SSH_* secrets and set the repository variable SELF_HOST_DEPLOY=true
           so .github/workflows/deploy.yml redeploys on every push to $BRANCH
           (the SSH user must own $APP_DIR and belong to the docker group: usermod -aG docker $DEPLOY_USER)
EOF
