import hashlib
import hmac
import json

import httpx
from fastapi.testclient import TestClient

from preventia.channels.base import InboundMessage, OutboundMessage
from preventia.channels.webhook import WEBHOOK_PATH, build_app
from preventia.channels.whatsapp_cloud import (
    StaticPatientDirectory,
    WhatsAppCloudChannel,
    WhatsAppCredentials,
)

CREDENTIALS = WhatsAppCredentials(
    phone_number_id="1300775323110140",
    access_token="test-token",
    verify_token="test-verify-token",
    app_secret="test-app-secret",
)

PAYLOAD = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messages": [
                            {
                                "from": "56912345678",
                                "id": "wamid.WEBHOOK1",
                                "timestamp": "1754400000",
                                "type": "text",
                                "text": {"body": "tomé el losartán"},
                            }
                        ]
                    },
                }
            ]
        }
    ],
}


def signed(body: bytes) -> str:
    return "sha256=" + hmac.new(b"test-app-secret", body, hashlib.sha256).hexdigest()


def build_client(sent):
    async def handler(message: InboundMessage) -> OutboundMessage:
        return OutboundMessage(text=f"recibido: {message.text}")

    def respond(request):
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"messages": [{"id": "wamid.OUT"}]})

    channel = WhatsAppCloudChannel(
        handler,
        CREDENTIALS,
        StaticPatientDirectory({"56912345678": "patient-001"}),
        client=httpx.AsyncClient(transport=httpx.MockTransport(respond)),
    )
    return TestClient(build_app(channel))


def test_meta_handshake_echoes_the_challenge():
    client = build_client([])

    response = client.get(
        WEBHOOK_PATH,
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "test-verify-token",
            "hub.challenge": "1158201444",
        },
    )

    assert response.status_code == 200
    assert response.text == "1158201444"


def test_handshake_with_a_wrong_verify_token_is_refused():
    client = build_client([])

    response = client.get(
        WEBHOOK_PATH,
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "guessed",
            "hub.challenge": "1158201444",
        },
    )

    assert response.status_code == 403


def test_an_unsigned_post_is_refused_and_never_reaches_the_agent():
    sent = []
    client = build_client(sent)
    body = json.dumps(PAYLOAD).encode()

    response = client.post(WEBHOOK_PATH, content=body, headers={"Content-Type": "application/json"})

    assert response.status_code == 403
    assert sent == []


def test_a_signed_post_is_acknowledged_and_the_reply_goes_out():
    sent = []
    client = build_client(sent)
    body = json.dumps(PAYLOAD).encode()

    response = client.post(
        WEBHOOK_PATH,
        content=body,
        headers={"Content-Type": "application/json", "X-Hub-Signature-256": signed(body)},
    )

    assert response.status_code == 200
    assert sent[0]["text"]["body"] == "recibido: tomé el losartán"
