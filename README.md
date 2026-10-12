# ¿Quién decide qué cuenta como mejor? — IA para la investigación

Material de la charla de 40 minutos de Juan David Martínez Vargas, Ph.D. (Universidad EAFIT) para el
**1er Simposio Somer Investiga: Métodos e Innovación en Investigación Clínica**.

**Tesis.** Cada etapa de la IA moderna es el mismo ciclo: algo propone, algo juzga, algo actualiza.
Lo que cambia es quién es el juez: el siguiente token, las preferencias humanas, un verificador,
las herramientas, tus reglas y, al final, tu métrica. Cuando el juez pasa de los datos a ti, tu
trabajo pasa de producir resultados a juzgarlos.

## Qué hay aquí

| Carpeta | Contenido |
| --- | --- |
| [`presentacion/`](presentacion/) | La presentación en la plantilla del simposio (`.pptx`, 23 diapositivas con notas del expositor y el video de la escena 1), el script que la genera y la fuente web del deck |
| [`figuras/`](figuras/) | `FIGURE_PROMPTS.md`, el brief para el agente que construye las figuras y animaciones, y la escena 1 ya hecha (script Manim, video y still) |
| [`demo-exo-deep-research/`](demo-exo-deep-research/) | Sistema de deep research multiagente para Claude Code sobre exoesqueletos: líder, investigadores en paralelo, verificador de citas y juez con rúbrica |
| [`revision-literatura/`](revision-literatura/) | Revisión de literatura con las 21 fuentes de la charla, verificadas contra los originales |

## Estructura de la charla (≈39 min)

| Diap. | Parte | Idea | Juez |
| --- | --- | --- | --- |
| 1–2 | Gancho y mapa | Un agente ya investiga solo; seis ciclos, una forma | — |
| 3–7 | 1 · Cómo funcionan | Siguiente token, atención, de simulador a asistente, razonamiento, multimodalidad | token → humanos → verificador |
| 8–10 | 2 · Agentes | Adopción (81% vs 20%), el ciclo del agente, deep research por dentro | las herramientas |
| 11–15 | 3 · Harness y skills | El harness, qué es un skill, cómo crearlo, galería, harness = diseñar el juez | tú, en reglas y checks |
| 16–19 | 4 · IA que investiga | autoresearch, Co-Scientist, ERA y AlphaEvolve, sistemas de punta a punta | tu métrica |
| 20–22 | 5 · Límites y cierre | Hasta el juez necesita un juez; cómo fallan los ciclos; qué hacer el lunes | — |

## Cómo regenerar la presentación

```bash
pip install python-pptx
python presentacion/build_pptx.py
```

El script toma los textos (titulares, notas del expositor, pies con fuentes) de
`presentacion/web/slides/*.html`, así que se edita el texto ahí y se regenera el `.pptx`.
La plantilla base (`presentacion/plantilla/base_23_diapositivas.pptx`) ya tiene los fondos del
simposio duplicados para las 23 diapositivas.

## Pendientes antes de la charla

- [ ] Re-renderizar la escena 1 con un `results.tsv` real y etiquetas en español (`figuras/FIGURE_PROMPTS.md`, S01)
- [ ] Construir las figuras y escenas marcadas como «FIGURA» y «ESCENA» en el deck (`figuras/FIGURE_PROMPTS.md`)
- [ ] Correr la demo del exoesqueleto y grabar el corte de 60 s (`demo-exo-deep-research/README.md`)
- [ ] Completar contacto y enlace o QR en la diapositiva de cierre
- [ ] Revisar la política de EAFIT sobre uso de IA y autoría (notas de la diapositiva 21)

## Notas sobre fuentes y derechos

- Todas las cifras de las diapositivas vienen de fuentes abiertas y leídas; ver `revision-literatura/`.
- La clase de Akari Asai (CMU 11-768) y las diapositivas de Claes Bäckman se citan, pero sus archivos
  no se incluyen en este repositorio.
- La plantilla y los logos son del 1er Simposio Somer Investiga y la Clínica Somer; se usan solo para
  esta charla.
