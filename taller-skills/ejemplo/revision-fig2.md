# Revisión de Fig. 2 (papers/paper.pdf, p. 2)

Imagen revisada: `revisiones/figuras/paper_p2.png`. Simulaciones de color: `revisiones/fig2_color/`.

## 1. Mensaje
«No se entiende del todo.» Panel izquierdo: curvas de ángulo de rodilla de «sano» y «exo» a lo largo de la marcha, con exo de menor amplitud (≈17° frente a ≈20°, valores estimados a ojo, p. 2 Fig. 2 izq.) y desfasada. Panel derecho: un mapa de calor 10×10 sin título, sin ejes con nombre, sin barra de color y sin mención en el pie. No se puede decir qué muestra.

## 2. Problemas (del más grave al menos grave)

### 🔴 1. Panel derecho sin ninguna explicación
- **Qué y dónde:** Fig. 2, panel derecho. Mapa de calor sin nombre de ejes, sin unidades, sin barra de color y sin que el pie lo mencione («Fig. 2. Knee angle during gait.»).
- **Por qué importa:** no se sabe qué variable es, ni su escala, ni qué relación tiene con el ángulo de rodilla. El lector no puede interpretarlo; el pie tampoco lo aclara.
- **Cómo corregir:** añadir `fig.colorbar(im, label="…(unidades)")`, nombrar ejes `xlabel`/`ylabel` y describirlo en el pie. Si no aporta al mensaje, quitarlo.

### 🔴 2. Colormap tipo jet/rainbow
- **Qué y dónde:** panel derecho; la paleta va de azul oscuro a rojo oscuro pasando por cian, verde y amarillo.
- **Por qué importa:** no es perceptualmente uniforme. En escala de grises (`paper_p2_gris.png`) el orden de valores no es monótono (el amarillo y el cian salen casi tan claros como el blanco, el rojo y el azul oscuro salen ambos oscuros), así que valores muy distintos se ven iguales. En deuteranopia (`paper_p2_deuteranopia.png`) se pierden los verdes. Además aparecen en la imagen tonos de bajo contraste con el fondo (p. ej. #77FF80, 1.3:1; #F8EC83, 1.2:1, medidos con `contraste.py`).
- **Cómo corregir:** `cmap="jet"` → `cmap="viridis"` (o `cividis`). Si los datos son divergentes con un cero con significado, usar un divergente centrado en cero (`coolwarm` con `vmin=-vmax`). No pude ver el script, así que el nombre exacto del colormap original es una suposición por su apariencia.

### 🔴 3. Pie de figura insuficiente y superpuesto a los datos
- **Qué y dónde:** el pie dice solo «Knee angle during gait.» y está dibujado encima de las marcas del eje x del panel izquierdo (se pisa con «20» y «40»; visible en la imagen y en el texto extraído de p. 2).
- **Por qué importa:** no dice n (sujetos o ciclos), si las curvas son promedios o un individuo, ni qué es «sano» y «exo»; los datos parecen una sinusoide perfecta, sin incertidumbre, y el pie no aclara si es un modelo o datos reales. Además, el texto tapa las marcas de los ejes.
- **Cómo corregir:** mover el pie fuera del área de la figura (en LaTeX `\caption`, no `fig.text`) y ampliarlo: población, n, promedio ± qué, qué es el panel derecho, definición de «exo».

### 🟠 4. Ejes sin nombre ni unidades en el panel izquierdo
- **Qué y dónde:** eje x (0–100) y eje y (−20 a 20) sin etiqueta.
- **Por qué importa:** probablemente % del ciclo de marcha y grados, pero eso es una suposición mía; el pie no lo dice. Falta «Ángulo de rodilla (°)» y «Ciclo de marcha (%)».
- **Cómo corregir:** `ax.set_xlabel("Ciclo de marcha (%)")`, `ax.set_ylabel("Ángulo de rodilla (°)")`.

### 🟠 5. Rojo–verde como única diferencia entre series
- **Qué y dónde:** curvas «sano» (#d62728) y «exo» (#2ca02c).
- **Por qué importa:** `contraste.py` da ΔE 7 en deuteranopia (< 10) y ΔE 11 en grises; en las simulaciones las dos líneas son casi idénticas y solo se distinguen por la posición. Ambas tienen el mismo grosor y estilo.
- **Cómo corregir:** cambiar a azul/naranja (p. ej. `#0072B2`, `#E69F00`) y/o dar a exo `linestyle="--"`; o etiquetar directamente las curvas.

### 🟠 6. Sin incertidumbre ni datos individuales
- **Qué y dónde:** panel izquierdo; dos curvas lisas, sin banda ni curvas individuales.
- **Por qué importa:** no se puede juzgar si la diferencia (~3° de amplitud, estimada a ojo) es mayor que la variabilidad. El pie no dice si hay una banda ni qué sería.
- **Cómo corregir:** `fill_between` con ±DE y decirlo en el pie, o mostrar los ciclos individuales en gris claro.

### 🟡 7. Idioma mixto
- Leyenda en español («sano», «exo»), pie en inglés, ejes sin texto. Elegir un idioma según la revista; «exo» debe definirse.

## 3. Lo que está bien
- El panel izquierdo permite comparar ambas series en el mismo eje, con límites compartidos (Fig. 2 izq.).
- Leyenda sin tapar datos (esquina superior derecha, donde no hay curva).
- Tamaño de texto de los ticks legible; figura en buena resolución.

## 4. Lo que no pude verificar
- **Todo lo que dice el texto del paper:** la p. 1 solo contiene «Introduction text page» y la p. 2 únicamente la figura; no hay párrafo que cite la Fig. 2, ni datos ni método.
- No hay script generador en la carpeta; no pude confirmar `cmap`, colores ni tamaños de fuente (los hex de las curvas los asumí de la paleta por defecto de matplotlib y el script los confirmó como colores dominantes de la imagen solo por la paleta que le pasé).
- Los valores de las curvas (≈17° y ≈20°) son lecturas visuales, no datos.
- Qué representa el mapa de calor, el n y si los datos son reales o sintéticos.
- No miré las simulaciones de protanopia y tritanopia; solo gris y deuteranopia.
