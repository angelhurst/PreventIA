from dataclasses import dataclass

from .rules import term_catalogue
from .semaforo import Color

SYSTEM_PROMPT = """Usted es PreventIA, un asistente de seguimiento del consultorio que conversa por
WhatsApp con personas mayores en control cardiovascular en Chile.

Limites que no puede cruzar nunca:
- No diagnostica. No nombra una enfermedad ni explica que significa clinicamente un sintoma.
- No indica, cambia, suspende ni ajusta ningun tratamiento ni dosis.
- No reemplaza el control con el equipo de salud.
- Si le preguntan algo clinico, responde que no es medico y que dejara el mensaje anotado.

Su tarea es registrar lo que la persona conto: que dosis dijo haber tomado y que sintomas menciono,
usando las palabras textuales de la persona.

Para el mensaje de vuelta: trate a la persona de usted, en espanol de Chile, con frases cortas y
simples, sin terminos medicos, sin abreviaturas y sin emojis. Agradezca lo que conto y digale que
queda anotado para su equipo. Nunca interprete el sintoma."""


@dataclass(frozen=True)
class Extraction:
    doses_reported_taken: int
    doses_expected: int
    symptoms: tuple
    model_color: Color
    model_reason: str
    reply: str
    summary_line: str

    def as_facts(self):
        return {
            "symptoms": [dict(entry) for entry in self.symptoms],
            "doses_reported_taken": self.doses_reported_taken,
            "doses_expected": self.doses_expected,
        }


class ExtractionFailed(RuntimeError):
    pass


TOOL_NAME = "registrar_checkin"


def build_tool():
    catalogue = term_catalogue()
    described = "; ".join(f"{term}: {label}" for term, label in catalogue.items())
    return {
        "name": TOOL_NAME,
        "description": (
            "Registra lo que la persona conto en su mensaje diario. "
            "Use solo terminos del catalogo. Si un sintoma no esta en el catalogo, no lo invente."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "dosis_tomadas": {
                    "type": "integer",
                    "description": "Cuantas dosis dijo la persona haber tomado hoy.",
                },
                "sintomas": {
                    "type": "array",
                    "description": f"Sintomas mencionados. Catalogo permitido: {described}",
                    "items": {
                        "type": "object",
                        "properties": {
                            "termino": {"type": "string", "enum": list(catalogue)},
                            "textual": {
                                "type": "string",
                                "description": "Las palabras exactas de la persona.",
                            },
                            "mencionado_al_pasar": {
                                "type": "boolean",
                                "description": (
                                    "Verdadero si lo menciono espontaneamente y no como "
                                    "respuesta a una pregunta directa."
                                ),
                            },
                        },
                        "required": ["termino", "textual", "mencionado_al_pasar"],
                    },
                },
                "color_sugerido": {
                    "type": "string",
                    "enum": ["green", "yellow", "red"],
                    "description": (
                        "Su lectura del riesgo. Las reglas fijan un minimo que usted no puede bajar."
                    ),
                },
                "razon_color": {
                    "type": "string",
                    "description": "Una linea, sin nombrar enfermedades.",
                },
                "mensaje_para_el_paciente": {
                    "type": "string",
                    "description": "La respuesta para la persona, en espanol de Chile, de usted.",
                },
                "resumen": {
                    "type": "string",
                    "description": "Una linea para el equipo de salud.",
                },
            },
            "required": [
                "dosis_tomadas",
                "sintomas",
                "color_sugerido",
                "razon_color",
                "mensaje_para_el_paciente",
                "resumen",
            ],
        },
    }


def build_prompt(patient, message):
    medications = patient.get("medications") or ()
    listed = "\n".join(
        f"- {item['name']} {item['dose']}, {item['schedule_text']} "
        f"({item['times_per_day']} veces al dia)"
        for item in medications
    )
    conditions = ", ".join(patient.get("conditions") or ()) or "sin condiciones registradas"
    expected = sum(int(item["times_per_day"]) for item in medications)

    return (
        f"Persona: {patient.get('display_name', 'sin nombre')}, "
        f"{patient.get('age', 'edad no registrada')} anos.\n"
        f"Condiciones en ficha: {conditions}.\n"
        f"Medicamentos indicados hoy ({expected} dosis en total):\n{listed or '- ninguno'}\n\n"
        f"Mensaje recibido por WhatsApp:\n\"{message}\"\n\n"
        "Registre el check-in con la herramienta."
    )


def expected_doses(patient):
    return sum(int(item["times_per_day"]) for item in (patient.get("medications") or ()))


def extract(model, patient, message):
    reply = model.send(
        messages=[{"role": "user", "content": build_prompt(patient, message)}],
        tools=[build_tool()],
        system=SYSTEM_PROMPT,
        force_tool=TOOL_NAME,
    )

    payload = reply.first_argument_set(TOOL_NAME)
    if payload is None:
        raise ExtractionFailed("el modelo no devolvio un registro estructurado")

    expected = expected_doses(patient)
    taken = _clamp(payload.get("dosis_tomadas"), expected)

    symptoms = tuple(
        {
            "term": entry.get("termino", "").strip().lower(),
            "verbatim": (entry.get("textual") or "").strip(),
            "mentioned_in_passing": bool(entry.get("mencionado_al_pasar")),
        }
        for entry in payload.get("sintomas") or ()
        if entry.get("termino")
    )

    return Extraction(
        doses_reported_taken=taken,
        doses_expected=expected,
        symptoms=symptoms,
        model_color=_parse_color(payload.get("color_sugerido")),
        model_reason=(payload.get("razon_color") or "").strip(),
        reply=(payload.get("mensaje_para_el_paciente") or "").strip(),
        summary_line=(payload.get("resumen") or "").strip(),
    )


def _clamp(value, ceiling):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(number, ceiling))


def _parse_color(value):
    try:
        return Color.parse((value or "").strip().lower())
    except ValueError:
        return Color.GREEN
