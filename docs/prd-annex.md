# PreventIA — Anexo del documento de producto

**Versión 1.0 · 5 de agosto de 2026**

`PRD.md` contiene lo que está resuelto: qué es el producto, qué no hace nunca, y bajo qué criterios
opera. Este anexo contiene lo que todavía está en movimiento, para que el documento estable no tenga
que reescribirse cada vez que una de estas piezas cambia. Cada sección lleva su propio estado, y ese
estado es lo primero que hay que leer.

Los estados posibles son cuatro: `Decidido`, `En revisión`, `Bloqueado en clínico`, `Sin definir`.

Ninguna cifra de este anexo es nueva. Todas provienen de `docs/research/` y de las fuentes archivadas
en `docs/research/sources/`. Donde algo no se sabe, se dice que no se sabe y se dice qué lo
resolvería.

---

## A1. Tabla de banderas por condición

**Estado:** Bloqueado en clínico

### Quién escribe esta tabla

ADR-0004 deja la autoría de la tabla de reglas en `clinical/rules/` al profesional de salud del
equipo, no al desarrollador. Esta sección reúne material candidato y no decide nada. **No hay ningún
color asignado aquí**, no se propone ningún umbral de escalación, y no se propone lógica de
combinación entre señales.

El criterio de selección del material es el más estrecho que había disponible: cada señal listada
abajo es una señal que **una guía le pide al paciente reportar**. Eso significa que la fuente ya
aceptó que una persona sin formación clínica puede reconocerla y comunicarla. No significa que la
señal sea sensible, específica, ni utilizable en la forma particular en que PreventIA quiere usarla.

Dos propiedades acompañan a cada candidata porque son propias de este producto y no de la medicina:
**sin dispositivo**, es decir si el paciente puede producir la señal solo con su cuerpo y su memoria;
y **espontánea plausible**, es decir si podría aparecer en una conversación cualquiera y no solo como
respuesta a una pregunta directa. La segunda es un juicio sobre conversación, no sobre medicina.

Todo esto está en el taller de investigación 1
(`docs/research/felipe/2026-08-03-self-reportable-decompensation-signals.md`), con las citas
completas y las páginas exactas.

### Calidad de la fuente por condición

| Condición | Fuente chilena oficial encontrada | Calidad para este uso |
|---|---|---|
| Insuficiencia cardíaca | MINSAL / SOCHICAR, *Guía Clínica Insuficiencia Cardíaca*, 2015 | Fuerte. Tiene una lista de alerta escrita para el paciente y una tabla de educación. |
| Diabetes tipo 2 | MINSAL, *Guía Clínica Diabetes Mellitus tipo 2*, 2010 | Parcial. Da los síntomas clásicos de hiperglicemia; no tiene lista de hipoglicemia para el paciente. |
| Hipoglicemia | MINSAL, *Guía Clínica Diabetes Mellitus Tipo 1*, 2013 | La lista existe textual, pero es la guía de **tipo 1**. |
| Hipertensión | MINSAL 2010 y resumen ejecutivo GPC 2018 | Débil por contenido, no por acceso. Ninguno de los dos documentos tiene lista de alerta para el paciente. |

Advertencia de vigencia, porque va a preguntarse en el Lab: la guía de insuficiencia cardíaca declara
un plazo estimado de vigencia de 5 años desde su publicación en 2015. Las búsquedas del 3 de agosto
de 2026 no encontraron una guía MINSAL posterior. **No verificado** que no exista; lo verificaría
leer directamente el índice de guías clínicas de DIPRECE o preguntarle a MINSAL.

### Insuficiencia cardíaca

De la lista *Signos y Síntomas de Alerta*, MINSAL / SOCHICAR 2015, sección 3.4, p.73:

| Señal candidata | Sin dispositivo | Espontánea plausible | Nota |
|---|---|---|---|
| Aumento brusco de peso superior a 2 kg en 3 días | **No**, necesita balanza | Solo si el paciente ya se pesa | Es la señal más citada y la menos compatible con un diseño sin dispositivo. |
| Edema de extremidades, habitualmente en los tobillos | Sí | Sí | Los pacientes lo ofrecen solos ("se me hincharon los pies"). |
| Anuria o poliuria | Sí | En parte | El paciente no usa esas palabras. Reporta un cambio en la frecuencia con que orina. |
| Disnea de pequeños esfuerzos, disnea paroxística nocturna, ortopnea | Sí | Sí, en lenguaje llano | Se describe como cansarse en la escalera, despertar con falta de aire, necesitar más almohadas. |
| Tos, cansancio generalizado | Sí | Sí | Baja especificidad. La tos choca con un efecto adverso de los IECA en la misma población. |
| Problemas de memoria o confusión | Sí | **Lo reportan terceros, no el paciente** | Un paciente confundido es el menos probable de reportar confusión. |

