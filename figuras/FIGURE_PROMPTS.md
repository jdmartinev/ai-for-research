# Prompts de figuras y animaciones — «¿Quién decide qué cuenta como mejor?»

Brief para el agente que construye los recursos visuales de una charla de 40 minutos sobre IA
para la investigación (Juan David Martínez Vargas, Universidad EAFIT). **La charla es en español:
todo texto en pantalla va en español.** Lee las secciones 0–3 una vez, luego construye en el orden
de la sección 4. Cada ítem de la sección 5 es un prompt autocontenido.

Versión 2 (11 oct. 2026). Reemplaza la versión en inglés: cambió la numeración de diapositivas, se
eliminaron figuras teóricas y se agregó el diagrama del harness.

---

## 0. La idea que todo recurso debe servir

La charla tiene una sola tesis: **cada etapa de la IA moderna es el mismo ciclo —algo propone,
algo juzga, algo actualiza— y lo que cambia es quién es el juez.**

| Parte | Ciclo | Juez |
| --- | --- | --- |
| 1 · Preentrenamiento | predecir → comparar → actualizar | el siguiente token |
| 1 · Alineación | responder → juzgar → actualizar | las preferencias humanas |
| 1 · Razonamiento | intentar → verificar → reforzar | un verificador |
| 2 · Agentes | actuar → observar → ajustar | las herramientas |
| 3 · Harness y skills | instruir → ejecutar → revisar | tú, en reglas y checks |
| 4 · IA que investiga | proponer → correr → ¿conservar? | tu métrica |

Conclusión: cuando el juez pasa de los datos a ti, tu trabajo pasa de producir resultados a juzgarlos.

Consecuencia visual: **el juez siempre es ámbar.** Lo que haga de juez en una figura (el token
objetivo, el humano, el verificador, el resultado de la herramienta, la métrica, el evaluador) va
en ámbar `#F2A541`. Nada más es ámbar, salvo lo que el juez conservó.

---

## 1. Reglas globales (aplican a todo)

### 1.1 Lienzo y exportación

| | Escenas (animaciones) | Figuras fijas |
| --- | --- | --- |
| Tamaño | 1920×720 px (8:3) | 1920×720 px (8:3) |
| Fondo | sólido `#0F1626` | PNG transparente (la diapositiva es `#141D2F`) |
| Formato | MP4, H.264, yuv420p, 30 fps, ≤ 20 MB | PNG (+ SVG si es vectorial) |
| Entregar también | `still.png`: el cuadro más representativo | — |
| Duración | 20–45 s; cuadro final sostenido ≥ 3 s | — |

La diapositiva muestra el recurso en una caja de 1664×576 (`object-fit: contain`), es decir a ~0.8×.
**El titular está en la diapositiva. Nunca pongas el titular dentro del recurso.**

### 1.2 Paleta y semántica (nunca reasignar un color)

| Token | Hex | Significado |
| --- | --- | --- |
| bg | `#0F1626` | fondo de escena |
| panel | `#141D2F` | paneles, terminales |
| card | `#1E2A40` | tarjetas dentro de paneles |
| border | `#2A3550` | bordes de panel |
| axis | `#3A475C` | ejes, rejilla, flechas inactivas |
| text | `#ECEEF0` | texto principal |
| muted | `#B9C3CF` | texto secundario, etiquetas |
| gray | `#5B6678` | descartado / rechazado / inactivo |
| **ámbar** | `#F2A541` | **el juez**, y lo que el juez conservó |
| modelo | `#5FA8D3` | el modelo / el agente / sus salidas |
| query Q | `#5FA8D3` | consultas de atención (solo diapositiva 4) |
| key K | `#B39DDB` | claves de atención (solo diapositiva 4) |
| value V | `#6FC2A5` | valores de atención (solo diapositiva 4) |
| error | `#C97B63` | falla / incorrecto (siempre con una palabra) |

