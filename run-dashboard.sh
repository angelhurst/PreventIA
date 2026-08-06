#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

HOST="${PREVENTIA_HOST:-127.0.0.1}"
PORT="${PREVENTIA_PORT:-8000}"

if [ ! -f preventia/data/preventia.db ]; then
  echo "No clinical record found. Seeding the synthetic cohort."
  python -m preventia.data.seed_cohort
fi

echo "Triage queue on http://${HOST}:${PORT}/cola"
exec python -m uvicorn preventia.dashboard.app:app --host "${HOST}" --port "${PORT}" --reload
