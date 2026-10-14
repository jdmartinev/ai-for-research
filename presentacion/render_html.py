"""spec.py → project/deck.json + project/slides/<id>.html (formato del tipo Slides)."""
import html
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import spec  # noqa: E402

OUT = HERE / "web"
ASSETS = json.loads((HERE / "assets.json").read_text())   # clave → {"still": "/_blob/…", "video": "/_blob/…"}

BG, PANEL, CARD, BORDER = "#0F1626", "#141D2F", "#1E2A40", "#2A3550"
TEXT, MUTED, FOOT, AMBER, MODEL, GRAY, ERR = "#ECEEF0", "#B9C3CF", "#7A8699", "#F2A541", "#5FA8D3", "#5B6678", "#C97B63"
DISP = "'Space Grotesk', Arial, sans-serif"
BODY = "'IBM Plex Sans', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Courier New', monospace"
ROLE = {"a": AMBER, "m": MODEL, "g": FOOT, "t": TEXT}

ORDER = [d["id"] for d in spec.SLIDES]
NUM = {sid: i for i, sid in enumerate(ORDER)}   # cover = 0


def refs(s):
    return re.sub(r"\{n:([\w-]+)\}", lambda m: str(NUM[m.group(1)]), s)


def e(s):
    return html.escape(refs(s), quote=False)


def title_lines(t, size=60, width=1664):
    return max(1, math.ceil(len(t) * size * 0.52 / width))


def head(d, gap=40):
    bg = BG if d.get("dark") else PANEL
    out = [f'<section id="{d["id"]}" data-transition="fade" style="background:{bg};color:{TEXT};font-family:{BODY};'
           f'padding:128px 128px 160px;display:flex;flex-direction:column;gap:{gap}px">',
           f'<p style="font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:{AMBER}">{e(d["eyebrow"])}</p>',
           f'<h2 style="font-family:{DISP};font-size:60px;font-weight:600;line-height:1.1;color:{TEXT}">{e(d["title"])}</h2>']
    return out


def tail(d, color=FOOT):
    out = []
    if d.get("judge"):
        out.append(f'<p style="position:absolute;right:128px;top:128px;width:720px;font-size:24px;font-weight:600;letter-spacing:3px;'
                   f'text-transform:uppercase;text-align:right;color:{FOOT}">Juez · <span style="color:{AMBER}">{e(d["judge"])}</span></p>')
    n = NUM[d["id"]]
    src = d.get("src", "IA para la investigación")
    out.append(f'<p style="position:absolute;left:128px;bottom:64px;width:1664px;font-size:24px;color:{color}">{n} · {e(src)}</p>')
    if d.get("notes"):
        out.append(f"<aside>{e(d['notes'])}</aside>")
    out.append("</section>")
    return out


def body_height(d, extra=0):
    lines = title_lines(d["title"])
    return 792 - 30 - 40 - int(66 * lines) - 40 - extra


def media_tag(key, alt, w, h):
    a = ASSETS.get(key)
    if not a:
        return (f'<div style="width:{w}px;height:{h}px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:16px;'
                f'border:2px dashed #3A475C;border-radius:16px"><p style="font-size:24px;font-weight:600;letter-spacing:2px;color:{BG};'
                f'background:{AMBER};padding:8px 20px;border-radius:999px">EN CONSTRUCCIÓN · {key}</p>'
                f'<p style="font-size:28px;color:{MUTED};text-align:center;width:{w - 160}px">{e(alt)}</p></div>')
    vid = f' data-video="{a["video"]}"' if a.get("video") else ""
    return f'<img src="{a["still"]}"{vid} alt="{e(alt)}" style="width:{w}px;height:{h}px;object-fit:contain">'


def p(text, size=28, color=MUTED, extra=""):
    return f'<p style="font-size:{size}px;color:{color}{";" + extra if extra else ""}">{e(text)}</p>'


def note_block(d):
    out = []
    if d.get("note"):
        out.append(f'<p style="font-size:30px;color:{AMBER}">{e(d["note"])}</p>')
    if d.get("warn"):
        out.append(f'<p style="font-size:28px;color:{TEXT};border-left:4px solid {ERR};padding:8px 0 8px 24px">{e(d["warn"])}</p>')
    return out


# ---------------------------------------------------------------- kinds
def k_cover(d):
    return [f'<section id="cover" data-transition="fade" style="background:{BG};color:{TEXT};font-family:{BODY};padding:128px;display:flex;flex-direction:column;justify-content:center;gap:40px">',
            f'<p style="font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:{AMBER}">1er Simposio Somer Investiga · 15 de octubre de 2026</p>',
            f'<h1 style="font-family:{DISP};font-size:120px;font-weight:700;line-height:1.05;color:{TEXT}">¿Quién decide qué cuenta como <span style="color:{AMBER}">mejor</span>?</h1>',
            f'<p style="font-size:44px;color:{MUTED}">IA para la investigación: de la atención al descubrimiento autónomo</p>',
            f'<p style="font-size:32px;color:{FOOT}">Juan David Martínez Vargas, Ph.D. · Universidad EAFIT</p>',
            f"<aside>{e(d['notes'])}</aside>", "</section>"]


