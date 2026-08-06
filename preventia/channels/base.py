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
