#!/usr/bin/env python3
"""Saca una figura de un PDF: renderiza la página y lista los pies de figura que hay en ella.

Uso:
    python3 extraer_figura.py paper.pdf --pagina 5 [--dpi 200] [--recorte x0,y0,x1,y1] [--salida carpeta]
    python3 extraer_figura.py paper.pdf --buscar "Fig. 3"     # encuentra en qué página está

--recorte usa fracciones de la página (0 a 1), desde la esquina superior izquierda.
Por ejemplo --recorte 0,0.1,1,0.55 conserva la franja entre el 10% y el 55% de la altura.

Usa pdftoppm y pdftotext (poppler). Si no están: macOS `brew install poppler`,
Ubuntu `sudo apt install poppler-utils`, Windows `conda install -c conda-forge poppler`.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


def requiere(prog):
    if shutil.which(prog) is None:
        sys.exit(f"No encuentro {prog}. Instala poppler (ver la ayuda de este script).")


def texto_paginas(pdf):
    requiere("pdftotext")
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    return out.split("\f")


PIE = re.compile(r"^\s*((?:Fig(?:ure|ura)?\.?|FIG\.?)\s*\d+[a-z]?[.:|]?.*)$", re.IGNORECASE)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf")
    ap.add_argument("--pagina", type=int, help="página a renderizar (empieza en 1)")
    ap.add_argument("--buscar", help="texto a buscar, p. ej. 'Fig. 3', para saber en qué página está")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--recorte", help="x0,y0,x1,y1 en fracciones de la página")
    ap.add_argument("--salida", default="revisiones/figuras")
    a = ap.parse_args()
    pdf = Path(a.pdf)
    paginas = texto_paginas(pdf)

    if a.buscar:
        aguja = a.buscar.lower().replace(" ", "")
        hits = [i + 1 for i, t in enumerate(paginas) if aguja in t.lower().replace(" ", "")]
        print(f"«{a.buscar}» aparece en las páginas: {hits or 'ninguna'}")
        if not a.pagina:
            return

    if not a.pagina:
        sys.exit("Indica --pagina N (o usa --buscar para encontrarla).")

    requiere("pdftoppm")
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)
    base = salida / f"{pdf.stem}_p{a.pagina}"
    subprocess.run(["pdftoppm", "-png", "-r", str(a.dpi), "-f", str(a.pagina), "-l", str(a.pagina),
                    "-singlefile", str(pdf), str(base)], check=True)
    png = base.with_suffix(".png")

    if a.recorte:
        x0, y0, x1, y1 = (float(v) for v in a.recorte.split(","))
        im = Image.open(png)
        w, h = im.size
        rec = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
        png = base.with_name(base.name + "_recorte.png")
        rec.save(png)

    print(f"Imagen: {png}")
    texto = paginas[a.pagina - 1] if a.pagina - 1 < len(paginas) else ""
    pies = [m.group(1).strip() for linea in texto.splitlines() if (m := PIE.match(linea))]
    print("Pies de figura en esta página:" if pies else "No encontré pies de figura en el texto de esta página.")
    for p in pies:
        print(f"  - {p[:200]}")
    print("(El pie suele seguir en las líneas siguientes; léelo completo con pdftotext -f N -l N.)")


if __name__ == "__main__":
    main()