def k_media(d):
    h = min(624, body_height(d))
    w = min(1664, int(h * 1920 / 720))
    h = int(w * 720 / 1920)
    return head(d) + [media_tag(d["media"], d["alt"], w, h)] + tail(d)


def k_media_stats(d):
    out = head(d, gap=32)
    w = 1664
    h = int(w * 440 / 1920)
    out.append(media_tag(d["media"], d["alt"], w, h))
    out.append('<div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:24px">')
    for v, c, acc in d["stats"]:
        out.append(f'<div style="display:flex;flex-direction:column;gap:4px"><p style="font-family:{DISP};font-size:72px;font-weight:700;line-height:1.0;color:{AMBER if acc else TEXT}">{e(v)}</p>'
                   f'<p style="font-size:24px;color:{MUTED}">{e(c)}</p></div>')
    out.append("</div>")
    return out + tail(d)


def k_table(d):
    out = head(d)
    out.append(f'<table style="font-size:28px;color:{TEXT};font-family:{BODY}">')
    w = ["32%", "38%", "30%"]
    out.append("<tr>" + "".join(f'<th style="width:{w[i]};color:{MUTED}">{e(h)}</th>' for i, h in enumerate(d["head"])) + "</tr>")
    for r, row in enumerate(d["rows"]):
        last = r == len(d["rows"]) - 1
        cells = [f"<td>{e(row[0])}</td>", f"<td>{e(row[1])}</td>",
                 f'<td style="color:{AMBER}">{"<b>" if last else ""}{e(row[2])}{"</b>" if last else ""}</td>']
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</table>")
    out.append(p(d["note"]))
    return out + tail(d)


def card_html(c, pad=40, title_size=32):
    acc = c.get("accent")
    border = f"border:2px solid {AMBER};" if acc else ""
    parts = [f'<div style="background:{CARD};{border}border-radius:16px;padding:{pad}px;display:flex;flex-direction:column;gap:16px">',
             f'<h3 style="font-size:{title_size}px;font-weight:600;color:{AMBER if acc else TEXT}">{e(c["t"])}</h3>']
    if c.get("sub"):
        parts.append(f'<p style="font-size:28px;font-weight:600;color:{AMBER}">{e(c["sub"])}</p>')
    parts.append(p(c["body"]))
    parts.append("</div>")
    return "".join(parts)


def k_cards(d):
    out = head(d)
    n = len(d["cards"])
    cols = d.get("grid", n)
    pad = 32 if n > 3 else 40
    out.append(f'<div style="display:grid;grid-template-columns:repeat({cols}, 1fr);gap:24px">')
    out += [card_html(c, pad=pad, title_size=30 if n > 3 else 32) for c in d["cards"]]
    out.append("</div>")
    out.append('<div style="flex:1"></div>')
    out += note_block(d)
    return out + tail(d)


def k_bignums(d):
    out = head(d)
    if d.get("lead"):
        out.append(p(d["lead"]))
    n = len(d["items"])
    big = any(i.get("big") for i in d["items"])
    size = 200 if big else (120 if n == 3 and max(len(i["v"]) for i in d["items"]) <= 6 else 88)
    out.append(f'<div style="flex:1;display:grid;grid-template-columns:repeat({n}, 1fr);gap:48px;align-items:center">')
    for it in d["items"]:
        col = AMBER if it.get("accent") else (MUTED if it.get("muted") else TEXT)
        rule = AMBER if it.get("accent") else "#3A475C"
        s = [f'<div style="display:flex;flex-direction:column;gap:16px;border-top:4px solid {rule};padding:32px 0 0 0">',
             f'<p style="font-family:{DISP};font-size:{size}px;font-weight:700;line-height:1.0;color:{col}">{e(it["v"])}</p>',
             p(it["cap"], size=32 if big else 28)]
        if it.get("src"):
            s.append(f'<p style="font-size:24px;font-weight:600;color:{FOOT}">{e(it["src"])}</p>')
        s.append("</div>")
        out.append("".join(s))
    out.append("</div>")
    out += note_block(d)
    return out + tail(d)


def k_compare(d):
    out = head(d)
    out.append('<div style="flex:1;display:grid;grid-template-columns:repeat(2, 1fr);gap:24px">')
    for side in (d["left"], d["right"]):
        acc = side.get("accent")
        border = f"border:2px solid {AMBER};" if acc else ""
        lis = "".join(f"<li>{e(x)}</li>" for x in side["items"])
        out.append(f'<div style="background:{CARD};{border}border-radius:16px;padding:40px;display:flex;flex-direction:column;gap:24px">'
                   f'<h3 style="font-size:32px;font-weight:600;color:{AMBER if acc else TEXT}">{e(side["t"])}</h3>'
                   f'<ul style="font-size:28px;line-height:1.5;color:{MUTED}">{lis}</ul></div>')
    out.append("</div>")
    out += note_block(d)
    return out + tail(d)