El color nunca carga el significado solo: todo estado ámbar/gris/error lleva además una palabra
(«conservado», «descartado», «correcta», «incorrecta», «falló»).

### 1.3 Tipografía y formato

- Etiquetas y texto: **IBM Plex Sans** (Google Fonts).
- Código, logs, tokens y números en tablas: **JetBrains Mono** (github.com/JetBrains/JetBrainsMono).
- Números grandes: **Space Grotesk** 600–700.
- Tamaño mínimo: **28 px a 1920 de ancho**. Solo la etiqueta «ilustrativo» puede bajar a 18 px.
- Máximo ~12 palabras en pantalla por momento.
- Números con el mismo formato del deck: punto decimal y coma de miles (`79.4%`, `1,260`).
- Español neutro, con tildes y signos de apertura (`¿`, `¡`). Revisa la ortografía.

### 1.4 Movimiento

- Manim Community Edition ≥ 0.19 (`pip install manim`; requiere las librerías de Pango/Cairo).
- Una idea por momento; ease-in-out; sin giros, rebotes ni transiciones llamativas.
- Patrón de ritmo de todo el deck: **lento primero, luego rápido** — 1 a 3 iteraciones a velocidad de
  lectura, luego acelerar para mostrar escala.
- Reutiliza los componentes de `common.py` (sección 3) para que todo parezca un solo sistema.
- Implementación de referencia ya hecha: `scene01_autoresearch_log.py` (diapositiva 1). Copia sus
  convenciones (constantes de paleta, tamaño de fuente por ancho de carácter, cargador de
  `results.tsv`, lógica de la etiqueta de datos ilustrativos, ciclo lento-luego-rápido).

### 1.5 Honestidad con los datos (reglas duras)

1. Cada número en pantalla está **calculado por el script** (con un modelo real, datos reales o una
   simulación declarada) o **tomado de una fuente que abriste**, registrada en `SOURCES.md`.
2. Todo lo simulado o ilustrativo lleva una etiqueta pequeña gris, abajo a la derecha:
   `ilustrativo` o `simulación de juguete, calculada` (18–20 px, `#5B6678`).
3. Nunca inventes títulos de papers, autores, citas, puntajes ni números de referencias.
4. Si no puedes abrir una fuente o verificar un valor, **detente y repórtalo** en `BUILD_LOG.md`; no
   lo reemplaces por un número plausible.
5. Fija todas las semillas aleatorias; el build debe ser reproducible.

Las cifras de la sección 5 ya fueron verificadas contra sus fuentes el 11 oct. 2026 (ver la revisión
de literatura de la charla). Vuelve a abrir la fuente antes de ponerlas en pantalla.

### 1.6 Estructura de entrega

```
figures/
  common.py                  # paleta, fuentes y componentes compartidos (sección 3)
  SOURCES.md                 # cada fuente usada, con URL y qué se tomó de ella
  BUILD_LOG.md               # qué se construyó, versiones de modelos, semillas, pendientes
  S01_autoresearch/  scene.py  S01.mp4  S01_still.png
  F03_siguiente_token/ make.py  F03.png
  S04_atencion/ ...
```

---

## 2. Índice de figuras

Escena = animación (MP4 + still). Figura = PNG fijo. Nativa = se construye directamente en el deck,
sin recurso. Captura = la toma el expositor; tú solo preparas el marco.

