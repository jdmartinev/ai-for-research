"""qa.py video.mp4 nombre [n]  → qa/nombre_grid.png con n cuadros repartidos en la duración."""
import subprocess
import sys
from pathlib import Path

from PIL import Image

video, name = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
out = Path(__file__).with_name("qa")
out.mkdir(exist_ok=True)
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", video]).decode())
times = [dur * (k + 1) / (n + 1) for k in range(n - 1)] + [max(dur - 0.3, 0)]
ims = []
for k, t in enumerate(times):
    f = out / f"{name}_{k}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", str(f)], check=True)
    ims.append(Image.open(f))
w, h = ims[0].size
cols = 2
rows = (len(ims) + 1) // 2
g = Image.new("RGB", (w * cols + 6, h * rows + 6 * (rows - 1)), "white")
for k, im in enumerate(ims):
    g.paste(im, ((k % cols) * (w + 6), (k // cols) * (h + 6)))
g.save(out / f"{name}_grid.png")
print(f"{dur:.1f}s", out / f"{name}_grid.png", [round(t, 1) for t in times])
