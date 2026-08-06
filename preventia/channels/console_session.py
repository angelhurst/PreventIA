from __future__ import annotations

import asyncio
import sys
from datetime import UTC, datetime
from itertools import count
from typing import TextIO

from preventia.channels.base import (
    Channel,
    CheckInHandler,
    InboundMessage,
    MessageKind,
    OutboundMessage,
)
from preventia.patient_copy import CONSOLE_FAREWELL, CONSOLE_GREETING

EXIT_WORDS = frozenset({"salir", "exit", "quit"})


class ConsoleSessionChannel(Channel):
    def __init__(
        self,
        handler: CheckInHandler,
        patient_id: str,
        stdin: TextIO | None = None,
        stdout: TextIO | None = None,
    ) -> None:
        super().__init__(handler)
        self._patient_id = patient_id
        self._stdin = stdin if stdin is not None else sys.stdin
        self._stdout = stdout if stdout is not None else sys.stdout
        self._sequence = count(1)

    async def send(self, patient_id: str, message: OutboundMessage) -> None:
        print(f"PreventIA > {message.text}", file=self._stdout, flush=True)

    async def run(self) -> None:
        print(CONSOLE_GREETING, file=self._stdout, flush=True)
        while True:
            line = await asyncio.to_thread(self._read_line)
            if line is None:
                break
            text = line.strip()
            if text.lower() in EXIT_WORDS:
                break
            if not text:
                continue
            await self.receive(self._inbound(text))
        print(CONSOLE_FAREWELL, file=self._stdout, flush=True)

    def _read_line(self) -> str | None:
        print(f"{self._patient_id} > ", end="", file=self._stdout, flush=True)
        line = self._stdin.readline()
        return line if line else None

    def _inbound(self, text: str) -> InboundMessage:
        return InboundMessage(
            patient_id=self._patient_id,
            kind=MessageKind.TEXT,
            text=text,
            channel_message_id=f"console-{next(self._sequence)}",
            received_at=datetime.now(UTC),
        )
