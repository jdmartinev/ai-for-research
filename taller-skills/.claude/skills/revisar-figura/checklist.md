# Checklist de figura científica

Marca solo lo que falla. Cada punto tiene entre paréntesis la gravedad habitual.

## Mensaje
- [ ] Se entiende la conclusión en 5 segundos sin leer el texto (🟠)
- [ ] La comparación principal está en el mismo panel o en paneles con el mismo eje (🟠)
- [ ] No hay paneles o series que no aporten al mensaje (🟡)

## Ejes y unidades
- [ ] Cada eje tiene nombre **y** unidades: «Ángulo de rodilla (°)», «Tiempo (% del ciclo)» (🔴 si faltan unidades)
- [ ] Las marcas son legibles y no hay más de 5–7 por eje (🟡)
- [ ] La escala es la adecuada (lineal o log) y está indicada si es log (🟠)
- [ ] Paneles que se comparan comparten límites de eje, o se dice explícitamente que no (🔴 si inducen a error)
- [ ] Barras con el eje empezando en cero; si no empieza en cero, está justificado y marcado (🔴)
- [ ] Sin doble eje Y salvo que sea imprescindible; si existe, cada serie dice a qué eje pertenece (🟠)

## Datos e incertidumbre
- [ ] Las barras de error dicen qué son (DE, EE, IC 95%) en el pie o la leyenda (🔴)
- [ ] Se indica n (sujetos, ensayos, ciclos) y si los puntos son individuos o promedios (🔴)
- [ ] Con n pequeño se muestran los datos individuales, no solo barras (🟠)
- [ ] Las marcas de significancia (*, **) dicen qué prueba y qué umbral (🟠)
- [ ] Las curvas promedio con banda dicen qué es la banda (🔴)

## Color
- [ ] Las series se distinguen en escala de grises o por otra vía además del color (estilo de línea, marcador, etiqueta directa) (🟠)
- [ ] No hay pares rojo–verde como única diferencia (🟠; corre `scripts/contraste.py`)
- [ ] Mapas de calor con colormap perceptualmente uniforme (viridis, cividis, magma); nada de jet/rainbow (🟠)
- [ ] Datos divergentes (con un cero con significado) usan colormap divergente centrado en cero (🔴 si el centro está corrido)
- [ ] El mismo color significa lo mismo en todos los paneles y figuras del paper (🟠)
- [ ] Texto y líneas finas con contraste ≥ 3:1 contra el fondo (🟡)

## Texto, leyenda y anotaciones
- [ ] El texto más pequeño se lee al tamaño final de impresión (≈ 6–8 pt en una columna) (🟠)
- [ ] La leyenda no tapa datos; si hay pocas series, mejor etiquetas directas (🟡)
- [ ] Las abreviaturas están definidas en el pie (🟠)
- [ ] Los paneles tienen letras (a, b, c) y el pie las usa (🟡)

## Pie de figura
- [ ] El pie se entiende sin leer el texto: qué se muestra, en quién, con qué n, qué es la incertidumbre (🟠)
- [ ] El pie no afirma algo que la figura no muestra (🔴)

## Formato
- [ ] Resolución suficiente (≥ 300 ppp en raster) o vectorial para líneas y texto (🟡)
- [ ] Sin efectos 3D, sombras o perspectivas que distorsionen valores (🔴 si distorsionan)
- [ ] Relación de aspecto que no exagere ni aplane la tendencia (🟠)
