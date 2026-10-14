"""Discurso de la charla: lo que se dice en cada diapositiva, en primera persona y para decirlo en voz alta.

Cada entrada reemplaza las notas del expositor de esa diapositiva. Unos 40–60 segundos por diapositiva.
Las cifras son las mismas de las diapositivas y sus fuentes están en el pie de cada una.
"""

DISCURSO = {
    "cover": (
        "Buenos días. Gracias a la Clínica Somer por la invitación. Soy Juan David Martínez, profesor de EAFIT, "
        "y trabajo en aprendizaje automático aplicado, sobre todo en análisis de marcha y exoesqueletos. "
        "Hoy quiero contarles qué cambió en la inteligencia artificial en los últimos años y cómo se está usando ya "
        "como herramienta de investigación. Y les voy a dejar una pregunta que nos va a acompañar toda la charla: "
        "¿quién decide qué cuenta como mejor?"
    ),
    "s01": (
        "Empiezo con esto. Lo que ven es el registro de un agente de IA que corrió toda una noche. "
        "Cada línea es un experimento: el agente cambia algo en el código de un modelo, lo entrena cinco minutos "
        "y mira si mejoró. Si mejoró, lo conserva; esos van en ámbar. Si no, lo descarta; esos van en gris. "
        "Setenta y dos experimentos, ocho horas, ninguna persona despierta. "
        "Les pregunto: ¿quién de ustedes corrió setenta y dos experimentos anoche? "
        "Fíjense en el color ámbar, porque va a aparecer toda la charla: es lo que el juez decidió conservar."
    ),
    "s02": (
        "Esta es la idea central de hoy. Todo lo que vamos a ver tiene la misma forma: algo propone, algo juzga "
        "y algo se actualiza. Lo que cambia de una etapa a otra es quién hace de juez. "
        "Al entrenar un modelo, el juez es el texto mismo. Al alinearlo, son las preferencias de personas. "
        "Para razonar, un verificador. En los agentes, las herramientas. Y al final, el juez es tu métrica. "
        "Mi tesis es esta: cuando el juez pasa de los datos a ustedes, el trabajo del investigador pasa de producir "
        "resultados a juzgarlos."
    ),
    "p1-archivos": (
        "Empecemos por lo básico. ¿Qué es un modelo de lenguaje? Literalmente, dos archivos. "
        "Uno tiene números, muchísimos: Llama 3.1, un modelo abierto de Meta, tiene 405 mil millones. "
        "El otro es un programa corto que multiplica esos números con el texto que le damos. "
        "Nadie escribió esos números a mano. Salieron de entrenar el modelo con texto. "
        "Las próximas diapositivas responden dos preguntas: qué hace ese programa con el texto, "
        "y cómo se aprenden esos números."
    ),
    "p1-tokens": (
        "Primero: el modelo no lee palabras, lee tokens. Un token es un pedazo de texto que tiene un número asignado. "
        "Esto que ven es un tokenizador real. Las palabras comunes, como «la» o «fase», son un solo token. "
        "Pero miren las palabras de nuestro campo: «tibiofemoral» queda partida en seis pedazos; "
        "«electromiografía», en cuatro. Eso explica dos cosas: por qué los modelos se equivocan más con vocabulario "
        "técnico, y por qué todo, los precios y los límites, se mide en tokens."
    ),
    "s03": (
        "Y con esos tokens, ¿qué hace el modelo? Una sola cosa: predice el siguiente. "
        "Le doy «Durante la fase de apoyo de la marcha, la rodilla…» y me devuelve una probabilidad para cada token "
        "posible. Fíjense que no devuelve una respuesta: devuelve una distribución. "
        "Esto es importante para nosotros como investigadores: el modelo no es una base de datos. "
        "Si no le damos la fuente, escribe lo que un texto así probablemente diría, sea cierto o no."
    ),
    "p1-generar": (
        "Para escribir un párrafo, el modelo repite ese paso. Predice, elige un token, lo agrega al texto y vuelve a "
        "predecir. Token por token. "
        "Y hay una perilla que se llama temperatura. Con temperatura baja casi siempre elige el más probable: "
        "respuestas estables pero repetitivas. Con temperatura alta se arriesga más: más variedad, pero más errores. "
        "Por eso, si le hacen la misma pregunta dos veces, pueden recibir dos respuestas distintas."
    ),
    "p1-embeddings": (
        "Ahora, adentro del programa, cada token se convierte en una lista de números, un vector. "
        "Lo interesante es que, después del entrenamiento, los tokens con significado parecido quedan cerca: "
        "rodilla, cadera y tobillo quedan juntos; marcha y carrera, juntos; proteína y enzima, lejos de todo eso. "
        "Este mapa es una simplificación en dos dimensiones; los reales tienen miles. "
        "Guarden esta idea, porque vuelve más adelante: así es como buscan información los agentes."
    ),
    "p1-perdida": (
        "Ahora sí, ¿cómo aprende el modelo? Con un juez muy simple: el texto mismo. "
        "Tomamos una frase real, tapamos la palabra siguiente y le pedimos al modelo que la prediga. "
        "Aquí la palabra correcta era «flexiona», y el modelo le había dado apenas un cinco por ciento. "
        "Eso lo medimos con la pérdida: qué tan sorprendido quedó el modelo con la respuesta correcta. "
        "Después de ajustar los números, le da sesenta y dos por ciento, y la pérdida baja. "
        "Aprender es eso: equivocarse cada vez menos."
    ),
    "p1-gradiente": (
        "¿Y cómo sabe qué números cambiar? Imaginen un solo número, un solo parámetro. "
        "Si lo subo un poquito, ¿la pérdida sube o baja? Esa pendiente es el gradiente. "
        "La regla es muy sencilla: mover el número un poco en contra de la pendiente, y repetir. "
        "Con un método que se llama retropropagación, esa pendiente se calcula para todos los números del modelo "
        "a la vez."
    ),
    "p1-descenso": (
        "Con dos parámetros ya podemos dibujarlo: es un paisaje, y el entrenamiento es bajar por él, paso a paso. "
        "A la derecha ven cómo cae la pérdida. "
        "Con 405 mil millones de parámetros no lo podemos dibujar, pero la regla es exactamente la misma. "
        "Y fíjense que ya aparece la forma de toda la charla: proponer, juzgar con la pérdida y actualizar."
    ),
    "p1-escala-entreno": (
        "Para que se hagan una idea de la escala: Llama 3.1 tiene 405 mil millones de parámetros, "
        "y se entrenó con 15.6 billones de tokens de texto. "
        "Eso se acerca a toda la web de buena calidad que se pudo recolectar y filtrar. "
        "A esta etapa se le llama preentrenamiento. Es la más costosa y es la que le da al modelo casi todo lo que "
        "sabe."
    ),
    "p1-sentido": (
        "Pero hay un problema. Lean estas dos frases. "
        "«El robot no levantó la caja porque estaba muy pesada»: pesada es la caja. "
        "«…porque estaba muy cansado»: cansado es el robot. "
        "Una palabra sola no basta; su sentido depende de las demás. "
        "El modelo necesita una forma de que cada palabra mire a las otras y decida cuáles le importan. "
        "Esa forma se llama atención."
    ),
    "s04": (
        "Así funciona la atención. La palabra «pesada» hace una pregunta, y la compara con cada una de las otras "
        "palabras. El resultado son pesos que suman uno: cuánto mira a cada palabra. "
        "Aquí el peso mayor cae en «caja», que es justamente a lo que se refiere. "
        "Con esos pesos, «pesada» mezcla la información de las otras palabras. "
        "Esa es la fórmula de abajo, y es la pieza central de todos los modelos actuales."
    ),
    "p1-bloque": (
        "Un bloque del transformer tiene dos pasos. Primero, la atención: los tokens intercambian información entre "
        "ellos. Después, una red neuronal que trabaja cada token por separado; ahí se guarda buena parte de lo que "
        "el modelo sabe. "
        "Las flechas de arriba son conexiones residuales: cada paso suma una corrección a lo que ya había, "
        "no lo reescribe todo."
    ),
    "p1-pila": (
        "Y esos bloques se apilan. Llama 3.1 tiene 126. "
        "Los vectores suben por la pila, bloque tras bloque, y se van refinando. "
        "Al final, el vector del último token se convierte en las probabilidades del siguiente token, "
        "las mismas que vimos hace un momento. "
        "Ese es, completo, el programa del que les hablé al principio."
    ),
    "p1-ventana": (
        "Una consecuencia muy práctica: el modelo solo puede mirar lo que está en su ventana de contexto. "
        "Es su memoria de trabajo. En Claude son unos 200 mil tokens: ahí caben sus instrucciones, sus papers, "
        "la conversación. "
        "Lo que no está en la ventana no existe para el modelo, salvo lo que aprendió en el entrenamiento, "
        "que tiene fecha de corte. "
        "Por eso lo que ustedes le dan, sus documentos y sus reglas, importa tanto como el modelo mismo."
    ),
    "p1-escala": (
        "¿Y por qué las empresas invierten miles de millones en entrenar modelos más grandes? "
        "Por esto: las leyes de escala. La pérdida baja de forma predecible cuando aumentan los parámetros y los "
        "datos. Cada curva es un tamaño de modelo, y la línea blanca es el mejor resultado posible para cada "
        "presupuesto. "
        "El trabajo de Chinchilla mostró que conviene crecer modelo y datos a la par: unos veinte tokens por "
        "parámetro. Se puede predecir el resultado antes de entrenar."
    ),
    "s05": (
        "Ahora, un modelo recién preentrenado no es un asistente. Solo sabe continuar textos. "
        "Si le pregunto «¿cuáles son las fases de la marcha?», puede seguir con más preguntas, como si fuera un "
        "examen. Sabe mucho, pero no sabe que tiene que responder. "
        "Para convertirlo en asistente hacen falta dos etapas más, y en cada una cambia el juez."
    ),
    "p1-sft": (
        "La primera es el ajuste fino. Se le muestran miles de conversaciones modelo, escritas o revisadas por "
        "personas: una pregunta y la respuesta ideal. "
        "Con eso aprende el formato y el rol: responder, seguir instrucciones, decir cuando no sabe. "
        "No aprende conocimiento nuevo; eso ya venía del preentrenamiento. "
        "El juez ya no es el texto de internet: son ejemplos humanos."
    ),
    "p1-rlhf": (
        "La segunda se llama RLHF, aprendizaje por refuerzo con retroalimentación humana. "
        "El modelo escribe dos respuestas, una persona elige la mejor, un segundo modelo aprende a predecir esas "
        "elecciones, y el modelo original se ajusta para ganar. "
        "Ahora el juez son las preferencias de las personas. Ojo con esto: premia lo que nos parece mejor, "
        "no necesariamente lo que es verdad. Por eso a veces los modelos suenan muy convincentes y se equivocan."
    ),
    "s06": (
        "La novedad de los últimos dos años es otro juez: un verificador. "
        "Le doy un problema con respuesta comprobable, por ejemplo 17 por 24. El modelo intenta ocho veces, "
        "un verificador marca cuáles son correctas, y el modelo se refuerza hacia las correctas. "
        "Nadie le enseña a multiplicar: solo hay un juez que dice sí o no. "
        "Así se entrenaron los modelos que razonan paso a paso. "
        "La lección para nosotros: los modelos son más fuertes donde la respuesta se puede verificar."
    ),
    "p1-pensar": (
        "Dos ideas más sobre esto. Primero, dejar que el modelo piense más tiempo, o que intente varias veces, "
        "mejora la precisión, pero solo si ya es bueno en esa tarea. "
        "Segundo, ¿qué pasa cuando no hay una respuesta única, como en un reporte de literatura? "
        "Un trabajo de este año, DR Tulu, usa rúbricas que se van refinando durante el entrenamiento. "
        "Es decir, el juez ya no solo evalúa: también entrena."
    ),
    "s07": (
        "Cierro esta parte con algo que les interesa directamente: las imágenes. "
        "Una imagen se corta en cuadritos, y cada cuadrito se vuelve un token, igual que una palabra. "
        "Esta imagen de marcha se convierte en 196 tokens, que entran junto con el texto al mismo modelo. "
        "Con el audio y el video pasa lo mismo. "
        "Es decir, sus videos clínicos y sus datos de sensores ya pueden ser entradas de un modelo general. "
        "Pero siguen necesitando una verdad de referencia contra la cual comparar."
    ),
    "s08": (
        "Pasemos a los agentes. Una encuesta de este año a más de mil científicos sociales encontró que el 81 por "
        "ciento ha probado chatbots para investigar, pero solo el 20 por ciento usa agentes con frecuencia. "
        "Con una advertencia: la muestra no es representativa; se reclutó ofreciendo cuentas de Claude. "
        "Aun así, la idea se sostiene: casi todos estamos en el chat, y la frontera está en los agentes."
    ),
    "p2-cambio": (
        "¿Qué cambió entre un chat y un agente? En el chat, el modelo responde una vez. "
        "Si le pido un script, me lo da; yo lo corro, me sale un error, se lo pego, y así. "
        "Yo soy el que actúa. "
        "Un agente recibe una meta. Busca, abre archivos, corre código, mira el resultado y decide el siguiente "
        "paso él mismo, hasta terminar. "
        "Lo importante: el modelo puede ser exactamente el mismo. Lo que cambia es el programa que lo rodea."
    ),
    "p2-nuevo": (
        "Ese programa le agrega tres cosas. Herramientas: puede buscar, leer archivos, ejecutar código. "
        "Estado: guarda un plan y notas que sobreviven entre pasos. "
        "Y muchos pasos: decenas o cientos de acciones sin que uno intervenga. "
        "Cada una trae su riesgo, y lo vamos a ver. Pero quédense con esto: lo nuevo no está en el modelo, "
        "está alrededor. A eso le vamos a llamar el harness."
    ),
    "p2-llamada": (
        "Les quiero quitar el misterio a la palabra «herramienta». Una herramienta es texto. "
        "Lo azul lo escribe el modelo: piensa, y luego escribe una orden de búsqueda con un formato acordado. "
        "El programa detecta esa orden, ejecuta la búsqueda de verdad y pega el resultado; eso es lo gris. "
        "Luego el modelo lee el resultado y decide: este estudio no tiene pacientes, lo descarto; abro el otro. "
        "El modelo nunca toca internet: solo lee lo que el programa le devuelve."
    ),
    "s09": (
        "Eso, en ciclo, es un agente: observar, pensar, actuar y ver el resultado. "
        "Y aquí el juez son las herramientas. Si el código falla, el error vuelve al modelo. "
        "Si la búsqueda no encuentra nada, eso también vuelve. "
        "Cada resultado es el juez del paso siguiente."
    ),
    "p2-porque": (
        "¿Por qué esto funciona ahora y no hace tres años? Porque los modelos se empezaron a entrenar para usar "
        "herramientas. En 2022 se le pedía al modelo, con instrucciones, que alternara pensar y actuar. "
        "En 2023 aprendieron el formato de las llamadas. "
        "Desde 2024 se entrenan con refuerzo sobre tareas de agente completas. "
        "Un grupo que se llama METR mide la duración de las tareas que logran terminar, y esa duración se ha "
        "duplicado más o menos cada siete meses."
    ),
    "p2-dr": (
        "Uno de los usos más útiles para nosotros es el deep research: investigación profunda. "
        "Hay preguntas que se responden con una búsqueda, como la oficina de una profesora. "
        "Y hay otras, como «¿pueden los agentes sintetizar literatura tan bien como los expertos?», "
        "que exigen planear, buscar, leer, darse cuenta de que falta algo, buscar otra vez y escribir con citas. "
        "Este ejemplo es de la clase de Akari Asai en Carnegie Mellon, que recomiendo mucho."
    ),
    "s10": (
        "Así funciona por dentro el sistema de deep research de Anthropic. Un agente líder recibe la pregunta, "
        "hace un plan y reparte el trabajo entre varios subagentes que buscan en paralelo, cada uno con su propia "
        "ventana de contexto. "
        "El líder decide si con eso basta; ese rombo ámbar es el juez. Al final, otro agente revisa que cada "
        "afirmación tenga su fuente. "
        "En su evaluación interna, esto supera en 90 por ciento a un solo agente, pero gasta unas quince veces "
        "más tokens que una conversación normal."
    ),
    "p2-eval": (
        "¿Y cómo sabemos si funcionan? Con benchmarks como BrowseComp: preguntas escritas para obligar a buscar "
        "mucho. "
        "Un modelo de chat responde menos del dos por ciento. Un modelo que razona, cerca del diez. "
        "El agente de deep research llega a la mitad. "
        "Pero ojo: estas son preguntas con respuesta corta. Un reporte de literatura es otra cosa, "
        "y para eso hacen falta otros jueces, que veremos al final."
    ),
    "p2-entreno": (
        "Y se entrenan con las mismas tres etapas que vimos en la primera parte, ahora con herramientas. "
        "Preentrenamiento con trayectorias de agentes. Ajuste fino imitando a un modelo maestro, "
        "pero solo las trayectorias que llegaron a la respuesta correcta. "
        "Y refuerzo, con un juez: la respuesta correcta, o rúbricas cuando se trata de reportes. "
        "Es la primera parte de la charla otra vez."
    ),
    "p2-busqueda": (
        "Y para buscar en sus propios documentos, los agentes usan los embeddings que vimos al principio. "
        "Cada documento se convierte en un vector; la pregunta también; y se devuelven los más cercanos. "
        "Un trabajo reciente, AgentIR, mostró que si al buscador se le pasa también el razonamiento del agente, "
        "y no solo la pregunta, encuentra más con menos búsquedas."
    ),
    "s11": (
        "Llegamos a la tercera parte, y aquí junto todo. Esto es el harness: todo lo que rodea al modelo. "
        "El modelo, que vimos en la primera parte. El contexto, que es la ventana de contexto. "
        "Las herramientas, de la segunda parte. Las instrucciones, los skills y los permisos, que veremos ahora. "
        "Y la verificación, en ámbar, que son los jueces de toda la charla. "
        "El mismo modelo da resultados muy distintos según el harness que lo rodea."
    ),
    "p3-claude-md": (
        "La pieza más sencilla son las instrucciones. En Claude Code se escribe un archivo, CLAUDE.md, "
        "que el agente lee al empezar cada sesión. "
        "Es lo que uno le diría a un estudiante nuevo del laboratorio el primer día: dónde están los datos, "
        "qué no se toca, que toda cifra lleva su fuente, que nunca invente una cita. "
        "Debe ser corto, un mapa y no un manual. Es su criterio, escrito una sola vez."
    ),
    "p3-contexto": (
        "La segunda pieza es el contexto: lo que el agente tiene a la vista. "
        "Siempre entran las instrucciones; al trabajar entran los archivos que abre y los resultados de cada "
        "herramienta. Y se llena rápido. "
        "Por eso los agentes resumen, o reparten el trabajo en subagentes, como en el sistema de deep research. "
        "Y una advertencia: más contexto no siempre es mejor; lo que no sirve distrae."
    ),
    "p3-permisos": (
        "La tercera pieza, y para una clínica quizás la más importante: los permisos. "
        "En un archivo de configuración se escribe qué puede hacer el agente sin preguntar, por ejemplo buscar o "
        "leer, y qué no puede hacer nunca, por ejemplo borrar archivos o abrir la carpeta de datos de pacientes. "
        "Las herramientas nuevas se conectan con un estándar abierto que se llama MCP: Zotero, una base de datos, "
        "el correo."
    ),
    "s12": (
        "La cuarta pieza son los skills. Un skill es una carpeta con instrucciones para una tarea que ustedes "
        "repiten: por ejemplo, revisar una figura antes de enviar un artículo. "
        "Tiene un archivo con los pasos, puede tener referencias y scripts. "
        "Es texto: se lee, se edita y se versiona como cualquier código. "
        "Y desde el año pasado es un estándar abierto, así que no depende de una sola herramienta."
    ),
    "p3-carga": (
        "Lo interesante de los skills es cómo se cargan. Al iniciar, el agente solo lee el nombre y la descripción "
        "de cada uno. Si la tarea coincide, abre las instrucciones completas. Si hace falta, abre las referencias. "
        "Y los scripts corren sin ocupar contexto. "
        "Por eso se pueden tener decenas de skills instalados sin llenar la ventana."
    ),
    "p3-anatomia": (
        "Así se ve uno por dentro. Arriba, dos campos: el nombre y la descripción. "
        "La descripción es lo más importante, porque es lo único que el agente ve al principio: "
        "si es vaga, el skill nunca se activa. "
        "Abajo van los pasos, escritos como se los explicaría a un estudiante."
    ),
    "s13": (
        "¿Cómo se crea uno? Elijan algo que ya hicieron tres veces. Escriban los pasos y los errores típicos. "
        "Describan cuándo usarlo. Pasen lo mecánico a un script. Y pruébenlo en casos reales. "
        "Lo pueden hacer pidiéndoselo al mismo agente: créame un skill con estos pasos. "
        "Si hay tiempo, lo muestro en vivo."
    ),
    "s14": (
        "Y no tienen que empezar de cero. Hay skills públicos para investigar. "
        "Uno que recomiendo es el de Claes Bäckman para revisar artículos: varios agentes revisores le escriben un "
        "reporte de árbitro a su borrador en unos quince minutos. "
        "Hay otros para bases de datos biomédicas, como PubMed. "
        "Una advertencia: instalen solo de fuentes confiables y léanlos antes, porque un skill le puede ordenar "
        "al agente cosas que ustedes no quieren."
    ),
    "s15": (
        "La última pieza del harness es la evaluación, y para mí es la más importante. "
        "Hacer harness engineering es diseñar el juez: un archivo corto de instrucciones, pruebas que el agente no "
        "puede saltarse, revisar cómo se comportó, y un revisor independiente, otro agente u otro modelo, que ataque "
        "el resultado. "
        "Todas son formas de escribir su criterio de «mejor» para que el agente lo respete sin ustedes al lado."
    ),
    "s16": (
        "Cuarta parte: IA que investiga. Vuelvo al ejemplo del principio. Esto es autoresearch, de Andrej Karpathy. "
        "El agente cambia una sola cosa del código, entrena cinco minutos, mira la métrica y conserva el cambio solo "
        "si mejora. Y otra vez, y otra vez. "
        "Aquí el juez es su métrica, y el agente hace todo lo demás. "
        "Es un repositorio, no un artículo; lo que sigue es la evidencia publicada."
    ),
    "p4-program": (
        "Lo que escribe la persona no es código: es un archivo de instrucciones, program.md. "
        "La meta, qué puede tocar, cuánto dura cada experimento, qué hacer si mejora y qué hacer si no. "
        "Fíjense que es un harness completo en una página: instrucciones, permisos, una herramienta, memoria en git "
        "y un juez que el agente no puede cambiar."
    ),
    "p4-cosci": (
        "Google lleva esto a las hipótesis científicas con Co-Scientist. Son seis agentes sobre el mismo modelo: "
        "uno propone hipótesis, otro las critica como un revisor, otro las ordena en un torneo, otro combina y "
        "mejora las mejores, otro agrupa las parecidas y otro resume las críticas. "
        "Es deep research con un ciclo de mejora encima."
    ),
    "s17": (
        "El torneo funciona como en el ajedrez. Todas las hipótesis empiezan con el mismo puntaje Elo. "
        "Se enfrentan por pares, los agentes debaten cuál es mejor, y el puntaje sube o baja. "
        "Pero ese puntaje es un juez interno, barato y rápido. "
        "El juez que de verdad importa viene después: el laboratorio."
    ),
    "p4-lab": (
        "Y lo llevaron al laboratorio. En leucemia mieloide aguda, un fármaco propuesto mostró una ventana de "
        "dieciocho veces entre células tumorales y células control. "
        "En fibrosis hepática, dos de tres fármacos propuestos funcionaron en organoides humanos. "
        "Pero para un público clínico hay que decirlo claro: esto es validación preliminar, en células y organoides, "
        "no en pacientes. Es el comienzo del ciclo, no el final."
    ),
    "s18": (
        "Otro par de sistemas de Google, ERA y AlphaEvolve, hacen lo mismo con código. "
        "Un modelo propone cambios a un programa, un evaluador automático los califica, y se conservan los mejores. "
        "ERA generó métodos de integración de datos de célula única, y 40 de 87 superan a todos los publicados. "
        "AlphaEvolve encontró una forma de multiplicar matrices de cuatro por cuatro con 48 multiplicaciones. "
        "Ambos funcionan solo porque existe un evaluador automático."
    ),
    "s19": (
        "Y ya hay sistemas que van de la idea al artículo. Un artículo escrito completamente por IA pasó la revisión "
        "de un taller de ICLR, aunque sus autores lo retiraron y reconocen citas inexactas. "
        "Kosmos acierta en cerca del 80 por ciento de sus afirmaciones; es decir, una de cada cinco está mal. "
        "Y en otro proyecto, un juez prefiere el artículo humano casi nueve de cada diez veces. "
        "Producir ya no es el cuello de botella. Juzgar, sí."
    ),
    "p4-demo": (
        "Les muestro una versión pequeña de todo esto, hecha para exoesqueletos. "
        "Es un sistema de deep research en Claude Code, y no tiene código: son seis archivos de texto. "
        "Un líder que planea, investigadores que buscan, un verificador que abre cada fuente "
        "y un juez que califica con una rúbrica. "
        "Le pregunto qué controles de exoesqueletos de tobillo reducen el costo metabólico al caminar… "
        "El harness se escribe, no se programa. Está en el repositorio, para que lo usen."
    ),
    "jueces": (
        "Última parte. Si todo depende del juez, hay que preguntar: ¿qué tan bueno es el juez? "
        "Una métrica automática de similitud coincide con los expertos el 58 por ciento de las veces, "
        "apenas por encima del azar. Un modelo de lenguaje usado como juez, con rúbricas, el 74. "
        "Y dos expertos entre sí, el 84: ese es el techo. "
        "Y las rúbricas también fallan. Antes de confiar en un juez automático, califiquen ustedes algunos casos "
        "y comparen."
    ),
    "s20": (
        "Todos estos ciclos fallan de la misma forma: con un juez débil o fácil de engañar. "
        "Sin juez, el modelo inventa citas. Con un juez débil, el agente aprende a engañarlo. "
        "Si el juez ya vio la respuesta, el resultado no vale. Y si alguien envenena lo que el agente lee, "
        "el agente obedece. "
        "Lo que ayuda: que otro agente ataque el resultado, que lo revise un modelo de otra empresa, "
        "y para lo que de verdad importa, reimplementarlo ustedes mismos."
    ),
    "s21": (
        "Cierro con esto. El modelo corre el ciclo; ustedes deciden qué cuenta como mejor. "
        "¿Qué pueden hacer el lunes? Tres niveles. "
        "Uno: escriban un archivo de instrucciones con su campo y sus reglas, y denle sus propios artículos. "
        "Dos: empaqueten en skills lo que repiten. "
        "Tres: monten ciclos autónomos solo donde tengan una métrica barata y honesta. "
        "Todo el material, las animaciones y la demo están en el repositorio. Muchas gracias."
    ),
}
