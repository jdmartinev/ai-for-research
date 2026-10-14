# Verificación de citas — sensado-fase-y-campo.md

| # | Afirmación (resumida) | Fuente | Veredicto | Pasaje o motivo (máx. 25 palabras) |
| --- | --- | --- | --- | --- |
| 1 | Reducción de costo energético 17±5% outdoor (n=10), +9±4% velocidad, 23±8% banda 1.5 m/s, 18% rampa 10°, sensores encoder+presión plantar | Slade et al. 2022, Nature 610:277–282 (PMC9556303) | ✔ respaldada | Texto confirma literalmente "17 ± 5%", "9 ± 4%", "23 ± 8%" a 1.5 m/s, y 18% en rampa; n=10/9 correctos. |
| 2 | TCN con IMU/encoder de exo de cadera, RMSE 0.142±0.021 N·m/kg, R²=0.840±0.045, 35 condiciones; reducción metabólica 5.4±5.6% (nivel vs No Exo) hasta 17.8±5.1% (rampa vs cero torque); trabajo positivo −17.5% (nivel) y −11.7% (rampa); n=10 eval., 34 entrenamiento; solo laboratorio | Molinaro et al. 2024, Science Robotics 9:eadi8852 (PDF leído directamente) | ✔ respaldada | PDF confirma cada cifra textualmente (RMSE, R², % metabólico, % trabajo, n=10 y n=34, todo en laboratorio). |
| 3 | Estimador cinemático de fase: RMSE 4.8±2.4% en banda (n=10) y 4.8±2.7% en terreno irregular (n=1); sin medición de costo metabólico | Medrano et al. 2023, IEEE T-RO 39(3) (arXiv:2205.00155) | ✔ respaldada | Abstract confirma "phase RMSE: 4.8 ± 2.4%" (N=10) y "4.8 ± 2.7%" (N=1); no menciona costo metabólico. |
| 4 | Control mioeléctrico proporcional (EMG sóleo, 7.6 A ref.) en Exoboot bilateral; variabilidad espaciotemporal mucho mayor outdoor que en banda (119–162% en longitud de zancada); exo no aumentó variabilidad outdoor vs sin exo; n=12; artículo no reporta costo metabólico | Hybart et al. 2023, PLOS ONE 18(11):e0294241 (PMC10642814) | ✔ respaldada | Confirma filtros EMG, 7.6 A, n=12, diferencias banda-outdoor ~119–162%, sin diferencias exo vs no-exo outdoor, remite a estudio PeerJ aparte para costo metabólico. |

## Conteo
✔ 4 · ⚠ 0 · ✘ 0 · no se pudo abrir 0

Nota: las fuentes 5, 6 y 7 de la "Tabla de fuentes" (PeerJ Hybart, Kim et al. 2019 Science, Molinaro et al. Nature 2024 cadera/rodilla) no tienen enlace URL en el documento y el propio autor de las notas ya las marca como "no abierta"; no aparecen asociadas a afirmaciones numéricas específicas fuera de la sección "Hallazgos", por lo que no se evaluaron aquí como filas adicionales.