| ID | Diap. | Tipo | Qué muestra | Estado |
| --- | --- | --- | --- | --- |
| C00 | — | Componente | Motivo del ciclo (propone → juzga → actualiza), reutilizable | **Construir primero** |
| S01 | 1 | Escena | Registro de autoresearch: conservado vs descartado, la pérdida baja | Hecha en inglés — **re-renderizar en español** con `results.tsv` real |
| — | 2 | Nativa | Tabla de los seis ciclos y sus jueces | Hecha en el deck |
| F03 | 3 | Figura | Top-8 de probabilidades del siguiente token, de un modelo real | Por construir |
| S04 | 4 | Escena | Una consulta atiende a cada clave; los pesos mezclan los valores | Por construir |
| — | 5 | Nativa | Tres etapas del entrenamiento y su juez | Hecha en el deck |
| S06 | 6 | Escena | 8 muestras, el verificador las marca, la política se mueve a la correcta | Por construir |
| S07 | 7 | Escena | Imagen → parches → tokens junto a tokens de texto | Por construir |
| — | 8 | Nativa | 81% vs 20% (encuesta de adopción) | Hecha en el deck |
| S09 | 9 | Escena | Ciclo del agente con herramientas; las herramientas son el juez | Por construir |
| F10 | 10 | Figura | Arquitectura del sistema multiagente de deep research de Anthropic | Por construir (**nueva**) |
| F11 | 11 | Figura | El harness: el modelo al centro y lo que lo rodea | Por construir (**nueva**) |
| — | 12–15 | Nativas | Anatomía de un skill, cómo crearlo, galería, harness = juez | Hechas en el deck |
| S16 | 16 | Escena | Ciclo maestro de autoresearch con el diff de `train.py` | Por construir |
| S17 | 17 | Escena | Torneo de hipótesis con Elo; la ganadora va al laboratorio | Por construir |
| S18 | 18 | Escena | Búsqueda evolutiva juzgada por un evaluador; cierra con ERA y AlphaEvolve | Por construir |
| — | 19–22 | Nativas | Tres números (AI Scientist, Kosmos, APE), evaluar al juez (58/74/84%), límites, cierre | Hechas en el deck |

Totales: 1 componente, 7 escenas nuevas + 1 re-render, 3 figuras fijas.

Eliminadas respecto a la versión 1: tokens y embeddings (antes S04), base vs chat (F06), leyes de
escala (F07), conversación de SFT (F08), diagrama de RLHF (F09), cómputo en inferencia (F11 antiguo),
encuesta de adopción (F14b, ahora nativa) y las capturas de las diapositivas 13 y 16 antiguas.

---

## 3. Componentes compartidos (`common.py`)

Constrúyelos una vez; todas las escenas los importan.

1. **Paleta y fuentes** — constantes exactas de 1.2/1.3; `config.background_color = "#0F1626"`,
   `config.frame_width = 16`, `config.frame_height = 6` (8:3).
2. **`LoopMotif(labels: list[str], judge_index: int, radius=1.6)`** — 3 o 4 nodos rectangulares
   redondeados sobre un círculo, con flechas curvas en sentido horario (`#3A475C`). El nodo juez va
   relleno en ámbar con texto oscuro (`#0F1626`); los demás con contorno `#5FA8D3` y texto `#ECEEF0`.
   Métodos:
   - `.pulse(i)` — resalta el nodo *i* y la flecha que sale de él (un paso de la vuelta).
   - `.lap(run_time)` — pulsa todos los nodos en orden una vez.
   - `.set_label(i, text)` — transforma la etiqueta de un nodo.
3. **`Terminal(title, width, height)`** — el panel de `scene01` (tres puntos, título, divisor).
4. **`TokenChip(text, color)`** — ficha monoespaciada redondeada; la usan S04 y S07.
5. **`Stamp(word, color)`** — la etiqueta en negrita «conservado / descartado / correcta /
   incorrecta / falló».
6. **`IllustrativeLabel(text="ilustrativo")`** — etiqueta gris abajo a la derecha.
7. **`BigNumber(value, caption)`** — número grande en Space Grotesk con una leyenda en muted.

Aceptación: una escena de prueba `ComponentSheet` que renderiza uno de cada uno, para revisión,
como `C00_sheet.png`.

---

## 4. Orden de construcción

1. `common.py` + `C00_sheet.png` (punto de revisión: paleta, fuentes, motivo del ciclo).
2. S09 (es el ciclo base; S16–S18 lo reutilizan).
3. S16, S18, S17.
4. S04, S07, S06.
5. Figuras fijas F03, F10 y F11.
6. Re-render de S01 en español (con el `results.tsv` del expositor, o con los datos de demo si aún
   no lo hay).

