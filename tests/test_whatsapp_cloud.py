import asyncio
import hashlib
import hmac
import json

import httpx
import pytest

from preventia.channels.base import InboundMessage, MessageKind, OutboundMessage
from preventia.channels.whatsapp_cloud import (
    ServiceWindowClosed,
    StaticPatientDirectory,
    VerificationRejected,
    WhatsAppCloudChannel,
    WhatsAppCredentials,
    parse_inbound,
    signature_is_valid,
    verification_challenge,
)
from preventia.patient_copy import UNSUPPORTED_MEDIA_REPLY

CREDENTIALS = WhatsAppCredentials(
    phone_number_id="1300775323110140",
    access_token="test-token",
    verify_token="test-verify-token",
    app_secret="test-app-secret",
)

DIRECTORY = StaticPatientDirectory({"56912345678": "patient-001"})


def webhook_payload(message_type="text", body="me duele el pecho", message_id="wamid.TEST1", sender="56912345678"):
    message = {"from": sender, "id": message_id, "timestamp": "1754400000", "type": message_type}
    if message_type == "text":
        message["text"] = {"body": body}
    return {
        "object": "whatsapp_business_account",
        "entry": [{"changes": [{"field": "messages", "value": {"messages": [message]}}]}],
    }


def channel_with(handler, status_code=200, response_payload=None, recorder=None):
    def respond(request):
        if recorder is not None:
            recorder.append(json.loads(request.content))
        return httpx.Response(status_code, json=response_payload or {"messages": [{"id": "wamid.OUT"}]})

    client = httpx.AsyncClient(transport=httpx.MockTransport(respond))
    return WhatsAppCloudChannel(handler, CREDENTIALS, DIRECTORY, client=client)


async def echo(message: InboundMessage) -> OutboundMessage:
    return OutboundMessage(text=f"recibido: {message.text}")


def test_signature_accepts_a_payload_signed_with_the_app_secret():
    body = b'{"object":"whatsapp_business_account"}'
    digest = hmac.new(b"test-app-secret", body, hashlib.sha256).hexdigest()

    assert signature_is_valid("test-app-secret", body, f"sha256={digest}")


def test_signature_rejects_a_tampered_payload():
    body = b'{"object":"whatsapp_business_account"}'
    digest = hmac.new(b"test-app-secret", body, hashlib.sha256).hexdigest()

    assert not signature_is_valid("test-app-secret", body + b" ", f"sha256={digest}")
    assert not signature_is_valid("test-app-secret", body, None)
    assert not signature_is_valid("test-app-secret", body, digest)


def test_handshake_returns_the_challenge_only_for_the_right_verify_token():
    assert verification_challenge(CREDENTIALS, "subscribe", "test-verify-token", "1158201444") == "1158201444"

    with pytest.raises(VerificationRejected):
        verification_challenge(CREDENTIALS, "subscribe", "wrong-token", "1158201444")

    with pytest.raises(VerificationRejected):
        verification_challenge(CREDENTIALS, "unsubscribe", "test-verify-token", "1158201444")


def test_a_text_message_becomes_an_inbound_message_with_a_patient_id():
    messages = parse_inbound(webhook_payload(), DIRECTORY)

    assert len(messages) == 1
    assert messages[0].patient_id == "patient-001"
    assert messages[0].text == "me duele el pecho"
    assert messages[0].kind is MessageKind.TEXT


def test_a_message_from_an_unregistered_number_is_dropped():
    assert parse_inbound(webhook_payload(sender="56999999999"), DIRECTORY) == []


def test_the_same_message_delivered_twice_is_handled_once():
    seen = []

    async def record(message):
        seen.append(message.channel_message_id)
        return OutboundMessage(text="ok")

    channel = channel_with(record)

    asyncio.run(channel.handle_payload(webhook_payload()))
    asyncio.run(channel.handle_payload(webhook_payload()))

    assert seen == ["wamid.TEST1"]


def test_the_reply_goes_out_as_a_cloud_api_text_message():
    sent = []
    channel = channel_with(echo, recorder=sent)

    asyncio.run(channel.handle_payload(webhook_payload()))

    assert sent == [
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": "56912345678",
            "type": "text",
            "text": {"preview_url": False, "body": "recibido: me duele el pecho"},
        }
    ]


def test_a_closed_service_window_raises_something_we_can_catch():
    channel = channel_with(echo, status_code=400, response_payload={"error": {"code": 131047}})

    with pytest.raises(ServiceWindowClosed):
        asyncio.run(channel.handle_payload(webhook_payload()))


def test_a_voice_note_gets_the_fixed_reply_and_never_reaches_the_agent():
    sent = []

    async def handler_that_must_not_run(message):
        raise AssertionError("a voice note reached the agent core")

    channel = channel_with(handler_that_must_not_run, recorder=sent)

    asyncio.run(channel.handle_payload(webhook_payload(message_type="audio")))

    assert sent[0]["text"]["body"] == UNSUPPORTED_MEDIA_REPLY
