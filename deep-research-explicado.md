# Deep research, explicado: el ejemplo de la charla y las recompensas verificables

Este documento explica dos cosas que en la charla van rápido:

1. **El ejemplo de la charla** (`demo-exo-deep-research/`): qué hace cada pieza y qué pasó en la
   corrida real del 14 de octubre de 2026.
2. **Cómo se entrena un agente de deep research**, y en particular qué significa una *recompensa
   verificable* (RLVR) en una tarea donde la respuesta es un reporte con citas.

La idea que conecta las dos: **en todo el sistema hay jueces, pero no todos hacen lo mismo.** Algunos
jueces *entrenan* al modelo (cambian sus pesos). Otros solo *revisan* el trabajo mientras corre (no
cambian nada del modelo). La demo de la charla usa solo los segundos. Confundir los dos es la fuente
más común de confusión con este tema.

---

## 1. Qué es deep research

Hay preguntas que se responden con una búsqueda:

> ¿Cuál es la oficina de Akari Asai en CMU?  → buscar → leer → responder

Y hay preguntas que exigen muchas:

> ¿Qué estrategias de control de exoesqueletos de tobillo reducen el costo metabólico al caminar,
> con qué evidencia y en qué poblaciones?
> → planear → buscar → leer → notar qué falta → buscar otra vez → sintetizar con citas

Un **agente de deep research** es un modelo de lenguaje en un ciclo: piensa, llama una herramienta
(búsqueda, abrir una página), lee el resultado, y decide qué hacer después. Lo que lo distingue de un
chat es que el resultado de cada herramienta vuelve al modelo: si la búsqueda no encontró nada, eso
también es información (diapositiva 28, el ciclo ReAct).

Los sistemas comerciales (OpenAI, Google, Anthropic) añaden una arquitectura encima: un **agente
líder** que planea y reparte la pregunta entre **subagentes** que buscan en paralelo, cada uno con su
propio contexto, y un paso final que revisa las citas (diapositiva 31; Hadfield et al., 2025).

---

## 2. El ejemplo de la charla

### 2.1 Las piezas

Todo el sistema son archivos de texto que Claude Code lee. No hay código.

| Pieza | Archivo | Qué hace | ¿Es un juez? |
| --- | --- | --- | --- |
| Reglas del grupo | `CLAUDE.md` | Lo que todos los agentes deben respetar: no citar sin abrir, separar sanos de clínicos, reportar n y efecto con unidades | No; es el contexto |
| Agente líder | `.claude/skills/investigar/SKILL.md` | Planea, reparte, decide si basta, escribe el reporte | **Sí**: decide «¿basta?» |
| Investigador | `.claude/agents/investigador.md` | Busca y lee para **una** subpregunta; escribe notas | No; produce |
| Verificador de citas | `.claude/agents/verificador-citas.md` | Abre cada fuente y marca ✔ ⚠ ✘ o «no se pudo abrir» | **Sí**: ¿la fuente dice eso? |
| Juez | `.claude/agents/juez.md` + `rubrica.md` | Califica el reporte con 8 criterios de 0 a 1 | **Sí**: ¿el reporte cumple la rúbrica? |
| Tú | — | Lees el reporte y la evaluación | **Sí**: lo que la rúbrica no mide |

### 2.2 Qué pasó en la corrida real

La carpeta está en `demo-exo-deep-research/salidas/control-tobillo-costo-metabolico/`.

**Plan (`plan.md`).** El líder clasificó la pregunta como *revisión amplia* y, según la tabla de
esfuerzo del skill, lanzó 4 investigadores en paralelo con subpreguntas que no se solapan:
estrategias de control en sanos · parámetros y mecanismo · sensado y fuera del laboratorio ·
poblaciones clínicas.

**El primer juez: «¿basta?».** Tras la ronda 1, el líder revisó su propio criterio (≥3 fuentes
primarias por subpregunta, ≥1 estudio con humanos por afirmación, contradicciones explicadas) y
concluyó que **no bastaba**: cifras clave sin fuente abierta (Zhang 2017, Collins 2015), ictus con un
solo estudio y una contradicción sin resolver. Lanzó una segunda ronda con 2 investigadores dirigidos
solo a esos huecos. Esa decisión es el rombo ámbar de la diapositiva 31.

