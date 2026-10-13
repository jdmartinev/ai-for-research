"""Tokeniza las frases de la escena de tokens con un tokenizador real y escribe tokens.json.

pip install mistral-common       (trae el tokenizador Tekken dentro del paquete; no descarga nada)
python datos_tokens.py
"""
import json
from pathlib import Path

import mistral_common
from mistral_common.tokens.tokenizers.tekken import Tekkenizer

DATA = Path(mistral_common.__file__).parent / "data" / "tekken_240911.json"
FRASES = ["Durante la fase de apoyo de la marcha, la rodilla se flexiona",
          "tibiofemoral", "electromiografía", "exoesqueleto"]

tok = Tekkenizer.from_file(str(DATA))
out = {"tokenizer": "Tekken (Mistral, 2024)", "vocab": tok.n_words, "frases": []}
for f in FRASES:
    ids = tok.encode(f, bos=False, eos=False)
    out["frases"].append({"texto": f, "tokens": [[tok.id_to_piece(i), i] for i in ids]})
    print(len(ids), [tok.id_to_piece(i) for i in ids])
Path(__file__).with_name("tokens.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
