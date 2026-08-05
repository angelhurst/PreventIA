# PreventIA — Documento de producto

**Versión 2.1 · 5 de agosto de 2026**

Este es un documento vivo. Define qué es PreventIA, qué hace, qué no hace nunca, y bajo qué
condiciones opera. Cada sección lleva su estado, porque no todas están cerradas al mismo tiempo: lo
que sigue en movimiento vive en `docs/prd-annex.md`, y el historial de cambios al final registra cada
revisión y qué la motivó. Está escrito en español porque su lector principal es el profesional de
salud del equipo. El resto de la documentación técnica del repositorio (`CLAUDE.md`, `ROADMAP.md`,
`docs/adr/`) está en inglés.

---

## 1. El problema

**Estado:** Decidido

Más de dos millones de personas esperan una primera consulta de especialidad en el sistema público:
2.088.245 al 31 de marzo de 2026, con una mediana de 236 días. Para un adulto mayor que ya está en
control, sin embargo, el problema no es la fila.

El Programa de Salud Cardiovascular tiene bajo control a 2,3 millones de personas, y el 65% de ellas
vive con más de una enfermedad crónica. Las garantías GES cubren la entrada: 45 días para confirmar
una hipertensión, 24 horas para iniciar el tratamiento. Ninguna cubre el intervalo. Una vez
compensado el paciente, el programa sugiere un control cada 3 meses si el riesgo cardiovascular es
alto, cada 6 si es moderado, cada 6 a 12 si es bajo. La insuficiencia cardíaca no es siquiera un
problema GES: no tiene plazo garantizado de ninguna clase.

En ese intervalo sí hay alguien mirando, y ahí está el costo. Los equipos municipales de atención
primaria están obligados a rescatar a quien falta a su control, con al menos tres intentos
documentados antes de poder darlo de baja. Nueve de cada diez de los 2.027 establecimientos que
hacen ese trabajo dependen de un municipio. Aun así, una descompensación que empezó a insinuarse
tres semanas antes llega a urgencias como si hubiera aparecido de golpe.

### De dónde salen estas cifras

La versión 1.0 de este documento citaba las cifras de listas de espera que publica el propio Lab en
su wiki de datos. El Lab las atribuye al Ministerio de Salud y a DEIS. Están desactualizadas contra
la Glosa 06, que es el informe trimestral que el mismo Ministerio entrega al Congreso por mandato
legal. La forma de decirlo en el pitch es directa: las cifras del Lab vienen del Minsal; estas son
las del último informe trimestral del Minsal al Congreso, al 31 de marzo de 2026.

| Cifra del Lab | Glosa 06, I trimestre 2026 (corte 31 de marzo) |
|---|---|
| ~2,4 millones en lista de espera | 2.088.245 personas esperando una nueva consulta de especialidad; 2.513.203 registros |
| 330.000–350.000 esperando cirugía | 398.496 personas |
| 400+ días promedio en consulta de especialidad | Promedio 329 días, mediana 236 |
| 500+ días promedio en cirugía | Promedio 383 días, mediana 259 |

Los tiempos de espera han bajado trimestre a trimestre en el período reciente. El pitch no debe
sugerir lo contrario. Fuentes y método en `docs/research/`.

## 2. Qué es PreventIA

**Estado:** Decidido

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

**Estado:** Decidido

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

Este límite no se negocia por sección ni por versión de este documento. Cualquier cambio en el resto
del producto que lo roce se resuelve del lado conservador.

## 4. Población objetivo

**Estado:** Decidido

Adultos mayores polimedicados con una o más de estas condiciones:

- Hipertensión arterial
- Diabetes mellitus tipo 2
- Insuficiencia cardíaca

Son las tres condiciones donde la adherencia diaria manda, donde la descompensación da señales
observables antes de la urgencia, y donde el intervalo entre controles es más largo de lo que la
enfermedad tolera.

"Polimedicado" no es una restricción que nos inventamos para acotar el alcance: es el caso mayoritario
del programa. El 65% de las personas bajo control en el Programa de Salud Cardiovascular vive con más
de una enfermedad crónica, según la evaluación DIPRES de 2018 sobre datos de 2017.

### La primera cohorte: adultos mayores que ya usan WhatsApp

