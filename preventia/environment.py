from __future__ import annotations

import os
from pathlib import Path


def env_file() -> Path:
    override = os.environ.get("PREVENTIA_ENV_FILE")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[1] / ".env"


def load_env_file(path: Path | None = None) -> None:
    path = path or env_file()
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
