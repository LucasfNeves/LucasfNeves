"""Gera wordmark.svg: o nome em ASCII que se "digita" linha a linha + um status.

Uso: python scripts/make_wordmark_svg.py
STATIC=1 gera um quadro parado (bom para pré-visualizar).
"""

import os
from pathlib import Path

import pyfiglet

from theme import BLUE, GREEN, MUTED, TEXT, esc, window

NAME = "LUCAS"
STATUS = [
    ("$ ", "cat status.txt"),
    ("> ", "fullstack @ Compass UOL"),
    ("> ", "foco: arquitetura de software"),
    ("> ", "aberto a projetos freelance"),
]

W, H = 370, 420
STATIC = os.environ.get("STATIC") == "1"
OUT = Path(__file__).resolve().parent.parent / "wordmark.svg"


def typed_line(idx: int, x: float, y: float, width: float, begin: float, dur: float, content: str) -> str:
    """Uma linha revelada da esquerda para a direita por um clip animado, com cursor na borda."""
    if STATIC:
        return content
    clip = f"c{idx}"
    return f"""  <clipPath id="{clip}"><rect x="{x}" y="{y - 14}" height="22" width="0">
    <animate attributeName="width" from="0" to="{width}" begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/>
  </rect></clipPath>
  <g clip-path="url(#{clip})">{content}</g>
  <rect y="{y - 11}" width="7" height="14" fill="{GREEN}" opacity="0">
    <animate attributeName="x" from="{x}" to="{x + width}" begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/>
    <set attributeName="opacity" to="0.85" begin="{begin:.2f}s"/>
    <set attributeName="opacity" to="0" begin="{begin + dur:.2f}s"/>
  </rect>"""


def main() -> None:
    rows = [r for r in pyfiglet.figlet_format(NAME, font="ansi_shadow").rstrip("\n").split("\n") if r.strip()]
    cols = max(len(r) for r in rows)
    char_w = 7.4
    font_size = 12.5
    art_w = cols * char_w
    x0 = (W - art_w) / 2
    y0 = 84
    line_h = 17

    parts = []
    t = 0.3
    seg = {  # caractere de caixa -> segmentos (do centro até as bordas)
        "═": "lr", "║": "ud", "╗": "ld", "╔": "rd", "╝": "lu", "╚": "ru",
    }
    for i, row in enumerate(rows):
        y = y0 + i * line_h
        top = y - 11.5
        shapes = []
        for c, ch in enumerate(row):
            cx = x0 + c * char_w
            if ch == "█":
                shapes.append(f'<rect x="{cx:.1f}" y="{top:.1f}" width="{char_w + 0.3:.1f}" height="{line_h + 0.3:.1f}" fill="{GREEN}"/>')
            elif ch in seg:
                mx, my = cx + char_w / 2, top + line_h / 2
                ends = {"l": (cx, my), "r": (cx + char_w, my), "u": (mx, top), "d": (mx, top + line_h)}
                d = " ".join(f"M{mx:.1f} {my:.1f} L{ends[k][0]:.1f} {ends[k][1]:.1f}" for k in seg[ch])
                shapes.append(f'<path d="{d}" stroke="#1f7a35" stroke-width="1.6" stroke-linecap="square" fill="none"/>')
        txt = '<g shape-rendering="crispEdges">' + "".join(shapes) + "</g>"
        parts.append(typed_line(i, x0, y, art_w, t, 0.35, txt) if not STATIC else "  " + txt)
        t += 0.22

    sub_y = y0 + len(rows) * line_h + 26
    sub = f'<text x="{W / 2}" y="{sub_y}" font-size="13" fill="{TEXT}" text-anchor="middle">Desenvolvedor Fullstack</text>'
    parts.append(
        sub if STATIC else
        f'  <g opacity="0">{sub}<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.5s" fill="freeze"/></g>'
    )
    t += 0.6

    sep_y = sub_y + 22
    parts.append(f'  <line x1="24" y1="{sep_y}" x2="{W - 24}" y2="{sep_y}" stroke="#21262d"/>')

    y = sep_y + 32
    for j, (prompt, text) in enumerate(STATUS):
        color = BLUE if prompt.startswith("$") else MUTED
        body_color = TEXT if prompt.startswith("$") else "#e6edf3"
        txt = (
            f'<text x="26" y="{y}" font-size="12.5" xml:space="preserve">'
            f'<tspan fill="{color}">{esc(prompt)}</tspan><tspan fill="{body_color}">{esc(text)}</tspan></text>'
        )
        width = (len(prompt) + len(text)) * 7.6 + 4
        parts.append(typed_line(100 + j, 26, y, width, t, 0.18 + len(text) * 0.022, txt) if not STATIC else "  " + txt)
        t += 0.25 + len(text) * 0.022
        y += 24

    # cursor piscando no fim
    cursor = f'<text x="26" y="{y}" font-size="12.5" fill="{BLUE}">$</text>'
    blink = (
        f'<rect x="40" y="{y - 11}" width="7" height="14" fill="{GREEN}">'
        + ("" if STATIC else f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite" begin="{t:.2f}s"/>')
        + "</rect>"
    )
    parts.append(f"  {cursor}\n  {blink}" if STATIC else
                 f'  <g opacity="0">{cursor}{blink}<set attributeName="opacity" to="1" begin="{t:.2f}s"/></g>')

    OUT.write_text(window(W, H, "lucas@github: ~", "\n".join(parts)), encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
