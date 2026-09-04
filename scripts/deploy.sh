#!/usr/bin/env bash
# Deploy Mindbattle to the VPS. Requires the `gfe` SSH alias and DNS for the
# configured domain before Caddy can obtain its TLS certificate.
set -euo pipefail

SSH_HOST="${DEPLOY_HOST:-gfe}"
APP_DIR="${APP_DIR:-/opt/mindbattle}"
DATA_DIR="/var/lib/mindbattle"
SERVICE="mindbattle.service"

echo "==> Building production bundle"
npm run build

echo "==> Syncing application to ${SSH_HOST}:${APP_DIR}"
rsync -az --delete \
  --exclude='.git' --exclude='.codex' --exclude='.agents' --exclude='node_modules' \
  --exclude='data' --exclude='playwright-report' --exclude='test-results' \
  ./ "${SSH_HOST}:${APP_DIR}/"

echo "==> Installing runtime and service"
ssh -o BatchMode=yes "${SSH_HOST}" "
  set -eu
  if ! id -u mindbattle >/dev/null 2>&1; then
    useradd --system --user-group --home-dir ${DATA_DIR} --shell /usr/sbin/nologin mindbattle
  fi
  install -d -o mindbattle -g mindbattle -m 750 ${DATA_DIR}
  chown -R root:root ${APP_DIR}
  cd ${APP_DIR}
  npm ci --omit=dev --ignore-scripts
  install -m 644 deploy/${SERVICE} /etc/systemd/system/${SERVICE}
  caddy_config_changed=0
  install -d -m 755 /etc/caddy/sites
  if ! cmp -s deploy/Caddyfile /etc/caddy/sites/mindbattle.caddy; then
    install -m 644 deploy/Caddyfile /etc/caddy/sites/mindbattle.caddy
    caddy_config_changed=1
  fi
  if ! grep -Fq 'import /etc/caddy/sites/*.caddy' /etc/caddy/Caddyfile; then
    printf '\n' >> /etc/caddy/Caddyfile
    printf 'import /etc/caddy/sites/*.caddy\n' >> /etc/caddy/Caddyfile
    caddy_config_changed=1
  fi
  if [ \"\$caddy_config_changed\" -eq 1 ]; then
    caddy validate --config /etc/caddy/Caddyfile
  fi
  systemctl daemon-reload
  systemctl enable ${SERVICE}
  systemctl restart ${SERVICE}
  systemctl is-active --quiet ${SERVICE}
  if [ \"\$caddy_config_changed\" -eq 1 ]; then
    systemctl restart caddy
  fi
  curl --fail --silent --show-error http://127.0.0.1:4173/api/difficulty-feedback/summary >/dev/null
"

echo "==> Done: https://mindbattle.afonasev.tech/"
