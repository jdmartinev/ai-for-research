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

## Estructura de la charla (56 diapositivas, ~45 s cada una)

| Diap. | Parte | Idea | Juez |
| --- | --- | --- | --- |
| 1–2 | Gancho y mapa | Un agente ya investiga solo; seis ciclos, una forma | — |
| 3–23 | 1 · Cómo funcionan | Tokens, siguiente token, muestreo, embeddings; pérdida, gradiente y descenso; atención, bloque y pila del transformer; ventana de contexto; leyes de escala; preentrenamiento, ajuste fino, RLHF, razonamiento, multimodal | el token → humanos → verificador |
| 24–34 | 2 · De LLM a agente | Qué cambió, herramientas como texto, ciclo del agente, por qué ahora, deep research por dentro, cómo se mide y se entrena, búsqueda con embeddings | las herramientas |
| 35–44 | 3 · El harness | El harness junta todo lo anterior: CLAUDE.md, contexto, permisos, skills (carga progresiva, anatomía, crear, galería), evaluación | tú, en reglas y checks |
| 45–52 | 4 · IA que investiga | autoresearch y program.md, Co-Scientist (agentes, torneo, laboratorio), ERA y AlphaEvolve, punta a punta, demo del exoesqueleto | tu métrica |
| 53–55 | 5 · Límites y cierre | El juez del juez, cómo fallan los ciclos, qué hacer el lunes | — |

## Cómo regenerar la presentación

Todo el contenido (titulares, cuerpo, fuentes y notas del expositor) vive en
`presentacion/spec.py`. De ahí salen el deck web y el `.pptx`:

```bash
pip install python-pptx
cd presentacion
python render_html.py     # → web/deck.json y web/slides/*.html (deck web)
python render_pptx.py     # → IA-para-la-investigacion_Simposio-Somer.pptx (plantilla Somer)
```

`render_pptx.py` inserta los videos de `figuras/render/` (arrancan solos al llegar a la
diapositiva) y las figuras PNG. `assets.json` guarda las direcciones de los videos en el deck web.

## Escenas y figuras

| Diap. | Recurso | Archivo | Datos |
| --- | --- | --- | --- |
| 4 | Tokens | `escenas/s_tokens.py` | tokenizador real (Tekken de Mistral), vía `datos_tokens.py` |
| 6 | Muestreo y temperatura | `escenas/s_muestreo.py` | ilustrativos; temperatura calculada |
| 7 | Embeddings | `escenas/s_embeddings.py` | posiciones ilustrativas |
| 8–10 | Pérdida, gradiente, descenso | `escenas/s_perdida.py`, `s_gradiente.py`, `s_descenso.py` | pérdidas de juguete, calculadas |
| 14–15 | Bloque y pila del transformer | `escenas/s_bloque.py`, `s_pila.py` | ilustrativos |
| 16 | F16 ventana de contexto | `escenas/f16_ventana.py` | segmentos ilustrativos |
| 17 | F17 leyes de escala | `escenas/f17_escala.py` | calculadas con el ajuste de Chinchilla |
| 32 | F32 BrowseComp | `escenas/f32_browsecomp.py` | Wei et al. (2025), vía Asai |
| 1 | S01 registro de autoresearch | `escena01/scene01_autoresearch_log.py` | ilustrativos hasta poner `results.tsv` |
| 5 | F03 siguiente token | `escenas/f03_siguiente_token.py` | ilustrativos hasta correr `datos_siguiente_token.py` (Qwen2.5-0.5B) |
| 13 | S04 atención | `escenas/s04_atencion.py` | ilustrativos hasta correr `datos_atencion.py` (BETO) |
| 21 | S06 verificador | `escenas/s06_verificador.py` | REINFORCE de juguete, calculado |
| 23 | S07 imágenes → tokens | `escenas/s07_imagenes.py` | imagen sintética; pon `input.jpg` para usar un cuadro tuyo |
| 28 | S09 ciclo del agente | `escenas/s09_agente.py` | traza ilustrativa; `trace.json` la reemplaza |
| 31 | F10 deep research | `escenas/f10_deep_research.py` | arquitectura de Anthropic (2025) |
| 35 | F11 harness | `escenas/f11_harness.py` | conceptual |
| 45 | S16 autoresearch | `escenas/s16_autoresearch.py` | mismo registro que S01 |
| 48 | S17 torneo Co-Scientist | `escenas/s17_torneo.py` | torneo ilustrativo, Elo calculado; `hipotesis.txt` pone tus títulos |
| 50 | S18 evolución | `escenas/s18_evolucion.py` | búsqueda evolutiva de juguete, calculada; cierra con cifras de ERA y AlphaEvolve |

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
