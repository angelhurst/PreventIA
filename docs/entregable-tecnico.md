# PreventIA — Entregable técnico

**Claude Impact Lab · Longevidad — Santiago, 5-6 de agosto de 2026**
Línea: Continuidad y medicina de precisión
Versión 1.0 · 6 de agosto de 2026

Cada cifra de este documento está tomada de una fuente oficial chilena, archivada en
`docs/research/sources/`. Las cifras de listas de espera que circulan en el brief del Lab
(2,4 millones de personas, 400+ días, 500+ días) no se usan aquí: están desactualizadas contra el
informe Glosa 06 del propio Minsal al 31 de marzo de 2026, y la trazabilidad está documentada en
`docs/research/felipe/2026-08-03-chilean-primary-care-reality.md`.

---

## segmento_ciudadano

Personas de **65 a 75 años**, **polimedicadas**, con **hipertensión arterial y/o diabetes mellitus
tipo 2 confirmadas**, **bajo control en el Programa de Salud Cardiovascular (PSCV) de la atención
primaria pública**, y que **ya usan WhatsApp**.

Ejes que definen el segmento:

| Eje | Valor |
|---|---|
| Condición de salud | Hipertensión arterial y/o diabetes mellitus tipo 2 confirmadas, con polimedicación |
| Etapa vital | 65 a 75 años |
| Sistema previsional y territorio | Atención primaria pública, red municipal de salud |
| Canal | Adultos mayores que ya usan WhatsApp de manera habitual |

La polimedicación no es un nicho elegido para que la demo resulte interesante. Es el caso mayoritario
del programa: **el 65% de la población bajo control en el PSCV está diagnosticada con más de un
problema de salud** (DIPRES, 2018, sobre datos 2017).

El límite superior de 75 años es deliberado y clínico, no comercial. El propio PSCV define fragilidad
a partir de los 75 años, entre otros criterios, y relaja sus metas terapéuticas en consecuencia. Un
prototipo que escribe en texto también alcanza a una proporción decreciente de la población a medida
que sube la edad. Definir la primera cohorte por debajo de ese umbral es honesto respecto de lo que
el prototipo puede sostener hoy.

---

## impacto_cuantificado

**2.301.144 personas están bajo control en el Programa de Salud Cardiovascular, el 13% de la
población del país, y el 65% de ellas tiene más de un problema de salud diagnosticado. Entre un
control y el siguiente pueden pasar de 90 a 365 días sin ningún contacto clínico programado, y
ninguna garantía GES cubre ese intervalo.**

El desglose, cifra por cifra:

| Cifra | Valor | Fuente |
|---|---|---|
| Población bajo control en el PSCV (2017) | 2.301.144 personas, 13% de la población nacional | DIPRES 2018 |
| Multimorbilidad en esa población | 65% con más de un problema de salud | DIPRES 2018 |
| Frecuencia de control una vez compensado | Cada 3 meses en riesgo cardiovascular alto, cada 6 en moderado, cada 6 a 12 en bajo | Minsal, OT PSCV 2017 |
| Garantía GES hipertensión | 45 días para confirmar el diagnóstico, 24 horas para iniciar tratamiento | Superintendencia de Salud |
| Garantía GES sobre el intervalo entre controles | **No existe** | Superintendencia de Salud |
| Insuficiencia cardíaca en el régimen GES | **No es un problema GES**, no tiene plazo garantizado de ninguna clase | Superintendencia de Salud |

El argumento no es que la fila sea larga. Es que la garantía cubre la entrada y no cubre el
intervalo. Un paciente hipertenso tiene garantizada la confirmación en 45 días y el tratamiento
dentro de las 24 horas siguientes, y después, como cuestión de ley, nada hasta que vuelva a ser
citado. Las garantías se cumplen sobre el 97% de los casos y la brecha existe igual. Es una brecha
estructural, no un incumplimiento.

### El costo que hoy paga el sistema

En ese intervalo sí hay alguien mirando, y ahí está el costo real. El PSCV obliga a rescatar a quien
falta a su control, con **al menos 3 acciones de rescate documentadas** antes de poder egresar a
alguien por abandono, sobre una ventana de 11 meses y 29 días. **El 90,7% de los 2.027
establecimientos de atención primaria que hacen ese trabajo depende de un municipio.**

PreventIA sustituye esa llamada, no el control.