---

## 5. Prompts

Cada prompt indica: el titular de la diapositiva que el recurso debe demostrar, qué mostrar momento
a momento, de dónde salen los datos y cómo verificarlo.

### C00 — Motivo del ciclo (componente)

- **Propósito:** la firma visual de la charla; aparece en S06, S09, S16, S17 y S18.
- **Construir:** `LoopMotif` como en la sección 3, más exportaciones fijas
  `C00_ciclo_<parte>.png` (600×600, transparente) para cada fila de la tabla de la sección 0, con
  esas etiquetas y ese juez.
- **Verificar:** el nodo juez es el único ámbar; las flechas van claramente en sentido horario;
  etiquetas ≥ 28 px.

### S01 — Registro de autoresearch (diapositiva 1) · re-render en español

- **Titular:** «Un agente ya puede correr un ciclo de investigación toda la noche, sin nosotros».
- **Acción:** sin cambios de diseño. En `scene01_autoresearch_log.py`, traduce todos los textos en
  pantalla:

  | Inglés (actual) | Español |
  | --- | --- |
  | `kept` / `discarded` / `crash` | `conservado` / `descartado` / `falló` |
  | `results.tsv · autoresearch` | igual |
  | `▶ waiting for first run` | `▶ esperando la primera corrida` |
  | `▶ running #NN · 5:00 training budget` | `▶ corriendo #NN · 5:00 de entrenamiento` |
  | `■ queue empty · N runs logged` | `■ cola vacía · N corridas registradas` |
  | `experiment →` | `experimento →` |
  | `N experiments · H hours · 0 humans` | `N experimentos · H horas · 0 humanos` |
  | `… · K changes kept` | `… · K cambios conservados` |
  | `illustrative data` | `datos ilustrativos` |

  Ajusta el ancho de la columna de estado: «descartado» es más largo que «discarded». Las
  descripciones de los cambios (`lr 3e-4 → 6e-4`) pueden quedar en notación técnica.
- **Datos:** cuando el expositor entregue el `results.tsv` de una corrida real de
  github.com/karpathy/autoresearch, ponlo junto al script y corre
  `manim -r 1920,720 --fps 30 scene01_autoresearch_log.py AutoresearchLog`. La etiqueta de datos
  ilustrativos desaparece sola. Ajusta `MINUTES_PER_RUN` a los minutos reales por experimento.
- **Verificar:** los números del contador final coinciden con el TSV (filas, pérdida inicial y
  mejor, cambios conservados); ningún texto en inglés salvo nombres de archivo y código.

### F03 — Probabilidades del siguiente token (diapositiva 3, figura)

- **Titular:** «Un modelo de lenguaje es un archivo de números que predice el siguiente token».
- **Mostrar:** barras horizontales con los 8 siguientes tokens más probables para un prompt. El
  prompt va arriba en JetBrains Mono, terminado en un bloque de cursor. Barras en azul `#5FA8D3`,
  valores al final de cada barra (p. ej. `31.2%`), tokens como fichas monoespaciadas que muestran
  los espacios iniciales como `␣`.
- **Datos:** calcula con un modelo abierto real que hable español, vía Hugging Face `transformers`
  (`Qwen/Qwen2.5-0.5B` base). Prompt (constante editable, del campo del expositor):
  `"Durante la fase de apoyo de la marcha, la rodilla"`. Softmax sobre los logits de la última
  posición; nombra el modelo en una leyenda muted bajo la gráfica.
- **Verificar:** las probabilidades suman ≤ 100%; la leyenda nombra el modelo exacto y aclara que son
  probabilidades de una sola pasada.

### S04 — Atención (diapositiva 4, escena, ~40 s)

