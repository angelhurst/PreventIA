import re
from dataclasses import dataclass

E164 = re.compile(r"^\+[1-9]\d{7,14}$")


class ChannelError(RuntimeError):
    pass


class InvalidRecipient(ChannelError):
    pass


class ChannelNotConfigured(ChannelError):
    pass


@dataclass(frozen=True)
class Receipt:
    delivered: bool
    channel: str
    reference: str = ""
    detail: str = ""


def normalise_recipient(value):
    raw = (value or "").strip().replace(" ", "").replace("-", "")
    if raw and not raw.startswith("+"):
        raw = f"+{raw}"
    if not E164.match(raw):
        raise InvalidRecipient(
            "el numero debe venir en formato internacional, por ejemplo +56912345678"
        )
    return raw


from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
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


class UnknownSender(ChannelError):
    pass


class PatientDirectory(ABC):
    @abstractmethod
    def patient_id_for(self, channel_address): ...

    @abstractmethod
    def channel_address_for(self, patient_id): ...


class Channel(ABC):
    def __init__(self, handler):
        self._handler = handler

    @abstractmethod
    async def send(self, patient_id, message): ...

    async def receive(self, message):
        reply = await self._reply_to(message)
        await self.send(message.patient_id, reply)
        return reply

    async def _reply_to(self, message):
        if message.kind is not MessageKind.TEXT:
            return OutboundMessage(text=UNSUPPORTED_MEDIA_REPLY)
        return await self._handler(message)
