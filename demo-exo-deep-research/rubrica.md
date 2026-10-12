# Rúbrica del juez

Adaptada de los cinco criterios que Anthropic usó para evaluar su sistema multiagente de
investigación (Hadfield et al., 2025), más tres criterios propios de biomecánica. Cada criterio se
califica de 0.0 a 1.0. El puntaje total es el promedio. **Aprobado** si el total es ≥ 0.75 y ningún
criterio marcado con \* está por debajo de 0.5.

## Criterios generales

| Criterio | 1.0 | 0.5 | 0.0 |
| --- | --- | --- | --- |
| **Exactitud factual\*** | Todas las afirmaciones coinciden con sus fuentes (verificación sin ✘) | Algún ⚠ sin advertir en el texto | Hay afirmaciones ✘ en el reporte |
| **Exactitud de citas\*** | Cada afirmación tiene una cita abierta y correcta | Algunas afirmaciones sin cita, o citas a revisiones cuando existe el estudio primario | Citas inventadas o que no abren |
| **Completitud** | Cubre todas las subpreguntas del plan y declara los huecos | Falta una subpregunta o los huecos no se declaran | Responde otra pregunta |
| **Calidad de fuentes** | Mayoría de artículos revisados por pares y estudios primarios | Mezcla con muchas fuentes secundarias | Blogs, prensa o páginas comerciales como base |
| **Eficiencia** | El esfuerzo corresponde al tipo de pregunta (según `plan.md`) | Una ronda de más o búsquedas repetidas | Esfuerzo desproporcionado o se detuvo sin evidencia |

## Criterios de biomecánica

| Criterio | 1.0 | 0.5 | 0.0 |
| --- | --- | --- | --- |
| **Población y contexto\*** | Separa sanos y clínicos, simulación y humanos, y reporta n y tarea | Los separa a veces | Los mezcla en una misma afirmación |
| **Magnitudes** | Los efectos llevan número, unidades y condición de comparación | Algunos efectos solo cualitativos | Sin magnitudes |
| **Inferencia** | Sin saltos causales; contradicciones reportadas | Alguna conclusión más fuerte que la evidencia | Conclusiones que la evidencia no sostiene |
