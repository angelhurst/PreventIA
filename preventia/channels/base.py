from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from preventia.patient_copy import UNSUPPORTED_MEDIA_REPLY


class MessageKind(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class InboundMessage:
    patient_id: str
    kind: MessageKind
    text: str
    channel_message_id: str
    received_at: datetime


@dataclass(frozen=True)
class OutboundMessage:
    text: str


CheckInHandler = Callable[[InboundMessage], Awaitable[OutboundMessage]]


class UnknownSender(Exception):
    pass


class PatientDirectory(ABC):
    @abstractmethod
    def patient_id_for(self, channel_address: str) -> str: ...

    @abstractmethod
    def channel_address_for(self, patient_id: str) -> str: ...


class Channel(ABC):
    def __init__(self, handler: CheckInHandler) -> None:
        self._handler = handler

    @abstractmethod
    async def send(self, patient_id: str, message: OutboundMessage) -> None: ...

    async def receive(self, message: InboundMessage) -> OutboundMessage:
        reply = await self._reply_to(message)
        await self.send(message.patient_id, reply)
        return reply

    async def _reply_to(self, message: InboundMessage) -> OutboundMessage:
        if message.kind is not MessageKind.TEXT:
            return OutboundMessage(text=UNSUPPORTED_MEDIA_REPLY)
        return await self._handler(message)
