"""Calcula las probabilidades reales del siguiente token para F03 y escribe siguiente_token.json.

pip install torch transformers
python datos_siguiente_token.py
python datos_siguiente_token.py --prompt "La marcha humana tiene dos fases:" --model Qwen/Qwen2.5-0.5B
Luego: manim -s -r 1920,720 f03_siguiente_token.py SiguienteToken
"""
import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
ap.add_argument("--prompt", default="Durante la fase de apoyo de la marcha, la rodilla")
ap.add_argument("--k", type=int, default=8)
a = ap.parse_args()

tok = AutoTokenizer.from_pretrained(a.model)
model = AutoModelForCausalLM.from_pretrained(a.model).eval()
ids = tok(a.prompt, return_tensors="pt").input_ids
with torch.no_grad():
    p = model(ids).logits[0, -1].float().softmax(-1)
top = torch.topk(p, a.k)
rows = []
for pr, i in zip(top.values.tolist(), top.indices.tolist()):
    s = tok.decode([i]).replace(" ", "␣").replace("\n", "↵")
    rows.append([s, round(pr, 4)])
out = {"prompt": a.prompt, "model": a.model.split("/")[-1], "top": rows}
Path(__file__).with_name("siguiente_token.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
for s, pr in rows:
    print(f"{s:>14s} {100 * pr:5.1f}% " + "█" * int(80 * pr))
