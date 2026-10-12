---
name: investigar
description: Investiga en profundidad una pregunta sobre exoesqueletos (control, biomecánica, sensado, validación clínica) repartiéndola entre subagentes investigadores en paralelo, verificando cada cita y calificando el reporte con una rúbrica. Úsalo cuando el usuario pida una revisión de literatura, el estado del arte o evidencia sobre exoesqueletos.
argument-hint: "[pregunta de investigación]"
---

# Investigar: deep research multiagente

Eres el **agente líder**. No buscas tú: planeas, delegas, decides cuándo basta y sintetizas.

Pregunta del usuario: $ARGUMENTS

## 1. Prepara la carpeta

Crea `salidas/<slug>/` con un slug corto en minúsculas a partir de la pregunta
(p. ej. `salidas/control-tobillo-costo-metabolico/`), y dentro una carpeta `notas/`.

## 2. Planea y escala el esfuerzo

Escribe `salidas/<slug>/plan.md` con:

- La pregunta reformulada en una línea, con sus términos clave en inglés para buscar.
- El **tipo de pregunta** y el esfuerzo que le corresponde (esta regla evita gastar de más):

  | Tipo | Ejemplo | Investigadores | Búsquedas por investigador |
  | --- | --- | --- | --- |
  | Dato puntual | ¿Qué masa tiene el exoesqueleto X? | 1 | hasta 5 |
  | Comparación | ¿Control por EMG o por fase de la marcha? | 2 a 3 | hasta 10 |
  | Revisión amplia | ¿Qué estrategias reducen el costo metabólico? | 3 a 4 | hasta 15 |

- Las subpreguntas, una por investigador. Que no se solapen y que juntas cubran la pregunta.
  Para preguntas amplias sobre exoesqueletos, un buen reparto suele ser:
  estrategias de control · resultados (metabólicos, cinemáticos, de EMG) · sensado y estimación
  de la fase · validación en poblaciones clínicas.
- El criterio de **«¿basta?»** para esta pregunta (ver paso 4).

El plan es tu memoria: si el contexto se alarga, vuelve a leerlo.

## 3. Delega en paralelo

Lanza **todos** los investigadores en un mismo paso, en paralelo, usando el subagente
`investigador`. A cada uno le das un brief completo, porque no ve esta conversación:

```
Subpregunta: <una sola subpregunta>
Contexto: forma parte de la pregunta "<pregunta>"; otros investigadores cubren <temas>,
no los repitas.
Límite: hasta <N> búsquedas. Para cuando tengas 4–8 fuentes primarias sólidas.
Escribe tus notas en: salidas/<slug>/notas/<tema>.md, con el formato de tu instrucción.
Devuélveme: 5 líneas con lo más importante y qué no encontraste.
```

## 4. Decide si basta (el juez en tiempo de ejecución)

Lee las notas. Basta cuando se cumplen las tres:

1. Cada subpregunta tiene al menos 3 fuentes primarias abiertas (no solo revisiones).
2. Hay al menos un estudio con humanos por estrategia o resultado que vayas a afirmar.
3. Las contradicciones están explicadas o reportadas.

Si no basta, lanza **una** ronda más solo para los huecos, con briefs nuevos y precisos.
**Máximo dos rondas en total.** Si después de dos sigue faltando, repórtalo como hueco en vez de
seguir buscando.

## 5. Verifica las citas

Lanza el subagente `verificador-citas` en paralelo, uno por archivo de notas. Cada uno escribe
`salidas/<slug>/verificacion-<tema>.md`. Una afirmación con cita marcada ✘ o «no se pudo abrir» no
entra al reporte como hecho.

## 6. Escribe el reporte

Escribe `salidas/<slug>/reporte.md`:

- **Respuesta corta** (3–5 líneas) que contesta la pregunta.
- **Tabla de evidencia**: estrategia o hallazgo · población · n · tipo de estudio · efecto con
  unidades · fuente.
- Secciones por subpregunta, solo con afirmaciones verificadas, cada una con su cita
  `[Autor, año](URL o DOI)`.
- **Huecos y contradicciones**: lo que no se encontró o no se pudo verificar.
- **Fuentes**: lista numerada de todo lo citado.

Respeta las reglas de `CLAUDE.md`.

## 7. Pide el juicio

Lanza el subagente `juez` sobre `reporte.md`. Escribe `salidas/<slug>/evaluacion.md`.

## 8. Cierra

Responde al usuario con: la respuesta corta, el puntaje del juez y sus tres fallas principales, y
la ruta del reporte. No corrijas el reporte por tu cuenta después del juicio; el usuario decide.
