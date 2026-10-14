# Notas de contexto (fuentes y detalles)
Lo que antes iba en las notas del expositor: cifras de respaldo, matices y fuentes, por diapositiva. El discurso para decir en voz alta está ahora en las notas del `.pptx` y del deck web (`discurso.py`).

## 0 · Portada

Portada. Déjala en pantalla mientras la gente se sienta.

## 1 · Un agente ya puede correr un ciclo de investigación toda la noche, sin nosotros

Pregunta: ¿quién corrió más experimentos anoche, ustedes o este script? Aquí se fija el código de color de toda la charla: ámbar es lo que el juez conservó, gris lo que descartó. El video usa datos ilustrativos (lo dice en la esquina); con tu results.tsv real se regenera.

## 2 · Seis ciclos, una forma: lo que cambia es quién juzga qué es «mejor»

Diapositiva de la tesis. Todo es el mismo ciclo: algo propone, algo juzga, algo actualiza. Lee la columna del juez de arriba abajo: pasa de los datos a los humanos, a los verificadores, a las herramientas, a tus reglas y al final a tu métrica. Cada diapositiva de ciclo lleva una etiqueta «Juez» arriba a la derecha.

## 3 · Un modelo de lenguaje son dos archivos: muchos números y un programa que los usa

El encuadre de Karpathy: un modelo abierto es un archivo de parámetros y un programa corto que lo corre. Lo que sigue en esta parte responde dos preguntas: qué hace ese programa con el texto, y de dónde salen los números.

## 4 · El modelo no lee palabras: lee tokens, pedazos de texto con un número

Los cortes y los números son reales: salen del tokenizador de Mistral. Las palabras comunes son un token; las técnicas se parten: «tibiofemoral» queda en seis pedazos. Por eso los modelos se equivocan más con vocabulario de nicho y por eso los precios y los límites se cuentan en tokens.

## 5 · Su único trabajo: dar una probabilidad a cada token posible

El modelo no devuelve una respuesta: devuelve una distribución sobre todo el vocabulario. Idea clave: no es una base de datos; si no le das la fuente, genera lo que un texto «probablemente diría». Las probabilidades son ilustrativas hasta correr datos_siguiente_token.py.

## 6 · Para escribir, repite: elige un token, lo agrega al texto y vuelve a predecir

Generar es un ciclo: predecir, elegir, agregar, repetir. La temperatura controla cuánto se arriesga al elegir: baja, casi siempre el más probable (repetitivo pero estable); alta, tokens menos probables (más variado, más errores). Por eso la misma pregunta da respuestas distintas.

## 7 · Cada token se vuelve un vector: tokens con significado parecido quedan cerca

Lo primero que hace el programa es cambiar cada número de token por una lista de miles de números: su embedding. Durante el entrenamiento, los tokens que aparecen en contextos parecidos terminan cerca. Este mapa es ilustrativo: los reales tienen miles de dimensiones. Vuelven en la Parte 2: así buscan los agentes.

## 8 · Aprender es equivocarse menos: la pérdida mide qué tan sorprendido quedó el modelo

Aquí está el primer juez de la charla. En el entrenamiento se tapa la palabra siguiente de un texto real y se le pide al modelo que la prediga. La pérdida es menos el logaritmo de la probabilidad que le dio a la correcta: si le dio 5%, la pérdida es alta; si le dio 90%, casi cero. El texto mismo es el juez.

## 9 · El gradiente dice hacia dónde mover cada número para que la pérdida baje

Imaginen un solo parámetro. Si lo subo un poquito, ¿la pérdida sube o baja? Esa pendiente es el gradiente, y se calcula para todos los parámetros a la vez con retropropagación. El paso: mover cada número un poco en contra de su pendiente. El tamaño del paso es la tasa de aprendizaje.

## 10 · Entrenar es repetir ese paso millones de veces: el descenso por gradiente

