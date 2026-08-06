import os
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import audit, auth, intake, labels, messaging, overrides, repository
from .. import channels
from ..agent import models
from ..agent.core import run_check_in
from ..clinical.extraction import ExtractionFailed
from ..environment import load_env_file

load_env_file()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB = BASE_DIR.parent / "data" / "preventia.db"
ASSETS_DIR = BASE_DIR.parent.parent / "assets"

CONTRAST_COOKIE = "preventia_contrast"
FONT_COOKIE = "preventia_font"
ACTOR_COOKIE = "preventia_actor"

CONTRAST_MODES = ("standard", "high")
FONT_STEPS = ("0", "1", "2")
COOKIE_MAX_AGE = 60 * 60 * 24 * 365

app = FastAPI(title="PreventIA")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
templates.env.globals["labels"] = labels
templates.env.globals["T"] = labels.TEXT
templates.env.globals["NEXT_STATE"] = audit.NEXT_STATE
templates.env.filters["color_label"] = labels.color_label
templates.env.filters["state_label"] = labels.state_label
templates.env.filters["condition_label"] = labels.condition_label
templates.env.filters["symptom_label"] = labels.symptom_label
templates.env.filters["when"] = labels.when
templates.env.filters["error_message"] = labels.error_message
templates.env.globals["DOCTOR_ROLE"] = audit.DOCTOR_ROLE
templates.env.filters["day"] = labels.day


def db_path():
    return Path(os.environ.get("PREVENTIA_DB", DEFAULT_DB))


def open_connection():
    return repository.connect(db_path())


def setup_response(request):
    return templates.TemplateResponse(
        request,
        "setup.html",
        {
            "db": str(db_path()),
            "roster": [],
            "actor": None,
            "view": view_settings(request),
        },
        status_code=503,
    )


def view_settings(request):
    contrast = request.cookies.get(CONTRAST_COOKIE, "standard")
    font = request.cookies.get(FONT_COOKIE, "0")
    return {
        "contrast": contrast if contrast in CONTRAST_MODES else "standard",
        "font": font if font in FONT_STEPS else "0",
    }


def acting_clinician(request, roster):
    code = request.cookies.get(ACTOR_COOKIE)
    known = {row["code"]: row for row in roster}
    if code in known:
        return known[code]
    return roster[0] if roster else None


def back_to(request, fallback="/cola"):
    target = request.headers.get("referer") or fallback
    if not target.startswith("/"):
        from urllib.parse import urlparse

        parsed = urlparse(target)
        target = parsed.path or fallback
        if parsed.query:
            target = f"{target}?{parsed.query}"
    return target


@app.middleware("http")
async def require_code(request: Request, call_next):
    if auth.is_open_path(request.url.path) or auth.is_authenticated(request):
        return await call_next(request)
    return RedirectResponse("/entrar", status_code=303)


@app.get("/entrar")
async def login_form(request: Request, error: str = ""):
    if auth.is_authenticated(request):
        return RedirectResponse("/cola", status_code=303)
    return templates.TemplateResponse(
        request,
        "entrar.html",
        {
            "error": labels.TEXT["login_bad_code"] if error else "",
            "actor": None,
            "roster": [],
            "view": view_settings(request),
        },
    )


@app.post("/entrar")
async def login(request: Request, code: str = Form("")):
    try:
        token = auth.verify(code)
    except auth.BadCode:
        return RedirectResponse("/entrar?error=1", status_code=303)

    response = RedirectResponse("/cola", status_code=303)
    response.set_cookie(
        auth.SESSION_COOKIE, token, max_age=COOKIE_MAX_AGE, samesite="lax", httponly=True
    )
    return response


@app.get("/salir")
async def logout():
    response = RedirectResponse("/entrar", status_code=303)
    response.delete_cookie(auth.SESSION_COOKIE)
    return response


@app.get("/")
async def root():
    return RedirectResponse("/cola", status_code=303)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(ASSETS_DIR / "favicon.ico", media_type="image/x-icon")