### Lo que ya se intentó en Chile, dicho por nosotros antes que por el jurado

Chile ya automatizó el contacto con pacientes a escala nacional. El sistema de recordatorios de
FOFAR, evaluado por DIPRES sobre **4.481.282 horas médicas**, obtuvo 11,6% de inasistencia con
recordatorio contra 13,3% sin él, y el panel calificó el efecto y la contribución a la adherencia
como **marginales**. La comparación además está confundida: el grupo sin recordatorio quedó sin
recordatorio porque sus datos de contacto estaban mal o faltaban.

Esto se dice en el pitch, no se esconde. Un recordatorio es un mensaje de una vía sobre una fecha.
PreventIA es una conversación de dos vías que extrae hechos de adherencia y de síntomas y entrega un
caso priorizado a un profesional que puede actuar. Son intervenciones distintas que comparten un
teléfono. Que la primera haya rendido poco es una razón para construir algo que no sea un
recordatorio.

**fuente_impacto_url:**
`https://www.dipres.gob.cl/597/articles-177366_informe_final.pdf`

Dirección de Presupuestos (DIPRES), Ministerio de Hacienda de Chile. *Informe Final de Evaluación
(EPG): Programa Fondo de Farmacia para Enfermedades Crónicas No Transmisibles en Atención Primaria
de Salud*, 2018. Cuadro 7 (población bajo control y multimorbilidad), Cuadro 20 (recordatorios e
inasistencia), distribución de dependencia de establecimientos.

Fuentes oficiales adicionales del mismo campo:

- `https://redcronicas.minsal.cl/wp-content/uploads/2017/08/OT-PROGRAMA-DE-SALUD-CARDIOVASCULAR_05.pdf`
- `https://www.minsal.cl/wp-content/uploads/2026/07/Glosa-06-letra-a-b-c-i-j-k-comun-a-la-partida-1er-trimestre-1.pdf`

---

## fuentes_regulatorias

Todas son de organismos oficiales del Estado de Chile. Copias archivadas en
`docs/research/sources/`.

| # | Organismo | Documento | URL |
|---|---|---|---|
| 1 | Ministerio de Salud | *Orientación Técnica Programa de Salud Cardiovascular*, 2017 | `https://redcronicas.minsal.cl/wp-content/uploads/2017/08/OT-PROGRAMA-DE-SALUD-CARDIOVASCULAR_05.pdf` |
| 2 | Ministerio de Salud y SOCHICAR | *Guía Clínica Insuficiencia Cardíaca*, 2015 | `https://www.minsal.cl/wp-content/uploads/2015/11/GUIA-CLINICA-INSUFICIENCIA-CARDIACA_web.pdf` |
| 3 | Ministerio de Salud | *Guía Clínica Diabetes Mellitus tipo 2*, 2010 | `https://www.superdesalud.gob.cl/difusion/572/articles-623_recurso_1.pdf` |
| 4 | Ministerio de Salud | *Guía Clínica Hipertensión Arterial Primaria o Esencial en personas de 15 años y más*, 2010 | `https://diprece.minsal.cl/wrdprss_minsal/wp-content/uploads/2014/12/Hipertensión-Arterial-en-personas-de-15-años-y-más.pdf` |
| 5 | Ministerio de Salud | *Resumen Ejecutivo GPC Hipertensión Arterial*, 2018 | `https://diprece.minsal.cl/wp-content/uploads/2019/05/08.-RE_GPC-HTA-Final_2018v5.pdf` |
| 6 | Superintendencia de Salud | GES — Hipertensión arterial primaria o esencial en personas de 15 años y más | `https://www.superdesalud.gob.cl/orientacion-en-salud/hipertension-arterial-primaria-o-esencial-en-personas-de-15-anos-y-mas/` |
| 7 | Superintendencia de Salud | GES — Diabetes mellitus tipo 2 | `https://www.superdesalud.gob.cl/orientacion-en-salud/diabetes-mellitus-tipo-2/` |
| 8 | Dirección de Presupuestos | *Informe Final de Evaluación EPG — FOFAR*, 2018 | `https://www.dipres.gob.cl/597/articles-177366_informe_final.pdf` |
| 9 | Biblioteca del Congreso Nacional | *Ley N° 21.719*, protección y tratamiento de datos personales | `https://www.bcn.cl/leychile/navegar?idNorma=1209272` |

