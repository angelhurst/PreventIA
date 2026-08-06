# Entregable técnico — campos del formulario del Lab

Texto listo para copiar. Cada afirmación apunta al archivo que la hace cumplir en el código, no a una
promesa. Las URLs se verificaron el 6 de agosto de 2026 y respondieron 200.

## fuentes_regulatorias

Las reglas clínicas de PreventIA no son criterio propio: cada bandera del semáforo cita la guía
ministerial de la que sale, y esa cita vive en `preventia/clinical/rules/flags.py`.

1. **Minsal, Guía Clínica Hipertensión Arterial Primaria o Esencial en personas de 15 años y más**
   https://diprece.minsal.cl/wrdprss_minsal/wp-content/uploads/2014/12/Hipertensi%C3%B3n-Arterial-en-personas-de-15-a%C3%B1os-y-m%C3%A1s.pdf
   Origen de las banderas de efecto adverso que sostienen la adherencia: tos seca persistente y mareo
   al ponerse de pie.

2. **Minsal, Guía de Práctica Clínica Hipertensión Arterial 2018, resumen ejecutivo**
   https://diprece.minsal.cl/wp-content/uploads/2019/05/08.-RE_GPC-HTA-Final_2018v5.pdf

3. **Minsal, Guía Clínica Diabetes Mellitus Tipo 1**
   https://diprece.minsal.cl/wrdprss_minsal/wp-content/uploads/2014/12/Diabetes-Mellitus-tipo-1.pdf
   Origen de las banderas de hipoglicemia: confusión, alteración del habla, visión borrosa, temblor,
   sudor frío y palidez.

4. **Minsal, Orientación Técnica Programa de Salud Cardiovascular**
   https://redcronicas.minsal.cl/wp-content/uploads/2017/08/OT-PROGRAMA-DE-SALUD-CARDIOVASCULAR_05.pdf
   Origen del criterio de rescate por inasistencia y de la bandera de dosis no tomadas.

5. **Minsal, acceso a las Guías Clínicas AUGE**
   https://diprece.minsal.cl/le-informamos/auge/acceso-guias-clinicas/guias-clinicas-auge/

El razonamiento clínico detrás de cada bandera, con lo que la fuente dice y lo que no dice, está en
`docs/research/felipe/2026-08-03-self-reportable-decompensation-signals.md`. Ese documento
deliberadamente **no** asigna colores: la asignación es decisión clínica y quedó registrada aparte.

## agente_no_hace

- **No diagnostica.** No nombra una condición, no explica qué significa clínicamente un síntoma y no
  ofrece un diferencial. Bloqueado en `preventia/clinical/guardrails.py`.
- **No indica, cambia, suspende ni ajusta un tratamiento o una dosis.** Pregunta si la persona tomó
  su medicamento; nunca le dice qué tomar. Bloqueado en el mismo filtro.
- **No reemplaza un control.** Trabaja entre controles y lo dice cuando se le pregunta.
- **No cierra un caso.** Su trabajo termina al dejar el caso resumido y priorizado frente al equipo
  de salud.
- **El modelo no puede bajar un color.** El piso lo fija una tabla determinista; el modelo solo puede
  subirlo. Está en el tipo (`preventia/clinical/semaforo.py`), en el esquema de la base de datos como
  restricción `CHECK`, y demostrado en `tests/test_semaforo.py`.
- **Un caso rojo no se apaga solo.** Sigue rojo hasta que una persona del equipo cambia su estado,
  aunque el paciente escriba después que está bien.
- **No transcribe audio.** Una nota de voz recibe una respuesta fija pidiendo texto, y no llega al
  agente. Un error de transcripción sería un error clínico introducido por ingeniería que ni el piso
  determinista ni el filtro de salida detectarían.

El filtro de salida no es una instrucción en el prompt: revisa cada mensaje antes de que salga y lo
reemplaza si cruza una de estas líneas. La suite adversarial que lo prueba se puede correr delante de
un evaluador.

## agente_deriva

- **Bandera clínica de la tabla determinista en rojo.** El caso entra rojo a la cola del equipo y a
  la persona se le pide contactar hoy su consultorio, con el 131 y el servicio de urgencia como
  alternativa si empeora.
- **El modelo sube el color a rojo por su cuenta.** El caso escala igual, y a la persona se le dice
  que su equipo de salud ya fue avisado. No se le da una instrucción de urgencia, porque esa
  instrucción está reservada a una bandera clínica con fuente.
- **Señales de crisis de salud mental.** La detección de ideación suicida o autolesión desvía de
  inmediato a contacto humano, fuera del triaje de hipertensión y diabetes.
- **El filtro de salida bloquea un mensaje.** La persona recibe una respuesta segura que dice que no
  es médico, y el caso queda marcado para revisión del equipo.
- **Adherencia incompleta sostenida.** Las dosis no tomadas levantan el color a amarillo según el
  criterio de rescate del Programa de Salud Cardiovascular.

En los cinco casos la derivación termina en una persona identificada, con registro de quién cambió el
estado y cuándo.

## Cómo se evalúa

La rúbrica del Lab, con el peso de cada bloque y qué campo la responde.

| Bloque | Peso | Criterio | Cómo se evalúa | Qué lo responde |
|---|---|---|---|---|
| Problema y población | 12% | La población está nombrada de forma específica, no "los pacientes" (50%) | Campo `segmento_ciudadano`: condición de salud o etapa vital más un eje adicional: edad, territorio, sistema previsional | `docs/entregable-tecnico.md`, sección `segmento_ciudadano` |
| Problema y población | 12% | El impacto está cuantificado con un número y una fuente oficial verificable (50%) | Campos `impacto_cuantificado` y `fuente_impacto_url`, en dominio oficial | `docs/entregable-tecnico.md`, sección `impacto_cuantificado` |
| Responsabilidad clínica | 12% | Cita al menos 2 fuentes oficiales de salud con URL (50%) | Campo `fuentes_regulatorias` con dos o más URLs de organismos oficiales | Este documento, `fuentes_regulatorias`: cinco fuentes Minsal |
| Responsabilidad clínica | 12% | Declara explícitamente qué no hace el agente y cuándo deriva a un profesional (50%) | Campos `agente_no_hace` y `agente_deriva` del entregable técnico | Este documento, ambas secciones |
| Construyó con Claude | 16% | El mentor vio el agente funcionando, aunque sea parcialmente (50%) | Observación directa del mentor en el venue. No requiere subir nada | Pantalla `/consulta`: entra el mensaje del paciente, sale el color y la respuesta |
| Construyó con Claude | 16% | Claude es el motor de la solución, no un agregado decorativo (50%) | Observación del mentor: si se saca a Claude, ¿la solución deja de funcionar? | `preventia/clinical/extraction.py`: sin el modelo no hay extracción de adherencia ni de síntomas, y el semáforo queda sin hechos que evaluar |

Dos advertencias sobre este cuadro, para que nadie las descubra por nosotros.

**Los dos campos que puntúa "Problema y población" no están en este archivo.** Viven en
`docs/entregable-tecnico.md`. Si el formulario se llena desde aquí, hay que ir a buscarlos allá.

**El segundo criterio de "Construyó con Claude" tiene una respuesta honesta y una trampa.** Sin Claude
no hay extracción: nadie convierte "ando con harta tos seca en la noche" en un hecho estructurado. Lo
que sí sigue funcionando sin Claude es la mitad determinista, y eso es deliberado: el piso del
semáforo, el filtro de salida y la detección de crisis son código, no modelo. Conviene decirlo en ese
orden. Claude es el motor de la comprensión; las barreras clínicas están puestas para no depender de
él.
