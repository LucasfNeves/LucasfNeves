"""Paleta e helpers compartilhados entre os SVGs do perfil."""

from xml.sax.saxutils import escape

BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#39d353"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"
ORANGE = "#ffa657"

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

USER = "lucas"
HOST = "github"


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def window(width: int, height: int, title: str, body: str, extra_style: str = "") -> str:
    """Janela de terminal (barra de título + três bolinhas) envolvendo `body`."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
  <style>
    text {{ font-family: {FONT}; }}
    {extra_style}
  </style>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
  <path d="M0.5 32 V10.5 a10 10 0 0 1 10 -10 H{width - 10.5} a10 10 0 0 1 10 10 V32 Z" fill="{PANEL}"/>
  <line x1="0.5" y1="32" x2="{width - 0.5}" y2="32" stroke="{BORDER}"/>
  <circle cx="18" cy="16" r="5.5" fill="#ff5f56"/>
  <circle cx="36" cy="16" r="5.5" fill="#ffbd2e"/>
  <circle cx="54" cy="16" r="5.5" fill="#27c93f"/>
  <text x="{width / 2}" y="20.5" text-anchor="middle" font-size="12" fill="{MUTED}">{esc(title)}</text>
{body}
</svg>
"""