Con dos parámetros ya se puede dibujar: un paisaje, y el modelo baja paso a paso. Con miles de millones no se puede dibujar, pero la regla es la misma. Esta es la forma de todo lo que sigue: proponer, juzgar con la pérdida, actualizar.

## 11 · Lo mismo, a escala: miles de millones de números ajustados con billones de tokens

Para dar escala: 15 billones de tokens son del orden de toda la web de buena calidad que se pudo filtrar. Ese es el preentrenamiento: la etapa que más cuesta y la que pone casi todo el conocimiento. Llama es de los pocos modelos de frontera que publica estas cifras.

## 12 · Pero un token solo no basta: su sentido depende de los demás

El embedding de «pesada» es el mismo en cualquier frase. Para entender, cada token necesita mirar a los demás y decidir cuáles importan. Ese mecanismo es la atención, la pieza central del transformer.

## 13 · La atención deja que cada token decida a qué otros tokens mirar

Cada token hace una consulta (Q) y la compara con la clave (K) de los demás; el softmax vuelve esos puntajes pesos que suman 1, y con ellos mezcla los valores (V). Q, K y V tienen colores fijos que no se usan en otra parte. Los pesos son ilustrativos hasta correr datos_atencion.py con BETO.

## 14 · Un bloque transformer: la atención mezcla entre tokens; la red MLP trabaja cada uno

Un bloque tiene dos pasos. Atención: cada token toma información de los otros. MLP: cada token, por separado, transforma lo que reunió; ahí se guarda buena parte del conocimiento. Las flechas que rodean cada paso son conexiones residuales: el bloque suma una corrección, no reescribe todo.

## 15 · Se apilan decenas de bloques; el vector del último token da las probabilidades

Las capas de abajo capturan forma; las de arriba, significado y razonamiento. Al final, el vector del último token se compara con todo el vocabulario y sale la distribución de la diapositiva 5. Eso es todo el programa de la diapositiva 3.

## 16 · Todo lo que el modelo ve está en su ventana de contexto: su memoria de trabajo

La atención solo mira lo que está en la ventana. Lo que no está ahí, el modelo no lo sabe, salvo lo que quedó en sus parámetros con fecha de corte. Por eso lo que le pones (tus papers, tus datos, tus reglas) importa tanto como el modelo. Esta idea vuelve en la Parte 3.

## 17 · Leyes de escala: la pérdida baja de forma predecible con más parámetros y más datos

Cada curva es un tamaño de modelo; la envolvente baja como una ley de potencia. Por eso los laboratorios apuestan miles de millones: el resultado se puede predecir antes de entrenar. Chinchilla mostró que conviene crecer parámetros y datos a la par, unos 20 tokens por parámetro.

## 18 · El modelo preentrenado solo completa textos: no sigue instrucciones

El modelo base aprendió a continuar documentos: si el texto parece un examen, sigue con más preguntas. Sabe mucho, pero no tiene el rol de asistente. Las dos etapas que siguen cambian el comportamiento, no el conocimiento.

## 19 · Ajuste fino: se le muestran miles de conversaciones modelo escritas por personas

SFT por sus siglas en inglés. La pérdida es la misma de antes, pero sobre textos elegidos: conversaciones. LIMA mostró que con solo 1,000 ejemplos bien escogidos ya se obtiene mucho del comportamiento de asistente.

## 20 · RLHF: personas eligen la mejor de dos respuestas y el modelo aprende de esa elección

Aprendizaje por refuerzo con retroalimentación humana. El juez ahora son las preferencias de personas, resumidas en un modelo de recompensa. Riesgo conocido: el modelo aprende a sonar convincente y a dar la razón. DPO hace lo mismo sin el modelo de recompensa aparte.

## 21 · Con un verificador como juez, los modelos aprendieron a razonar paso a paso

Aprendizaje por refuerzo con recompensas verificables: matemáticas, tests que pasan. Nadie le muestra el procedimiento: solo un verificador que dice sí o no. Así salieron los modelos de razonamiento con cadenas de pensamiento largas. Idea clave: los modelos son más fuertes donde la respuesta se puede verificar.

