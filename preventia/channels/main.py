from __future__ import annotations

import asyncio
import os
from pathlib import Path

import uvicorn

from preventia.agent.core import run_check_in
from preventia.agent.models import ModelUnavailable
from preventia.channels.base import InboundMessage, OutboundMessage
from preventia.channels.webhook import build_app
from preventia.channels.whatsapp_webhook import (
    StaticPatientDirectory,
    WhatsAppWebhookChannel,
    WhatsAppCredentials,
)
from preventia.dashboard.intake import connect, patient_for_agent, persist
from preventia.patient_copy import FALLBACK_ACKNOWLEDGEMENT

DEFAULT_PORT = 8080
DEFAULT_DB = Path(__file__).resolve().parents[1] / "data" / "preventia.db"


def webhook_port() -> int:
    return int(os.environ.get("PREVENTIA_WEBHOOK_PORT") or DEFAULT_PORT)


def database_path() -> Path:
    return Path(os.environ.get("PREVENTIA_DB") or DEFAULT_DB)


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


def check_in(message: InboundMessage) -> str:
    connection = connect(database_path())
    try:
        patient = patient_for_agent(connection, message.patient_id)
        if patient is None:
            return FALLBACK_ACKNOWLEDGEMENT
        try:
            result = run_check_in(patient, message.text)
        except ModelUnavailable:
            return FALLBACK_ACKNOWLEDGEMENT
        persist(connection, result)
        return result.agent_message
    finally:
        connection.close()


async def handle_check_in(message: InboundMessage) -> OutboundMessage:
    return OutboundMessage(text=await asyncio.to_thread(check_in, message))


def build_channel() -> WhatsAppWebhookChannel:
    return WhatsAppWebhookChannel(
        handle_check_in,
        WhatsAppCredentials.from_environment(),
        StaticPatientDirectory.from_environment(),
    )


def main() -> None:
    load_env_file()
    uvicorn.run(build_app(build_channel()), host="127.0.0.1", port=webhook_port())


if __name__ == "__main__":
    main()