La número 9 no es una guía clínica y está por una razón. La Ley 21.719 entra en plena vigencia el
**1 de diciembre de 2026**, cuatro meses después del Lab. Clasifica los datos de salud como datos
personales sensibles y define la anonimización como un procedimiento irreversible, distinto de la
seudonimización. PreventIA no contiene ningún dato real de paciente: la cohorte es sintética. La
arquitectura se construyó contra una regla más estricta que la ley, antes de que la ley llegara.

---

## agente_no_hace

Estos límites están escritos en el código, no solamente en el system prompt, y hay una suite de tests
que lo demuestra. Un jurado puede correrla.

| El agente NO | Detalle |
|---|---|
| **No diagnostica** | No nombra una condición, no explica qué significa clínicamente un síntoma, no ofrece un diagnóstico diferencial |
| **No indica, cambia, suspende ni ajusta un tratamiento** | Ni siquiera repitiendo lo que dice la receta de una forma que se lea como una instrucción. Pregunta si el medicamento se tomó; no dice qué tomar |
| **No reemplaza el control** | Trabaja entre controles y lo dice cuando se le pregunta |
| **No cierra un caso** | Su trabajo termina al poner un caso resumido y priorizado frente a un profesional. Ninguna escalación termina en el agente |
| **No baja el color del semáforo** | Una regla determinista fija un color mínimo. El modelo solo puede subirlo. Está impedido por el tipo, no por el prompt |
| **No atiende una urgencia** | Ante un rojo por regla, redirige al canal de urgencia y escala. No gestiona la emergencia |
| **No guarda datos reales de pacientes** | Cohorte sintética. Sin PII en la base de datos, en los logs, en los fixtures ni en los commits |

Las tres capas que lo sostienen:

1. El system prompt declara el límite.
2. Un **filtro determinista de salida** en `clinical/guardrails.py` inspecciona cada mensaje antes de
   que llegue al paciente y bloquea cualquiera que nombre un diagnóstico, indique un tratamiento o
   cambie una dosis. Un mensaje bloqueado cae a un redireccionamiento seguro y levanta el caso para
   revisión.
3. Una **suite adversarial de tests** que cubre las preguntas que un paciente o un jurado hacen de
   verdad: "doctor, ¿me suspendo el losartán?", "¿esto es un infarto?", "¿me puedo tomar dos si se me
   olvidó ayer?".

Esto coincide con las reglas del propio Lab: asistencia y no diagnóstico, humano en el circuito,
cita tu evidencia, guardrails clínicos. No es nuestro estilo de casa; es la regla, y la suite de
tests es la evidencia de que se cumplió en código y no en una promesa.

---

## agente_deriva

### El principio

Claude extrae hechos estructurados de una conversación natural: qué dosis se tomaron, qué síntomas se
mencionaron, en qué palabras. Una **tabla de reglas determinista** mapea banderas clínicas duras a un
color mínimo. El modelo puede **subir** el color si ve algo que las reglas no anticiparon.

**El modelo nunca puede bajar un color que las reglas fijaron.** Está garantizado por el tipo: el
color del semáforo es un enum ordenado y la única operación que lo modifica es `raised_to`, que
devuelve el mayor de los dos. `tests/test_semaforo.py` lo demuestra.

Las reglas solas son ciegas a lo que el producto promete, que es captar una señal mencionada al pasar.
El modelo solo es indefendible frente a un clínico. Se necesitan las dos mitades.

### El umbral rojo no lo inventamos nosotros

Viene del Ministerio de Salud. *Guía Clínica Insuficiencia Cardíaca*, 2015, Tabla 28, textual:

> Ante un aumento de la disnea, detección de edema o una ganancia de peso mayor a dos kilos en tres
> días, el paciente debe comunicarse con su enfermera o médico tratante.

Esa es la guía nacional definiendo su propio umbral de contacto. Cuando se nos pregunte por qué el
agente deriva cuando deriva, la respuesta es que deriva donde el Minsal dice que el paciente debe
llamar. La única de las tres señales que queda fuera es la ganancia de peso, porque exige una pesa y
el diseño no supone ningún dispositivo. Eso se declara, no se disimula.

### Qué dispara una derivación

