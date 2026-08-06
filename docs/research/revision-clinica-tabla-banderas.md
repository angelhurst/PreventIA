# Revisión clínica de la tabla de banderas

**Para:** las dos médicas del equipo
**De:** el equipo de desarrollo
**Fecha:** 6 de agosto de 2026
**Tiempo estimado:** 10 minutos

## Qué se le pide

Esta es la tabla determinista que fija el **piso** del semáforo de PreventIA. El modelo puede subir un
color por encima de este piso, nunca bajarlo, y eso está garantizado en el tipo, en una restricción
`CHECK` de la base de datos y en pruebas automatizadas.

La fuente de cada síntoma es una guía del Minsal y está citada. **Lo que no tiene autor clínico es la
asignación de color.** El documento de investigación que alimentó esta tabla dice explícitamente que
no asigna colores, porque esa decisión es clínica y no de ingeniería. La tomó el equipo de desarrollo
de forma provisional para poder construir, y necesita revisión antes de que alguien la vea funcionar.

Marque cada fila: **OK**, o el color que corresponda. Si una fila le parece que no debería estar,
táchela. Al final hay tres preguntas abiertas.

## Rojo

| Término | Etiqueta | Fuente | ¿OK? |
|---|---|---|---|
| `disnea_aumentada` | aumento de la falta de aire | Guía Insuficiencia Cardíaca 2015, Tabla 28 | |
| `edema` | edema de extremidades | Guía Insuficiencia Cardíaca 2015, Tabla 28 | |
| `confusion` | confusión | Guía Diabetes Mellitus Tipo 1 2013, sección 8.2 | |
| `alteracion_habla` | alteración del habla | Guía Diabetes Mellitus Tipo 1 2013, sección 8.2 | |
| `vision_borrosa` | visión borrosa | Guía Diabetes Mellitus Tipo 1 2013, sección 8.2 | |

## Amarillo

| Término | Etiqueta | Fuente | ¿OK? |
|---|---|---|---|
| `temblor` | temblor | Guía DM1 2013, sección 8.2 | |
| `sudor_frio` | sudor frío | Guía DM1 2013, sección 8.2 | |
| `palidez` | palidez | Guía DM1 2013, sección 8.2 | |
| `herida_pie` | herida o lesión en el pie | Guía DM2 2010, sección 3.5.3 | |
| `sed_intensa` | sed intensa | Guía DM2 2010, sección 3.5.3 | |
| `poliuria` | orinar mucho más de lo habitual | Guía DM2 2010, sección 3.5.3 | |
| `baja_de_peso` | baja de peso no explicada | Guía DM2 2010, sección 3.5.3 | |
| `tos_seca` | tos seca persistente | Guía HTA 2010, p.30 y p.34 | |
| `mareo_al_pararse` | mareo al ponerse de pie | Guía HTA 2010, p.30 y p.34 | |
| `nauseas` | náuseas o falta de apetito | Guía Insuficiencia Cardíaca 2015 | |
| `palpitaciones` | palpitaciones | Guía Insuficiencia Cardíaca 2015 | |
| `cansancio` | cansancio generalizado | Guía Insuficiencia Cardíaca 2015 | |
| `dosis_no_tomada` | dosis no tomadas en el último control | Orientación Técnica PSCV 2017 | |

## Preguntas abiertas

**1. No existe una bandera para dolor torácico, y esto ya falló en producción.**

El 6 de agosto una paciente escribió *"hola, siento dolor en el pecho"*. Como no hay un término para
dolor torácico, el modelo lo archivó bajo `nauseas`, con el texto literal guardado correctamente pero
el término clínico equivocado. El caso quedó en rojo, pero sólo porque el modelo subió el color por su
cuenta: el piso determinista dijo amarillo, y por la razón incorrecta.

En una cohorte cardiovascular ésta es probablemente la primera pregunta que hará un evaluador clínico.
¿Qué término y qué color corresponde? ¿Distingue usted dolor torácico en reposo de dolor con
esfuerzo, y puede una persona de 71 años reportar esa diferencia por escrito de forma confiable?

**2. Los estados más graves son los menos auto-reportables.**