- **Titular:** «La atención deja que cada token decida qué otros tokens importan».
- **Momentos:**
  1. (0–4 s) Una fila de ~9 fichas de tokens:
     `El robot no levantó la caja porque estaba muy pesada`.
  2. (4–10 s) Selecciona el token consulta `pesada`: sube de él una caja azul (Q). Bajo cada token
     aparece una caja lavanda (K).
  3. (10–18 s) Líneas de Q a cada K; aparece el puntaje del producto punto en cada línea, luego el
     softmax los convierte en pesos: grosor de línea y etiqueta en %. El mayor peso debería caer en
     `caja` o en `robot`, el que dé la cabeza real.
  4. (18–28 s) Aparecen cajas verde azulado (V) bajo los tokens; cada una sube escalada por su peso
     y se suman en un vector de salida sobre `pesada`.
  5. (28–34 s) Zoom out: lo mismo pasa para todos los tokens a la vez; aparece el mapa de calor
     completo de esa cabeza (tokens × tokens) en intensidad azul.
  6. (34–40 s) Se escribe la fórmula debajo:
     `Atención(Q, K, V) = softmax(QKᵀ / √d) · V`. Sostener.
- **Datos:** corre un modelo en español con `output_attentions=True`, por ejemplo
  `dccuchile/bert-base-spanish-wwm-cased` (BETO). Elige programáticamente la capa y cabeza donde
  `pesada` atiende más a `caja`; muestra «capa L, cabeza H» en una leyenda muted. Los puntajes y
  pesos en pantalla son los reales (redondeados). Las cajas Q/K/V son esquemáticas (no imprimas
  componentes de vectores). Si el tokenizador parte una palabra, muestra las piezas reales. Si
  ninguna cabeza da un patrón claro, muestra el más fuerte real y anótalo en `BUILD_LOG.md`.
- **Verificar:** los pesos suman 100% (± redondeo); los colores Q/K/V no aparecen en ninguna otra
  parte del deck.

### S06 — Aprendizaje por refuerzo con verificador (diapositiva 6, escena, ~35 s)

- **Titular:** «Con un verificador como juez, los modelos aprendieron a razonar paso a paso».
- **Momentos:**
  1. (0–4 s) Una tarjeta de pregunta: `17 × 24 = ?`. El modelo (nodo azul) emite 8 respuestas
     muestreadas como tarjetas.
  2. (4–10 s) Un nodo verificador (ámbar) revisa cada tarjeta: sello `correcta` (ámbar) o
     `incorrecta` (gris).
  3. (10–28 s) A la derecha: barras con la probabilidad de la política sobre K respuestas
     candidatas (incluida `408`). Reproduce los pasos de entrenamiento; las barras se mueven; la de
     `408` crece. Contador de pasos en mono. Los 2 primeros pasos lentos, luego rápido.
  4. (28–35 s) Estado final: probabilidad de la respuesta correcta, antes → después, como un par de
     `BigNumber`. Sostener.
- **Datos:** una corrida real de REINFORCE de juguete sobre una política softmax categórica con
  K = 6 respuestas (logits iniciales que favorecen dos incorrectas), recompensa 1 si es correcta y 0
  si no, lote de 8, semilla fija. Las 8 tarjetas del momento 1 son muestras reales del paso 0.
  Etiqueta: `simulación de juguete, calculada`.
- **Verificar:** la altura de las barras es igual a las probabilidades simuladas en cada paso
  mostrado.

### S07 — Las imágenes se vuelven tokens (diapositiva 7, escena, ~30 s)

- **Titular:** «Imágenes, audio y video se vuelven tokens que lee el mismo transformer».
- **Momentos:**
  1. (0–4 s) Aparece la imagen de entrada (izquierda).
  2. (4–9 s) Se dibuja una rejilla de 14×14 encima (parches de 16×16 píxeles sobre una imagen
     redimensionada a 224×224).
  3. (9–17 s) Los parches se levantan fila por fila y se aplanan en una sola fila de cuadritos;
     después de ~24 el resto se comprime en `… 196 parches`.
  4. (17–23 s) La fila pasa por una cajita «proyección lineal» y se convierte en `TokenChip`s azules.
  5. (23–30 s) Entra desde la derecha una fila de fichas de texto (`Describe este ciclo de marcha:`);
     ambas filas entran a un solo bloque «transformer». Sostener.
