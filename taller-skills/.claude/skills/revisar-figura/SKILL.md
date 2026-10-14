---
name: revisar-figura
description: Revisa una figura científica (mensaje, ejes, unidades, color, daltonismo, leyenda, pie de figura, integridad de los datos) y entrega los problemas del más grave al menos grave con cómo corregirlos. Úsalo cuando el usuario pida revisar, criticar o mejorar una figura o gráfica, propia o de un paper, en PNG, JPG, SVG o dentro de un PDF.
argument-hint: "[figura.png | paper.pdf página-o-'Fig. N'] [script.py opcional]"
allowed-tools: Read, Write, Glob, Bash(python3 *), Bash(pdftotext *), Bash(pdftoppm *), Bash(pdfinfo *)
---

# Revisar figura

Pedido del usuario: $ARGUMENTS

Eres un revisor exigente de figuras científicas. Tu trabajo es encontrar lo que un árbitro o un
lector notaría, no reescribir la figura a tu gusto.

## 1. Consigue la imagen

- **Imagen (PNG, JPG):** úsala tal cual.
- **SVG:** léelo como texto (colores, fuentes y tamaños están ahí) y, si puedes, conviértelo a PNG.
- **PDF:** si te dan «Fig. N» y no la página, encuéntrala primero:
  `python3 ${CLAUDE_SKILL_DIR}/scripts/extraer_figura.py <pdf> --buscar "Fig. N"`
  Luego renderiza la página:
  `python3 ${CLAUDE_SKILL_DIR}/scripts/extraer_figura.py <pdf> --pagina P`
  Mira la imagen; si la página tiene más cosas, vuelve a correr con `--recorte x0,y0,x1,y1`
  (fracciones de la página) hasta que quede solo la figura con su pie.
- Lee el **pie de figura completo** (`pdftotext -layout -f P -l P <pdf> -`) y, si es un paper,
  el párrafo que cita la figura. Sin eso no sabes qué afirma la figura.

Si no encuentras la figura o el pie, dilo y pide la página. No adivines.

## 2. Mírala

Abre la imagen con Read y descríbete en dos líneas: qué tipo de gráfica es, qué variables cruza y
cuál parece ser el mensaje. Si no puedes decir el mensaje, ese ya es el primer problema.

## 3. Recorre la lista

Recorre [checklist.md](checklist.md) sección por sección. Para cada punto que falle, anota
qué ves y dónde (panel, eje, serie).

## 4. Mide el color (no lo estimes)

`python3 ${CLAUDE_SKILL_DIR}/scripts/contraste.py <imagen> --salida revisiones/<nombre>_color`

Si tienes el script que generó la figura, pásale los colores exactos de las series con
`--paleta "#hex1,#hex2,..."`; es más fiable que la detección automática.
Después **abre con Read** al menos `_gris.png` y `_deuteranopia.png` y confirma con tus ojos lo
que dice el script: un ΔE bajo entre dos colores que nunca están juntos no es un problema.

## 5. Si hay script, conéctalo

Si el usuario dio (o hay en la carpeta) el script que generó la figura, para cada problema indica
la línea a cambiar y el cambio concreto (por ejemplo, `cmap="jet"` → `cmap="viridis"`). No edites
el script salvo que te lo pidan.

## 6. Entrega

Escribe `revisiones/<nombre-de-la-figura>.md` con:

1. **Mensaje** de la figura en una línea (o «no se entiende», si es el caso).
2. **Problemas**, del más grave al menos grave, cada uno con: gravedad (🔴 engaña o impide leer /
   🟠 dificulta / 🟡 estética), qué y dónde, por qué importa, y cómo corregirlo.
3. **Lo que está bien** (2–3 puntos), para que no se pierda al corregir.
4. **Lo que no pude verificar** (por ejemplo, si los datos coinciden con el texto).

Responde al usuario con los tres problemas más graves y la ruta del archivo.

## Errores típicos (no los cometas)

- Opinar sobre el color sin correr el script ni mirar las simulaciones.
- Pedir cambios de estilo (fuente, paleta «más bonita») como si fueran problemas graves.
- Revisar la figura sin leer su pie: muchos «problemas» los aclara el pie, y otros solo aparecen
  al compararlo con la figura.
- Inventar valores: si un número no se puede leer en la figura, dilo.
