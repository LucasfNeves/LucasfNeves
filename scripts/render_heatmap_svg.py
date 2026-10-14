"""Desenha contrib-heatmap.svg a partir de data/contributions.json.

As caixas entram na diagonal, uma vez, e congelam.
Uso: python scripts/render_heatmap_svg.py   (STATIC=1 para quadro parado)
"""

import json
import os
from datetime import date
from pathlib import Path

from theme import MUTED, TEXT, GREEN, esc, window

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"
STATIC = os.environ.get("STATIC") == "1"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
MONTHS = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

W, H = 860, 232
CELL, GAP = 12, 3
STEP = CELL + GAP


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"]
    st = data["stats"]

    # O GitHub usa nível 0–4; o topo do ramp (5) fica para dias excepcionais.
    peak = max((d["count"] for d in days), default=0)

    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # domingo = linha 0
    grid_w = ((len(days) + offset + 6) // 7) * STEP - GAP
    x0 = (W - grid_w) / 2 + 12
    y0 = 70

    cells, months = [], []
    last_month = None
    for i, d in enumerate(days):
        idx = i + offset
        col, row = divmod(idx, 7)
        dt = date.fromisoformat(d["date"])
        level = d["level"]
        if peak >= 10 and d["count"] >= peak * 0.9:
            level = 5
        x, y = x0 + col * STEP, y0 + row * STEP
        style = "" if STATIC else f' style="animation-delay:{(col + row) * 0.018:.3f}s"'
        cells.append(
            f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[level]}"{style}>'
            f'<title>{d["count"]} em {dt.strftime("%d/%m/%Y")}</title></rect>'
        )
        if dt.month != last_month and row <= 1:
            if not months or col - months[-1][0] >= 3:
                months.append((col, MONTHS[dt.month - 1]))
            last_month = dt.month

    labels = "".join(
        f'<text x="{x0 + c * STEP}" y="{y0 - 9}" font-size="10.5" fill="{MUTED}">{m}</text>' for c, m in months
    )
    labels += "".join(
        f'<text x="{x0 - 8}" y="{y0 + r * STEP + 9.5}" font-size="10" fill="{MUTED}" text-anchor="end">{t}</text>'
        for r, t in ((1, "seg"), (3, "qua"), (5, "sex"))
    )

    foot_y = y0 + 7 * STEP + 26
    best = st["best_day"]
    best_txt = f'{best["count"]} em {date.fromisoformat(best["date"]).strftime("%d/%m")}' if best["count"] else "—"
    sep = f'<tspan fill="{MUTED}">  ·  </tspan>'
    footer = (
        f'<text x="{x0}" y="{foot_y}" font-size="11.5" xml:space="preserve">'
        f'<tspan fill="{GREEN}" font-weight="700">{fmt(st["total"])}</tspan>'
        f'<tspan fill="{TEXT}"> contribuições no último ano</tspan>{sep}'
        f'<tspan fill="{MUTED}">sequência </tspan><tspan fill="{TEXT}">{st["current_streak"]}d</tspan>{sep}'
        f'<tspan fill="{MUTED}">recorde </tspan><tspan fill="{TEXT}">{st["longest_streak"]}d</tspan>{sep}'
        f'<tspan fill="{MUTED}">melhor dia </tspan><tspan fill="{TEXT}">{esc(best_txt)}</tspan></text>'
    )
    lx = x0 + grid_w - 6 * STEP - 28
    legend = f'<text x="{lx - 6}" y="{foot_y}" font-size="10.5" fill="{MUTED}" text-anchor="end">menos</text>'
    legend += "".join(
        f'<rect x="{lx + i * STEP}" y="{foot_y - 10}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>'
        for i, c in enumerate(PALETTE)
    )
    legend += f'<text x="{lx + 6 * STEP + 3}" y="{foot_y}" font-size="10.5" fill="{MUTED}">mais</text>'

    css = "" if STATIC else (
        ".c{opacity:0;transform-box:fill-box;transform-origin:center;"
        "animation:pop .45s cubic-bezier(.2,.8,.2,1) forwards}"
        "@keyframes pop{0%{opacity:0;transform:translateY(-6px) scale(.6)}100%{opacity:1;transform:none}}"
    )
    body = "\n".join(["  " + labels, "  " + "".join(cells), "  " + footer, "  " + legend])
    OUT.write_text(window(W, H, "lucas@github: ~/contribuicoes", body, css), encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