- **Datos:** `input.jpg` que entrega el expositor (p. ej. un cuadro de sus propios videos). Si no hay,
  usa una foto de prueba neutra con licencia libre y registra fuente y licencia en `SOURCES.md`.
- **Verificar:** la rejilla es exactamente 14×14; el texto de conteo dice 196.

### S09 — Ciclo del agente (diapositiva 9, escena, ~35 s) · ciclo base de S16–S18

- **Titular:** «Un agente cierra el ciclo con el mundo: las herramientas le responden».
- **Momentos:**
  1. (0–4 s) Se dibuja
     `LoopMotif(["observar", "pensar", "actuar", "resultado"], judge_index=3)`.
  2. (4–8 s) Cuatro íconos de herramientas alrededor del ciclo (íconos de línea simples, sin logos
     de marcas): búsqueda, código, archivos, API.
  3. (8–30 s) Tres vueltas. En cada vuelta: «pensar» muestra un pensamiento de una línea; «actuar»
     enciende una herramienta; una tarjeta de resultado vuelve de la herramienta a «resultado»
     (ámbar) y luego a «observar». Vuelta 1 lenta, vueltas 2 y 3 más rápidas.
  4. (30–35 s) Una tarjeta «respuesta» sale del ciclo hacia la derecha. Sostener.
- **Datos:** usa una traza real de agente si el expositor entrega `trace.json`
  (`[{thought, tool, result}]`). Si no, escribe una traza genérica corta en español (buscar tres
  papers sobre un tema, correr un script, resumir) y muestra la etiqueta `ilustrativo`.
- **Verificar:** cada vuelta usa una herramienta distinta; las tarjetas se leen a ≥ 28 px.

### F10 — Deep research por dentro (diapositiva 10, figura) · nueva

- **Titular:** «Deep research por dentro: un agente líder reparte la búsqueda entre subagentes».
- **Tamaño especial:** **1920×440 px** (la diapositiva lleva debajo una fila de tres números, así
  que la caja es más baja). PNG transparente.
- **Mostrar:** un flujo de izquierda a derecha:
  1. Tarjeta «pregunta».
  2. Nodo «agente líder» (azul, el más grande) con una pequeña tarjeta adjunta «plan → memoria».
  3. Un abanico hacia 4 tarjetas «subagente» apiladas (azul más claro), cada una con un ícono de
     búsqueda y su propia «ventana de contexto» dibujada como un marco; una etiqueta muted
     «3 a 5 en paralelo».
  4. Las flechas de los subagentes vuelven al líder, a un rombo «¿basta?» en **ámbar** (el juez
     en tiempo de ejecución). Del rombo sale una flecha «no → más subagentes» que vuelve al abanico,
     y otra «sí» hacia adelante.
  5. Tarjeta «agente de citas» (asocia cada afirmación con su fuente) → tarjeta final «reporte».
- **Datos:** ninguno numérico (los números van nativos en la diapositiva). La arquitectura sigue a
  Hadfield et al. (2025), *How we built our multi-agent research system*, Anthropic,
  https://www.anthropic.com/engineering/multi-agent-research-system — regístralo en `SOURCES.md` y
  revisa que los nombres de los componentes coincidan (LeadResearcher, subagentes, memoria,
  CitationAgent).
- **Opcional:** versión animada de ~20 s (la pregunta entra, el líder escribe el plan, los
  subagentes se abren en abanico y buscan a la vez, una vuelta por «no», luego «sí» → citas →
  reporte), como `F10.mp4` + still, con el mismo tamaño 1920×440.