De la tabla de educación al paciente, Tabla 28, p.73, dos candidatas más:

| Señal candidata | Sin dispositivo | Espontánea plausible | Nota |
|---|---|---|---|
| Pérdida del apetito o náuseas | Sí | Sí | Se menciona al pasar con facilidad. |
| Aumento de la frecuencia cardíaca | En parte | Sí, como palpitaciones | La guía la enuncia como una frecuencia medible. Si la sensación sirve como sustituto es una pregunta clínica. **REQUIERE REVISIÓN CLÍNICA.** |

**El umbral que la propia guía define.** La misma tabla dice, textual: "Ante un aumento de la disnea,
detección de edema o una ganancia de peso mayor a dos kilos en tres días, el paciente debe
comunicarse con su enfermera o médico tratante". Es lo más parecido a una regla de escalación ya
escrita que existe en cualquiera de los documentos consultados. Se ofrece como punto de partida para
quien escriba la tabla, y nada más que eso.

**El problema del peso, dicho de frente.** La regla de 2 kg en 3 días aparece dos veces en la guía,
es la señal más precisa de las tres condiciones, y necesita una balanza. PreventIA no supone ningún
dispositivo. Hay tres caminos y el anexo no elige: aceptar que esa señal queda fuera, preguntar si el
paciente tiene balanza y usarla solo en quienes la tengan, o buscar un sustituto sin dispositivo. El
tercero es el tentador y es el peligroso: los sustitutos que se repiten habitualmente, como que el
anillo, el zapato o el cinturón queden apretados, **no aparecen en ninguno de los documentos chilenos
consultados**. Está marcado como no verificado y no debe entrar en la tabla por parecer razonable.

**Depresión, listada aparte por la misma guía.** Tabla 28, p.74, enumera tristeza constante,
decaimiento, irritabilidad, impotencia, frustración, bajo rendimiento y reducción del nivel de
actividad habitual. Son señales conversacionales casi por definición y se acumulan en días, que es
justamente lo que un contacto diario está bien puesto para notar. Si PreventIA debe actuar sobre
ellas es a la vez una decisión clínica y una decisión de alcance del producto.

### Diabetes tipo 2, hiperglicemia

MINSAL 2010 da los síntomas clásicos: polidipsia, poliuria, polifagia y baja de peso. Los cuatro son
reportables sin dispositivo, con distinta facilidad.

**El límite que pesa sobre los cuatro:** son los criterios **diagnósticos** de la guía para detectar
diabetes no diagnosticada, no una lista validada de señales de descompensación en alguien que ya
tiene el diagnóstico. Usarlos como banderas de descompensación es una extrapolación que la fuente no
hace. **REQUIERE REVISIÓN CLÍNICA.**

**Pie diabético.** La misma guía enseña al paciente a reconocer y anticipar problemas en sus pies, e
incluye la autoexploración como procedimiento enseñado. Una herida o úlcera en el pie es la única
candidata de todo el material con carácter simultáneamente sin dispositivo, de alta especificidad y
observable por el propio paciente. También es aquella donde el encuadre de la guía es prevención en
meses y no descompensación en días, lo que puede o no calzar con un contacto diario.
**REQUIERE REVISIÓN CLÍNICA.**

### Diabetes tipo 2, hipoglicemia

La guía chilena de tipo 2 manda educar sobre hipoglicemia pero no enumera los síntomas. La lista
enumerada se encontró en la guía de **tipo 1**, 2013, sección 8.2: síntomas autonómicos (palidez,
temblor, sudoración fría, taquicardia), neuroglucopénicos (alteración del juicio y conducta,
confusión, compromiso de conciencia, visión borrosa, alteración del habla, convulsiones) e
inespecíficos (irritabilidad, terrores nocturnos, llanto, náuseas, hambre, cefalea).

Tres advertencias, y las tres necesitan a un clínico:

1. **Es la guía de tipo 1.** Si esa lista aplica a adultos mayores con diabetes tipo 2, con
   hipoglicemiantes orales o insulina, es exactamente el tipo de extrapolación que este proyecto no
   puede hacer por cuenta propia. **REQUIERE REVISIÓN CLÍNICA.**
2. **La misma sección documenta que hay pacientes sin síntomas**, en particular quienes tienen
   hipoglicemias frecuentes. Un producto que escucha síntomas es estructuralmente ciego frente a los
   pacientes de mayor riesgo. Esto pertenece al pitch como limitación declarada, no como algo que
   descubra un jurado.
3. **Los betabloqueadores enmascaran los síntomas**, según la propia guía chilena de hipertensión de
   2010, p.34. En una población polimedicada con hipertensión y diabetes a la vez, que es exactamente
   la de PreventIA, esa combinación es rutina y no un caso de borde.

### Hipertensión

