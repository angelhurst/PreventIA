import os

from .base import (
    Channel,
    ChannelError,
    CheckInHandler,
    InboundMessage,
    MessageKind,
    OutboundMessage,
    PatientDirectory,
    Receipt,
    UnknownSender,
)
from .local_console import LocalConsoleChannel
from .whatsapp_cloud import WhatsAppCloudChannel

CONSOLE = "console"
WHATSAPP = "whatsapp"


def resolve_channel_name():
    return (os.environ.get("PREVENTIA_CHANNEL", CONSOLE) or CONSOLE).strip().lower()


def build_channel(name=None):
    chosen = (name or resolve_channel_name()).lower()
    if chosen == WHATSAPP:
        return WhatsAppCloudChannel()
    return LocalConsoleChannel()


def recipient_for_patient(patient_code):
    from .whatsapp_webhook import StaticPatientDirectory

    return StaticPatientDirectory.from_environment().channel_address_for(patient_code)


def has_recipient(patient_code):
    try:
        recipient_for_patient(patient_code)
    except UnknownSender:
        return False
    return True


def describe_channel():
    name = resolve_channel_name()
    if name == WHATSAPP:
        return {"name": WHATSAPP, "configured": WhatsAppCloudChannel.is_configured()}
    return {"name": CONSOLE, "configured": True}


__all__ = [
    "CONSOLE",
    "WHATSAPP",
    "Channel",
    "ChannelError",
    "CheckInHandler",
    "InboundMessage",
    "MessageKind",
    "OutboundMessage",
    "PatientDirectory",
    "Receipt",
    "UnknownSender",
    "build_channel",
    "describe_channel",
    "has_recipient",
    "recipient_for_patient",
    "resolve_channel_name",
]