**El segundo juez: el verificador de citas.** Seis verificadores, uno por archivo de notas,
revisaron 48 afirmaciones con cita: 30 ✔, 5 ⚠, 1 ✘ y 12 que no pudo abrir (muros de pago,
páginas que no cargan). La regla del skill: lo ✘ y lo que no se pudo abrir no entra al reporte
como hecho; lo ⚠ entra solo con la cifra corregida.

**El reporte (`reporte.md`).** 24 fuentes, una tabla de evidencia con población, n, tipo de estudio
y efecto con unidades, y resultados nulos incluidos (dos exoesqueletos rígidos en ictus que no
redujeron el costo; control mioeléctrico en exterior sin efecto).

**El tercer juez: la rúbrica (`evaluacion.md`).** Puntaje 0.86, aprobado, con tres fallas reales:
una contradicción entre dos estudios que el reporte no reconcilia, citas débiles en afirmaciones
clave, y una familia de control que el plan pedía y nadie buscó. Además dijo lo que la rúbrica no
mide: si faltan estudios clásicos que un experto echaría de menos.

**El juez también se equivocó.** Escribió que no encontró el archivo de verificación de la
subpregunta 3. El archivo existía (`verificacion-sensado-fase-y-campo.md`, 4 ✔): el juez lo buscó con
el nombre del plan y el investigador lo había guardado con otro. Se corrigió en `juez.md` (ahora
busca todos los `verificacion-*.md` y lista cuáles leyó). Es el mensaje de la Parte 4 en miniatura:
cada juez necesita un juez, y el último eres tú.

### 2.3 Lo importante: aquí nadie aprende

En la demo, los tres jueces **revisan** pero **no entrenan**. El modelo que corrió hoy es idéntico al
de mañana, saque 0.86 o 0.20. Si el sistema mejora, es porque **tú** editas los archivos: cambias la
rúbrica, la regla de «¿basta?» o el prompt del investigador, y vuelves a correr las 10 preguntas de
`preguntas-prueba.md`. Tú haces de algoritmo de optimización; los archivos son los parámetros.

En el entrenamiento de un agente (sección 3), el juez hace otra cosa: su veredicto se convierte en un
número, la **recompensa**, y ese número cambia los pesos del modelo.

| | Juez en ejecución (la demo) | Juez en entrenamiento (RL) |
| --- | --- | --- |
| Cuándo actúa | Mientras el agente trabaja para ti | Millones de veces, antes de que lo uses |
| Qué produce | Un veredicto que lees tú (o el líder) | Un número que entra al gradiente |
| Qué cambia | Nada, salvo que edites los archivos | Los pesos del modelo |
| Si se equivoca | Lees un reporte malo con buena nota | El modelo **aprende** a explotar el error |

La última fila es la razón por la que los jueces importan tanto más en entrenamiento: un juez débil en
la demo te da un mal reporte; un juez débil en entrenamiento te da un modelo entrenado para engañarlo.

---

## 3. Recompensas verificables (RLVR)

### 3.1 La idea, en una tarea simple

*RLVR* es *reinforcement learning with verifiable rewards*: aprendizaje por refuerzo donde la
recompensa la calcula **un programa**, no una persona ni otro modelo. La diapositiva 21 lo muestra con
17 × 24:

1. El modelo intenta 8 veces.
2. Un programa compara cada respuesta con 408 y da 1 o 0.
3. Los intentos correctos se refuerzan; los incorrectos se debilitan.

Nadie le enseña a multiplicar ni le muestra la solución paso a paso: solo hay un juez que dice sí o
no. Funciona porque el juez es **barato, objetivo e imposible de convencer con palabras**.

### 3.2 Cómo se vuelve verificable una tarea de búsqueda

El truco para deep research es elegir preguntas con una propiedad especial: **difíciles de encontrar,
fáciles de verificar**. La respuesta es corta y conocida, pero llegar a ella exige muchas búsquedas.
Ejemplo de ese estilo, con datos de nuestra corrida:

> ¿Cuál es el apellido del primer autor del artículo de *Science* de 2017 que optimizó en línea, con
> el humano en el lazo, el perfil de torque de un exoesqueleto de tobillo y redujo el costo metabólico
> cerca de 24 %?
>
> Respuesta conocida: **Zhang**