- **Verificar:** solo el rombo «¿basta?» es ámbar; el flujo se lee de izquierda a derecha sin
  cruces de flechas; texto ≥ 28 px.

### F11 — El harness (diapositiva 11, figura) · nueva

- **Titular:** «El modelo es el motor; el harness es el carro».
- **Mostrar:** un diagrama de concentrador. Al centro, un nodo «modelo» (azul `#5FA8D3`, el más
  grande). Alrededor, seis tarjetas `#1E2A40` conectadas al centro con flechas hacia adentro, cada
  una con un título y una línea de ejemplo:

  | Componente | Ejemplo |
  | --- | --- |
  | Instrucciones | `CLAUDE.md` / `AGENTS.md` |
  | Contexto | tus archivos, papers y memoria |
  | Herramientas | búsqueda, código, APIs, MCP |
  | Skills | carpetas con `SKILL.md` |
  | Permisos | qué puede leer, escribir y ejecutar |
  | **Verificación** | tests, linters, un revisor independiente |

  Solo «Verificación» va en ámbar (contorno y título): es el juez. Una flecha de retorno curva sale
  del modelo, pasa por «Verificación» y vuelve al modelo, para mostrar que el harness cierra el
  ciclo. Etiqueta exterior pequeña en muted: «harness».
- **Datos:** ninguno (conceptual). Los nombres de componentes siguen a Lopopolo (2026, OpenAI) y a
  Böckeler (2026, «guías y sensores»); registra ambos en `SOURCES.md`.
- **Opcional:** una versión animada de 15 s (las tarjetas aparecen una por una y la flecha de
  retorno se dibuja al final), con el mismo diseño, como `F11.mp4` + still.
- **Verificar:** seis componentes, solo uno en ámbar; legible a ≥ 28 px; sin logos de marcas.

### S16 — Ciclo maestro de autoresearch (diapositiva 16, escena, ~35 s)

- **Titular:** «En autoresearch, tu métrica es el juez y el agente hace el resto».
- **Momentos:**
  1. (0–4 s) A la izquierda,
     `LoopMotif(["proponer", "correr 5 min", "evaluar", "¿conservar?"], judge_index=2)`.
  2. (4–8 s) Al centro, un `Terminal` pequeño titulado `train.py` con un diff de 3 líneas (líneas
     agregadas en azul con `+`, eliminadas en gris tachadas con `−`).
  3. (8–28 s) Vueltas: cada vuelta cambia el diff (proponer), se llena una barra de progreso
     (correr), el valor de la métrica aparece en el nodo «evaluar» (ámbar) y un `Stamp` dice
     `conservado` o `descartado`. A la derecha, la gráfica escalonada del mejor resultado crece con
     cada vuelta. 3 vueltas lentas, luego ~20 rápidas.
  4. (28–35 s) Leyenda bajo el ciclo: «tú escribes program.md; el agente escribe train.py». Sostener.
- **Datos:** **el mismo `results.tsv` de S01**, para que las diapositivas 1 y 16 cuenten una sola
  historia. Las líneas del diff salen de la descripción de cada fila (p. ej. `lr 3e-4 → 6e-4` se
  vuelve `- lr = 3e-4` / `+ lr = 6e-4`). Con el TSV de demo, muestra la etiqueta `ilustrativo`.
- **Verificar:** los sellos y la gráfica coinciden con las filas del TSV.

### S17 — Torneo de Co-Scientist (diapositiva 17, escena, ~35 s)

- **Titular:** «Co-Scientist: los agentes juzgan las hipótesis, y luego el laboratorio».
- **Momentos:**
  1. (0–5 s) Ocho tarjetas de hipótesis `H1`…`H8` (títulos genéricos cortos, o el `hipotesis.txt` del
     expositor) entran a una llave de torneo. Cada tarjeta muestra su Elo inicial: 1,200.
  2. (5–25 s) Se juegan los duelos: dos tarjetas se enfrentan; dos marcas de «debate» se alternan; la
     ganadora brilla en ámbar (la elección del juez) y avanza; una tabla Elo lateral se reordena tras
     cada duelo. Primera ronda lenta, luego rápido.
  3. (25–31 s) La campeona entra a una caja «validación en laboratorio» (contorno simple de un
     matraz).
  4. (31–35 s) Leyenda muted: «generar · reflexionar · rankear · evolucionar». Sostener.
