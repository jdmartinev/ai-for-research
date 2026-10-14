#!/usr/bin/env python3
"""Revisa el color de una figura: contraste, legibilidad en gris y daltonismo.

Uso:
    python3 contraste.py figura.png [--salida carpeta] [--colores 8]
    python3 contraste.py figura.png --paleta "#d62728,#2ca02c"   # compara los colores exactos del script

Qué hace:
1. Reduce la figura a sus N colores dominantes y toma el más frecuente como fondo.
2. Para cada color reporta su proporción, su luminancia y su contraste contra el fondo (WCAG).
3. Para cada par de colores de datos calcula la diferencia perceptual (ΔE en CIELAB):
   en color normal, en escala de grises y con daltonismo simulado (protan, deutan, tritan;
   matrices de Machado et al., 2009, severidad 1.0).
4. Guarda la figura en gris y con cada simulación, para que alguien (o un agente) la mire.

Umbrales usados: ΔE < 10 se marca «difícil de distinguir»; contraste < 3:1 contra el fondo se
marca «bajo». Son reglas prácticas, no normas: el criterio final es mirar las imágenes.

Solo depende de numpy y Pillow.
"""
import argparse
import itertools
from pathlib import Path

import numpy as np
from PIL import Image

MACHADO = {
    "protanopia": np.array([[0.152286, 1.052583, -0.204868],
                            [0.114503, 0.786281, 0.099216],
                            [-0.003882, -0.048116, 1.051998]]),
    "deuteranopia": np.array([[0.367322, 0.860646, -0.227968],
                              [0.280085, 0.672501, 0.047413],
                              [-0.011820, 0.042940, 0.968881]]),
    "tritanopia": np.array([[1.255528, -0.076749, -0.178779],
                            [-0.078411, 0.930809, 0.147602],
                            [0.004733, 0.691367, 0.303900]]),
}
UMBRAL_DE = 10.0
UMBRAL_CONTRASTE = 3.0


def a_lineal(rgb):
    rgb = np.asarray(rgb, dtype=float) / 255.0
    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


def a_srgb(lin):
    lin = np.clip(lin, 0, 1)
    s = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
    return np.round(s * 255).astype(np.uint8)


def luminancia(rgb):
    return a_lineal(rgb) @ np.array([0.2126, 0.7152, 0.0722])


def contraste(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def a_lab(rgb):
    lin = a_lineal(rgb)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = lin @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def simular(rgb, tipo):
    lin = a_lineal(rgb)
    if tipo == "gris":
        y = lin @ np.array([0.2126, 0.7152, 0.0722])
        return a_srgb(np.repeat(y[..., None], 3, -1))
    return a_srgb(lin @ MACHADO[tipo].T)


def delta_e(c1, c2):
    return float(np.linalg.norm(a_lab(c1) - a_lab(c2)))


def colores_dominantes(img, n):
    pequeña = img.copy()
    pequeña.thumbnail((500, 500))
    q = pequeña.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    paleta = np.array(q.getpalette()[: 3 * n]).reshape(-1, 3)
    cuentas = np.bincount(np.asarray(q).ravel(), minlength=n)
    orden = np.argsort(cuentas)[::-1]
    total = cuentas.sum()
    return [(paleta[i], cuentas[i] / total) for i in orden if cuentas[i] > 0]


def hexa(c):
    return "#{:02X}{:02X}{:02X}".format(*map(int, c))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("imagen")
    ap.add_argument("--salida", default=None, help="carpeta para las simulaciones (por defecto, junto a la imagen)")
    ap.add_argument("--colores", type=int, default=8)
    ap.add_argument("--min-proporcion", type=float, default=0.004,
                    help="ignora colores que ocupan menos que esta fracción (antialiasing)")
    ap.add_argument("--paleta", help="colores de las series separados por coma (p. ej. los del script de "
                    "matplotlib); si se da, se comparan estos en vez de los detectados")
    a = ap.parse_args()

    ruta = Path(a.imagen)
    img = Image.open(ruta).convert("RGB")
    salida = Path(a.salida) if a.salida else ruta.parent / f"{ruta.stem}_color"
    salida.mkdir(parents=True, exist_ok=True)

    dom = [(c, p) for c, p in colores_dominantes(img, a.colores) if p >= a.min_proporcion]
    fondo, _ = dom[0]
    l_fondo = luminancia(fondo)
    datos = dom[1:]

    print(f"# Color de {ruta.name}\n")
    print(f"Tamaño: {img.width}×{img.height} px. Fondo supuesto: {hexa(fondo)} (el color más frecuente).\n")
    print("## Colores dominantes\n")
    print("| color | proporción | contraste con el fondo | aviso |")
    print("|---|---|---|---|")
    for c, p in datos:
        cr = contraste(luminancia(c), l_fondo)
        aviso = "bajo" if cr < UMBRAL_CONTRASTE else ""
        print(f"| {hexa(c)} | {p:.1%} | {cr:.1f}:1 | {aviso} |")

    # descarta grises casi neutros (texto, ejes) de la comparación entre pares
    def croma(c):
        lab = a_lab(c)
        return float(np.hypot(lab[1], lab[2]))
    if a.paleta:
        series = [np.array([int(h.strip().lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]) for h in a.paleta.split(",")]
        print(f"\n## Pares de la paleta indicada ({len(series)} colores)\n")
    else:
        series = [c for c, _ in datos if croma(c) > 12]
        print(f"\n## Pares de colores de datos ({len(series)} colores con tono; se excluyen grises)\n")
        print("Nota: un mapa de calor aporta muchos colores; si la figura tiene líneas o barras, "
              "es más fiable pasar sus colores exactos con --paleta.\n")
    if len(series) < 2:
        print("Menos de dos colores con tono: la figura no depende del color para distinguir series.")
    else:
        vistas = ["normal", "gris", "protanopia", "deuteranopia", "tritanopia"]
        print("| par | " + " | ".join(f"ΔE {v}" for v in vistas) + " |")
        print("|---|" + "---|" * len(vistas))
        problemas = []
        for c1, c2 in itertools.combinations(series, 2):
            fila = []
            for v in vistas:
                s1 = c1 if v == "normal" else simular(c1, v)
                s2 = c2 if v == "normal" else simular(c2, v)
                d = delta_e(s1, s2)
                marca = " ⚠" if d < UMBRAL_DE else ""
                if d < UMBRAL_DE and v != "normal":
                    problemas.append((hexa(c1), hexa(c2), v, d))
                fila.append(f"{d:.0f}{marca}")
            print(f"| {hexa(c1)} – {hexa(c2)} | " + " | ".join(fila) + " |")
        print("\n## Resumen\n")
        if problemas:
            for h1, h2, v, d in problemas:
                print(f"- {h1} y {h2} se confunden en **{v}** (ΔE {d:.0f} < {UMBRAL_DE:.0f}).")
        else:
            print("- Ningún par de colores de datos se confunde en gris ni con daltonismo simulado.")

    arr = np.asarray(img)
    for v in ["gris", "deuteranopia", "protanopia", "tritanopia"]:
        Image.fromarray(simular(arr, v)).save(salida / f"{ruta.stem}_{v}.png")
    print(f"\nSimulaciones guardadas en {salida}/ (gris, deuteranopia, protanopia, tritanopia). Míralas.")


if __name__ == "__main__":
    main()
