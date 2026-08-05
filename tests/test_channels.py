import asyncio
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

import preventia.channels.base as base_module
import preventia.channels.local_console as console_module
from preventia.channels.base import InboundMessage, MessageKind, OutboundMessage
from preventia.channels.local_console import LocalConsoleChannel
from preventia.patient_copy import UNSUPPORTED_MEDIA_REPLY


def make_inbound(kind: MessageKind, text: str = "hola") -> InboundMessage:
    return InboundMessage(
        patient_id="patient-001",
        kind=kind,
        text=text,
        channel_message_id="test-1",
        received_at=datetime.now(UTC),
    )


async def echo(message: InboundMessage) -> OutboundMessage:
    return OutboundMessage(text=f"recibido: {message.text}")


def test_text_message_reaches_the_handler_and_the_reply_goes_out():
    stdout = StringIO()
    channel = LocalConsoleChannel(echo, "patient-001", stdin=StringIO(), stdout=stdout)

    reply = asyncio.run(channel.receive(make_inbound(MessageKind.TEXT)))

    assert reply.text == "recibido: hola"
    assert "PreventIA > recibido: hola" in stdout.getvalue()


def test_audio_message_never_reaches_the_handler():
    async def handler_that_must_not_run(message: InboundMessage) -> OutboundMessage:
        raise AssertionError("a non-text message reached the agent core")

    channel = LocalConsoleChannel(
        handler_that_must_not_run, "patient-001", stdin=StringIO(), stdout=StringIO()
    )

    reply = asyncio.run(channel.receive(make_inbound(MessageKind.AUDIO, "")))

    assert reply.text == UNSUPPORTED_MEDIA_REPLY


def test_a_whole_conversation_runs_with_no_telephony():
    stdout = StringIO()
    channel = LocalConsoleChannel(
        echo, "patient-001", stdin=StringIO("hola\nme siento bien\nsalir\n"), stdout=stdout
    )

    asyncio.run(channel.run())

    transcript = stdout.getvalue()
    assert "PreventIA > recibido: hola" in transcript
    assert "PreventIA > recibido: me siento bien" in transcript


def test_the_channel_seam_holds():
    for module in (base_module, console_module):
        source = Path(module.__file__).read_text(encoding="utf-8")
        assert "whatsapp" not in source.lower()