El agente tiene que buscar, leer, descartar candidatos y confirmar. Pero la recompensa es trivial:
¿la respuesta final es «Zhang»? Así se entrenó Search-R1 (COLM 2025), con *exact match* contra la
respuesta conocida, y así están construidos benchmarks como BrowseComp (diapositiva 32).

### 3.3 Qué pasa con la recompensa: GRPO

El algoritmo más usado hoy es **GRPO** (DeepSeekMath, 2024). Para cada pregunta:

1. El modelo genera un **grupo** de G trayectorias completas (pensar, buscar, leer, responder).
2. Cada trayectoria recibe su recompensa: 1 si la respuesta final es correcta, 0 si no.
3. Se compara cada trayectoria **con el promedio de su grupo**:
   ventaja Aᵢ = (rᵢ − media) / desviación estándar.
4. Se sube la probabilidad de todos los tokens que el modelo generó en las trayectorias con ventaja
   positiva, y se baja en las de ventaja negativa. Un recorte (*clip*) y una penalización KL evitan
   que un paso cambie demasiado el modelo.

En Python, el juez y la ventaja caben en 20 líneas:

```python
import re, statistics

def normalizar(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)          # quita puntuación
    s = re.sub(r"\b(et al|el|la|los|the)\b", " ", s)
    return " ".join(s.split())

def recompensa(respuesta, oro):
    """Exact match: 1 si la respuesta final coincide con la conocida, 0 si no."""
    return 1.0 if normalizar(respuesta) == normalizar(oro) else 0.0

oro = "Zhang"
intentos = ["Zhang", "Collins", "zhang.", "Sawicki"]   # respuesta final de 4 trayectorias
r = [recompensa(a, oro) for a in intentos]
media, desv = statistics.mean(r), statistics.pstdev(r) or 1.0
ventaja = [(ri - media) / desv for ri in r]           # GRPO: comparar dentro del grupo
for a, ri, A in zip(intentos, r, ventaja):
    print(f"{a:8s} recompensa={ri:.0f}  ventaja={A:+.1f}")
```

```
Zhang    recompensa=1  ventaja=+1.0
Collins  recompensa=0  ventaja=-1.0
zhang.   recompensa=1  ventaja=+1.0
Sawicki  recompensa=0  ventaja=-1.0
```

Si las cuatro trayectorias aciertan (o las cuatro fallan), todas las ventajas son 0 y esa pregunta no
enseña nada. Por eso se eligen preguntas que el modelo acierta a veces: ni tan fáciles ni imposibles.

### 3.4 Lo que no es obvio: se premia el final, se aprende el camino

La recompensa **solo mira la respuesta final**. Nadie califica cada búsqueda. Y sin embargo el modelo
aprende a buscar mejor, porque la ventaja se aplica a **todos los tokens que generó** en la
trayectoria: la consulta que escribió, la decisión de abrir un resultado, la de buscar otra vez. Las
trayectorias que buscaron bien tienden a acertar, así que esas decisiones se refuerzan en conjunto.

Dos detalles técnicos que importan:

- **El texto de las páginas no se entrena.** Lo que devuelve la búsqueda lo escribió otro, no el
  modelo; Search-R1 lo enmascara en la pérdida y solo actualiza sobre los tokens que el modelo generó.
- **La recompensa es escasa.** Una trayectoria de 30 búsquedas recibe un solo número al final. Por eso
  antes del refuerzo hay ajuste fino imitando trayectorias buenas de un modelo maestro (diapositiva
  33): el refuerzo mejora un comportamiento que ya existe, no lo crea desde cero. En DR Tulu, incluso
  un 5 % de ese ajuste fino previo ayuda.

### 3.5 Cómo falla una recompensa verificable

Verificable no significa perfecta:

- **Acertar por la razón equivocada.** «Zhang» es un apellido común: una trayectoria que adivina sin
  buscar recibe la misma recompensa que una que confirmó el artículo. Con suficientes preguntas el
  efecto se diluye, pero el juez no ve el camino.
- **Normalización.** «J. Zhang», «Zhang et al.» y «Juanjuan Zhang» son la misma respuesta; un exact
  match estricto castiga a dos de tres. Se usan normalizaciones o F1 por tokens.