## 22 · Pensar más compra precisión; y sin verificador, el juez puede ser una rúbrica

Dos ideas. Primero, cómputo en inferencia: dejar pensar al modelo, o muestrear varias respuestas y votar. Segundo, ¿qué pasa cuando no hay respuesta verificable? DR Tulu usa rúbricas que se refinan a partir de las respuestas y de la evidencia recuperada. Lo retomamos en deep research.

## 23 · Imágenes, audio y video también se vuelven tokens que lee el mismo transformer

La imagen se corta en parches, cada parche se proyecta a un vector, y entra a la misma secuencia que el texto. Audio y video igual, por fragmentos. Idea clave: tus videos y datos de sensores ya son entradas posibles, pero siguen necesitando una verdad de referencia.

## 24 · Casi todos probamos chatbots; muy pocos usamos agentes

Gancho de la Parte 2: «La mayoría de ustedes está en el ciclo del chat. La frontera está en este otro ciclo.» Por disciplina: 39% de los economistas y 25% de los politólogos usan agentes, frente a cifras de un dígito en salud pública, educación y comunicación. Por etapa: algo más de un cuarto de doctorandos y posdocs. Sé honesto con la muestra: se reclutó ofreciendo cuentas de Claude Max, así que sobrerrepresenta a interesados en IA, y Anthropic es parte interesada.

## 25 · Qué cambió: un LLM responde una vez; un agente actúa, mira el resultado y sigue

El modelo puede ser exactamente el mismo. Lo que cambia es el programa que lo envuelve: en el chat, tú eres quien ejecuta y trae los resultados de vuelta; en el agente, el programa lo hace y el modelo decide el siguiente paso.

## 26 · Tres cosas nuevas: herramientas, estado y muchos pasos

Estas tres piezas convierten un predictor de texto en algo que trabaja. Cada una trae su riesgo: herramientas que hacen daño, estado que se ensucia, y errores que se acumulan a lo largo de muchos pasos.

## 27 · Una herramienta es texto: el modelo escribe la llamada y el programa la ejecuta

Desmitifica la palabra «herramienta». El modelo solo genera texto; cuando genera una llamada con el formato acordado, el programa la detecta, la ejecuta y pega el resultado en el contexto. El modelo nunca toca internet: lee lo que el programa le devuelve.

## 28 · Un agente cierra el ciclo con el mundo: las herramientas le responden

El patrón ReAct: un modelo de lenguaje en un ciclo con herramientas. El resultado de cada herramienta vuelve como retroalimentación: el error de un script, el contenido de un archivo, una búsqueda vacía. Ese es el juez de esta parte.

## 29 · Por qué ahora: los modelos se entrenan para usar herramientas, no solo para conversar

Al principio los agentes eran puro prompt sobre un chat. Hoy los modelos se entrenan sobre trayectorias de agente, con las etapas de la Parte 1: preentrenamiento, ajuste fino y refuerzo. METR mide la duración, en tiempo humano, de las tareas que un modelo completa con 50% de éxito; entre 2019 y 2025 se duplicó cada siete meses aproximadamente.

## 30 · Deep research: preguntas que necesitan muchas búsquedas y una síntesis con fuentes

El ejemplo es de la clase de Akari Asai. La segunda pregunta no se responde con un dato: hay que separar benchmarks de comparaciones directas con expertos, y la respuesta honesta es matizada: prometedor en las tareas probadas, paridad con expertos aún no demostrada.

## 31 · Por dentro: un agente líder reparte la búsqueda entre subagentes

Patrón orquestador-trabajadores: el líder guarda su plan en memoria y lanza subagentes que buscan en paralelo, cada uno con su propia ventana de contexto. El «¿basta?» es el juez en tiempo de ejecución. Al final, un agente de citas asocia cada afirmación con su fuente. Ojo: es una evaluación interna del propio fabricante.