**El hallazgo es que casi no hay nada que escuchar.** Ninguno de los dos documentos chilenos contiene
una lista de alerta dirigida al paciente. No es una falla de búsqueda: el resumen ejecutivo de 2018
es un conjunto de recomendaciones GRADE de tratamiento, y la guía de 2010 discute síntomas solo en el
contexto de efectos adversos de fármacos, hipertensión secundaria y crisis hipertensiva. Entre
controles, la hipertensión es silenciosa para la mayoría de los pacientes la mayor parte del tiempo.
Lo que PreventIA puede observar en el brazo de hipertensión es adherencia y tolerancia al fármaco, no
descompensación.

Lo que sí hay son efectos adversos que empujan al abandono del tratamiento: tos seca con IECA,
documentada entre 7 y 15%; síntomas de hipotensión, que el paciente reporta como mareo al pararse; y
fatiga, cefalea, insomnio y ánimo bajo con betabloqueadores, de muy baja especificidad. Son los
síntomas que hacen que un adulto mayor deje de tomar una pastilla en silencio, y notar eso está
dentro de lo que la sección 3 del PRD permite hacer sin interpretar nada.

**Y hay un antipatrón explícito, dicho por la propia guía.** MINSAL 2010, sección 3.2.10, p.41
advierte que pacientes con cifras elevadas sin síntomas consultan en urgencia por síntomas
inespecíficos "que coexisten con la HTA pero no son producidos por ella, tales como epistaxis,
vértigo paroxístico benigno, cefaleas tensionales o migraña", y que en esas situaciones el manejo
agresivo puede ser peligroso. Cefalea, epistaxis y mareo son justamente los síntomas que un paciente
chileno atribuye a su presión. Una regla ingenua que mapee "me duele la cabeza" a una alarma de
hipertensión estaría equivocada y apuntada en una dirección con daño documentado aguas abajo. La
tensión con ADR-0004, que acepta el sobre-aviso como el modo de falla seguro, es real y este anexo no
la resuelve. **REQUIERE REVISIÓN CLÍNICA.**

### Advertencias que cruzan las tres condiciones

1. **La tos pertenece a dos condiciones a la vez.** Señal de alerta de insuficiencia cardíaca y
   efecto adverso de IECA en 7-15%, en una población que probablemente tenga ambas.
2. **Fatiga, cefalea y ánimo bajo aparecen en tres listas distintas** a la vez: alerta de
   insuficiencia cardíaca, depresión, y efectos adversos de betabloqueadores. Aisladas discriminan
   poco.
3. **Los betabloqueadores enmascaran la hipoglicemia**, en exactamente el paciente objetivo.
4. **Los estados más graves son los menos auto-reportables.** Confusión, compromiso de conciencia y
   alteración del habla figuran como alerta en dos listas, y un paciente en cualquiera de esos
   estados no manda un mensaje describiéndolo. Lo alcanzable es el silencio, o un cambio en cómo
   escribe. Si la ausencia de respuesta debe ser una bandera está sin resolver y no está en el PRD.
5. **La señal cuantificada más fuerte necesita una balanza.**

### La advertencia de fragilidad, P4

El PSCV ya varía sus metas por edad y por fragilidad. La meta de presión arterial es <140/90, pero en
personas de **80 años y más** es **<150/90 y >120/60**, un piso además de un techo. Las metas de
HbA1c en personas de 65 y más están estratificadas por estado clínico: <7-7,5% si la persona está
sana e independiente, <8% si es frágil, <8,5% en estados de salud muy complejos. La fragilidad, para
este propósito, está definida como al menos uno de: más de 75 años, comorbilidad crónica
significativa, desnutrición (IMC <23), dependencia en actividades básicas de la vida diaria (Barthel
≤60), expectativa de vida menor a 5 años, caídas frecuentes, depresión severa, deterioro cognitivo
moderado a severo, alto riesgo social y económico.

**"Compensado" no es un número.** Una HbA1c que está en meta para una persona frágil de 85 años está
fuera de meta para una persona sana de 66. Una tabla de banderas que se apoye en valores absolutos
sin el estado de fragilidad del paciente va a estar equivocada para alguien. Si la tabla debe ser
sensible a fragilidad es decisión del profesional clínico. Lo que el PRD no debe hacer es dar a
entender que existe un único conjunto de umbrales.

Nota lateral y útil: estos criterios de fragilidad describen a la población real mejor que cualquier
descripción que escribiéramos nosotros, y conviene leerlos antes de construir la cohorte sintética.

### Qué queda esperando decisión clínica en esta sección

Palpitaciones como sustituto de frecuencia cardíaca medida. Aplicabilidad de la lista de hipoglicemia
de tipo 1 a tipo 2. Reutilización de los síntomas diagnósticos de tipo 2 como señales de
descompensación. Manejo de la hipertensión dado el antipatrón. Pie diabético preguntado de forma
proactiva o esperado. Depresión dentro o fuera del alcance. Ausencia de respuesta como bandera.
Sensibilidad a fragilidad. Y el umbral de contacto de la guía de 2015 como punto de partida.

