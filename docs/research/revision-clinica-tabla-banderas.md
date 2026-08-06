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

## Lo que ocurre después

Su revisión se registra como decisión clínica: la tabla queda con autor, y la ADR correspondiente lleva
su nombre en la línea `Deciders`. Eso cambia lo que se puede afirmar frente a un panel clínico — deja
de ser "el equipo de desarrollo eligió estos colores" y pasa a ser "una médica los revisó y los firmó".
