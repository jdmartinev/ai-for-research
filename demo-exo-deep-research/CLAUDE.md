# Proyecto: investigación sobre exoesqueletos de miembro inferior

Este proyecto es un sistema de *deep research* multiagente para preguntas sobre exoesqueletos
(control, biomecánica, sensado y validación clínica). Lo usa un grupo de investigación
universitario. Las respuestas alimentan revisiones de literatura y propuestas de investigación,
así que la exactitud importa más que la velocidad.

## Cómo está organizado

- `/investigar <pregunta>` (skill en `.claude/skills/investigar/`) es el punto de entrada. Tú, la
  sesión principal, haces de **agente líder**.
- `.claude/agents/investigador.md` busca y lee fuentes para **una** subpregunta.
- `.claude/agents/verificador-citas.md` abre cada fuente citada y confirma que dice lo que la nota
  afirma.
- `.claude/agents/juez.md` califica el reporte final con `rubrica.md`.
- Todo lo que se produce va en `salidas/<slug-de-la-pregunta>/`.

## Reglas del grupo (aplican a todos los agentes)

1. **Nunca cites una fuente que no abriste.** Un título en una lista de resultados no es una fuente.
2. Prefiere, en este orden: artículos revisados por pares (con DOI), revisiones sistemáticas y
   metaanálisis, preprints identificados (arXiv, bioRxiv, medRxiv), tesis. Evita blogs, notas de
   prensa y páginas comerciales salvo para datos de un producto, y márcalos como tales.
3. Para cada hallazgo registra: **población** (sanos / clínicos, cuál condición), **n**, **tipo de
   estudio** (experimento con humanos, simulación, revisión), **tarea** (caminar en banda, terreno,
   velocidad) y **magnitud del efecto** con unidades.
4. Separa siempre resultados en **simulación** de resultados en **humanos**, y en **sujetos sanos**
   de **poblaciones clínicas**.
5. No conviertas correlación en causalidad. Si un estudio no tiene grupo control o condición sin
   asistencia, dilo.
6. Si las fuentes se contradicen, reporta ambas posiciones y qué explicaría la diferencia; no
   escojas una en silencio.
7. Si no encuentras evidencia suficiente, dilo. "No encontré estudios en humanos sobre X" es una
   respuesta válida.
8. Escribe en español. Los títulos de los artículos van en su idioma original.
