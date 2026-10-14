# Taller: CLAUDE.md y skills, paso a paso

Tres prácticas, de la más simple a la más compleja. Cada una se corre abriendo Claude Code
**dentro de la carpeta correspondiente**, porque Claude carga el `CLAUDE.md` y los skills de
`.claude/skills/` de la carpeta donde lo inicias.

| Práctica | Carpeta | Comando | Qué aprendes |
|---|---|---|---|
| 1. Revisar una figura de un paper | `taller-skills/` | `/revisar-figura` | Anatomía de un skill: instrucciones + checklist + scripts |
| 2. Skills de Bäckman (los de la charla) | `taller-skills/` | `/pdf-to-markdown`, `/review-paper-light` | Instalar skills de otros, leerlos y adaptarlos |
| 3. Estado del arte | `demo-exo-deep-research/` | `/investigar` | Un skill que orquesta subagentes y un juez |

## 0. Preparar (una vez)

```bash
git clone https://github.com/jdmartinev/ai-for-research.git
cd ai-for-research

# dependencias de los scripts de revisar-figura
python3 -m pip install numpy pillow
# poppler (pdftotext, pdftoppm): para sacar figuras de un PDF
#   macOS:   brew install poppler
#   Ubuntu:  sudo apt install poppler-utils
#   Windows: usa WSL, o conda install -c conda-forge poppler
```

Pon en `taller-skills/papers/` uno o dos PDFs de tu área (por ejemplo, un paper de exoesqueletos
con figuras de cinemática). Esa carpeta no se sube a git.

## 1. Revisar una figura de un paper

```bash
cd taller-skills
claude
```

La primera vez, Claude Code pregunta si confías en la carpeta: acepta. Sin eso ignora los
permisos de `.claude/settings.json` y te pedirá aprobar cada comando.

Dentro de Claude Code:

1. Escribe `/skills`. Debe aparecer `revisar-figura`. Si no aparece, no iniciaste `claude` dentro
   de `taller-skills/`.
2. Primera prueba, **invocación manual**:

   ```
   /revisar-figura papers/mi-paper.pdf Fig. 3
   ```

   Mira lo que hace, en orden: busca la página con `extraer_figura.py`, abre la imagen, lee el
   pie, recorre `checklist.md`, corre `contraste.py` y mira las simulaciones en gris y con
   daltonismo. El resultado queda en `revisiones/`.
3. Segunda prueba, **activación automática**. Sale con `/clear` y escribe en lenguaje natural:

   ```
   ¿Qué le mejorarías a la figura 2 de papers/mi-paper.pdf?
   ```

   No mencionaste el skill: Claude lo carga porque tu frase coincide con su `description`.
4. Tercera prueba, con **tu propia figura y su script**:

   ```
   /revisar-figura figuras/mi_figura.png src/graficar.py
   ```

   Ahora puede señalar la línea exacta del script que hay que cambiar.

¿Sin un paper a mano? Usa `ejemplo/paper-sintetico.pdf`: tiene una figura con errores puestos a
propósito (rojo–verde, colormap jet, ejes sin unidades, pie pobre). En `ejemplo/revision-fig2.md`
está lo que produjo el skill en una corrida real, para que compares.

Después abre los archivos y compara con lo que viste:

```
.claude/skills/revisar-figura/
├── SKILL.md              ← el procedimiento (6 pasos + errores típicos)
├── checklist.md          ← se lee solo en el paso 3
└── scripts/
    ├── extraer_figura.py ← PDF → PNG + pies de figura
    └── contraste.py      ← colores, contraste, gris y daltonismo (Machado et al., 2009)
```

Los scripts también se pueden correr a mano, sin Claude:

```bash
python3 .claude/skills/revisar-figura/scripts/extraer_figura.py papers/mi-paper.pdf --buscar "Fig. 3"
python3 .claude/skills/revisar-figura/scripts/contraste.py figura.png --paleta "#d62728,#2ca02c"
```

**Ejercicio:** cambia la `description` del skill para que solo hable de «gráficas» y repite la
prueba 3. Así ves qué tanto depende la activación automática de esa línea.

## 2. Los skills de Bäckman

Son los de la diapositiva «No empieces de cero» ([claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback),
licencia MIT). Instálalos **solo en esta carpeta**, para no mezclarlos con tus otros proyectos:

```bash
cd taller-skills
git clone --depth 1 https://github.com/claesbackman/AI-research-feedback.git /tmp/airf
cp -R /tmp/airf/Skills/pdf-to-markdown /tmp/airf/Skills/review-paper-light .claude/skills/
rm -rf /tmp/airf
```