---

## A2. Tablero clínico: contenido y exclusiones

**Estado:** En revisión

### Lo que ADR-0006 ya fija, y no se vuelve a discutir aquí

Un **tablero web** con una cola de triage: una lista **ordenada por riesgo, rojo primero**, donde
cada fila trae ya armado el resumen longitudinal de adherencia y síntomas del paciente. La restricción
de diseño es el tiempo del profesional y no la completitud de la interfaz: **si una fila toma más que
unos segundos en leerse, la fila está mal**, no el lector. La cola **lee del registro clínico en
SQLite** (ADR-0002) y **no lee transcripciones**.

Eso está decidido y es inmutable como decisión. Lo que sigue es lo que no está decidido.

### Lo que el taller 8 tenía que establecer y todavía no se ejecuta

El taller 8 está enunciado en `docs/research/felipe/PROMPT.md` y no se ha ejecutado. Su entregable es
una especificación de contenido y exclusiones, no un diseño visual y no una decisión. Lo que falta
por establecer, en el orden del brief:

**Quién lo lee en un CESFAM, y en qué momento de su día.** Médico, matrona, TENS, encargado del
programa cardiovascular. Y si la persona que recibe la alerta es la misma que tiene el control del
paciente. Lo único ya sabido por la investigación previa: en el PSCV el seguimiento es **conducido
por enfermería**, con enfermera universitaria y nutricionista corriendo los controles de rutina, y
entre sus tareas listadas están "Evaluación y refuerzo de la adherencia" y "Notificación de efectos
adversos". Eso calza con la superficie de escalación de ADR-0006. En cambio, el rol específico de
**matrona** en seguimiento cardiovascular, que el PRD nombra, **no fue verificado**.

**Qué está obligado a registrar el clínico cuando actúa sobre un caso**, y si el tablero tiene que
alimentar ese registro o vive al lado. El caso concreto son los **REM** y las categorías del
**rescate de inasistentes** del PSCV, que el taller 3 ya estableció textualmente:

- **Inasistencias:** cualquier paciente que faltó a su control programado sin re-agendamiento.
- **Pasivos:** inasistentes por más de 11 meses y 29 días **sin ninguna actividad de rescate**. No
  pueden ser egresados automáticamente del programa.
- **Abandono:** inasistentes por más de 11 meses y 29 días **con al menos 3 acciones de rescate**
  efectuadas en ese periodo.
- **Rescatados:** usuarios que vuelven al programa después de haber estado en abandono sin rescate o
  pasivos.

Estas categorías alimentan los REM, es decir el rescate se mide administrativamente. Un tablero que
ignore esa contabilidad le agrega trabajo al equipo en vez de quitárselo, y un tablero que la duplique
crea un segundo registro. Cuál de las dos cosas hace es exactamente lo que el taller 8 tiene que
resolver. **Pendiente.**

**Qué NO puede estar en el tablero**, como lista explícita de exclusiones, porque es la parte que un
jurado clínico va a probar.

**Qué cambia entre instituciones y qué es invariante**, como dos listas. Lo invariante es lo que se
construye; lo variable es lo que configura cada despliegue. El tablero es la única superficie que un
clínico toca y es la pieza que no se puede diseñar una sola vez para todos: lo que un equipo de
CESFAM puede accionar no es lo que puede accionar un servicio hospitalario ni una caja. **Pendiente.**

**Qué precedente existe**: cualquier tablero de triage o de alertas ya en uso en la atención primaria
chilena, cómo se ve, y qué se sabe sobre si efectivamente se lee. **Pendiente.**

### Lista de exclusiones, hasta donde los no negociables ya la determinan

Esto no es el entregable del taller 8. Es la parte de la lista que ya está fijada por la sección 2 de
`CLAUDE.md` y por la sección 3 del PRD, y que por lo tanto no depende de ninguna investigación
pendiente. El resto de la lista queda pendiente del taller 8.

El tablero **no** puede contener:

1. **Nada que se lea como una recomendación clínica.** Ni una sugerencia de conducta, ni una
   indicación, ni un cambio de dosis, ni una suspensión, ni un "considerar" seguido de algo que un
   clínico haría. El agente no indica tratamiento, y el tablero es una salida del agente.
2. **Ninguna inferencia presentada como hallazgo.** Lo que el paciente dijo es un hecho; lo que el
   modelo dedujo de lo que dijo es una inferencia, y las dos no pueden aparecer con el mismo peso
   visual ni con la misma redacción. Un síntoma extraído se muestra como reportado por el paciente y
   atribuido a él.
3. **Ningún nombre de condición ni interpretación clínica de un síntoma.** PreventIA no diagnostica,
   y escribir un diagnóstico en la fila es diagnosticar aunque el destinatario sea un profesional.