## 32 · Cómo se mide: BrowseComp, preguntas hechas para obligar a buscar mucho

1,266 preguntas escritas por personas, cada una armada con pistas para que la respuesta sea fácil de verificar y difícil de encontrar. Buscar en la web ayuda poco a un chat; un agente entrenado para buscar llega a la mitad. Pero un benchmark de respuesta corta no mide un reporte: para eso están las rúbricas, en la Parte 5.

## 33 · Un agente de deep research se entrena con las mismas tres etapas, ahora con herramientas

Es la Parte 1 otra vez: preentrenar, ajustar con ejemplos y reforzar con un juez. Lo único nuevo es que el texto incluye llamadas a herramientas y sus resultados. Así el agente no solo «sabe» usar herramientas por prompt: lo aprendió.

## 34 · Para buscar, el agente usa embeddings: la pregunta y los documentos como vectores

Además de la búsqueda web, muchos agentes usan búsqueda por embeddings sobre una colección propia: tus PDFs, por ejemplo. El problema que señala Asai: el buscador normalmente solo ve la última consulta, no lo que el agente está pensando.

## 35 · El harness junta todo lo anterior: modelo, contexto, herramientas, reglas y jueces

Este es el momento de juntar piezas. El modelo es la Parte 1; la ventana de contexto, la diapositiva 16; las herramientas, la Parte 2; la verificación, los jueces de toda la charla. Harness es el nombre de todo lo que rodea al modelo. Ejemplo extremo: el equipo de OpenAI que escribió cerca de un millón de líneas sin escribir ninguna a mano; su trabajo fue diseñar el entorno.

## 36 · Instrucciones: un CLAUDE.md que el agente lee al empezar cada sesión

La pieza más barata del harness. Claude Code lee CLAUDE.md; otros agentes usan AGENTS.md, que hoy es casi un estándar. Pon ahí lo que le dirías a un estudiante nuevo del laboratorio el primer día.

## 37 · Contexto: lo que el agente tiene a la vista, y hay que elegir qué entra

Vuelve a la diapositiva 16, la de la ventana de contexto. Un agente que trabaja horas llena 200,000 tokens rápido: cada resultado de herramienta entra ahí. Por eso el sistema de deep research usa subagentes: cada uno busca con una ventana limpia y le devuelve al líder solo un resumen.

## 38 · Herramientas y permisos: qué puede hacer el agente, y qué no sin preguntarte

Con datos clínicos, esta es la diapositiva más importante de la parte. Lo que no está en allow, el agente lo pregunta; lo que está en deny, no lo puede hacer. MCP es un protocolo abierto para conectar herramientas nuevas sin programar el agente.

## 39 · Un skill es una carpeta con instrucciones que el agente abre solo cuando la necesita

Un skill empaqueta algo que haces seguido: la forma en que tu grupo revisa una figura, prepara un reporte o limpia datos. El ejemplo de las próximas diapositivas es revisar-figura.

## 40 · Carga progresiva: el agente lee cada parte del skill solo cuando la necesita

Conecta con la diapositiva anterior de contexto: los skills son la forma de tener mucho conocimiento disponible sin pagarlo en tokens hasta que se usa.

## 41 · Anatomía de un SKILL.md: la descripción decide cuándo se activa

Los dos campos obligatorios son name y description. El error más común es una descripción vaga: el agente decide si abrir el skill solo con ella. El cuerpo puede apuntar a otros archivos para no crecer demasiado.

## 42 · Crear un skill: de una tarea repetida a una instrucción reutilizable

Demo en vivo (con respaldo grabado): pídele al agente que cree el skill revisar-figura a partir de estos cinco pasos, luego dale una figura real y muestra que el skill se activa solo, por su descripción. Puntos clave de Anthropic: empieza por ver dónde falla el agente; cuida la descripción, porque decide cuándo se activa; divide un SKILL.md largo en archivos; e itera con el propio agente, pidiéndole que guarde lo que funcionó y los errores comunes. Un skill es texto plano: lo puedes leer, editar y versionar en git como cualquier código.

