# Revisión de literatura — IA para la investigación

Oct 11, 2026 · @Juan Martinez

## Resumen

La charla se apoya en 13 fuentes verificadas: tres papers de *Nature* 2026, dos preprints, un repositorio, dos estudios sobre cómo los investigadores usan la IA y cinco textos técnicos sobre harness, skills y deep research (el sistema multiagente de Anthropic va en las diapositivas 10 y 15). Todas cuentan la misma historia: **la IA ya investiga donde hay un juez medible, y falla donde el juez es débil.**

| Trabajo | Tipo | Dato que usamos | Diapositiva |
| --- | --- | --- | --- |
| [Co-Scientist](https://www.nature.com/articles/s41586-026-10644-y) (Gottweis et al.) | *Nature* 2026 | Torneo Elo de hipótesis; KIRA6 con ventana de 18× en células de AML | 17 |
| [ERA](https://www.nature.com/articles/s41586-026-10658-6) (Aygün et al.) | *Nature* 2026 | 40 de 87 métodos generados superan todo el leaderboard de integración single-cell | 18 |
| [AlphaEvolve](https://arxiv.org/abs/2506.13131) (Novikov et al.) | Preprint 2025 | Matrices complejas 4×4 con 48 multiplicaciones | 18 |
| [The AI Scientist](https://sakana.ai/ai-scientist-nature/) (Sakana) | *Nature* 2026 | Paper 100% generado con puntaje 6.33 en un workshop de ICLR 2025 | 19 |
| [Kosmos](https://arxiv.org/abs/2511.02824) (Mitchener et al.) | Preprint 2025 | 79.4% de sus afirmaciones son correctas | 19 |
| [Project APE](https://ape.socialcatalystlab.org/) (Social Catalyst Lab) | Proyecto abierto 2026 | \~1,000 papers; el juez prefiere el paper humano el 88.1% de las veces | 19 |
| [autoresearch](https://github.com/karpathy/autoresearch) (Karpathy) | Repositorio | Corridas de 5 min; el agente solo edita `train.py` | 1, 16 |
| [Coding agents in the social sciences](https://www.anthropic.com/research/coding-agents-social-sciences) (Lyttelton et al.) | Estudio Anthropic 2026 | 81% probó chatbots; 20% usa agentes cada semana | 8 |
| [Jagged Technological Frontier](https://pubsonline.informs.org/doi/10.1287/orsc.2025.21838) (Dell'Acqua et al.) | *Organization Science* 2026 | +12.2% de tareas dentro de la frontera; 19% menos correctas fuera | 20 |
| [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (Anthropic) | Blog técnico 2025 | Tres niveles de carga progresiva; estándar abierto desde dic. 2025 | 12–14 |
| [Harness engineering](https://openai.com/index/harness-engineering/) (OpenAI) | Blog técnico 2026 | \~1 millón de líneas, 0 escritas a mano, 3→7 ingenieros | 11, 15 |
| [Anatomy of Harness Engineering](https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/) (Google) | Blog técnico 2026 | Evaluaciones de comportamiento como "tests de integración" del harness | 15 |

Lo que dejamos fuera: los ejemplos de Novy-Marx & Velikov y de López-Lira que venían en las diapositivas de Bäckman. No abrí sus fuentes originales, así que no van en la charla hasta verificarlos.

## IA que investiga

Los seis sistemas tienen la misma estructura de propuesta, juez y actualización. Lo que los distingue es qué tan confiable es su juez.

| Sistema | Quién propone | Quién juzga | Resultado clave | Límite que reconocen |
| --- | --- | --- | --- | --- |
| Co-Scientist | Agentes de generación sobre Gemini 2.0 | Torneo Elo entre agentes (inicio en 1,200), luego el laboratorio | En AML, KIRA6 tuvo IC50 de 10 nM en KG-1a frente a 180 nM en células control (18×). En fibrosis hepática, 2 de 3 fármacos propuestos fueron antifibróticos en organoides | Validación preliminar (líneas celulares, no in vivo); el Elo es un proxy, no la verdad |
| ERA | Un LLM que reescribe código Python | Una métrica automática por tarea, con búsqueda en árbol tipo PUCT | Single-cell: 40 de 87 métodos superan todo el leaderboard. COVID: WIS de 26 frente a 29 del ensamble de CDC | Optimiza software empírico, no reemplaza el razonamiento teórico; se satura tras \~300–1,000 nodos |
| AlphaEvolve | LLMs que editan código | Uno o más evaluadores automáticos | Matrices complejas 4×4 con 48 multiplicaciones; mejoras en scheduling de centros de datos y en diseño de hardware | Preprint; solo problemas con evaluador automático |
| The AI Scientist | Agentes con búsqueda en árbol, de la idea al paper | Un revisor automático (69% de exactitud balanceada) y luego revisión humana | Paper sin edición aceptable en un workshop de ICLR 2025: puntajes 6, 7 y 6, por encima del 55% de los papers humanos | Ideas ingenuas a veces; citas inexactas; solo experimentos computacionales |
| Kosmos | Agentes de análisis de datos y de literatura con un modelo del mundo compartido | Científicos independientes que revisan cada afirmación | \~1,500 papers leídos y \~42,000 líneas de código por corrida de hasta 12 h; 79.4% de las afirmaciones son correctas | Cerca de 1 de cada 5 afirmaciones está mal; evaluado en 4 dominios |
| autoresearch | Un agente de código que edita `train.py` | La pérdida de validación tras 5 minutos de entrenamiento | Es un experimento de código abierto, no un paper; sirve como demo del ciclo | No tiene evaluación formal |

Project APE es el contraejemplo en ciencias sociales. Generó \~1,000 papers de evaluación de políticas entre enero y abril de 2026, y un juez automático prefirió el paper humano el 88.1% de las veces. Su propio verificador estima que todos los papers tienen errores o defectos, y el equipo pide no usarlos para decidir políticas. Es el mejor ejemplo de que la producción ya está resuelta y el juicio no.

## Harness y skills

El harness es todo lo que rodea al modelo: instrucciones, contexto, herramientas, skills, permisos y verificación. El término "harness engineering" se popularizó en 2026 y todavía no tiene una definición formal; las cuatro fuentes coinciden en la idea, no en las palabras.

**Agent Skills** — Anthropic, [*Equipping agents for the real world with Agent Skills*](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (Zhang, Lazuka y Murag, 16 oct. 2025).

- Un skill es una carpeta con un `SKILL.md`, cuyo encabezado YAML lleva dos campos obligatorios: `name` y `description`. Puede incluir archivos de referencia y scripts.
- Carga progresiva en tres niveles: (1) al iniciar, el agente solo ve nombre y descripción de cada skill; (2) si la tarea lo pide, lee el `SKILL.md` completo; (3) abre archivos adicionales o corre scripts solo cuando los necesita, sin meter su código en el contexto.
- Buenas prácticas: empezar evaluando dónde falla el agente, cuidar mucho la descripción (decide cuándo se activa) e iterar con el propio agente.
- Seguridad: un skill puede inducir acciones no deseadas; instalar solo de fuentes confiables y auditarlos antes.
- Desde el 18 de diciembre de 2025 es un estándar abierto ([agentskills.io](https://agentskills.io)).

**Harness engineering (OpenAI)** — Lopopolo, [*Harness engineering: leveraging Codex in an agent-first world*](https://openai.com/index/harness-engineering/) (11 feb. 2026).

- El trabajo del ingeniero pasa de escribir código a diseñar el entorno, especificar la intención y construir ciclos de retroalimentación.
- Un `AGENTS.md` de \~100 líneas como mapa, no como manual; el repositorio como única fuente de verdad; linters y tests como restricciones mecánicas.
- Resultado reportado: \~1 millón de líneas de código y \~1,500 pull requests en cinco meses, con 0 líneas escritas a mano, por un equipo que pasó de 3 a 7 ingenieros.

**Lectura crítica** — Böckeler (Thoughtworks), [*Harness Engineering – first thoughts*](https://www.martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html) (17 feb. 2026). Resume el harness como "guías y sensores" y advierte que el texto de OpenAI dice poco sobre verificar el comportamiento.

**Evaluar el harness** — Mullen y Gunderman (Google), [*The Anatomy of Harness Engineering*](https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/) (9 sep. 2026). Proponen evaluaciones de comportamiento (¿el agente corrió el validador?, ¿preguntó antes de asumir?) como tests de integración del harness. Es la pieza que conecta con la tesis: el harness es donde se construye el juez.

**Skills ya disponibles para investigar** — el `/review-paper` de Bäckman ([AI-research-feedback](https://github.com/claesbackman/AI-research-feedback), licencia MIT) y su [página del taller de Aarhus](https://claesbackman.com/aarhus/).

**Ejemplo de harness y de juez: deep research multiagente** — Hadfield et al., [*How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system) (Anthropic, 13 jun. 2025). Se usa en las diapositivas 10 y 15.

- Arquitectura orquestador-trabajadores: un agente líder guarda su plan en memoria, lanza 3 a 5 subagentes en paralelo con contextos separados, decide si hace falta más búsqueda, y un agente de citas asocia cada afirmación con su fuente.
- Un líder Opus 4 con subagentes Sonnet 4 superó a un solo Opus 4 en 90.2% en su evaluación interna. En BrowseComp, el uso de tokens explica el 80% de la varianza del desempeño. Un agente gasta \~4× los tokens de un chat; un sistema multiagente, \~15×.
- Evaluación: un LLM como juez con una rúbrica de cinco criterios (exactitud factual, de citas, completitud, calidad de fuentes y eficiencia), empezando con \~20 preguntas. Los evaluadores humanos encontraron lo que la rúbrica no veía: los primeros agentes preferían granjas de contenido SEO.
- Límite que reconocen: el patrón sirve poco para tareas con mucha dependencia entre agentes, como la mayoría del código. Es una evaluación interna del propio fabricante.

## Cómo usan la IA los investigadores

La mayoría de los investigadores ya usa chatbots, pero pocos usan agentes. Y la IA ayuda dentro de su frontera y perjudica fuera de ella.

**Adopción** — Lyttelton, Massenkoff y Wilmers, [*Coding agents in the social sciences*](https://www.anthropic.com/research/coding-agents-social-sciences) (Anthropic, 27 may. 2026). Encuesta a 1,260 científicos sociales cuantitativos, levantada entre finales de febrero y marzo de 2026.

- 81% ha probado chatbots para investigar; solo 20% usa agentes de código más de una vez por semana.
- Por disciplina: 39% de los economistas y 25% de los politólogos, frente a cifras de un dígito en salud pública, educación y comunicación.
- Por etapa: algo más de un cuarto de doctorandos y posdocs; menos de la mitad de esa tasa entre profesores titulares.
- Advertencia: la muestra no es representativa; se reclutó ofreciendo cuentas de Claude Max, así que sobrerrepresenta a interesados en IA. Anthropic también es parte interesada.

**Frontera irregular** — Dell'Acqua et al., [*Navigating the Jagged Technological Frontier*](https://pubsonline.informs.org/doi/10.1287/orsc.2025.21838) (*Organization Science* 37(2), 2026). Experimento preregistrado con 758 consultores de BCG en 18 tareas.

- Dentro de la frontera de la IA: 12.2% más tareas completadas y 25.1% más rápido.
- Fuera de la frontera: 19% menos probabilidad de llegar a la solución correcta que sin IA.
- Para la charla: sin un juez propio, el investigador no sabe de qué lado de la frontera está.

## Evaluar al juez

Un juez automático solo sirve si coincide con los expertos, y eso hay que medirlo. Se usa en la diapositiva 20. El encuadre viene de la clase 10 de Akari Asai, *Deep Research Agents: Tasks, Benchmarks, and Methods* (CMU 11-768, otoño 2026); los números se tomaron de los papers originales que ella cita.

| Juez | Coincide con la preferencia de expertos | Fuente |
| --- | --- | --- |
| ROUGE / BERTScore / BLEURT | 58% / 57% / 62% (azar: 50%), sobre 109 pares | [Xu et al., ACL 2023](https://aclanthology.org/2023.acl-long.181/), tabla 4 |
| LLM como juez con rúbricas (ensamble) | 74% | [Li et al., ResearchQA, TACL 2026](https://arxiv.org/abs/2509.00496) |
| Dos expertos entre sí | 84% | Mismo paper |

- ResearchQA también auditó las rúbricas: el 11% de los criterios generados por el modelo sin apoyarse en surveys eran vacíos, erróneos o poco claros.
- [OpenScholar](https://www.nature.com/articles/s41586-025-10072-4) (Asai et al., *Nature* 650, 2026): los expertos prefirieron sus respuestas sobre las escritas por expertos el 70% de las veces (108 pares), y GPT-4o inventó citas en el 78–90% de los casos al pedirle literatura reciente. Se usa en las notas de las diapositivas 19 y 21.
- DR Tulu (Shao, Asai et al., ICML 2026) usa rúbricas que evolucionan como recompensa de RL para reportes abiertos. Tomado de la clase, sin abrir el paper; solo va en las notas de la diapositiva 6.

**Discrepancias con la clase:** la clase dice 15% de criterios defectuosos y el paper de ResearchQA dice 11%. También atribuye a OpenScholar un acuerdo experto–LLM de 79% frente a 80% entre expertos, que no encontré en el artículo. Por eso se citan los originales y no la clase.

## Surveys para el mapa

Uno solo basta para la diapositiva de deep research.

- **[Deep Research: A Systematic Survey](https://arxiv.org/abs/2512.02038)** (Shi et al., 26 autores, nov. 2025). Propone cuatro componentes de un sistema de deep research: planificación de la consulta, adquisición de información, manejo de memoria y generación de la respuesta. Sirve para la diapositiva 10.
- Para la teoría (diapositivas 3–7) basta citar el artículo original de atención, Vaswani et al., [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762) (2017), sin cifras.

## Fuentes

Todas abiertas y leídas el 11 de octubre de 2026.

1. Gottweis et al. (2026). [Accelerating scientific discovery with Co-Scientist](https://www.nature.com/articles/s41586-026-10644-y). *Nature* 655, 487–496.
2. Aygün et al. (2026). [An AI system to help scientists write expert-level empirical software](https://www.nature.com/articles/s41586-026-10658-6). *Nature* 654, 909–916.
3. Sakana AI et al. (2026). [The AI Scientist, publicado en *Nature*](https://sakana.ai/ai-scientist-nature/) ([artículo](https://www.nature.com/articles/s41586-026-10265-5)).
4. Novikov et al. (2025). [AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131). arXiv 2506.13131.
5. Nagda, Thakurta y Raghavan (2025). [AI as a research partner: Advancing theoretical computer science with AlphaEvolve](https://research.google/blog/ai-as-a-research-partner-advancing-theoretical-computer-science-with-alphaevolve/). Google Research.
6. Mitchener et al. (2025). [Kosmos: An AI Scientist for Autonomous Discovery](https://arxiv.org/abs/2511.02824). arXiv 2511.02824.
7. Social Catalyst Lab (2026). [Project APE](https://ape.socialcatalystlab.org/). Universidad de Zurich.
8. Karpathy (2026). [autoresearch](https://github.com/karpathy/autoresearch). GitHub.
9. Lyttelton, Massenkoff y Wilmers (2026). [Coding agents in the social sciences](https://www.anthropic.com/research/coding-agents-social-sciences). Anthropic.
10. Dell'Acqua et al. (2026). [Navigating the Jagged Technological Frontier](https://pubsonline.informs.org/doi/10.1287/orsc.2025.21838). *Organization Science* 37(2).
11. Zhang, Lazuka y Murag (2025). [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills). Anthropic.
12. Lopopolo (2026). [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/). OpenAI.
13. Böckeler (2026). [Harness Engineering – first thoughts](https://www.martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html). martinfowler.com.
14. Mullen y Gunderman (2026). [The Anatomy of Harness Engineering](https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/). Google Developers Blog.
15. Shi et al. (2025). [Deep Research: A Systematic Survey](https://arxiv.org/abs/2512.02038). arXiv 2512.02038.
16. Bäckman (2026). [Practical AI for Academics, Aarhus](https://claesbackman.com/aarhus/) y [AI-research-feedback](https://github.com/claesbackman/AI-research-feedback).
17. Hadfield et al. (2025). [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system). Anthropic.
18. Asai (2026). *Deep Research Agents: Tasks, Benchmarks, and Methods*. Clase 10, 11-768 AI Agents, Carnegie Mellon University (PDF compartido por el expositor).
19. Xu, Song, Iyyer y Choi (2023). [A Critical Evaluation of Evaluations for Long-form Question Answering](https://aclanthology.org/2023.acl-long.181/). ACL 2023.
20. Li, Chang, Malaviya y Yatskar (2026). [ResearchQA: Evaluating Scholarly Question Answering at Scale Across 75 Fields](https://arxiv.org/abs/2509.00496). TACL 2026.
21. Asai et al. (2026). [Synthesizing scientific literature with retrieval-augmented language models](https://www.nature.com/articles/s41586-025-10072-4). *Nature* 650, 857–863.
