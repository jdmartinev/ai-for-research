# Plan: control de exoesqueletos de tobillo y costo metabólico

## Pregunta reformulada

¿Qué estrategias de control de exoesqueletos de tobillo reducen el costo metabólico de la marcha,
con qué evidencia (tipo de estudio, n, magnitud) y en qué poblaciones (sanos vs. clínicas)?

Términos en inglés: *ankle exoskeleton*, *ankle exosuit*, *ankle-foot orthosis (powered)*,
*metabolic cost / metabolic rate / net metabolic power*, *walking*, *control strategy*,
*human-in-the-loop optimization*, *proportional myoelectric control*, *time-based / phase-based
torque profile*, *biological torque*, *stroke*, *cerebral palsy*, *older adults*, *incomplete SCI*.

## Tipo de pregunta y esfuerzo

**Revisión amplia** → 4 investigadores, hasta 15 búsquedas cada uno. Máximo dos rondas.

## Subpreguntas (una por investigador)

1. **estrategias-control** — Qué familias de estrategias de control de alto nivel se han probado
   en exoesqueletos de tobillo para reducir el costo metabólico (perfiles por tiempo/fase fijos,
   imitación de torque biológico, control mioeléctrico proporcional, optimización con humano en el
   lazo, control basado en modelos neuromusculares, exoesqueletos pasivos con resorte/embrague como
   contraste), y qué reducción logró cada una en **sujetos sanos** caminando.
2. **parametros-y-resultados** — Qué parámetros del perfil de asistencia (tiempo de pico, magnitud
   de torque/potencia, trabajo positivo neto, tiempo de inicio) explican la reducción metabólica, y
   qué pasa con resultados secundarios (cinemática, EMG del sóleo/gastrocnemio) y con la adaptación
   o el entrenamiento del usuario. Incluye condiciones de comparación (sin exo vs. exo sin
   asistencia) y efecto de la masa añadida.
3. **sensado-fase-y-fuera-del-laboratorio** — Cómo se sensa y estima la fase de la marcha o el
   estado del usuario para estas estrategias (IMU, sensores de presión, EMG, estimadores
   basados en datos/ML) y qué evidencia hay de reducción metabólica fuera del laboratorio o en
   condiciones variables (velocidad, pendiente, terreno, exoesqueletos portátiles autónomos).
4. **poblaciones-clinicas** — Qué evidencia hay de reducción del costo metabólico (o costo de
   transporte) con exoesqueletos de tobillo en poblaciones clínicas o especiales: ictus/hemiparesia,
   parálisis cerebral, adultos mayores, lesión medular incompleta, Parkinson, amputados u otras.

Separación: 1 = qué controlador y cuánto reduce en sanos; 2 = por qué funciona (parámetros,
mecanismo, adaptación); 3 = sensado/estimación y validez fuera del laboratorio; 4 = clínicos.

## Criterio «¿basta?»

1. Cada subpregunta tiene ≥3 fuentes primarias abiertas (no solo revisiones).
2. Hay ≥1 estudio con humanos por cada estrategia o resultado que se afirme en el reporte.
3. Las contradicciones (p. ej., efectos que no se replican, magnitudes distintas entre grupos)
   están explicadas o reportadas.

Específico de esta pregunta: para clínicos se acepta declarar el hueco si hay <3 estudios por
condición, siempre que haya al menos uno con medición metabólica real.

## Decisión tras la ronda 1 (2026-10-14)

Criterio 1 cumplido por poco (≈3 primarias abiertas por subpregunta). Criterio 2 incompleto:
cifras clave sin fuente abierta (Zhang 2017, Collins 2015, Poggensee & Collins 2021) y ictus con un
solo estudio (exotraje). Criterio 3 incompleto: contradicción Slade 2022 vs. Hybart PeerJ 2023 sin
abrir la segunda fuente. → **Ronda 2 (última)**, 2 investigadores, hasta 8 búsquedas cada uno:

- **ronda2-sanos**: abrir Zhang 2017, Collins 2015, Poggensee & Collins 2021, Hybart et al. 2023
  PeerJ (costo metabólico con control mioeléctrico, banda y exterior).
- **ronda2-clinicos**: abrir Awad 2017 (Sci Transl Med) y Lerner 2018 (TNSRE, PC); buscar
  exoesqueletos de tobillo rígidos en ictus con costo metabólico (p. ej. McCain 2019), incluidos
  resultados nulos; reporte de caso en Parkinson.

Molinaro 2024 es de cadera: no se usa como evidencia de tobillo.