Confusión, alteración del habla y compromiso de conciencia aparecen como signos de alarma en las guías
de insuficiencia cardíaca y de hipoglicemia, y una persona en ese estado no escribe un mensaje. Hoy la
tabla los trata igual que a cualquier otra bandera. ¿Debería la **ausencia de respuesta** a una
consulta diaria valer como señal, y de qué color?

**3. La adherencia incompleta hoy es siempre amarilla.**

Una dosis olvidada y cuatro dosis no tomadas producen el mismo color. ¿Corresponde un umbral, y en qué
punto?

## Segunda parte: lo que la paciente lee

Todo lo que PreventIA le dice a una paciente está en un solo archivo, para que ustedes puedan
revisarlo sin leer código. Nunca ha sido revisado por una médica. Son seis frases.

**1. Presentación, primer contacto**

> Le escribe PreventIA, un asistente virtual del consultorio. No soy una persona ni un profesional de
> la salud, y no reemplazo sus controles. Cada día le voy a preguntar si tomó sus remedios y cómo se
> ha sentido. Lo que usted me cuente queda anotado para su equipo de salud.

**2. Cuando la paciente pregunta algo que el agente no puede responder**

> Prefiero no responderle eso, porque no soy médico. Estoy dejando su mensaje anotado para el equipo
> del consultorio, que se va a comunicar con usted.

**3. Cuando una bandera clínica marca rojo** (única frase que menciona urgencia)

> Por lo que me cuenta, le pido que se comunique hoy con su consultorio. Si se siente peor, llame al
> 131 o vaya al servicio de urgencia más cercano. Ya avisé a su equipo de salud.

**4. Cuando el modelo sube el color a rojo pero ninguna regla clínica se activó**

> Ya avisé a su equipo de salud para que se comunique con usted.

**5. Cuando se detecta una señal de crisis de salud mental**

> Gracias por contarme algo así de difícil. Usted no tiene que pasar por esto sin apoyo. Estoy
> avisando ahora mismo a su equipo de salud para que se comuniquen con usted lo antes posible. Por
> favor manténgase acompañado y deje su teléfono cerca.

**6. Cuando llega una nota de voz** (la transcripción está fuera de alcance por ahora)

> Recibí su mensaje, pero por ahora solo puedo leer texto. ¿Me lo puede escribir, por favor?

**Pregunta 4.** ¿Alguna de estas frases dice de más, dice de menos, o suena mal para una persona de 71
años? La frase 5 es la que más nos preocupa: se envía sola, sin que alcance a intervenir una persona.

**Nota técnica que ustedes deben saber:** el resto de las respuestas las redacta el modelo en el
momento, no salen de esta lista. Hoy se le escapa el tuteo — hemos visto "me alegra saber que te
sientes bien" cuando la regla del proyecto es usted siempre. Eso lo corregimos nosotros, pero si ven
otra cosa en el tono, díganlo.

## Tercera parte: las palabras que gatillan el protocolo de crisis

Si un mensaje contiene una de estas frases, PreventIA deja de hacer triaje de hipertensión o diabetes
y deriva de inmediato a contacto humano. La lista la escribió el equipo de desarrollo.

`quiero morirme` · `me quiero morir` · `quisiera morirme` · `quitarme la vida` · `acabar con mi vida` ·
`terminar con mi vida` · `terminar con todo` · `acabar con todo` · `matarme` · `no quiero vivir` ·
`no quiero seguir viviendo` · `no vale la pena vivir` · `para qué sigo viviendo` · `estaría mejor
muerta` · `mejor no despertar` · `hacerme daño` · `cortarme`

Hay excepciones para los usos idiomáticos: "morirme de risa", "morirme de hambre", "cortarme el pelo"
y similares no gatillan nada.

**Pregunta 5.** ¿Falta alguna forma de decirlo que ustedes escuchan en consulta y que aquí no está?
Una mujer de 71 años en Chile probablemente no dice "quiero suicidarme"; dice otra cosa. Esa otra cosa
es la que necesitamos.

## Lo que ocurre después

Su revisión se registra como decisión clínica: la tabla queda con autor, y la ADR correspondiente lleva
su nombre en la línea `Deciders`. Eso cambia lo que se puede afirmar frente a un panel clínico — deja
de ser "el equipo de desarrollo eligió estos colores" y pasa a ser "una médica los revisó y los firmó".