El prototipo es de texto, y el uso de texto en esta población cae con la edad. Entre chilenos de 60 y
más, el uso de mensajes o llamadas de chat en el último mes llega a **78% entre 60 y 69 años, 51%
entre 70 y 79, y 22% de 80 y más**, mientras que usar el teléfono para hablar con alguien se mantiene
en 96%, 90% y 73% (Encuesta Nacional de Calidad de Vida en la Vejez, Centro UC y Caja Los Andes,
2022). Los valores por tramo etario están leídos de un gráfico del informe y su verificación contra
el PDF original queda pendiente antes de ponerlos en una lámina; los totales sí están citados del
texto.

La decisión es nombrar la cohorte en vez de dejarla implícita: **la primera cohorte son adultos
mayores polimedicados que ya usan WhatsApp**. Es la mayoría de la población entre 60 y 79 años, es
una decisión de alcance y no una limitación escondida, y deja explícito que el siguiente tramo
—los pacientes de más edad, que son también los de mayor necesidad clínica— requiere otra modalidad
y es la cohorte siguiente, no un detalle pendiente.

## 5. Cómo se decide el color

**Estado:** Bloqueado en clínico

El color se decide en dos pasos y en ese orden.

**Paso 1, reglas.** El agente extrae hechos estructurados de la conversación: qué dosis se reportaron
tomadas, qué síntomas se mencionaron, con qué palabras. Una tabla determinista de banderas clínicas
mapea esos hechos a un color **mínimo**. La tabla vive en `clinical/rules/` y es data, no lógica:
por eso su comportamiento se puede enumerar y sus casos borde se pueden fijar como pruebas.

**Paso 2, modelo.** El modelo puede **subir** el color si detecta algo que la tabla no anticipó.

**El modelo nunca puede bajar un color que las reglas fijaron.** Esto está garantizado en código, no
en una instrucción al modelo, y `tests/test_semaforo.py` lo demuestra. Es también la frase más clara
que tenemos frente a un juez clínico: ninguna salida del modelo puede degradar una bandera roja.

Qué pasa con cada color:

| Color | Qué pasa |
|-------|----------|
| Verde | Se registra, no se molesta a nadie |
| Amarillo | Queda en la cola del equipo, sin urgencia |
| Rojo | Escala de inmediato al equipo de salud |

El diseño evita deliberadamente el sobre-aviso. Un sistema que alerta demasiado se ignora, y un
sistema ignorado es peor que ninguno, porque genera la sensación de que alguien está mirando. Dicho
eso, un piso solo sube: el sistema va a sobre-alertar respecto de un clasificador perfectamente
afinado, y esa asimetría es intencional, porque sub-alertar es el modo de falla que le hace daño a
una persona.

**Lo que este documento no decide.** La tabla de banderas —qué señal corresponde a qué color, para
cada condición— es entrada clínica y la escribe el profesional de salud del equipo, no un
desarrollador. Vive en `docs/prd-annex.md` mientras se construye, y el prototipo no está completo sin
ella. La ingeniería puede construir y probar el motor contra banderas de relleno; publicar criterios
clínicos de relleno sería peor que no publicar nada.

Una pregunta abierta que la tabla tiene que resolver antes de escribirse: el Programa de Salud
Cardiovascular ya varía sus metas según edad y estado de fragilidad, de modo que "compensado" no es
un número único. Si la tabla debe ser sensible a fragilidad es una decisión clínica, y está en la
lista de preguntas al profesional de salud en `docs/research/README.md`.

## 6. Escalación y tablero clínico

**Estado:** En revisión

La escalación llega a un tablero web para el equipo de salud: una lista ordenada por riesgo, rojo
primero, donde cada fila muestra el resumen longitudinal de adherencia y síntomas del paciente ya
armado. El tablero lee del registro clínico en SQLite y no lee transcripciones.

El criterio de diseño es el tiempo del profesional. La promesa del producto es que el caso se lee en
segundos durante el control siguiente, o en el momento en que llega la alerta roja. Si leer una fila
toma más que eso, la fila está mal diseñada, no el lector.

Una cola que nadie mira no interrumpe a nadie. Un despliegue real necesita además un canal de aviso
que empuje la alerta; eso es un problema de piloto, no del prototipo.

**Lo que falta.** El tablero es la única superficie que toca un profesional, y es la pieza que no se
puede diseñar una sola vez para todos: lo que un equipo de CESFAM puede accionar no es lo que puede
accionar un servicio hospitalario o una caja. Quedan pendientes dos listas explícitas —qué debe
contener el tablero y qué no debe contener nunca, incluida cualquier inferencia presentada como
hallazgo o cualquier campo que lo convierta en una ficha clínica paralela— y la separación entre lo
invariante, que construimos, y lo configurable por institución. Ese trabajo es el workstream 8 y sus
resultados van a `docs/prd-annex.md`.