@app.get("/cola")
async def queue(request: Request, filtro: str = "abiertos"):
    try:
        conn = open_connection()
    except repository.MissingClinicalRecord:
        return setup_response(request)
    try:
        only_open = filtro != "todos"
        rows = repository.queue_rows(conn, only_open=only_open)
        roster = repository.clinicians(conn)
        crises = intake.open_crises(conn)
    finally:
        conn.close()

    return templates.TemplateResponse(
        request,
        "queue.html",
        {
            "rows": rows,
            "crises": crises,
            "filtro": "todos" if filtro == "todos" else "abiertos",
            "roster": roster,
            "actor": acting_clinician(request, roster),
            "view": view_settings(request),
        },
    )


@app.get("/cola/{code}")
async def patient(request: Request, code: str, error: str = "", sent: str = ""):
    try:
        conn = open_connection()
    except repository.MissingClinicalRecord:
        return setup_response(request)
    try:
        detail = repository.patient_detail(conn, code)
        roster = repository.clinicians(conn)
        thread = messaging.messages_for(conn, code) if detail else []
    finally:
        conn.close()

    if detail is None:
        return RedirectResponse("/cola", status_code=303)

    return templates.TemplateResponse(
        request,
        "patient.html",
        {
            "patient": detail,
            "roster": roster,
            "actor": acting_clinician(request, roster),
            "view": view_settings(request),
            "states": audit.STATES,
            "error": error,
            "messages": thread,
            "channel": channels.describe_channel(),
            "sent": sent,
        },
    )


