# PreventIA — Documento de producto

Este documento define qué es PreventIA, qué hace, qué no hace nunca, y bajo qué criterios clínicos
opera. Está escrito en español porque su lector principal es el profesional de salud del equipo.

El resto de la documentación técnica del repositorio (`CLAUDE.md`, `ROADMAP.md`, `docs/adr/`) está
en inglés.

---

## 1. El problema

En Chile alrededor de 2,4 millones de personas esperan en listas del sistema público. El promedio de
espera supera los 400 días para una consulta de especialidad y los 500 días para cirugía, y el peso
cae sobre personas de menores ingresos, adultos mayores y habitantes de regiones.

Para un adulto mayor polimedicado con hipertensión, diabetes tipo 2 o insuficiencia cardíaca, el
seguimiento real entre un control y el siguiente depende hoy de dos cosas frágiles: su memoria y un
control cada 3 a 6 meses. En el intervalo no hay nadie mirando. Una descompensación que empezó a
insinuarse tres semanas antes llega a urgencias como si hubiera aparecido de golpe.

## 2. Qué es PreventIA

Un acompañante conversacional que hace seguimiento diario al paciente por WhatsApp. Cada día
pregunta por la toma de medicamentos, conversa en lenguaje natural, y escucha. De esa conversación
extrae dos cosas: si las dosis se tomaron, y si aparecieron señales tempranas de descompensación
mencionadas al pasar, no como respuesta a un cuestionario.

Cada interacción queda clasificada en un semáforo de riesgo. Cuando hay una señal real de alarma, y
solo entonces, el caso escala al equipo de salud con un resumen longitudinal ya armado: adherencia
de las últimas semanas, síntomas mencionados, y la razón concreta por la que se levantó la alerta.

**Línea de impacto del Lab: Continuidad y medicina de precisión.** Seguimiento post-tratamiento y
autonomía en el envejecimiento.

## 3. Qué NO hace, nunca

Esto no es una lista de precauciones. Es el límite que define el producto.

- **No diagnostica.** No nombra una condición, no explica qué significa clínicamente un síntoma, no
  ofrece un diferencial.
- **No indica, cambia, suspende ni dosifica un tratamiento.** Pregunta si el medicamento se tomó; no
  dice qué tomar. Ni siquiera repite la receta de una forma que se lea como instrucción.
- **No reemplaza un control.** Opera entre controles y lo dice cuando se lo preguntan.
- **No cierra un caso.** Toda escalación termina en una persona: matrona o médico de cabecera. El
  agente entrega el caso priorizado y resumido, y ahí termina su trabajo.
- **No trabaja con datos reales de pacientes en este repositorio.** Cohorte sintética o el dataset
  anonimizado y agregado que entrega el Lab. Nada más.

La razón de fondo: PreventIA amplía el alcance del equipo clínico entre controles. No toma
decisiones clínicas y no está diseñado para poder tomarlas.

## 4. Población objetivo

Adultos mayores polimedicados con una o más de estas condiciones:

- Hipertensión arterial
- Diabetes mellitus tipo 2
- Insuficiencia cardíaca

Son las tres condiciones donde la adherencia diaria manda, donde la descompensación da señales
observables antes de la urgencia, y donde el intervalo entre controles es más largo de lo que la
enfermedad tolera.

## 5. Criterios del semáforo

El color se decide en dos pasos y en ese orden.

**Paso 1, reglas.** Una tabla determinista de banderas clínicas fija un color **mínimo**. Estas
reglas las define y las revisa el profesional de salud del equipo, no el desarrollador. Viven en
`clinical/rules/` y su fundamento clínico se documenta en `docs/research/`.

**Paso 2, modelo.** El modelo puede **subir** el color si detecta algo que la tabla no anticipó.

**El modelo nunca puede bajar un color que las reglas fijaron.** Esto está garantizado en código, no
en una instrucción al modelo, y hay pruebas automatizadas que lo demuestran.

Interpretación de cada color:

| Color | Qué significa | Qué pasa |
|-------|---------------|----------|
| Verde | Adherencia adecuada, sin señales | Se registra, no se molesta a nadie |
| Amarillo | Adherencia irregular o síntoma leve | Queda en la cola del equipo, sin urgencia |
| Rojo | Señal de alarma clínica | Escala de inmediato al equipo de salud |

El diseño evita deliberadamente el sobre-aviso. Un sistema que alerta demasiado se ignora, y un
sistema ignorado es peor que ninguno, porque genera la sensación de que alguien está mirando.

**Pendiente para el profesional de salud del equipo:** la tabla concreta de banderas por condición.
Esa tabla es entrada clínica, no una decisión de ingeniería, y el prototipo no está completo sin
ella.

## 6. Escalación

La escalación llega a un tablero para el equipo de salud: una lista ordenada por riesgo, rojo
primero, donde cada fila muestra el resumen longitudinal de adherencia y síntomas del paciente.

El criterio de diseño es el tiempo del profesional. La promesa del producto es que el caso se lee en
segundos durante el control siguiente, o en el momento en que llega la alerta roja. Si leer una fila
toma más que eso, la fila está mal diseñada.

## 7. Conversación con el paciente

Todo lo que el paciente lee está en español de Chile, tratando de **usted**, en frases cortas, con
registro llano. Sin jerga clínica, sin abreviaturas, sin anglicismos. El lector es una persona de 80
años leyendo en la pantalla de un teléfono.

Todos los textos que ve el paciente están reunidos en un solo lugar del código para que el
profesional de salud del equipo pueda revisarlos sin leer una línea de Python.

## 8. Datos

**Ahora:** cohorte sintética de adultos mayores construida a mano, con las tres condiciones, cargada
en SQLite. Permite construir y probar antes del Lab y demostrar de forma determinista.

**Durante el Lab:** un adaptador documentado lee el dataset anonimizado y agregado que entrega la
organización a través de MCP, si llega en forma utilizable dentro del tiempo disponible.

La cohorte sintética no es un atajo, es lo que hace reproducible la demo. El dataset anonimizado es
lo que hace creíble la proyección.

## 9. Alcance del prototipo del Lab

**Dentro:**

- Conversación diaria de seguimiento por WhatsApp, en un teléfono real.
- Extracción de adherencia y síntomas desde lenguaje natural.
- Semáforo con piso determinista.
- Registro clínico longitudinal.
- Tablero de triage para el equipo de salud.
- Barrera clínica verificada con pruebas automatizadas.

**Fuera, y es una decisión, no una omisión:**

- Canal de voz. Está en la visión del producto y no en el prototipo de dos días.
- Integración con ficha clínica de una institución.
- Cualquier forma de decisión clínica automatizada.

## 10. Criterio de éxito

Para el Lab, el prototipo está terminado cuando se puede mostrar, en este orden:

1. Un adulto mayor respondiendo una consulta diaria en español natural, en un teléfono real.
2. Un síntoma mencionado al pasar, no como respuesta a una pregunta directa, siendo detectado.
3. El semáforo poniéndose en rojo, con la razón dicha en una línea.
4. La escalación llegando al tablero del equipo con el resumen longitudinal ya armado.
5. El agente negándose a diagnosticar o a cambiar una dosis, y una suite de pruebas que demuestra
   que esa negativa está garantizada en el código y no solamente pedida en una instrucción.

Para el producto más allá del Lab, el criterio es otro: menos reconsultas de urgencia y menos
reingresos hospitalarios evitables en población adulta mayor. Eso no se mide en dos días y no se va
a afirmar como si se hubiera medido.