## 43 · No empieces de cero: ya hay skills para investigar

Los tres ejemplos son reales y públicos. El de Bäckman es el mejor punto de partida para cualquier investigador: corre varios revisores en paralelo sobre tu borrador y guarda el reporte en una carpeta reviews/. Sus propias instrucciones advierten que el reporte «no es todo correcto»: el agente produce, tú juzgas. La advertencia de seguridad viene de Anthropic: un skill de una fuente poco confiable puede inducir acciones no deseadas o exfiltrar datos, así que se audita antes de instalarlo, igual que una dependencia de código.

## 44 · La última pieza, la evaluación: harness engineering es diseñar el juez

Esta diapositiva conecta la Parte 3 con la tesis. Las cuatro prácticas vienen de los textos de OpenAI y Google: un archivo de instrucciones corto que funciona como mapa; restricciones que se verifican mecánicamente; evaluaciones de comportamiento, que Google describe como tests de integración del harness; y una revisión independiente. Todas son formas de escribir tu criterio de «mejor» para que el agente lo respete sin ti. Ejemplo concreto, el sistema multiagente de la diapositiva 31: Anthropic lo evaluó con un LLM como juez y una rúbrica de cinco criterios (exactitud factual, exactitud de citas, completitud, calidad de fuentes y eficiencia en el uso de herramientas); empezó con unas 20 preguntas, sin esperar una batería grande; y aun así los evaluadores humanos encontraron lo que la rúbrica no veía: los primeros agentes preferían granjas de contenido optimizadas para SEO sobre fuentes autorizadas. El juez automático escala; el juez humano detecta lo que nadie pensó medir. Puente a la Parte 4: en autoresearch, Karpathy no escribe Python; escribe program.md, y la métrica decide.

## 45 · En autoresearch, tu métrica es el juez y el agente hace el resto

La versión en miniatura de todo lo que sigue, y la única que pueden correr esta noche. El agente edita un solo archivo, entrena 5 minutos y conserva el cambio solo si mejora la validación. Ojo: es un repositorio, no un paper; los trabajos que siguen son la evidencia publicada.

## 46 · Tú escribes program.md; el agente escribe train.py

Es un harness completo en un archivo de texto: instrucciones, permisos (solo train.py), herramienta (entrenar), memoria (git) y juez (val_bpb). El humano programa en lenguaje natural; el agente, en Python.

## 47 · Co-Scientist: seis agentes que proponen, critican y ordenan hipótesis

Es deep research más un ciclo de mejora. Cada agente es un prompt distinto sobre el mismo modelo, como los subagentes de la Parte 2. Todas las hipótesis empiezan con Elo 1,200 y suben o bajan según ganen debates.

## 48 · El torneo: los agentes juzgan cada par de hipótesis y el Elo las ordena

El Elo es el juez interno: barato y rápido, pero es un proxy. El juez que importa viene después: el laboratorio.

## 49 · Lo que se validó en el laboratorio

Tres áreas, tres tipos de evidencia. Lo que los autores reconocen: validación preliminar, no in vivo. Para un público clínico vale subrayarlo: es el inicio del ciclo de validación, no el final.

## 50 · ERA y AlphaEvolve escriben código y dejan que un evaluador lo juzgue

La misma idea: un LLM propone cambios de código y un puntaje automático decide qué se queda. ERA: en integración de datos single-cell, 40 de 87 métodos generados superan el leaderboard publicado. AlphaEvolve: multiplicó matrices complejas 4×4 con 48 multiplicaciones escalares. Ambos solo funcionan donde hay un evaluador automático.

## 51 · Ya hay investigación de punta a punta; el juicio sigue siendo el cuello de botella