- **Hackeo de formato.** Si el programa extrae la respuesta de una etiqueta, el modelo puede aprender
  a meter varias candidatas. Por eso se añaden recompensas de formato y límites de longitud.

---

## 4. Cuando no hay respuesta única: el reporte

Nuestra pregunta de la demo **no tiene una respuesta corta**. No existe una cadena «oro» contra la cual
comparar un reporte de 3,700 palabras. Aquí la recompensa deja de ser estrictamente verificable y se
vuelve una escala:

| Qué se puede verificar | Cómo | ¿Verificable? |
| --- | --- | --- |
| Respuesta corta conocida | Programa: exact match | Sí, totalmente |
| ¿La cita existe? | Programa: ¿abre el DOI o la URL? | Sí |
| ¿La fuente respalda la afirmación? | Un LLM lee la página y la frase (como nuestro verificador; DeepResearch Bench lo hace así) | Casi: depende del lector |
| ¿El reporte cubre lo importante? | Un LLM con una rúbrica (como nuestro juez) | Parcial: depende de la rúbrica |
| ¿Es la síntesis correcta del campo? | Un experto | No: es juicio |

### 4.1 Recompensa con rúbrica

Para cada pregunta se escribe una lista de criterios con pesos, y un modelo juez marca cuáles cumple
el reporte. La recompensa es el promedio ponderado. Ejemplo de ScholarQABench (clase de Asai):

| Criterio | Peso | ¿Lo cumple? |
| --- | --- | --- |
| Reporta una comparación directa con expertos | 2 | 1 |
| Matiza la conclusión según la tarea y el dominio | 1 | 0 |

recompensa = (2 × 1 + 1 × 0) / (2 + 1) = **0.67**

Es exactamente lo que hace nuestro `rubrica.md`, con una diferencia: aquí el número entra al
gradiente.

### 4.2 Por qué una rúbrica fija se deja engañar

Una rúbrica fija, usada millones de veces durante el entrenamiento, se convierte en un blanco. Si un
criterio dice «menciona estudios en poblaciones clínicas», el modelo aprende a mencionar poblaciones
clínicas en todos los reportes, vengan o no al caso. Los reportes se alargan, se vuelven listas de
todo, y la nota sube sin que la calidad suba. Además, las rúbricas mismas fallan: en ResearchQA
(TACL 2026), el 11 % de los criterios generados por un modelo sin apoyarse en fuentes eran vacíos,
erróneos o poco claros.

### 4.3 DR Tulu: rúbricas que evolucionan

DR Tulu (Shao, Asai et al., ICML 2026) ataca ese problema con **RLER**, *reinforcement learning with
evolving rubrics*:

1. **Criterios iniciales apoyados en búsqueda.** Antes de entrenar, se busca cada pregunta en internet
   y un modelo escribe los criterios leyendo esos documentos, no solo con lo que ya sabe. Así salen
   criterios más concretos: 56 % afirman algo específico, frente a 22 % de los escritos sin buscar.
2. **Criterios que evolucionan.** En cada paso de entrenamiento, un modelo compara los reportes que
   la política acaba de producir y escribe criterios nuevos:
   - *positivos*, para lo bueno que el modelo descubrió y la rúbrica aún no premiaba;
   - *negativos*, para los trucos que aparecieron. Los que reporta el paper: copiar texto recuperado
     palabra por palabra para inflar la precisión de las citas, y rellenar el reporte con afirmaciones
     citadas pero irrelevantes.
3. **Se descartan los criterios que no distinguen.** Un criterio que todos los reportes cumplen (o
   ninguno) tiene varianza cero: igual que la pregunta que todos aciertan en GRPO, no enseña nada. Se
   conservan los de mayor varianza.
4. **Recompensas auxiliares** con peso pequeño: formato, búsqueda y citas (se extraen afirmaciones y se
   verifica que el fragmento citado las respalde).

La idea: si el modelo encuentra una forma de engañar al juez, el juez aprende a verlo. El resultado es
DR Tulu-8B, un modelo abierto de 8 mil millones de parámetros. En la clase de
Asai, la comparación es clara: entrenar con rúbricas que evolucionan supera a entrenar con las
rúbricas iniciales, y ambas superan a no hacer refuerzo o a usar recompensas al azar.

