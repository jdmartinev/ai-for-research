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
| [`presentacion/`](presentacion/) | La presentación en la plantilla del simposio (`.pptx`, 23 diapositivas con notas del expositor y los videos de las escenas), el script que la genera y la fuente web del deck |
| [`figuras/`](figuras/) | Las escenas Manim y las figuras (`escenas/`, `escena01/`), los videos y PNG ya renderizados (`render/`) y `FIGURE_PROMPTS.md`, el brief original |
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

## Escenas y figuras

| Diap. | Recurso | Archivo | Datos |
| --- | --- | --- | --- |
| 1 | S01 registro de autoresearch | `escena01/scene01_autoresearch_log.py` | ilustrativos hasta poner `results.tsv` |
| 3 | F03 siguiente token | `escenas/f03_siguiente_token.py` | ilustrativos hasta correr `datos_siguiente_token.py` (Qwen2.5-0.5B) |
| 4 | S04 atención | `escenas/s04_atencion.py` | ilustrativos hasta correr `datos_atencion.py` (BETO) |
| 6 | S06 verificador | `escenas/s06_verificador.py` | REINFORCE de juguete, calculado |
| 7 | S07 imágenes → tokens | `escenas/s07_imagenes.py` | imagen sintética; pon `input.jpg` para usar un cuadro tuyo |
| 9 | S09 ciclo del agente | `escenas/s09_agente.py` | traza ilustrativa; `trace.json` la reemplaza |
| 10 | F10 deep research | `escenas/f10_deep_research.py` | arquitectura de Anthropic (2025) |
| 11 | F11 harness | `escenas/f11_harness.py` | conceptual |
| 16 | S16 autoresearch | `escenas/s16_autoresearch.py` | mismo registro que S01 |
| 17 | S17 torneo Co-Scientist | `escenas/s17_torneo.py` | torneo ilustrativo, Elo calculado; `hipotesis.txt` pone tus títulos |
| 18 | S18 evolución | `escenas/s18_evolucion.py` | búsqueda evolutiva de juguete, calculada; cierra con cifras de ERA y AlphaEvolve |

Cada video que usa datos ilustrativos lo dice en la esquina inferior derecha. Para renderizar
(Manim CE 0.21, fuentes IBM Plex Sans, JetBrains Mono y Space Grotesk instaladas):

```bash
cd figuras/escenas
manim -r 1920,720 --fps 30 s04_atencion.py Atencion          # video 8:3
manim -s -r 1920,720 f03_siguiente_token.py SiguienteToken   # figura fija
manim -s -r 1920,440 f10_deep_research.py DeepResearch       # F10 es más baja
python qa.py <video.mp4> nombre 4                            # cuadros de revisión
```

Copia el `.mp4` y su último cuadro como `.png` a `figuras/render/` con el nombre del recurso
(`S04.mp4`, `S04.png`, `F03.png`, …) y regenera el `.pptx`: el script los inserta solo.

## Pendientes antes de la charla

- [ ] Correr `datos_siguiente_token.py` y `datos_atencion.py` en tu máquina (necesitan Hugging Face) y re-renderizar F03 y S04
- [ ] Poner tu `results.tsv` real de autoresearch y re-renderizar S01 y S16
- [ ] Opcional: `input.jpg` (S07), `trace.json` (S09) y `hipotesis.txt` (S17) con material tuyo
- [ ] Correr la demo del exoesqueleto y grabar el corte de 60 s (`demo-exo-deep-research/README.md`)
- [ ] Completar contacto y enlace o QR en la diapositiva de cierre
- [ ] Revisar la política de EAFIT sobre uso de IA y autoría (notas de la diapositiva 21)

## Notas sobre fuentes y derechos

- Todas las cifras de las diapositivas vienen de fuentes abiertas y leídas; ver `revision-literatura/`.
- La clase de Akari Asai (CMU 11-768) y las diapositivas de Claes Bäckman se citan, pero sus archivos
  no se incluyen en este repositorio.
- La plantilla y los logos son del 1er Simposio Somer Investiga y la Clínica Somer; se usan solo para
  esta charla.