def k_steps(d):
    out = head(d)
    n = len(d["steps"])
    out.append(f'<div style="display:grid;grid-template-columns:repeat({n}, 1fr);gap:24px">')
    for i, s in enumerate(d["steps"], 1):
        out.append(f'<div style="background:{CARD};border-radius:16px;padding:32px;display:flex;flex-direction:column;gap:16px">'
                   f'<p style="font-family:{DISP};font-size:56px;font-weight:700;color:{AMBER}">{i}</p>{p(s, color=TEXT)}</div>')
    out.append("</div>")
    out.append('<div style="flex:1"></div>')
    if d.get("demo"):
        out.append(f'<p style="font-family:{MONO};font-size:28px;color:{MUTED};background:{BG};border:2px solid {BORDER};border-radius:12px;padding:24px 32px">{e(d["demo"])}</p>')
    out += note_block(d)
    return out + tail(d)


def code_line(ln):
    if isinstance(ln, str):
        return e(ln).replace("  ", "&#160;&#160;") if ln else "&#160;"
    return "".join(f'<span style="color:{ROLE[r]}">{e(t).replace("  ", "&#160;&#160;")}</span>' for t, r in ln)


def k_code(d):
    out = head(d)
    n = len(d["code"])
    size = 26 if n <= 9 else (24 if n <= 11 else 22)
    code = "<br>".join(code_line(ln) for ln in d["code"])
    out.append('<div style="flex:1;display:grid;grid-template-columns:1080px 1fr;gap:24px">')
    out.append(f'<div style="background:{BG};border:2px solid {BORDER};border-radius:16px;padding:40px">'
               f'<p style="font-family:{MONO};font-size:{size}px;line-height:1.5;color:{MUTED}">{code}</p></div>')
    side = "".join(f'<div style="display:flex;flex-direction:column;gap:8px"><p style="font-size:28px;font-weight:600;color:{AMBER}">{e(a)}</p>{p(b)}</div>'
                   for a, b in d["side"])
    out.append(f'<div style="background:{CARD};border-radius:16px;padding:40px;display:flex;flex-direction:column;gap:28px">{side}</div>')
    out.append("</div>")
    return out + tail(d)


def k_timeline(d):
    out = head(d)
    n = len(d["items"])
    out.append(f'<div style="flex:1;display:grid;grid-template-columns:repeat({n}, 1fr);gap:24px;align-items:start">')
    for i, (when, what) in enumerate(d["items"]):
        last = i == n - 1
        out.append(f'<div style="display:flex;flex-direction:column;gap:16px;border-top:4px solid {AMBER if last else "#3A475C"};padding:32px 0 0 0">'
                   f'<p style="font-family:{DISP};font-size:56px;font-weight:700;color:{AMBER if last else TEXT}">{e(when)}</p>{p(what)}</div>')
    out.append("</div>")
    return out + tail(d)


def k_closing(d):
    out = [f'<section id="{d["id"]}" data-transition="fade" style="background:{AMBER};color:{BG};font-family:{BODY};padding:128px 128px 160px;display:flex;flex-direction:column;gap:48px">',
           f'<p style="font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:{BG}">{e(d["eyebrow"])}</p>',
           f'<h2 style="font-family:{DISP};font-size:72px;font-weight:700;line-height:1.1;color:{BG}">{e(d["title"])}</h2>',
           '<div style="flex:1;display:grid;grid-template-columns:repeat(3, 1fr);gap:24px;align-items:start">']
    for c in d["cards"]:
        out.append(f'<div style="display:flex;flex-direction:column;gap:12px;border-top:4px solid {BG};padding:24px 0 0 0">'
                   f'<h3 style="font-size:32px;font-weight:700">{e(c["t"])}</h3><p style="font-size:28px">{e(c["body"])}</p></div>')
    out.append("</div>")
    n = NUM[d["id"]]
    out.append(f'<p style="position:absolute;left:128px;bottom:64px;width:1664px;font-size:24px;color:{BG}">{n} · {e(d["src"])}</p>')
    out.append(f"<aside>{e(d['notes'])}</aside>")
    out.append("</section>")
    return out


KINDS = {k[2:]: v for k, v in globals().items() if k.startswith("k_")}


def main():
    sl = OUT / "slides"
    sl.mkdir(parents=True, exist_ok=True)
    for d in spec.SLIDES:
        (sl / f"{d['id']}.html").write_text("\n".join(KINDS[d["kind"]](d)) + "\n", encoding="utf-8")
    base = json.loads((HERE / "deck_base.json").read_text())
    base["order"] = ORDER
    base["sections"] = {k: {"description": v[0], "start": v[1]} for k, v in spec.SECTIONS.items()}
    (OUT / "deck.json").write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
    print(len(ORDER), "slides")


if __name__ == "__main__":
    main()