4. **Ningún campo que convierta al tablero en una ficha clínica paralela.** El tablero muestra lo que
   PreventIA registró entre controles. No es el registro clínico de la institución, no lo reemplaza y
   no debe invitar a usarlo como tal.
5. **Ninguna acción que cierre un caso sin una persona.** Toda escalación termina en un humano, y el
   agente no cierra casos. Un tablero con un botón que resuelve automáticamente rompe ese límite.
6. **Ninguna transcripción de la conversación.** Es decisión de ADR-0006 y aquí se repite porque
   funciona además como exclusión de contenido.
7. **Ningún dato personal identificable de un paciente real.** El repositorio no contiene datos reales
   de pacientes bajo ninguna circunstancia, y el tablero es parte del repositorio.

Todo lo demás de la lista de exclusiones —en particular las exclusiones que dependen de qué está
obligado a registrar el equipo, y de qué puede accionar cada institución— queda **pendiente del
taller 8**.

---

## A3. El guardián

**Estado:** Sin definir

### Lo que existe hoy: una caja en un diagrama

El único lugar del repositorio donde aparece el guardián es el diagrama de flujo del piloto,
`docs/diagrams/2026-08-03-flujo-piloto-quinta-normal.excalidraw`, versión v0.0.1, para el CESFAM de
Quinta Normal. Lo que el diagrama muestra, literalmente:

- La doctora inscribe a la persona en el piloto, en el CESFAM, al terminar un control.
- Inmediatamente después hay una decisión rotulada **"¿Queda con guardián?"**, descrita como
  **"Un familiar o cuidador que la doctora designa"**.
- La propia caja lleva la anotación **"Elemento nuevo. Falta definir qué cambia en el flujo."**

De ahí en adelante el diagrama entra al ciclo diario, que se repite todos los días: PreventIA
pregunta por WhatsApp, la persona responde, se calcula el semáforo del día, y según el color queda sin
señales (verde), en la lista sin urgencia (amarillo) o escala ahora al equipo (rojo). El tablero de la
doctora está ordenado por riesgo, rojo primero, con el resumen ya armado. La doctora decide, y el
egreso del piloto es la única salida del ciclo y la decide ella.

**El guardián no aparece en ninguna otra parte del ciclo.** Ni en la pregunta diaria, ni en el
semáforo, ni en la escalación, ni en el tablero. El diagrama lo introduce y declara, en su propia
etiqueta, que no está definido qué cambia.

### La pregunta que va primero

**No está resuelto si el guardián es un concepto de PreventIA o un campo que la institución ya tiene
y que nosotros deberíamos leer en vez de inventar.** Esa es la primera pregunta del taller 7 y hasta
que se responda ninguna de las siguientes tiene sentido, porque diseñar un campo nuevo para algo que
el CESFAM ya registra sería crear un segundo registro de la misma persona.

### Las preguntas abiertas del taller 7

El taller 7 está enunciado en `docs/research/felipe/PROMPT.md` y **no se ha ejecutado**. Sus
preguntas, en el orden en que fueron planteadas:

1. **¿Existe ya una figura equivalente en la atención primaria chilena, y cómo se llama ahí?**
   Cuidador, cuidador principal, acompañante, apoderado, representante. Si el PSCV o alguna
   orientación técnica de MINSAL registra una, en qué campo, y quién está autorizado a designarla.
2. **¿Qué estaría autorizado a recibir esa persona?** Un tercero leyendo los síntomas de un paciente
   es una pregunta de privacidad distinta de un paciente leyendo los suyos. La Ley 20.584, sobre
   derechos y deberes del paciente, es el primer lugar donde mirar.
3. **¿Designar un guardián es una configuración del tablero clínico, un campo capturado en la
   inscripción, o ambas cosas?** Y si puede cambiarse después sin un nuevo consentimiento.
4. **¿Qué cambia aguas abajo, si es que cambia algo?** La frecuencia del contacto diario, el umbral
   para escalar a rojo, o a quién llega la escalación. **REQUIERE REVISIÓN CLÍNICA.** El taller no
   decide esto: reúne las opciones y su fundamento para que el profesional clínico decida.

### Lo que la investigación ya registró sobre la Ley 20.584, y dónde se detiene

Lo único registrado hasta ahora, en el taller 6, sección 8: la wiki de datos del Lab nombra la
**Ley N° 20.584** como la norma que protege la ficha clínica y regula quién puede acceder a ella,
junto con el consentimiento informado. **La ley no fue leída.** Está marcado como no verificado qué
exige respecto de un sistema que guarda hechos clínicos extraídos sobre un paciente fuera de una
ficha clínica formal, que es exactamente lo que son las tablas SQLite de PreventIA. Lo que lo
verificaría: leer la Ley 20.584 en BCN, y un abogado.