### 4.4 Por qué esto importa para un investigador

Los modelos son más fuertes **donde el juez es más fuerte**. Un agente de deep research es muy bueno
encontrando datos con respuesta comprobable, y menos confiable en lo que nadie puede verificar con un
programa: si la selección de estudios es representativa, si la síntesis es justa con el campo. En la
corrida de la demo se ve igual: las cifras salieron casi todas correctas; las fallas que encontró el
juez estaban en la síntesis (una contradicción sin reconciliar, una familia de control que nadie
buscó).

Esa es la tesis de la charla aplicada a deep research: **la IA ya investiga bien donde hay un juez
medible, y necesita al humano donde el juez es débil.**

---

## 5. Cómo usar esto con la demo

- **Para evaluar el sistema**, haz lo que haría un equipo que entrena: muchas preguntas, un juez fijo, y
  mira el promedio. Son las 10 de `preguntas-prueba.md`.
- **Para auditar al juez**, califica tú tres reportes con `rubrica.md` sin mirar `evaluacion.md` y
  compara criterio por criterio. Como referencia, en ResearchQA un juez LLM con rúbricas coincidió con
  expertos el 74 % de las veces, y dos expertos entre sí el 84 %.
- **Para mejorar el sistema**, cambia un archivo por vez y vuelve a correr las mismas preguntas. Si
  solo sube la nota del juez pero los reportes no te parecen mejores, el sistema está aprendiendo a
  complacer la rúbrica: lo mismo que pasa en el entrenamiento, pero contigo como optimizador.

---

## Glosario

| Término | Qué es |
| --- | --- |
| Trayectoria | Todo lo que hizo el agente en un intento: pensamientos, búsquedas, lecturas, respuesta |
| Recompensa | El número que el juez le asigna a una trayectoria |
| RLVR | Refuerzo con recompensas calculadas por un programa (exact match, tests, verificador) |
| Exact match (EM) | 1 si la respuesta normalizada coincide con la conocida; 0 si no |
| GRPO | Refuerzo que compara cada intento con el promedio de su grupo, sin un modelo crítico aparte |
| Ventaja | Cuánto mejor (o peor) fue un intento que el promedio de su grupo |
| Rúbrica | Lista de criterios con pesos que un modelo juez revisa uno por uno |
| RLER | Refuerzo con rúbricas que evolucionan durante el entrenamiento (DR Tulu) |
| Hackeo de recompensa | Cuando el modelo sube la recompensa sin mejorar en lo que querías |
| Harness | Todo lo que rodea al modelo: instrucciones, herramientas, skills, permisos y jueces |

## Fuentes

- Asai, A. (2026). *Deep Research Agents: Tasks, Benchmarks, and Methods*. CMU 11-768. (Base de las
  secciones 3 y 4: Search-R1, GRPO, ScholarQABench, DR Tulu.)
- Jin, B. et al. (2025). [Search-R1: Training LLMs to Reason and Leverage Search Engines with
  Reinforcement Learning](https://arxiv.org/abs/2503.09516). COLM 2025 (según la clase).
- Shao, Z. et al. (2024). [DeepSeekMath](https://arxiv.org/abs/2402.03300) (GRPO).
- Shao, R., Asai, A. et al. (2026). [DR Tulu: Reinforcement Learning with Evolving Rubrics for Deep
  Research](https://arxiv.org/abs/2511.19399). ICML 2026. (Secciones 3.2 y 4.3, leídas en el original.)
- Wei, J. et al. (2025). [BrowseComp](https://arxiv.org/abs/2504.12516). OpenAI.
- Li, Y. et al. (2026). [ResearchQA](https://arxiv.org/abs/2509.00496). TACL 2026.
- Du, M. et al. (2026). [DeepResearch Bench](https://arxiv.org/abs/2506.11763). ICLR 2026 (según la clase).
- Hadfield, J. et al. (2025). [How we built our multi-agent research
  system](https://www.anthropic.com/engineering/multi-agent-research-system). Anthropic.
- DeepSeek-AI (2025). [DeepSeek-R1](https://arxiv.org/abs/2501.12948).
- Corrida de la demo: `demo-exo-deep-research/salidas/control-tobillo-costo-metabolico/`.
