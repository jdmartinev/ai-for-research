# Completar evidencia clínica: exoesqueletos/exotrajes de tobillo y costo metabólico de la marcha (ronda 2)

Nota: por instrucción del líder, no se repiten aquí Bae/Awad 2018 (JNER, ictus, exotraje, n=7, −10.4%),
Tagoe 2024, Orekhov 2022 (parálisis cerebral) ni el estudio de adultos mayores 2024 (JNER), ya
verificados en la ronda 1.

## Hallazgos

- En ictus crónico, un exotraje de tobillo con control iterativo basado en fuerza/posición redujo
  el costo energético de caminar en banda un 10 ± 3 % (0.1979 ± 0.0218 ml O₂/kg/m con asistencia
  activa vs 0.2204 ± 0.0275 ml O₂/kg/m con el exotraje atado pero sin potencia), P = 0.009,
  equivalente a un 32 ± 9 % de reducción en la carga metabólica atribuible al ictus (más cercano a
  la economía normal de 0.151 ml O₂/kg/m), P = 0.009. [Awad et al., 2017, Sci Transl Med](https://doi.org/10.1126/scitranslmed.aai9084)
  — población: ictus crónico (4.4 ± 1.4 años post-ictus); n = 9 reclutados, n = 7 con datos de
  propulsión/energética válidos (2 excluidos por falta de medición bilateral de GRF); tipo:
  experimento con humanos, cruzado, sin grupo control externo (control = mismo exotraje sin
  potencia, "tethered unpowered"); tarea: caminata en banda instrumentada a la velocidad habitual
  overground de cada participante (0.53–1.3 m/s).
- El mismo estudio incluyó un sub-experimento con el exotraje puesto pero sin potencia (pasivo,
  "worn but unpowered") comparado con no llevarlo puesto (n = 5): no hubo cambio significativo en
  la generación de propulsión ni en el costo energético de caminar solo por llevar el dispositivo
  puesto sin asistencia. [Awad et al., 2017, Sci Transl Med](https://doi.org/10.1126/scitranslmed.aai9084)
  — población: ictus crónico; n = 5; tipo: experimento con humanos; tarea: banda, exo puesto
  apagado vs no puesto.
- En una extensión overground con exotraje no atado (untethered) de primera generación, la
  asistencia potenciada aumentó el ángulo de dorsiflexión pico en fase de balanceo (+4.9°,
  P = 0.002) y redujo la asimetría de propulsión interextremidades en 16.3 ± 6.8 % (P = 0.045),
  pero **no se reportó medición de costo metabólico en esta condición overground** (solo
  cinemática/cinética). [Awad et al., 2017, Sci Transl Med](https://doi.org/10.1126/scitranslmed.aai9084)
  — población: ictus crónico; n no especificado por separado para esta sub-prueba (subconjunto de
  los 9); tipo: experimento con humanos; tarea: caminata overground.
- Estrategia de control (Awad 2017): controlador iterativo de posición basado en fuerza; usa
  giroscopios montados en el zapato para detección de eventos de marcha y celdas de carga
  integradas en el textil para medir fuerza de interacción; la posición comandada del cable Bowden
  se ajusta paso a paso para alcanzar la fuerza de plantarflexión (apoyo) y dorsiflexión
  (balanceo) prescritas; el momento (tiempo) de inicio de la asistencia se ajustó
  individualmente para cada participante (ajuste manual del equipo investigador, no adaptación
  automática en tiempo real). [Awad et al., 2017, Sci Transl Med](https://doi.org/10.1126/scitranslmed.aai9084)
- En parálisis cerebral, un exoesqueleto de tobillo no atado (untethered) mejoró el costo
  metabólico de transporte (CMT) en 19 ± 5 % (p = 0.011) con asistencia potenciada vs la condición
  de "Zero-Torque-Ctrl" (dispositivo puesto, sin asistencia); la mejora individual varió entre 4 %
  y 29 % según el participante. [Lerner et al., 2018, IEEE TNSRE](https://doi.org/10.1109/TNSRE.2018.2870756)
  — población: parálisis cerebral, GMFCS I–III, edades 5–30 años; n = 5; tipo: experimento con
  humanos, piloto, tras ~130 min de práctica con el dispositivo; tarea: banda a velocidad
  preferida (0.55–1.10 m/s), ensayos de 5 min.
- Estrategia de control (Lerner 2018): máquina de estados finitos activada por resistencias
  sensibles a fuerza (FSR) en la plantilla del zapato; durante el estado "Plantar-Flexor
  Assist-On" (apoyo medio-tardío) se entrega un perfil de torque suavizado con función sigmoide a
  partir de una onda cuadrada. [Lerner et al., 2018, IEEE TNSRE](https://doi.org/10.1109/TNSRE.2018.2870756)
- **Resultado nulo en ictus (exoesqueleto rígido, control mioeléctrico adaptativo a velocidad):**
  no se observó beneficio metabólico promedio del grupo con asistencia vs sin asistencia; costo de
  transporte (CoT) 3.4 J/(m·kg) sin asistencia vs 3.6 J/(m·kg) con asistencia (ligero aumento,
  no reducción), p > 0.05, pese a que la potencia articular del tobillo parético y de la
  extremidad total aumentaron significativamente con la asistencia a las seis velocidades
  probadas. [McCain et al., 2019, J NeuroEngineering Rehabil](https://doi.org/10.1186/s12984-019-0523-y)
  — población: ictus crónico (edad media 49.7 años, 74.5 meses post-ictus); n = 6; tipo:
  experimento con humanos, control = exoesqueleto sin asistencia (mismo dispositivo apagado);
  tarea: protocolo de rampa de velocidad en banda, iniciando al 60 % de la velocidad overground
  cómoda y aumentando 0.1 m/s cada minuto. Estrategia de control: mioeléctrica proporcional
  adaptativa a la velocidad, basada en EMG de sóleo modulado en tiempo real por la velocidad de
  marcha, entregando ~25 % del momento biológico normal de plantarflexión. Los autores sugieren
  que la asistencia redirigió energía mecánica hacia el plano vertical en lugar de hacia la
  propulsión horizontal (menor ángulo de la extremidad en el despegue y menor GRF anterior
  integrada), lo que podría explicar la ausencia de beneficio metabólico pese a las ganancias
  articulares.
- **Resultado nulo/no significativo adicional en ictus (exoesqueleto rígido, control mioeléctrico
  proporcional por fase de propulsión):** la potencia metabólica neta no cambió
  significativamente con la asistencia potenciada (p = 0.21); valores: 2.52 ± 0.46 W/kg en
  condición basal (sin exo/sin potencia) vs 2.97 ± 0.60, 2.80 ± 0.51 y 2.67 ± 0.47 W/kg en la
  primera, segunda y tercera sesión potenciada respectivamente (tendencia a la baja entre
  sesiones repetidas, pero nunca por debajo de la línea base). El momento de plantarflexión
  parético aumentó 16 % con la asistencia (p < 0.05), pero no hubo cambio significativo en el
  trabajo positivo del tobillo parético ni en otras variables mecánicas.
  [Takahashi et al., 2015, J NeuroEngineering Rehabil](https://doi.org/10.1186/s12984-015-0015-7)
  — población: ictus crónico (edad media 61.2 ± 14.3 años); n = 5; tipo: experimento con humanos,
  condiciones control = sin exoesqueleto (NoEXO) y exoesqueleto sin potencia (UnPOW); tarea:
  banda al ~75 % de la velocidad preferida (rango 0.40–0.80 m/s), tres sesiones potenciadas de 5
  min con descansos de 5 min. Control: "propulsión mioeléctrica proporcional" (PMP) — EMG de
  sóleo combinada con datos de fuerza de reacción del suelo de la banda instrumentada; la
  asistencia solo se activa durante la fase de propulsión (GRF dirigida anteriormente).
- No pude abrir el reporte de caso de Lerner 2020 en enfermedad de Parkinson (Topics in Geriatric
  Rehabilitation, DOI 10.1097/TGR.0000000000000273; PMC4367918 según el convertidor de ID de
  NCBI corresponde en realidad al artículo de Takahashi 2015, no al de Lerner 2020 — es decir,
  este case report de Parkinson **no tiene versión PMC**). ResearchGate devolvió error 403 y la
  página del editor (journals.lww.com) devolvió error 402 "Payment Required". Según fragmentos de
  resultados de búsqueda (no verificados por lectura directa de la fuente, por lo que **no se
  citan como hallazgo**), el estudio sería n = 1 (mujer de 85 años, Hoehn y Yahr 2.5, 4 visitas en
  4 semanas con 3 sesiones de entrenamiento de 30 min) y reportaría ~26 % de reducción en el costo
  metabólico de caminar. Esta cifra **no está verificada** y debe tratarse con cautela si se
  incluye en el reporte final.

## Tabla de fuentes

| # | Fuente | Año | Tipo | Población | n | Abierta |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Awad et al., "A soft robotic exosuit improves walking in patients after stroke", Sci Transl Med | 2017 | Experimento con humanos (cruzado) | Ictus crónico | 9 (7 con datos de energética/propulsión válidos) | Sí (PDF de texto completo vía sites.bu.edu/nrl, mirror abierto del artículo de Science Transl Med) |
| 2 | Lerner et al., "An untethered ankle exoskeleton improves walking economy in a pilot study of individuals with cerebral palsy", IEEE TNSRE | 2018 | Experimento con humanos (piloto) | Parálisis cerebral (GMFCS I–III) | 5 | Sí (PMC6217810) |
| 3 | McCain et al., "Mechanics and energetics of post-stroke walking aided by a powered ankle exoskeleton with speed-adaptive myoelectric control", J NeuroEngineering Rehabil | 2019 | Experimento con humanos | Ictus crónico | 6 | Sí (PMC6521500) |
| 4 | Takahashi et al., "A neuromechanics-based powered ankle exoskeleton to assist walking post-stroke: a feasibility study", J NeuroEngineering Rehabil | 2015 | Experimento con humanos (factibilidad) | Ictus crónico | 5 | Sí (PMC4367918) |
| 5 | Lerner, "Effects of Lightweight Wearable Ankle Exoskeleton in an Individual With Parkinson Disease: A Case Report", Topics in Geriatric Rehabilitation | 2020 | Reporte de caso | Enfermedad de Parkinson | 1 | No (ResearchGate 403; editor LWW 402 Payment Required; sin versión PMC) |

## Contradicciones

- Dentro de la **misma población (ictus crónico)**, los resultados metabólicos dependen
  marcadamente de la estrategia de control y del tipo de dispositivo: Awad 2017 (exotraje,
  control iterativo de posición/fuerza con tiempo de asistencia ajustado manualmente por
  participante) encontró una reducción significativa del 10 ± 3 % en el costo energético,
  mientras que McCain 2019 (exoesqueleto rígido, control mioeléctrico proporcional adaptativo a
  la velocidad) y Takahashi 2015 (exoesqueleto rígido, control mioeléctrico proporcional por fase
  de propulsión) no encontraron beneficio metabólico significativo —e incluso una tendencia no
  significativa al aumento del costo—, pese a lograr incrementos significativos en el momento o la
  potencia articular del tobillo. Una explicación plausible que ofrecen los propios autores
  (McCain) es que la asistencia mioeléctrica, al depender de la activación residual (a menudo
  alterada) del sóleo parético, puede redirigir la energía mecánica generada hacia el plano
  vertical en lugar de aumentar la propulsión horizontal, sin traducirse en ahorro metabólico neto
  a nivel de cuerpo completo. En contraste, el control de Awad no depende de EMG residual sino de
  una trayectoria de posición/fuerza prescrita y ajustada externamente, lo que podría explicar la
  diferencia. Ningún estudio de este grupo tiene un n mayor a 9, por lo que estas diferencias
  deben interpretarse con cautela (estudios piloto, sin potencia estadística para comparaciones
  entre estrategias).
- El reporte de caso de Lerner 2020 en Parkinson (n = 1, no verificado por lectura directa)
  mencionaría una reducción de ~26 % en costo metabólico, en la misma dirección que los hallazgos
  positivos en ictus (Awad) y parálisis cerebral (Lerner 2018), pero al no haber podido abrir la
  fuente no se puede confirmar el diseño del control ni la robustez estadística de esa cifra.

## Lo que no encontré

- No pude abrir una versión PMC/manuscrito de autor de Awad et al. 2017: el convertidor de IDs de
  NCBI (idconv) devuelve explícitamente "Identifier not found in PMC" tanto para el PMID
  (28747517) como para el DOI del artículo, lo que indica que este artículo de *Science
  Translational Medicine* de 2017 no tiene una versión depositada en PMC. Sí logré abrir el texto
  completo mediante un PDF alojado públicamente por el Neuromotor Recovery Laboratory de Boston
  University (sites.bu.edu/nrl), que reproduce el artículo publicado.
- No pude abrir el reporte de caso de Lerner 2020 en Parkinson (ver arriba); por tanto no reporto
  sus cifras como hallazgo verificado.
- No encontré estudios adicionales con exoesqueletos de tobillo **rígidos** en ictus con medición
  metabólica más allá de McCain 2019 y Takahashi 2015 dentro del límite de búsquedas asignado;
  es posible que existan otros (p. ej. estudios de Sawicki/Lewek posteriores, o de otros grupos)
  que no se exploraron por el límite de 8 búsquedas.
- No encontré estudios en humanos con exoesqueletos de tobillo rígidos motorizados en otras
  poblaciones clínicas (p. ej. esclerosis múltiple, lesión medular incompleta) con medición de
  costo metabólico dentro del alcance de esta subpregunta.