**Este anexo no da ninguna interpretación legal y no puede darla.** El límite está exactamente ahí:
la investigación puede reportar qué dice la norma y qué exige; determinar si un tercero designado
puede recibir información clínica de un paciente, bajo qué condiciones y con qué consentimiento, es
una pregunta para un abogado y no para este equipo.

Relacionado, y también sin resolver: la Ley N° 21.719 de protección de datos personales entra en
plena vigencia el **1 de diciembre de 2026** y clasifica los datos de salud como datos personales
sensibles. Eso es posterior al Lab y anterior a cualquier piloto real. El propio Lab pide diseñar
pensando en ella.

### Por qué la figura importa, con lo que ya está documentado

No es un argumento para crear el campo, es contexto para quien lo decida. El taller 1 dejó registrado
que varias de las señales de alerta más graves **no son auto-reportables por construcción**: la
palidez la nota normalmente un familiar y no el paciente, y la confusión, el compromiso de conciencia
y la alteración del habla son estados en los que nadie escribe un mensaje describiéndose a sí mismo.
Quien podría reportar eso es un tercero. Qué se hace con esa observación es decisión clínica y de
producto, no de este anexo.

---

## A4. Forma del dataset del Lab

**Estado:** En revisión

### La propuesta P9, en sus propios términos

La wiki de datos del Lab establece la regla, textual: "Solo datos anonimizados/agregados, fuentes
públicas curadas o prospección sintética. Nunca PII de pacientes ni re-identificación". Y mapea los
datos por línea de desafío: a **Continuidad**, que es la nuestra, le corresponden **egresos
hospitalarios y datos agregados de crónicos**. Las listas de espera pertenecen a Descompresión, no a
nosotros.

ADR-0007 describe un adaptador que lee el dataset anonimizado del Lab por MCP "en el mismo esquema".
Contra datos genuinamente **agregados** eso no es posible, porque un dato agregado no tiene fila por
persona y no hay nada que poner en una tabla `patients`.

Lo que sí es posible, y es a la vez más pequeño y más defendible, es un adaptador que lea los
agregados y **calibre la forma de la cohorte sintética**: distribución de edad, razón de sexos,
distribución por comuna, prevalencia de cada condición, tasa de multimorbilidad. La línea del pitch
sale sola: la cohorte es sintética, su forma viene de los agregados anonimizados de la propia
institución, y podemos decir exactamente qué es cada cosa.

Vale la pena notar además que el propio Lab entrega datos sintéticos: la wiki lista "Prospección
sintética — Datos sintéticos provistos por el Lab para casos que lo requieran". La cohorte sintética
de ADR-0007 no es un rodeo a las reglas, es uno de los tres modos de datos que el Lab sanciona
explícitamente.

### Supuestos de esquema en riesgo, del taller 6

Contra las tablas nombradas en `CLAUDE.md` sección 3. El riesgo es el juicio del taller sobre qué tan
probable es que el supuesto falle contra datos reales de la Caja, no una probabilidad.

| Elemento del esquema | Supuesto que codifica | Riesgo | Por qué |
|---|---|---|---|
| `patients` como filas de personas | El dataset tiene un registro por persona | **Muy alto** | "Agregado" está en la propia regla de datos del Lab. Un dato agregado no tiene fila por persona por construcción |
| `patients.age` o fecha de nacimiento | La edad está disponible por persona | **Muy alto** | Tramo etario en el mejor caso; una fecha de nacimiento es PII y el Lab la prohíbe |
| `patients.sex`, `comuna` | Disponibles | Medio | Dimensiones estándar de agregación; plausibles, igual a nivel de tramo |
| Diagnósticos por paciente (HTA / DM2 / IC) | El proveedor sabe qué condiciones tiene cada persona | **Alto** | Una caja de compensación no tiene razón estatutaria para guardar el diagnóstico de un pensionado |
| `medications` con fármaco, dosis y horario | Existe una lista de medicamentos por paciente | **Muy alto** | No es un registro de una caja. Lo más cercano es un historial de compras en farmacia de un socio comercial, que no es lo mismo que una receta |
| `check_ins`, historial de contacto diario | Existe algo parecido de donde partir | **Muy alto** | Nada en la función de una caja produce esto |
| `risk_events`, `escalations` | — | Ninguno | Los genera PreventIA por completo. Sin dependencia externa |
| Un número de teléfono al cual escribir | Se puede sembrar un paciente contactable desde los datos | **Falla segura** | Un dato agregado y anonimizado no contiene datos de contacto, por definición y por la regla del Lab. **La demo nunca podía correr contra un paciente real de la Caja** |
| Adherencia longitudinal por semanas | El dataset soporta una serie de tiempo por persona | **Muy alto** | Requiere filas por persona y observación repetida. La agregación elimina lo primero |
| Estado de fragilidad, Barthel, estado cognitivo | Disponibles para apoyar la tabla de reglas | **Muy alto** | Son instrumentos de evaluación clínica administrados en un servicio de salud, no registros de beneficios |

