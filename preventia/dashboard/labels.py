from datetime import date, datetime

MONTHS = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]

COLOR_LABELS = {
    "red": "ROJO",
    "yellow": "AMARILLO",
    "green": "VERDE",
}

STATE_LABELS = {
    "pending": "pendiente",
    "in_review": "en revisión",
    "contacted": "contactado",
    "closed": "cerrado",
}

STATE_ACTIONS = {
    "in_review": "Tomar el caso",
    "contacted": "Marcar contactado",
    "closed": "Cerrar el caso",
    "pending": "Devolver a pendiente",
}

CONDITION_LABELS = {
    "hipertension": "hipertensión",
    "diabetes_tipo_2": "diabetes tipo 2",
    "insuficiencia_cardiaca": "insuficiencia cardíaca",
}

SYMPTOM_LABELS = {
    "disnea_de_esfuerzo": "falta de aire al esforzarse",
    "edema_de_extremidades": "hinchazón de piernas",
    "mareo": "mareo",
    "dolor_toracico": "dolor en el pecho",
    "hipoglicemia": "azúcar baja",
    "poliuria": "orina frecuente",
    "vision_borrosa": "visión borrosa",
    "palpitaciones": "palpitaciones",
    "ortopnea": "ahogo al acostarse",
    "aumento_de_peso": "aumento de peso",
    "tos_nocturna": "tos en la noche",
    "caida": "caída",
}

TEXT = {
    "queue_title": "Cola de seguimiento",
    "queue_subtitle": "Ordenada por riesgo. Los casos rojos van primero.",
    "empty_queue": "No hay casos en esta vista.",
    "column_color": "Semáforo",
    "adherence": "Adherencia",
    "adherence_window": "últimos 7 contactos",
    "last_contact": "Último contacto",
    "no_contact": "sin contacto registrado",
    "state": "Estado",
    "state_never_changed": "sin cambios de estado registrados",
    "open_record": "Ver ficha",
    "change_state": "Cambiar estado",
    "back_to_queue": "Volver a la cola",
    "history_title": "Historial de contactos",
    "audit_title": "Registro de cambios de estado",
    "audit_empty": "Este caso no ha cambiado de estado.",
    "audit_note_label": "Nota",
    "audit_actor_label": "Responsable",
    "medications_title": "Medicamentos indicados",
    "mentioned_in_passing": "mencionado al pasar",
    "rules_floor": "Piso por regla",
    "model_raised": "El modelo subió el color",
    "filter_all": "Todos",
    "filter_open": "Solo casos abiertos",
    "contrast_toggle": "Alto contraste",
    "font_size_toggle": "Tamaño de letra",
    "font_size_steps": ["Normal", "Grande", "Muy grande"],
    "skip_to_queue": "Saltar a la cola",
    "state_change_failed": "El cambio de estado no se registró. El caso sigue como estaba.",
    "acting_as": "Registrando como",
    "setup_title": "Falta la ficha clínica",
    "setup_body": "El tablero no encontró la base de datos del registro clínico, así que no hay nada que mostrar todavía. Ejecute esto en la carpeta del proyecto y vuelva a cargar la página.",
    "setup_command": "python -m preventia.data.seed_cohort",
    "setup_path_label": "Ruta que se buscó",
    "not_a_diagnosis": "PreventIA no diagnostica ni indica tratamientos. Este resumen es apoyo al seguimiento entre controles.",
}


def color_label(value):
    return COLOR_LABELS.get(value, value)


def state_label(value):
    return STATE_LABELS.get(value, value)


def condition_label(value):
    return CONDITION_LABELS.get(value, value.replace("_", " "))


def symptom_label(value):
    return SYMPTOM_LABELS.get(value, value.replace("_", " "))


def when(value, today=None):
    if not value:
        return TEXT["no_contact"]
    moment = datetime.fromisoformat(value)
    today = today or date.today()
    elapsed = (today - moment.date()).days
    clock = moment.strftime("%H:%M")
    if elapsed <= 0:
        return f"hoy {clock}"
    if elapsed == 1:
        return f"ayer {clock}"
    if elapsed < 7:
        return f"hace {elapsed} días, {clock}"
    return f"{moment.day} de {MONTHS[moment.month - 1]}, {clock}"


def day(value):
    if not value:
        return ""
    moment = datetime.fromisoformat(value)
    return f"{moment.day} de {MONTHS[moment.month - 1]} de {moment.year}"
