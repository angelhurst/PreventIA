from __future__ import annotations

import os
from pathlib import Path

import uvicorn

from preventia.channels.base import InboundMessage, OutboundMessage
from preventia.channels.webhook import build_app
from preventia.channels.whatsapp_cloud import (
    StaticPatientDirectory,
    WhatsAppCloudChannel,
    WhatsAppCredentials,
)
from preventia.patient_copy import RECEIPT_ACKNOWLEDGEMENT

DEFAULT_PORT = 8080


def env_file() -> Path:
    override = os.environ.get("PREVENTIA_ENV_FILE")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[2] / ".env"


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


async def acknowledge(message: InboundMessage) -> OutboundMessage:
    return OutboundMessage(text=RECEIPT_ACKNOWLEDGEMENT)


def build_channel() -> WhatsAppCloudChannel:
    return WhatsAppCloudChannel(
        acknowledge,
        WhatsAppCredentials.from_environment(),
        StaticPatientDirectory.from_environment(),
    )


def main() -> None:
    load_env_file()
    port = int(os.environ.get("PREVENTIA_WEBHOOK_PORT", DEFAULT_PORT))
    uvicorn.run(build_app(build_channel()), host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