### Lo que falta para que esto deje de estar en revisión

**ADR-0007 está Aceptado y es inmutable.** Si se adopta la propuesta P9, necesita un ADR nuevo, con el
número siguiente, cuyo Status diga que supersede a 0007, y la única edición que se le hace a 0007 es
cambiar su línea de Status. **Ese ADR no está escrito.** Y por la regla del proyecto, la decisión la
escribe Felipe, no la investigación.

Queda además una pregunta que solo se responde mirando los datos el día uno: **si el Lab usa
"agregado" en sentido estricto o en sentido laxo** para decir "desidentificado". Son cosas distintas
y decidirían la tabla de arriba casi completa. Ligado a esto: bajo la Ley 21.719 la anonimización es
un procedimiento irreversible, y un dato que puede re-identificarse es seudonimizado y sigue siendo
dato personal. Si el dataset del Lab está desidentificado y no anonimizado de forma irreversible, la
palabra correcta es "seudonimizado", y un jurado de la administración de salud puede conocer la
diferencia.

---

## A5. Riesgos de despliegue nombrados

**Estado:** En revisión

Ninguno de los dos está hoy en `PRD.md`. Los dos son mejores preguntas de tener respondidas que de
que te las hagan.

### P10. Los datos de contacto

**El mismo modo de falla ha derrotado a tres esfuerzos chilenos distintos por alcanzar a esta
población.** No es una hipótesis, son tres registros separados:

- **FOFAR.** En la evaluación de DIPRES sobre 4.481.282 horas del PSCV, el grupo que **no** recibió
  recordatorio no lo recibió porque **sus datos de contacto estaban equivocados o faltaban**, según
  la nota al pie de la propia tabla del informe.
- **El rescate de inasistentes.** El protocolo escala a **visita domiciliaria** precisamente cuando
  el contacto telefónico falla. El teléfono que no funciona es lo que convierte una llamada en el
  viaje de un funcionario.
- **El estudio chileno más grande de adherencia antihipertensiva.** Sandoval y colaboradores
  perdieron **443 de 956 pacientes muestreados**, de los cuales **245 fueron "error en la información
  de contacto"**. Una cuarta parte de una muestra extraída de un registro PSCV vivo, inalcanzable
  porque el registro estaba equivocado.

**PreventIA supone un número de WhatsApp que funciona.** La evidencia chilena dice que el sistema de
salud frecuentemente no lo tiene, y que los pacientes cuyos números están equivocados son
sistemáticamente los más propensos a descompensarse sin que nadie lo vea. Esto debería estar nombrado
en el PRD como una precondición de despliegue.

La pregunta que lo cierra es una sola conversación con un equipo de CESFAM: **cómo sabe un CESFAM el
número de teléfono actual de un paciente, y con qué frecuencia está equivocado.** Es la misma
conversación que responde la pregunta 1 de la sección A6.

### P11. El instrumento de adherencia y la licencia Morisky

Lo que está establecido, y nada de esto es interpretación:

- **El PSCV ya exige un instrumento.** La Orientación Técnica de 2017 recomienda explícitamente el
  **Test de Morisky Green Levine-4** para evaluar adherencia en el seguimiento. Alinearse a un
  instrumento que el equipo clínico ya conoce es más barato y más creíble que inventar un puntaje
  propio.
- **Las escalas Morisky son instrumentos comerciales con derechos de autor.** El titular publica en
  su propio sitio precios de **USD 4 por administración para MMAS-4 y USD 7 para MMAS-8**, licencias
  por suscripción desde **USD 1.000 al año**, y traducciones a **USD 250 y USD 500**; y establece que
  las escalas no pueden ser "modificadas, vendidas, traducidas a otro idioma o adaptadas a otro
  medio" sin licencia. Los precios son los publicados en la fecha de consulta y no se garantizan
  vigentes.
- **"Adaptado a otro medio" describe exactamente lo que haría un agente conversacional.** Preguntar
  las cuatro preguntas en español de Chile dentro de una conversación de WhatsApp es una adaptación y
  una traducción a la vez.
- **Una tarifa por administración es estructuralmente hostil a un contacto diario.** El instrumento
  fue tarificado para un cuestionario aplicado en una consulta, no para algo que se pregunta todas las
  mañanas.
- **El nombre no protege.** "Test de Morisky Green Levine-4", que es como lo llama el documento de
  MINSAL, y "MMAS-4", que es el nombre registrado, son las mismas cuatro preguntas.
- **La fiscalización no es teórica.** Existe publicado un *Corrigendum and Editorial Warning*
  asociado al uso de MMAS-8 en un artículo sobre una aplicación de adherencia a medicamentos, que es
  precisamente el caso de uso que ocupa PreventIA.
