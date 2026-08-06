import json
import os
import urllib.error
import urllib.request

from .base import ChannelNotConfigured, Receipt, normalise_recipient

GRAPH_VERSION = "v21.0"
TIMEOUT_SECONDS = 15

REENGAGEMENT_CODE = 131047
NOT_ON_WHATSAPP_CODE = 131030
RATE_LIMIT_CODES = {131056, 130429}

FRIENDLY_ERRORS = {
    REENGAGEMENT_CODE: (
        "la ventana de 24 horas esta cerrada: la persona debe escribir primero, "
        "o hay que usar una plantilla aprobada"
    ),
    NOT_ON_WHATSAPP_CODE: "ese numero no tiene WhatsApp",
}


class WhatsAppCloudChannel:
    name = "whatsapp"

    def __init__(self, phone_number_id=None, access_token=None):
        self.phone_number_id = phone_number_id or os.environ.get("WHATSAPP_PHONE_NUMBER_ID", "")
        self.access_token = access_token or os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
        if not self.phone_number_id or not self.access_token:
            raise ChannelNotConfigured(
                "faltan WHATSAPP_PHONE_NUMBER_ID o WHATSAPP_ACCESS_TOKEN en .env"
            )

    @staticmethod
    def is_configured():
        return bool(
            os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
            and os.environ.get("WHATSAPP_ACCESS_TOKEN")
        )

    @property
    def endpoint(self):
        return f"https://graph.facebook.com/{GRAPH_VERSION}/{self.phone_number_id}/messages"

    def send(self, recipient, text):
        to = normalise_recipient(recipient)
        body = json.dumps(
            {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"preview_url": False, "body": text},
            }
        ).encode("utf-8")

        request = urllib.request.Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                payload = json.loads(response.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as exc:
            return Receipt(False, self.name, detail=_explain(exc))
        except urllib.error.URLError as exc:
            return Receipt(False, self.name, detail=f"no hubo conexion con Meta: {exc.reason}")

        messages = payload.get("messages") or []
        reference = messages[0].get("id", "") if messages else ""
        return Receipt(bool(reference), self.name, reference=reference)


def _explain(exc):
    try:
        payload = json.loads(exc.read().decode("utf-8") or "{}")
    except (ValueError, OSError):
        return f"Meta respondio HTTP {exc.code}"

    error = payload.get("error", {})
    code = error.get("code")
    if code in FRIENDLY_ERRORS:
        return FRIENDLY_ERRORS[code]
    if code in RATE_LIMIT_CODES:
        return "limite de envio alcanzado, intente de nuevo en unos segundos"
    message = error.get("message") or f"HTTP {exc.code}"
    return f"Meta rechazo el envio: {message}"
