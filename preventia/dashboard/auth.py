import hashlib
import hmac
import os

SESSION_COOKIE = "preventia_sesion"
DEFAULT_CODE = "0000"
CODE_LENGTH = 4

OPEN_PATHS = ("/entrar", "/salir", "/static", "/assets", "/favicon.ico", "/salud")


class BadCode(ValueError):
    pass


def expected_code():
    return (os.environ.get("PREVENTIA_DOCTOR_CODE") or DEFAULT_CODE).strip()


def _salt():
    return os.environ.get("PREVENTIA_SESSION_SALT", "preventia-demo")


def session_token():
    material = f"{_salt()}:{expected_code()}".encode("utf-8")
    return hashlib.sha256(material).hexdigest()[:32]


def verify(code):
    candidate = (code or "").strip()
    if not candidate.isdigit() or len(candidate) != CODE_LENGTH:
        raise BadCode("el codigo son 4 numeros")
    if not hmac.compare_digest(candidate, expected_code()):
        raise BadCode("codigo incorrecto")
    return session_token()


def is_open_path(path):
    return any(path == item or path.startswith(f"{item}/") for item in OPEN_PATHS)


def is_authenticated(request):
    presented = request.cookies.get(SESSION_COOKIE, "")
    return bool(presented) and hmac.compare_digest(presented, session_token())
