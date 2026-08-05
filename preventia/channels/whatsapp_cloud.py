from __future__ import annotations

import hashlib
import hmac
import os
from collections import OrderedDict
from dataclasses import dataclass
from datetime import UTC, datetime

import httpx

from preventia.channels.base import (
    Channel,
    CheckInHandler,
    InboundMessage,
    MessageKind,
    OutboundMessage,
    PatientDirectory,
    UnknownSender,
)

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
SERVICE_WINDOW_CLOSED_CODE = 131047
RECIPIENT_NOT_ON_WHATSAPP_CODE = 131030
SEEN_MESSAGE_LIMIT = 512


class ServiceWindowClosed(Exception):
    pass


class RecipientUnreachable(Exception):
    pass


class SignatureRejected(Exception):
    pass


class VerificationRejected(Exception):
    pass


@dataclass(frozen=True)
class WhatsAppCredentials:
    phone_number_id: str
    access_token: str
    verify_token: str
    app_secret: str

    @classmethod
    def from_environment(cls) -> WhatsAppCredentials:
        return cls(
            phone_number_id=os.environ["WHATSAPP_PHONE_NUMBER_ID"],
            access_token=os.environ["WHATSAPP_ACCESS_TOKEN"],
            verify_token=os.environ["WHATSAPP_VERIFY_TOKEN"],
            app_secret=os.environ["WHATSAPP_APP_SECRET"],
        )


class StaticPatientDirectory(PatientDirectory):
    def __init__(self, patient_ids_by_address: dict[str, str]) -> None:
        self._by_address = dict(patient_ids_by_address)
        self._by_patient = {v: k for k, v in self._by_address.items()}

    @classmethod
    def from_environment(cls, variable: str = "PREVENTIA_PATIENT_DIRECTORY") -> StaticPatientDirectory:
        raw = os.environ.get(variable, "")
        pairs = {}
        for item in raw.split(","):
            if not item.strip():
                continue
            address, _, patient_id = item.partition("=")
            pairs[normalise_address(address)] = patient_id.strip()
        return cls(pairs)

    def patient_id_for(self, channel_address: str) -> str:
        key = normalise_address(channel_address)
        if key not in self._by_address:
            raise UnknownSender(key)
        return self._by_address[key]

    def channel_address_for(self, patient_id: str) -> str:
        if patient_id not in self._by_patient:
            raise UnknownSender(patient_id)
        return self._by_patient[patient_id]


def normalise_address(address: str) -> str:
    return address.strip().lstrip("+")


def kind_for(whatsapp_type: str) -> MessageKind:
    if whatsapp_type == "text":
        return MessageKind.TEXT
    if whatsapp_type == "audio":
        return MessageKind.AUDIO
    return MessageKind.UNSUPPORTED


def signature_is_valid(app_secret: str, raw_body: bytes, header: str | None) -> bool:
    if not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(app_secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header.removeprefix("sha256="))


def verification_challenge(
    credentials: WhatsAppCredentials,
    mode: str | None,
    token: str | None,
    challenge: str | None,
) -> str:
    if mode != "subscribe" or not hmac.compare_digest(token or "", credentials.verify_token):
        raise VerificationRejected(mode or "")
    return challenge or ""


def parse_inbound(payload: dict, directory: PatientDirectory) -> list[InboundMessage]:
    parsed: list[InboundMessage] = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            for message in change.get("value", {}).get("messages", []):
                kind = kind_for(message.get("type", ""))
                try:
                    patient_id = directory.patient_id_for(message.get("from", ""))
                except UnknownSender:
                    continue
                parsed.append(
                    InboundMessage(
                        patient_id=patient_id,
                        kind=kind,
                        text=message.get("text", {}).get("body", "") if kind is MessageKind.TEXT else "",
                        channel_message_id=message.get("id", ""),
                        received_at=datetime.fromtimestamp(int(message.get("timestamp", 0)), UTC),
                    )
                )
    return parsed


class WhatsAppCloudChannel(Channel):
    def __init__(
        self,
        handler: CheckInHandler,
        credentials: WhatsAppCredentials,
        directory: PatientDirectory,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(handler)
        self._credentials = credentials
        self._directory = directory
        self._client = client if client is not None else httpx.AsyncClient(timeout=15.0)
        self._seen: OrderedDict[str, None] = OrderedDict()

    @property
    def credentials(self) -> WhatsAppCredentials:
        return self._credentials

    async def send(self, patient_id: str, message: OutboundMessage) -> None:
        response = await self._client.post(
            f"{GRAPH_API_BASE}/{self._credentials.phone_number_id}/messages",
            headers={"Authorization": f"Bearer {self._credentials.access_token}"},
            json={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self._directory.channel_address_for(patient_id),
                "type": "text",
                "text": {"preview_url": False, "body": message.text},
            },
        )
        if response.is_success:
            return
        raise self._failure(response)

    async def handle_payload(self, payload: dict) -> list[InboundMessage]:
        delivered: list[InboundMessage] = []
        for message in parse_inbound(payload, self._directory):
            if self._already_seen(message.channel_message_id):
                continue
            await self.receive(message)
            delivered.append(message)
        return delivered

    def _already_seen(self, message_id: str) -> bool:
        if not message_id:
            return False
        if message_id in self._seen:
            return True
        self._seen[message_id] = None
        while len(self._seen) > SEEN_MESSAGE_LIMIT:
            self._seen.popitem(last=False)
        return False

    def _failure(self, response: httpx.Response) -> Exception:
        try:
            code = response.json().get("error", {}).get("code")
        except ValueError:
            code = None
        if code == SERVICE_WINDOW_CLOSED_CODE:
            return ServiceWindowClosed(str(code))
        if code == RECIPIENT_NOT_ON_WHATSAPP_CODE:
            return RecipientUnreachable(str(code))
        return httpx.HTTPStatusError(
            f"{response.status_code}", request=response.request, response=response
        )