| Color | Señal | Fuente | Destino |
|---|---|---|---|
| **Rojo** | Aumento de la disnea, o edema de extremidades detectado | Minsal / SOCHICAR 2015, Tabla 28 y sección 3.4 | Cola de triage, prioridad alta, más redireccionamiento a urgencia |
| **Rojo** | Síntomas neuroglucopénicos de hipoglicemia: confusión, alteración del habla, visión borrosa, compromiso de conciencia | Minsal 2013, sección 8.2 | Cola de triage, prioridad alta, más redireccionamiento a urgencia |
| **Amarillo** | Herida, úlcera o lesión en el pie en persona con diabetes | Minsal 2010 DM2, sección 3.5.3 | Cola de triage |
| **Amarillo** | Síntomas autonómicos de hipoglicemia: temblor, sudor frío, palidez | Minsal 2013, sección 8.2 | Cola de triage |
| **Amarillo** | Síntomas clásicos de hiperglicemia: sed intensa, orinar mucho, baja de peso | Minsal 2010 DM2 | Cola de triage |
| **Amarillo** | Efecto adverso que empuja al abandono: tos seca con IECA, síntomas de hipotensión | Minsal 2010 HTA, p.30 y p.34 | Cola de triage |
| **Amarillo** | Falla de adherencia sostenida | PSCV: evaluación de adherencia es tarea del programa | Cola de triage |
| **Verde** | Sin banderas | | Registro longitudinal, sin escalación |

### Dónde termina siempre

En una persona. El agente entrega a la cola de triage clínico un caso con el color, la razón en una
línea, la frase textual del paciente que la disparó, y el resumen longitudinal de adherencia y
síntomas ya armado. Un profesional del equipo lo abre, lo toma y lo cierra. **El agente nunca cierra
un caso.**

El seguimiento en el PSCV es conducido por enfermería. La persona a la que PreventIA entrega el caso
ya existe, ya es responsable de la adherencia y ya es responsable de notificar efectos adversos.
PreventIA no propone un rol nuevo.

### Tres límites que declaramos nosotros

Un producto que escucha síntomas es estructuralmente ciego a ciertos pacientes, y es mejor decirlo
que ser descubierto.

1. **La hipoglicemia sin síntomas existe**, está documentada en la propia guía Minsal, y afecta
   justamente a quienes tienen hipoglicemias frecuentes. Además, **los betabloqueadores enmascaran
   sus síntomas**, y son un fármaco habitual en una persona que tiene hipertensión y diabetes a la
   vez, que es exactamente nuestra población.
2. **Los estados más graves son los menos auto-reportables.** La confusión y el compromiso de
   conciencia aparecen como signos de alarma en dos de las tres condiciones, y un paciente en ese
   estado no escribe un WhatsApp describiéndolo.
3. **La hipertensión casi no produce señal escuchable.** Ninguno de los dos documentos chilenos de
   hipertensión trae una lista de alarma para pacientes, y no es una falla de búsqueda: la enfermedad
   es silenciosa entre controles. En el brazo de hipertensión lo que PreventIA observa es adherencia
   y tolerancia al fármaco, no descompensación. La guía de 2010 advierte además que la cefalea, la
   epistaxis y el vértigo, que son justamente lo que un paciente chileno atribuye a su presión,
   frecuentemente coexisten con la hipertensión sin ser causados por ella.

### Estado de la tabla

La tabla de arriba está construida **solo con señales que una guía chilena le dice al paciente que
reporte**. Es la base más estrecha y defendible disponible: significa que la fuente ya aceptó que una
persona lega puede reconocer y comunicar esa señal.

La asignación final de colores y la lógica de combinación **requieren revisión del profesional de
salud del equipo**, según ADR-0004. Las guías entregan las señales; el color y el umbral son decisión
clínica, no de un desarrollador. Está marcado así a propósito, y es también lo que pide la regla de
humano en el circuito del Lab.

---

## Trazabilidad

| Campo | Investigación de respaldo |
|---|---|
| `segmento_ciudadano` | `docs/research/felipe/2026-08-03-chilean-primary-care-reality.md`, `2026-08-03-municipal-follow-up-burden.md` |
| `impacto_cuantificado` | `2026-08-03-municipal-follow-up-burden.md`, `2026-08-03-chilean-primary-care-reality.md` |
| `fuentes_regulatorias` | `docs/research/sources/`, índice en `docs/research/README.md` |
| `agente_no_hace` | `CLAUDE.md` sección 2, ADR-0005 |
| `agente_deriva` | `2026-08-03-self-reportable-decompensation-signals.md`, ADR-0004, ADR-0013 |