- **No verificado:** si MINSAL o la atención primaria chilena tienen una licencia que cubra el uso
  rutinario en el PSCV, y si tal licencia se extendería a un tercero construyendo una herramienta. Lo
  verificaría preguntarle directamente a MINSAL o al titular de los derechos.

**PreventIA no ha elegido ningún instrumento de adherencia.** Por eso hoy no hay nada que corregir en
el PRD. Pero **esto tiene que quedar resuelto antes de que se escriba nada en `clinical/`**, porque
después de eso el costo de deshacerlo es distinto.

Las tres opciones registradas por la investigación son licenciar, no usar el instrumento, o alinearse
conceptualmente a él sin reproducir sus ítems. Solo la última es gratis.

**Esto no es asesoría legal y este documento no la da.** Es una decisión de Felipe, y la parte de
derechos de autor y licenciamiento requiere un abogado. El límite está ahí: la investigación reporta
qué publica el titular de los derechos y qué precedente existe; qué significa eso para nuestro caso
particular no lo determina este equipo.

### El techo que ningún instrumento de auto-reporte puede evitar

Contexto para cualquier decisión sobre adherencia, ya establecido por el taller 4: una revisión de
117 artículos con 251 comparaciones contra monitoreo electrónico encontró que la adherencia mediana
es **sobreestimada en 17% por auto-reporte**, 8% por conteo de comprimidos y 6% por escalas de
valoración. **PreventIA es un instrumento de auto-reporte por construcción**, y no debería dejar de
serlo, porque la alternativa es un dispositivo y la premisa del producto es que no hay dispositivo.
Lo defendible es decir que PreventIA mide adherencia **reportada**, a diario, longitudinalmente y en
las palabras del paciente, y que eso es más información de la que hoy tiene una enfermera en un
control tres meses después. No que mide adherencia.

---

## A6. Preguntas abiertas para el profesional clínico

**Estado:** Bloqueado en clínico

Consolidadas a través de los seis talleres de investigación ejecutados, en el orden de
`docs/research/README.md`. La primera es la de mayor valor.

1. **¿Cuánto tiempo de personal cuesta una acción de rescate?** Convierte "ahorramos tiempo del
   equipo" de afirmación en número. Se responde con una conversación con un equipo de CESFAM.
2. ¿Es el umbral de contacto de la guía MINSAL 2015 de insuficiencia cardíaca —aumento de disnea,
   edema, o más de 2 kg en 3 días— el punto de partida correcto para la tabla de banderas?
3. ¿Cómo debe tratar la tabla el peso, dado que no se supone ningún dispositivo?
4. ¿Pueden usarse los síntomas de hipoglicemia de la guía de tipo 1 en adultos mayores con diabetes
   tipo 2?
5. ¿Pueden reutilizarse los síntomas diagnósticos de diabetes tipo 2 como señales de descompensación
   en pacientes ya diagnosticados?
6. ¿Cómo se maneja la hipertensión, dado que casi no produce señal escuchable y que la guía nacional
   advierte que los síntomas que los pacientes le atribuyen frecuentemente no son causados por ella?
7. ¿Debe la tabla de banderas ser sensible al estado de fragilidad? (P4.)
8. **¿Está la depresión dentro del alcance?** El taller 4 lo agudizó: el malestar emocional y los
   síntomas depresivos son el predictor más fuerte de no adherencia en el único estudio chileno
   grande sobre esto, con OR 1,93. Eso pone a la depresión dentro del propósito declarado del PRD por
   razones de adherencia, no solo clínicas.
9. ¿Debe la ausencia de respuesta ser una bandera?
10. ¿Qué programa, si alguno, estructura el seguimiento de la insuficiencia cardíaca en Chile, dado
    que no es ni GES ni PSCV?
11. ¿Puede la evidencia chilena sobre MMAS-8 sustituir a la del MGL-4 que el PSCV efectivamente
    exige? (Taller 4.)
12. ¿Puede alimentar la capa de extracción un audio transcrito, y con qué nivel de confianza, si
    alguna vez se aceptan notas de voz? (Taller 5.)
13. **¿Cómo sabe un CESFAM el número de teléfono actual de un paciente, y con qué frecuencia está
    equivocado?** (P10.) Es la misma conversación que la pregunta 1 y casi igual de valiosa.

Dos condiciones del Lab que se cruzan con esta sección y no son recomendaciones sino requisitos:
**todo equipo debe incluir al menos un profesional de salud**, y **toda afirmación clínica debe
llevar fuente verificable o decir "no sé"**. La segunda es la razón por la que el taller 1 le adjunta
una cita de MINSAL a cada señal candidata en vez de proponer umbrales.

---

## A7. Historial de cambios

| Versión | Fecha | Qué cambió | Origen |
|---|---|---|---|
| 1.0 | 2026-08-05 | Creación del anexo. Se separa de `PRD.md` todo lo que sigue en movimiento, con un estado por sección | Separación de `PRD.md` v2.0 |