**El guardián.** El flujo del piloto dibujado en
`docs/diagrams/2026-08-03-flujo-piloto-quinta-normal.excalidraw` (v0.0.1) incluye un paso en que la
doctora, al inscribir a la paciente, designa o no designa un guardián: un familiar o cuidador. Ese
elemento **no está definido** en ninguna parte del repositorio. Qué recibe, quién lo designa, si es
un campo que la institución ya tiene o un concepto que estaríamos inventando, y qué cambia aguas
abajo, es el workstream 7. Hasta que esté resuelto, el guardián no forma parte del alcance del
prototipo.

## 7. Conversación con el paciente

**Estado:** Decidido

Todo lo que el paciente lee está en español de Chile, tratando de **usted**, en frases cortas, con
registro llano. Sin jerga clínica, sin abreviaturas, sin anglicismos. El lector es una persona de 80
años leyendo en la pantalla de un teléfono.

Todos los textos que ve el paciente están reunidos en un solo lugar del código para que el
profesional de salud del equipo pueda revisarlos sin leer una línea de Python.

Dos reglas más, que la evidencia sostiene:

- **Nunca exigirle al paciente escribir más que unas pocas palabras.** La habilidad limitante en esta
  población es componer, no comprender. La forma por defecto de una pregunta es la que se contesta
  con "sí", "no" o una palabra. El texto libre siempre se acepta y nunca se exige.
- **Todo estado de falla lo repara el sistema, no el paciente.** En 2022, el **52,9%** de los
  chilenos de 60 y más se calificó a sí mismo con 3 o menos en una escala de 7 al evaluar su
  capacidad de usar internet para informarse o hacer un trámite. Un paciente confundido no va a
  explorar la interfaz para salir del problema: el mensaje siguiente tiene que hacer la reparación.

## 8. Datos

**Estado:** En revisión

**Ahora:** cohorte sintética de adultos mayores construida a mano, con las tres condiciones, cargada
en SQLite. El registro clínico —pacientes, medicamentos, contactos diarios, síntomas extraídos,
eventos de riesgo y escalaciones— vive en SQLite. Las transcripciones crudas de conversación no:
esas las guarda el gestor de sesiones en archivos, y nada las consulta salvo el propio agente.

La cohorte sintética no es un atajo, es lo que hace reproducible la demo: el mismo paciente, la misma
conversación, la misma bandera roja, en cada toma.

**Durante el Lab:** el Lab publica datasets curados, anonimizados y agregados, al abrir la
convocatoria. Para nuestra línea son egresos hospitalarios y datos agregados de crónicos.

**El hallazgo que cambia el diseño del adaptador.** La versión 1.0 y el ADR-0007 describen un
adaptador que lee el dataset del Lab "en el mismo esquema". Contra datos genuinamente **agregados**
eso no es posible, porque un dato agregado no tiene una fila por persona que poner en una tabla de
pacientes. Lo que sí es posible, y es a la vez más chico y más defendible, es un adaptador que lee
los agregados y **calibra la cohorte sintética**: distribución etaria, razón por sexo, distribución
por comuna, prevalencia de condiciones, tasa de multimorbilidad. La frase del pitch sale sola: la
cohorte es sintética, su forma viene de los agregados anonimizados de la propia institución, y
podemos decir exactamente qué es qué.

**Esto todavía no está adoptado.** El ADR-0007 está Aceptado y es inmutable. Cambiar el diseño del
adaptador exige un ADR nuevo que lo supersede, y ese ADR no está escrito. Hasta que lo esté, la
sección queda en revisión.

**Una precondición de despliegue que hay que nombrar antes de que la pregunten.** PreventIA supone un
número de WhatsApp que funciona. El registro chileno dice que el sistema de salud frecuentemente no
lo tiene: el estudio chileno más grande de adherencia a antihipertensivos perdió 443 de 956 pacientes
muestreados, y de esos, 245 fueron por error en la información de contacto, sobre una muestra sacada
de un registro PSCV vivo. Un rescate escala a visita domiciliaria precisamente cuando el teléfono
falla. Los pacientes cuyo número está malo son sistemáticamente los que más probablemente se
descompensan sin que nadie lo vea. Cuánto cuesta y cómo se mantiene un número vigente en un CESFAM es
una de las preguntas abiertas al profesional de salud del equipo.

