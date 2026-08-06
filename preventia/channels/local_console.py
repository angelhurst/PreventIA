import os
from datetime import datetime, timezone
from pathlib import Path

from .base import Receipt, normalise_recipient

DEFAULT_OUTBOX = Path("agent_sessions") / "outbox.log"


class LocalConsoleChannel:
    name = "console"

    def __init__(self, outbox=None):
        self.outbox = Path(os.environ.get("PREVENTIA_OUTBOX", outbox or DEFAULT_OUTBOX))

    def send(self, recipient, text):
        to = normalise_recipient(recipient)
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

        self.outbox.parent.mkdir(parents=True, exist_ok=True)
        with self.outbox.open("a", encoding="utf-8") as handle:
            handle.write(f"[{stamp}] -> {to}\n{text}\n\n")

        return Receipt(
            delivered=True,
            channel=self.name,
            reference=f"console-{stamp}",
            detail=f"escrito en {self.outbox}",
        )
