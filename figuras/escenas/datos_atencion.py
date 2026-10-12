"""Calcula los pesos de atención reales para S04 y escribe atencion.json.

pip install torch transformers
python datos_atencion.py                      # BETO, capa 8, promedio de cabezas
python datos_atencion.py --layer 10 --model dccuchile/bert-base-spanish-wwm-cased

Los sub-tokens se agrupan por palabra: la fila de la consulta es el promedio de sus sub-tokens
y la columna de cada palabra es la suma de los suyos. [CLS] y [SEP] se excluyen y se renormaliza.
Pruebe varias capas: en BERT la resolución de correferencia suele aparecer en capas intermedias.
"""
import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModel, AutoTokenizer

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="dccuchile/bert-base-spanish-wwm-cased")
ap.add_argument("--sentence", default="El robot no levantó la caja porque estaba muy pesada")
ap.add_argument("--query", default="pesada")
ap.add_argument("--layer", type=int, default=8, help="1 = primera capa")
a = ap.parse_args()

words = a.sentence.split()
tok = AutoTokenizer.from_pretrained(a.model)
model = AutoModel.from_pretrained(a.model, output_attentions=True).eval()
enc = tok(words, is_split_into_words=True, return_tensors="pt")
with torch.no_grad():
    att = model(**enc).attentions[a.layer - 1][0].mean(0)   # (seq, seq), promedio de cabezas
wid = enc.word_ids()
qi = words.index(a.query)
q_rows = [i for i, w in enumerate(wid) if w == qi]
row = att[q_rows].mean(0)
weights = [float(sum(row[i] for i, w in enumerate(wid) if w == k)) for k in range(len(words))]
s = sum(weights)
weights = [w / s for w in weights]
out = {"tokens": words, "query": a.query, "weights": [round(w, 4) for w in weights],
       "model": a.model.split("/")[-1], "layer": a.layer}
Path(__file__).with_name("atencion.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
for w, x in zip(words, weights):
    print(f"{w:>10s} {x:.3f} " + "█" * int(60 * x))
