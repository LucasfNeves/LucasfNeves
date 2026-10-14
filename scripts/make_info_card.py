"""Gera info-card.svg: painel estilo neofetch que imprime linha a linha.

Edite a lista INFO abaixo para mudar o conteúdo.
Uso: python scripts/make_info_card.py   (STATIC=1 para quadro parado)
"""

import os
from pathlib import Path

from theme import BLUE, GREEN, HOST, MUTED, ORANGE, PURPLE, TEXT, USER, esc, window

# (chave, valor). Chave vazia = continuação da linha anterior.
INFO = [
    ("Nome", "Lucas Farias"),
    ("Função", "Desenvolvedor Fullstack"),
    ("Empresa", "Compass UOL · grupo AI/R"),
    ("Local", "Guarulhos, SP · Brasil"),
    ("Na área", "desde 2023"),
    ("Formação", "Análise e Desenv. de Sistemas · Mackenzie"),
    ("Pós", "Engenharia de Software · FIAP"),
    ("Foco", "Arquitetura de Software"),
    ("", "Clean Arch · DDD · Hexagonal · Event-Driven"),
    ("Front", "React · Next.js · TypeScript · Tailwind"),
    ("Back", "Node.js · NestJS · GraphQL · Express"),
    ("Dados", "PostgreSQL · Prisma · MongoDB"),
    ("DevOps", "Docker · CI/CD · Vitest · Jest"),
    ("Projetos", "Vivo Commerce · Lusiana E-commerce"),
    ("", "ProSESMT · Mobi Logística"),
]

W, H = 490, 420
STATIC = os.environ.get("STATIC") == "1"
OUT = Path(__file__).resolve().parent.parent / "info-card.svg"


def appear(content: str, begin: float) -> str:
    if STATIC:
        return "  " + content
    return (
        f'  <g opacity="0" transform="translate(-6 0)">{content}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="-6 0" to="0 0" begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>'
        f"</g>"
    )


def main() -> None:
    x_key, x_val = 26, 120
    y = 62
    t = 0.4
    parts = []

    head = (
        f'<text x="{x_key}" y="{y}" font-size="13.5" font-weight="700">'
        f'<tspan fill="{GREEN}">{USER}</tspan><tspan fill="{TEXT}">@</tspan><tspan fill="{GREEN}">{HOST}</tspan></text>'
    )
    parts.append(appear(head, t))
    y += 9
    parts.append(appear(f'<line x1="{x_key}" y1="{y}" x2="{x_key + 118}" y2="{y}" stroke="{MUTED}" stroke-dasharray="3 3"/>', t))
    y += 22
    t += 0.15

    prev = ""
    for key, val in INFO:
        line = (
            f'<text y="{y}" font-size="12.5" xml:space="preserve">'
            + (f'<tspan x="{x_key}" fill="{BLUE}" font-weight="700">{esc(key)}</tspan>' if key else "")
            + f'<tspan x="{x_val}" fill="{MUTED if (not key and prev == "Foco") else TEXT}">{esc(val)}</tspan></text>'
        )
        parts.append(appear(line, t))
        y += 19
        t += 0.12
        prev = key or prev

    # blocos de cor do neofetch
    y += 6
    colors = ["#21262d", "#ff7b72", GREEN, "#d29922", BLUE, PURPLE, "#39c5cf", TEXT]
    blocks = "".join(f'<rect x="{x_key + i * 26}" y="{y}" width="22" height="12" rx="2" fill="{c}"/>' for i, c in enumerate(colors))
    parts.append(appear(f"<g>{blocks}</g>", t))
    parts.append(appear(
        f'<text x="{W - 24}" y="{y + 10}" font-size="11" fill="{ORANGE}" text-anchor="end">neofetch --pt-br</text>', t
    ))

    OUT.write_text(window(W, H, "lucas@github: ~/neofetch", "\n".join(parts)), encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