## 9. Alcance del prototipo del Lab

**Estado:** Decidido

**Dentro:**

- Conversación diaria de seguimiento por WhatsApp, en un teléfono real.
- Extracción de adherencia y síntomas desde lenguaje natural.
- Semáforo con piso determinista.
- Registro clínico longitudinal.
- Tablero de triage para el equipo de salud.
- Barrera clínica verificada con pruebas automatizadas.

**El canal.** Es el número de prueba de la WhatsApp Cloud API de Meta, detrás de un adaptador de
canal. Es gratis, no exige verificación de negocio, se aprovisiona en menos de 30 minutos y manda
mensajes reales de WhatsApp a teléfonos reales. Habla únicamente con hasta **cinco números
destinatarios verificados por OTP**, que es una limitación de producción y exactamente el aislamiento
que una demo quiere. Nada por debajo de `channels/` sabe qué es WhatsApp, y existe un canal de
consola local que implementa la misma interfaz sin telefonía alguna.

**El motor.** PreventIA no está atado a un proveedor de modelo. La construcción del modelo vive en un
solo archivo, `agent/models.py`, y ningún otro módulo sabe quién contestó. Cambiar de proveedor es
una variable de entorno, no una reescritura. En el Lab corre sobre Claude. La vía de despliegue
documentada es un modelo abierto servido por Ollama dentro de la propia institución, de manera que
las conversaciones con pacientes pueden quedarse en hardware que la institución controla, que es lo
que un servicio de salud necesita poder decidir por su cuenta. Tampoco hay un framework de agentes de
por medio: el orquestador es código propio, y por eso el semáforo, el filtro de salida y el registro
clínico no dependen del comportamiento de la librería de un tercero (ADR-0010 y ADR-0012).

**Fuera, y es una decisión, no una omisión:**

- **Canal de voz.** El uso de texto cae con la edad justo donde sube la necesidad clínica, y esa
  brecha es real y está medida (sección 4). La voz es la cohorte siguiente, no un adorno pendiente.
  Su costo tampoco es una tarde: transcribir audio agrega un componente que no está en la
  arquitectura actual, y un error de transcripción que convierte un síntoma en otro es un error
  clínico introducido por una pieza de ingeniería, que ni el piso determinista ni el filtro de salida
  detectarían. Una llamada de voz por WhatsApp, además, corre por una API distinta de disponibilidad
  limitada.
- Integración con ficha clínica de una institución.
- Cualquier forma de decisión clínica automatizada.

**Y una cosa que sí entra, porque es barata y el producto no puede permitirse lo contrario:** una
nota de voz que llega se contesta. Los pacientes que no escriben mandan audio. Ignorar un audio en
silencio se ve, para una persona de 80 años, exactamente igual que no estar siendo escuchada, que es
la única cosa que este producto no puede parecer. Una respuesta fija pidiéndole que escriba es
suficiente mientras la transcripción esté fuera de alcance.

## 10. Criterio de éxito

**Estado:** Decidido

Para el Lab, el prototipo está terminado cuando se puede mostrar, en este orden:

1. Un adulto mayor respondiendo una consulta diaria en español natural, en un teléfono real.
2. Un síntoma mencionado al pasar, no como respuesta a una pregunta directa, siendo detectado.
3. El semáforo poniéndose en rojo, con la razón dicha en una línea.
4. La escalación llegando al tablero del equipo con el resumen longitudinal ya armado.
5. El agente negándose a diagnosticar o a cambiar una dosis, y una suite de pruebas que demuestra
   que esa negativa está garantizada en el código y no solamente pedida en una instrucción.

Más allá del Lab, el argumento que se sostiene primero es el de la carga de trabajo, porque no
depende de evidencia que todavía no tenemos. El rescate de inasistentes es una obligación con al
menos tres intentos documentados, la cargan 2.027 establecimientos de los cuales el 90,7% depende de
un municipio, y desplazar parte de ese trabajo se sostiene en el mandato y en la escala, aunque el
efecto clínico fuera cero. Ese es el argumento que hay que poner delante de un juez de criterio de
gestión.

Después viene el clínico, y hay que decirlo con lo que la evidencia efectivamente respalda:

