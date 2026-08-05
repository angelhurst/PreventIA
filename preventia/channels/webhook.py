from __future__ import annotations

import json

from fastapi import BackgroundTasks, FastAPI, Request, Response

from preventia.channels.whatsapp_cloud import (
    VerificationRejected,
    WhatsAppCloudChannel,
    signature_is_valid,
    verification_challenge,
)

SIGNATURE_HEADER = "X-Hub-Signature-256"
WEBHOOK_PATH = "/webhook/whatsapp"


def build_app(channel: WhatsAppCloudChannel) -> FastAPI:
    app = FastAPI(title="PreventIA channel")

    @app.get(WEBHOOK_PATH)
    async def verify(request: Request) -> Response:
        params = request.query_params
        try:
            challenge = verification_challenge(
                channel.credentials,
                params.get("hub.mode"),
                params.get("hub.verify_token"),
                params.get("hub.challenge"),
            )
        except VerificationRejected:
            return Response(status_code=403)
        return Response(content=challenge, media_type="text/plain")

    @app.post(WEBHOOK_PATH)
    async def receive(request: Request, background: BackgroundTasks) -> Response:
        raw = await request.body()
        header = request.headers.get(SIGNATURE_HEADER)
        if not signature_is_valid(channel.credentials.app_secret, raw, header):
            return Response(status_code=403)
        try:
            payload = json.loads(raw)
        except ValueError:
            return Response(status_code=400)
        background.add_task(channel.handle_payload, payload)
        return Response(status_code=200)

    return app
