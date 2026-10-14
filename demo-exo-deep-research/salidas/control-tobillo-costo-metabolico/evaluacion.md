# Evaluación

Material revisado: `rubrica.md`, `reporte.md`, `plan.md`, `notas/estrategias-control.md` y cinco
archivos de verificación (`verificacion-estrategias-control.md`, `-parametros-y-resultados.md`,
`-poblaciones-clinicas.md`, `-ronda2-sanos.md`, `-ronda2-clinicos.md`). **No pude localizar el archivo
de verificación de la subpregunta 3 (sensado/fase/fuera del laboratorio)**. Para compensar, abrí con
WebFetch tres fuentes de esa sección: Slade et al. 2022 (PMC9556303), Hybart et al. 2023b
(PMC10642814) y Medrano et al. (arXiv 2205.00155).

| Criterio | Puntaje | Justificación |
| --- | --- | --- |
| Exactitud factual\* | 0.85 | Los cuatro ⚠ de la verificación se corrigieron en el texto (Malcolm n = 8 de 10; Sawicki 0.65 kg; Poggensee −39.6 %; Lerner 2018 «vs. caminar sin exo») y el ✘ de 11.6 % se excluyó y se declaró. Pero en mi comprobación de Hybart 2023b, la frase «el exoesqueleto no la aumentó respecto a caminar sin él» solo vale para el exterior: en banda el exo **sí** aumentó significativamente los coeficientes de variación, y el reporte lo omite. |
| Exactitud de citas\* | 0.75 | Orekhov et al. 2022 se cita con una página divulgativa de embs.org y no con el artículo de IEEE TBME (no hay DOI), y la fuente 24 (adultos mayores, JNER 2024) va sin autores. Zhang 2017 se apoya solo en el resumen, Jackson & Collins 2015 se verificó en un «espejo oa.mg» y Poggensee en el preprint, aunque existe la versión publicada. La frase «todos los estudios tienen n ≤ 15, … sin cegamiento» no tiene cita ni verificación. |
| Completitud | 0.80 | Cubre las cuatro subpreguntas y declara huecos (LME, EM, Parkinson, metaanálisis). Pero la familia «imitación de torque biológico», que pide la subpregunta 1 del plan, no aparece, y la nota `estrategias-control.md` admite que «no busqué específicamente»: es un hueco que el reporte no declara. La subpregunta 3 apenas trata el sensado por IMU/EMG y la variación de velocidad o pendiente en sanos. |
| Calidad de fuentes | 0.85 | Casi todas las fuentes son estudios primarios revisados por pares (Nature, Science, JNER, PLOS ONE, J Appl Physiol). Bajan la nota el preprint de Poggensee usado como base, la página de embs.org para Orekhov y el uso de la revisión narrativa de Sawicki 2020 para afirmaciones de mecanismo («más no siempre es mejor»). |
| Eficiencia | 1.00 | `plan.md` clasifica la pregunta como revisión amplia: 4 investigadores y 2 rondas como máximo. Se hicieron 4 + 2 con una ronda 2 dirigida a huecos concretos (Zhang, Collins, Hybart, ictus rígido), sin repetir búsquedas. |
| Población y contexto\* | 0.90 | La tabla tiene columnas de población, n, tipo y tarea. Marca la simulación de Jackson 2017 en negrita, deja fuera el exo de cadera de Molinaro, presenta a los adultos mayores como «población especial, no clínica» y advierte que Bae 2018 es la misma cohorte que Awad. Faltan el n de Zhang 2017 y el de Jackson & Collins 2015 («no confirmado»), dos estudios en los que descansan conclusiones centrales. |
| Magnitudes | 0.90 | Casi todos los efectos llevan número, DE, unidades y comparación (p. ej., «−7.2 ± 2.6 % vs. sin exo (2.88 → 2.67 W/kg)»), y la contradicción 3 explica por qué las filas no son comparables. Jackson & Collins 2015 («−17 % / +13 %») no dice contra qué condición se compara, y Orekhov 2022 da solo porcentajes, sin dispersión. |
| Inferencia | 0.80 | Las contradicciones entre Koller y Hybart y entre exotraje y exo rígido en ictus están bien reportadas, sin atribuir la diferencia a la causa equivocada. Pero queda sin reconciliar una tensión interna: la sección 2 dice que el torque sin trabajo neto **aumentó** el costo hasta +13 %, y la sección 1 dice que el exo pasivo (sin trabajo neto) lo **redujo** 7 % y que «no hace falta aportar energía neta». Además, «la única comparación directa entre familias» es una afirmación universal que no se verificó. |

**Puntaje total:** 0.86 / 1.00 · **Veredicto:** aprobado

## Fallas principales
1. **Contradicción interna no tratada (regla 6).** Jackson & Collins 2015 dice que el torque sin
   trabajo neto sube el costo (+13 %), y Collins 2015 dice que un resorte pasivo sin trabajo neto lo baja
   (−7.2 %). El reporte presenta ambos hallazgos en secciones distintas y no los reconcilia. Explicaciones
   posibles que habría que discutir: la rigidez y el tiempo de enganche, el nivel de torque o la condición de
   comparación (exo a torque cero frente a caminar sin exo).
2. **Citas débiles o incompletas en afirmaciones clave.** Orekhov 2022 se cita con una página divulgativa
   de embs.org y no con el artículo; la fuente 24 no tiene autores. Además, Zhang 2017 (la cifra principal
   de humano en el lazo, −24.2 %) se apoya solo en el resumen y no tiene n, y Jackson & Collins 2015 se verificó en
   un espejo no oficial y tampoco tiene n. La frase de síntesis «sin cegamiento, casi siempre en una sola
   sesión» no tiene ninguna fuente.
3. **Resultado secundario recortado y hueco no declarado.** En Hybart 2023b el exo sí aumentó la
   variabilidad en banda, y el reporte da a entender que no la aumentó en ninguna condición. Además, la familia «imitación
   de torque biológico» del plan no se buscó y el reporte no lo dice. Tampoco pude encontrar el archivo de
   verificación de la subpregunta 3, así que las cifras de Slade, Medrano y Hybart 2023b solo las respalda
   mi comprobación puntual.

## Lo que esta rúbrica no mide
- Si la selección de estudios es representativa. Faltan trabajos conocidos que un experto echaría de menos,
  por ejemplo los de Sawicki/Ferris con control mioeléctrico de mediados de los 2000, Galle 2017 sobre la
  dosis de potencia, o Quinlivan 2017 (exotraje en sanos). Un humano debería juzgar si su ausencia sesga la
  conclusión de que el control mioeléctrico «empata» con el control por tiempo.
- La validez del protocolo metabólico de cada estudio: duración de los ensayos, estado estacionario, cómo se
  restó la condición en reposo y si la «potencia metabólica neta» y el «costo de transporte» se calcularon
  igual. Esto condiciona que las cifras puedan compararse entre filas más allá de la condición de
  comparación.