Para el producto más allá del Lab, el criterio es otro: menos reconsultas de urgencia y menos
reingresos hospitalarios evitables en población adulta mayor. Eso no se mide en dos días y no se va a
afirmar como si se hubiera medido.

Hay que decir además lo que ya se sabe. Chile automatizó el contacto con pacientes a escala nacional
con el sistema de recordatorios de FOFAR, y la evaluación del propio Estado, sobre 4.481.282 horas,
encontró un efecto marginal. Y el ensayo que comparó de frente mensajes interactivos contra mensajes
de una sola vía en 1.372 hipertensos no encontró diferencia entre ambos. La evidencia que sí es
positiva, en insuficiencia cardíaca, corresponde a seguimiento telefónico estructurado conducido por
enfermería y a telemonitoreo dentro de un servicio clínico.

Eso es precisamente lo que separa a un recordatorio de lo que hace PreventIA: el caso termina en una
persona del equipo de salud que puede actuar sobre él. No prometemos el resultado clínico. Sostenemos
que la arquitectura es la que la evidencia disponible respalda, y que la carga de trabajo que
desplaza el sistema no depende de ese resultado.

### La vía de escalamiento

El propio Lab describe su retorno a la inversión por la cadena de las licencias médicas: la COMPIN
valida las licencias, las cajas de compensación como La Araucana pagan el subsidio, y la SUSESO
supervigila. La Araucana pone en esa cadena del orden de mil millones de pesos al año. Una licencia
médica es un beneficio de trabajador, y la población de PreventIA son personas mayores, de modo que
la economía que describe la institución anfitriona no pasa por nuestra población objetivo.

**Eso no cambia el alcance.** Lo que se dice es lo siguiente: la misma arquitectura aplicada a
pacientes crónicos en edad de trabajar —la mayoría de los 2,3 millones bajo control del Programa de
Salud Cardiovascular, que cubre desde los 15 años— cae directamente sobre la cadena
COMPIN–caja–SUSESO, y eso es lo que mediría un piloto. No cuesta nada decirlo, muestra que leímos el
brief, y responde al juez de criterio de gestión antes de que pregunte.

Este argumento acompaña al de la carga municipal, no lo reemplaza. El de la carga es el que se
sostiene sin evidencia que nos falte; el de las licencias es el que la institución anfitriona
reconoce como plata.

---

## Historial de cambios

| Versión | Fecha | Qué cambió | Origen |
|---|---|---|---|
| 2.1 | 2026-08-05 | Sección 9 gana el párrafo "El motor": el producto no está atado a un proveedor de modelo, el cambio de proveedor es una variable de entorno, la vía de despliegue documentada deja las conversaciones en hardware de la institución, y no hay framework de agentes entre el semáforo, el filtro de salida y el registro. La propiedad ya estaba decidida en los ADR pero no aparecía en ningún documento de producto | ADR-0010 y ADR-0012 |
| 2.0 | 2026-08-05 | Cada sección lleva estado. Sección 1 reescrita completa: las cifras de listas de espera se corrigen contra la Glosa 06 al 31 de marzo de 2026 y se explicita que vienen del propio Minsal, y se elimina "en el intervalo no hay nadie mirando", que era falso respecto del rescate de inasistentes. Sección 4 nombra la primera cohorte y agrega el 65% de multimorbilidad del PSCV. Sección 5 pasa a describir solo el mecanismo; la tabla de banderas se mueve a `docs/prd-annex.md`. Sección 6 incorpora el tablero del ADR-0006 y marca como pendientes el guardián y las listas de contenido y exclusión. Sección 7 agrega dos reglas de copy. Sección 8 registra que un adaptador contra datos agregados calibra la cohorte en vez de poblarla, pendiente de un ADR que supersede al 0007, y nombra la calidad del dato de contacto como precondición de despliegue. Sección 9 fija el canal, el porqué de dejar la voz fuera y la respuesta a notas de voz. Sección 10 lidera con el argumento de carga, ajusta el párrafo de evidencia a lo que los estudios sostienen y nombra la cadena COMPIN–caja–SUSESO como vía de escalamiento | Workstreams 1 a 6 en `docs/research/felipe/`, propuestas P1, P2, P3, P5, P6, P7, P8, P9, P10 y P12 en `docs/research/README.md`; workstreams 7 y 8 briefeados y aún no ejecutados; ADR-0002, 0003, 0004, 0006, 0007 y 0010 |
| 1.0 | 2026-08-03 | Versión inicial | Diseño del producto y ADR-0001 a 0009 |