- **Datos:** simula un torneo Elo real (K = 32, inicio 1,200) sobre puntajes de «calidad» ocultos,
  con semilla fija; los resultados de cada duelo se sortean con la probabilidad de victoria Elo.
  Etiqueta: `torneo ilustrativo, Elo calculado`. El mecanismo (agentes de generación, reflexión,
  ranking por torneo Elo desde 1,200, evolución y meta-revisión) sigue a Gottweis et al. (2026),
  *Nature* 655, 487–496, https://www.nature.com/articles/s41586-026-10644-y — regístralo en
  `SOURCES.md`.
- **Verificar:** los números Elo en pantalla son los simulados; ninguna hipótesis real se atribuye
  a Co-Scientist.

### S18 — ERA y AlphaEvolve: evolución contra un evaluador (diapositiva 18, escena, ~40 s)

- **Titular:** «ERA y AlphaEvolve escriben código y dejan que un evaluador lo juzgue».
- **Momentos:**
  1. (0–5 s) Una población de 12 tarjetas de «programa» (cada una muestra un dibujo pequeño de su
     solución candidata) en una rejilla; a la derecha, un nodo ámbar «evaluador».
  2. (5–25 s) Generaciones: las tarjetas pasan por el evaluador y reciben un puntaje; las de puntaje
     bajo se vuelven grises; las sobrevivientes generan hijos mutados (un morph corto). Una curva del
     mejor puntaje (ámbar) sube en una gráfica pequeña. Contador de generaciones en mono; las 2
     primeras lentas, luego rápido hasta ~200.
  3. (25–31 s) Zoom a la mejor solución encontrada.
  4. (31–40 s) Se limpia la pantalla y aparecen dos `BigNumber` lado a lado:
     - **40 de 87** — «métodos generados por ERA que superan todo el leaderboard de integración
       single-cell» (Aygün et al., *Nature* 2026).
     - **48** — «multiplicaciones para multiplicar dos matrices complejas 4×4» (AlphaEvolve,
       Novikov et al., 2025).
     Sostener.
- **Datos:** corre una búsqueda evolutiva real de juguete: ubicar 12 puntos en un cuadrado unitario
  para maximizar la distancia mínima entre pares (puntaje = distancia mínima); mutación = ruido
  gaussiano; selección por truncamiento; semilla fija. Etiqueta: `búsqueda evolutiva de juguete,
  calculada — ERA y AlphaEvolve usan un LLM para proponer cambios de código`. Fuentes de los números
  finales: Aygün et al. (2026), https://www.nature.com/articles/s41586-026-10658-6, y Novikov et al.
  (2025), https://arxiv.org/abs/2506.13131 — ábrelas y confirma la redacción antes de usarlas.
- **Verificar:** la curva no decrece nunca (mejor hasta el momento); las leyendas de los números
  coinciden con las fuentes.

---

## 6. Lista de entrega (por recurso)

- [ ] Renderizado a 1920×720; MP4 ≤ 20 MB; `still.png` exportado para cada escena
- [ ] Sin el titular de la diapositiva dentro del recurso; texto ≥ 28 px salvo la etiqueta ilustrativa
- [ ] Todo el texto en pantalla en español, con tildes, revisado
- [ ] El juez es el único elemento ámbar (más lo que conservó)
- [ ] Cada número rastreable al script o a `SOURCES.md`; lo simulado está etiquetado
- [ ] Semillas fijas; `BUILD_LOG.md` lista versiones de modelos y comandos
- [ ] Nombres de archivo según la sección 1.6