@app.post("/cola/{code}/mensaje")
async def send_message(
    request: Request,
    code: str,
    actor_code: str = Form(...),
    body: str = Form(""),
    confirm_code: str = Form(""),
):
    if not auth.confirms(confirm_code):
        return RedirectResponse(f"/cola/{code}?error=confirmacion", status_code=303)

    try:
        conn = open_connection()
    except repository.MissingClinicalRecord:
        return setup_response(request)

    try:
        receipt = messaging.send_doctor_message(conn, code, actor_code, body)
        target = f"/cola/{code}?sent={'1' if receipt.delivered else '0'}"
    except audit.NotADoctor:
        target = f"/cola/{code}?error=mensaje_solo_medico"
    except messaging.EmptyMessage:
        target = f"/cola/{code}?error=mensaje_vacio"
    except messaging.MissingRecipient:
        target = f"/cola/{code}?error=mensaje_sin_numero"
    except (audit.UnknownActor, ValueError):
        target = f"/cola/{code}?error=estado"
    finally:
        conn.close()

    response = RedirectResponse(target, status_code=303)
    response.set_cookie(ACTOR_COOKIE, actor_code, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response


@app.post("/cola/{code}/estado")
async def change_state(
    request: Request,
    code: str,
    to_state: str = Form(...),
    actor_code: str = Form(...),
    note: str = Form(""),
    confirm_code: str = Form(""),
):
    if not auth.confirms(confirm_code):
        return RedirectResponse(f"/cola/{code}?error=confirmacion", status_code=303)

    try:
        conn = open_connection()
    except repository.MissingClinicalRecord:
        return setup_response(request)
    try:
        audit.record_transition(conn, code, to_state, actor_code, note, confirmed_by=actor_code)
        target = back_to(request, f"/cola/{code}")
    except (audit.UnknownState, audit.UnknownActor, ValueError):
        target = f"/cola/{code}?error=estado"
    finally:
        conn.close()

    response = RedirectResponse(target, status_code=303)
    response.set_cookie(ACTOR_COOKIE, actor_code, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response


@app.post("/cola/{code}/contacto")
async def record_contact(
    request: Request,
    code: str,
    actor_code: str = Form(...),
    note: str = Form(""),
    confirm_code: str = Form(""),
):
    if not auth.confirms(confirm_code):
        return RedirectResponse(f"/cola/{code}?error=confirmacion", status_code=303)

    try:
        conn = open_connection()
    except repository.MissingClinicalRecord:
        return setup_response(request)
    try:
        audit.record_doctor_contact(conn, code, actor_code, note, confirmed_by=actor_code)
        target = f"/cola/{code}"
    except audit.NotADoctor:
        target = f"/cola/{code}?error=solo_medico"
    except audit.MissingContactNote:
        target = f"/cola/{code}?error=falta_nota"
    except (audit.UnknownActor, ValueError):
        target = f"/cola/{code}?error=estado"
    finally:
        conn.close()

    response = RedirectResponse(target, status_code=303)
    response.set_cookie(ACTOR_COOKIE, actor_code, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response


@app.post("/cola/{code}/color")
async def change_color(
    request: Request,
    code: str,
    color: str = Form(...),
    actor_code: str = Form(...),
    reason: str = Form(""),
    confirm_code: str = Form(""),
):
    if not auth.confirms(confirm_code):
        return RedirectResponse(f"/cola/{code}?error=confirmacion", status_code=303)

    try:
        conn = open_connection()
    except repository.MissingClinicalRecord:
        return setup_response(request)
    try:
        overrides.record_override(conn, code, color, actor_code, reason, confirmed_by=actor_code)
        target = f"/cola/{code}"
    except audit.NotADoctor:
        target = f"/cola/{code}?error=color_solo_medico"
    except overrides.MissingReason:
        target = f"/cola/{code}?error=color_sin_razon"
    except overrides.UnknownColor:
        target = f"/cola/{code}?error=color_desconocido"
    except (audit.UnknownActor, ValueError):
        target = f"/cola/{code}?error=estado"
    finally:
        conn.close()

    response = RedirectResponse(target, status_code=303)
    response.set_cookie(ACTOR_COOKIE, actor_code, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response


def consulta_response(request, conn, result=None, error="", message="", selected=""):
    return templates.TemplateResponse(
        request,
        "consulta.html",
        {
            "roster": intake.roster_for_intake(conn),
            "runtime": models.describe_runtime(),
            "result": result,
            "error": error,
            "message": message,
            "selected": selected,
            "actor": None,
            "view": view_settings(request),
        },
    )


@app.get("/consulta")
async def consulta(request: Request):
    try:
        conn = open_connection()
    except repository.MissingClinicalRecord:
        return setup_response(request)
    try:
        return consulta_response(request, conn)
    finally:
        conn.close()


@app.post("/consulta")
async def run_consulta(
    request: Request,
    patient_code: str = Form(...),
    message: str = Form(...),
):
    try:
        conn = open_connection()
    except repository.MissingClinicalRecord:
        return setup_response(request)

    try:
        patient = intake.patient_for_agent(conn, patient_code)
        if patient is None:
            return consulta_response(
                request, conn, error="No encontramos a esa persona en la ficha."
            )

        try:
            result = run_check_in(patient, message.strip())
        except models.MissingModelToken as exc:
            return consulta_response(
                request, conn, error=str(exc), message=message, selected=patient_code
            )
        except models.ModelUnavailable as exc:
            return consulta_response(
                request,
                conn,
                error=f"El modelo no respondio: {exc}",
                message=message,
                selected=patient_code,
            )
        except ExtractionFailed as exc:
            return consulta_response(
                request, conn, error=str(exc), message=message, selected=patient_code
            )

        intake.persist(conn, result)
        return consulta_response(request, conn, result=result, selected=patient_code)
    finally:
        conn.close()


@app.post("/preferencias/contraste")
async def set_contrast(request: Request, contrast: str = Form(...)):
    value = contrast if contrast in CONTRAST_MODES else "standard"
    response = RedirectResponse(back_to(request), status_code=303)
    response.set_cookie(CONTRAST_COOKIE, value, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response


@app.post("/preferencias/letra")
async def set_font(request: Request, font: str = Form(...)):
    value = font if font in FONT_STEPS else "0"
    response = RedirectResponse(back_to(request), status_code=303)
    response.set_cookie(FONT_COOKIE, value, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response


@app.post("/preferencias/responsable")
async def set_actor(request: Request, actor_code: str = Form(...)):
    response = RedirectResponse(back_to(request), status_code=303)
    response.set_cookie(ACTOR_COOKIE, actor_code, max_age=COOKIE_MAX_AGE, samesite="lax")
    return response