Tres sistemas que van de la idea al paper, y un número de cada uno. The AI Scientist (Sakana, Nature 2026): un paper sin edición obtuvo 6, 7 y 6 en un workshop de ICLR 2025, por encima del 55% de los papers humanos; los autores lo retiraron antes de publicarse, y reconocen citas inexactas e ideas ingenuas. Kosmos (Edison): corridas de hasta 12 horas que leen ~1,500 papers y ejecutan ~42,000 líneas de código; científicos independientes juzgaron correctas el 79.4% de sus afirmaciones. Project APE (Zurich): ~1,000 papers de evaluación de políticas en cuatro meses; un juez automático prefiere el paper humano el 88.1% de las veces y su verificador estima que todos tienen errores. Si preguntan por síntesis de literatura en general: OpenScholar (Asai et al., Nature 2026) responde preguntas científicas buscando en la literatura y citando sus fuentes; en una evaluación con 108 pares, los expertos prefirieron sus respuestas sobre las escritas por expertos el 70% de las veces. Mensaje: producir ya no es el cuello de botella; juzgar sí.

## 52 · Demo: deep research sobre exoesqueletos, hecho solo con archivos de texto

Corre la demo, o muestra el corte grabado de 60 segundos. Señala los archivos de salida: plan.md, las notas de cada investigador, la verificación de cada cita y la evaluación del juez. El punto: el harness se escribe, no se programa.

## 53 · Hasta el juez necesita un juez: hay que medirlo contra expertos

Esta diapositiva cierra la tesis: no basta con tener un juez, hay que saber qué tan bueno es. Los tres números responden la misma pregunta en dos estudios distintos, así que compáralos como orden de magnitud, no como una tabla exacta. 58%: Xu et al. (ACL 2023, tabla 4), 109 pares con respuesta de referencia; BERTScore da 57% y BLEURT 62%, apenas por encima del azar. 74% y 84%: ResearchQA (Li, Chang, Malaviya y Yatskar, TACL 2026), un juez LLM con rúbricas frente al acuerdo entre dos expertos. 11%: el mismo paper, sobre las rúbricas generadas por el modelo sin apoyarse en surveys; las que se basan en fuentes fallan menos. El encuadre viene de la clase 10 de Akari Asai, Deep Research Agents, CMU 11-768 (otoño 2026), que recomienda auditar la rúbrica antes de usarla. Llévalo a la práctica: antes de confiar en tu juez automático, califica tú tres reportes y compara con sus puntajes.

## 54 · Todos los ciclos fallan igual: con un juez débil o fácil de engañar

Vuelve a la diapositiva 2: cada falla es una falla del juez. Las citas inventadas son un ciclo sin juez: en el estudio de OpenScholar (Asai et al., Nature 2026), GPT-4o sin búsqueda inventó citas en el 78–90% de los casos al pedirle literatura reciente; el reward hacking es un juez que el agente aprendió a engañar; la fuga de datos es un juez que ya vio la respuesta; el prompt injection envenena lo que el agente observa. Los checks van de más barato a más caro: minutos para los tres primeros, horas para reimplementar; guarda eso para tus tablas principales. Un segundo modelo de la misma familia comparte los mismos puntos ciegos: usa uno de otro laboratorio. La frontera irregular (Dell'Acqua et al., 758 consultores de BCG): dentro de la frontera de la IA, 12.2% más tareas y 25.1% más rápido; fuera de ella, 19% menos probabilidad de acertar. Sin un juez propio no sabes de qué lado estás. Menciona la política de EAFIT sobre uso de IA y autoría, y la regla práctica de divulgación: decláralo donde aparezca tu nombre.

## 55 · El modelo corre el ciclo. Tú decides qué cuenta como mejor.

Haz una pausa en el titular antes de mostrar los tres niveles. Cada nivel le pasa más trabajo al agente y exige un juez más explícito: en el 1 juzgas tú cada respuesta; en el 2 tu criterio queda escrito en el skill; en el 3, en la métrica. Luego abre a preguntas.