(Para tenerlos en todos tus proyectos, cópialos a `~/.claude/skills/` en vez de `.claude/skills/`.)

**Antes de correrlos, léelos.** Abre `.claude/skills/review-paper-light/SKILL.md` y fíjate en el
encabezado:

- `disable-model-invocation: true`: Claude nunca lo lanza solo; solo corre si escribes
  `/review-paper-light`. Tiene sentido: lanza agentes y gasta tokens.
- `allowed-tools: ... Agent`: puede lanzar subagentes. El cuerpo lanza dos revisores en paralelo
  y luego consolida sus reportes.
- El texto dice «economics paper» y espera **LaTeX**. Ese es un límite real del skill.

### 2a. `/pdf-to-markdown` (el más simple)

```bash
claude
```
```
/pdf-to-markdown papers/mi-paper.pdf
```

Convierte el PDF a Markdown cortado antes de las referencias. Este sí se activa solo: prueba
«lee papers/mi-paper.pdf y resúmelo».

### 2b. `/review-paper-light` sobre un paper de arXiv

Necesita la fuente LaTeX. En arXiv, cualquier paper tiene un enlace *TeX Source*, o
`https://arxiv.org/e-print/<id>`:

```bash
mkdir -p papers/arxiv && cd papers/arxiv
curl -L -o fuente.tar.gz https://arxiv.org/e-print/<id-del-paper>
tar -xzf fuente.tar.gz && cd ../..
claude
```
```
/review-paper-light papers/arxiv/<archivo-principal>.tex
```

(Si no sabes cuál es el principal, escribe solo `/review-paper-light`: lo busca. Algunos papers de
arXiv vienen como un solo `.gz` en vez de `.tar.gz`; en ese caso, `gunzip` y renómbralo a `.tex`.)

El reporte queda en `reviews/QUICK_REVIEW_<fecha>.md` (los skills de Bäckman usan su propia carpeta, no `revisiones/`). Léelo con ojo crítico: los revisores están
escritos para economía (identificación causal, contribución). Verás cosas útiles y cosas fuera de
lugar para un paper de biomecánica.

**Ejercicio (el más instructivo del taller):** copia la carpeta a
`.claude/skills/review-paper-light-bio/`, cambia el `name`, y edita los dos revisores para tu
área (el editor de una revista como *J. NeuroEng. Rehabil.*; validez de un estudio con n pequeño,
sujetos sanos frente a clínicos, simulación frente a humanos). Corre los dos sobre el mismo paper
y compara. Así se adapta un skill ajeno: se lee, se copia y se edita el texto.

## 3. Estado del arte con `/investigar`

```bash
cd ../demo-exo-deep-research
claude
```
```
/investigar ¿Qué estrategias de control de exoesqueletos de tobillo reducen el costo metabólico al caminar, con qué evidencia y en qué poblaciones?
```

Aquí el skill es el **agente líder**: escribe un plan, lanza investigadores en paralelo
(`.claude/agents/investigador.md`), verifica cada cita (`verificador-citas.md`) y pide la
calificación de un juez (`juez.md` + `rubrica.md`). Tarda varios minutos y gasta bastantes
tokens; empieza con una pregunta acotada (las de `preguntas-prueba.md` sirven).

Mientras corre, abre en otra terminal `salidas/<pregunta>/plan.md`: ahí ves cómo el líder partió
la pregunta. Al final revisa `reporte.md` y `evaluacion.md`. Los detalles están en el
[README de la demo](../demo-exo-deep-research/README.md).

## 4. Ver qué está cargado

| Comando | Para qué |
|---|---|
| `/skills` | Lista los skills disponibles en esta sesión |
| `/context` | Muestra cuánto contexto ocupan CLAUDE.md y las descripciones de los skills |
| `/memory` | Abre los CLAUDE.md cargados para editarlos |
| `/init` | Genera un CLAUDE.md inicial en un repo que no tenga uno |
| `/reload-skills` | Recarga si creaste la carpeta `.claude/skills/` con Claude abierto |

## 5. Tu propio skill

Elige algo que hayas hecho tres veces (preparar los datos de un sujeto nuevo, revisar el formato
de una tesis, armar la tabla de una revisión) y pídeselo a Claude:

```
Crea un skill en .claude/skills/<nombre>/ que haga <tarea>. Los pasos son: ... Los errores
típicos son: ... Úsalo cuando yo diga cosas como: ...
```

Luego pruébalo en tres casos reales, y cada vez que falle, corrige el `SKILL.md`.
