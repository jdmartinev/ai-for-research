# exo-deep-research

Un sistema de *deep research* multiagente para preguntas sobre exoesqueletos, hecho solo con
archivos de texto para Claude Code. Es una copia en pequeño de la arquitectura que Anthropic
describe en [*How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system)
(Hadfield et al., 2025): un agente líder, investigadores en paralelo, un verificador de citas y un
juez.

No hay código: todo el sistema son seis archivos `.md` y un `settings.json`. Ese es el punto de
la demo: **el harness se escribe, no se programa.**

## Qué hay

```
exo-deep-research/
├── CLAUDE.md                          # reglas del grupo para todos los agentes
├── rubrica.md                         # los criterios del juez
├── preguntas-prueba.md                # 10 preguntas para evaluar el sistema
├── .claude/
│   ├── settings.json                  # permite búsqueda y lectura web sin preguntar
│   ├── skills/investigar/SKILL.md     # /investigar: el agente líder (orquestación)
│   └── agents/
│       ├── investigador.md            # busca una subpregunta (Sonnet)
│       ├── verificador-citas.md       # abre cada fuente y la contrasta (Sonnet)
│       └── juez.md                    # califica con la rúbrica (Opus)
└── salidas/                           # se crea al correr: una carpeta por pregunta
```

| Rol | Archivo | Juez de qué |
| --- | --- | --- |
| Líder | `skills/investigar/SKILL.md` | Decide «¿basta?» tras cada ronda (máximo dos) |
| Investigador | `agents/investigador.md` | — (produce) |
| Verificador de citas | `agents/verificador-citas.md` | ¿La fuente dice lo que la nota afirma? |
| Juez | `agents/juez.md` + `rubrica.md` | ¿El reporte cumple la rúbrica? |
| Tú | — | Lo que la rúbrica no mide |

## Cómo correrlo

1. Copia la carpeta a tu computador y ábrela en una terminal.
2. Inicia Claude Code dentro de la carpeta: `claude`.
3. Escribe:

   ```
   /investigar ¿Qué estrategias de control de exoesqueletos de tobillo reducen el costo metabólico al caminar, con qué evidencia y en qué poblaciones?
   ```

4. Claude escribirá archivos en `salidas/`. Aprueba las escrituras cuando lo pida, o inicia la
   sesión con el modo que acepta ediciones automáticamente si prefieres no aprobar cada una.
5. Al terminar, revisa en `salidas/<pregunta>/`:
   - `plan.md`: cómo el líder partió la pregunta y cuánto esfuerzo decidió gastar.
   - `notas/`: lo que encontró cada investigador.
   - `verificacion-*.md`: el veredicto de cada cita (✔ ⚠ ✘).
   - `reporte.md`: la respuesta, solo con afirmaciones verificadas.
   - `evaluacion.md`: el puntaje del juez y sus fallas principales.

También puedes pedirlo en lenguaje natural («investiga la evidencia sobre…»): el skill se activa
solo por su descripción.

## Antes de usarlo en serio: evalúalo

1. Corre las 10 preguntas de `preguntas-prueba.md`.
2. Lee cada `evaluacion.md` y revisa tú mismo dos o tres reportes completos.
3. Donde falle, cambia el prompt del agente responsable y vuelve a correr esa pregunta.
4. Las preguntas 9 y 10 son trampas: el sistema debe reportar huecos, no inventar.
5. **Audita al juez.** Califica tú mismo, con `rubrica.md`, tres reportes sin mirar `evaluacion.md`;
   luego compara criterio por criterio. Como referencia, en ResearchQA (Li et al., TACL 2026) un
   juez LLM con rúbricas coincidió con expertos el 74% de las veces, y dos expertos entre sí el 84%.
   Si tu juez coincide contigo bastante menos, ajusta la rúbrica antes de confiar en sus puntajes:
   en ese mismo estudio, el 11% de los criterios de rúbricas generadas sin fuentes eran vacíos,
   erróneos o poco claros.

Así lo hizo Anthropic: empezaron con unas 20 preguntas, sin esperar una batería grande, y los
evaluadores humanos encontraron fallas que la rúbrica no veía.

## Costo y límites

- Un sistema multiagente gasta unas 15 veces los tokens de una conversación normal, según
  Anthropic. Una pregunta amplia puede tardar varios minutos. Úsalo para preguntas que lo valgan.
- La regla de esfuerzo de `SKILL.md` (1 investigador para un dato puntual, hasta 4 para una
  revisión amplia) existe para no gastar de más; ajústala a tu presupuesto.
- No reemplaza una revisión sistemática: no sigue un protocolo PRISMA ni garantiza cobertura. Es
  un primer mapa verificado, para que tú decidas dónde leer a fondo.
- Muchos artículos están detrás de muros de pago; el verificador marcará esos casos como «no se
  pudo abrir».

## Para la charla (diapositivas 31 y 52)

1. **La noche antes:** corre la pregunta 6 completa y guarda la carpeta `salidas/`.
2. **Graba** la terminal mientras corre (o al menos el momento en que se lanzan los investigadores
   en paralelo) y edita un corte de unos 60 segundos.
3. **En vivo**, abre solo tres archivos, uno tras otro (2 minutos):
   - `agents/investigador.md`: «esto es un subagente: un nombre, una descripción, herramientas».
   - `skills/investigar/SKILL.md`, paso 4: «aquí está el juez del líder: cuándo basta».
   - `salidas/…/evaluacion.md`: «y aquí el juez final, con las fallas que encontró».
4. Cierra con la idea de la Parte 3: *el harness entero son seis archivos de texto, y la mitad de
   ellos define quién juzga.*

## Cómo adaptarlo a otro tema

Cambia `CLAUDE.md` (el contexto y las reglas del grupo), el reparto sugerido de subpreguntas en el
paso 2 de `SKILL.md`, los criterios de dominio de `rubrica.md` y las preguntas de prueba. Los
agentes no tienen nada específico de exoesqueletos salvo los ejemplos de fuentes del investigador.
