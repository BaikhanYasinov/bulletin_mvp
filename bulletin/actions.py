"""
Логика "сформировать бюллетень прямо сейчас".

Используется и из CLI (main.py), и из Flask-приложения (app.py) —
чтобы не дублировать вызовы build_bulletin/render_html/render_pdf.
"""

from pathlib import Path

from .generator import build_bulletin
from .render_html import render_html
from .render_pdf import render_pdf


def generate_now(chart_url_prefix: str = "") -> tuple[Path, Path, dict]:
    context = build_bulletin()
    html_path = render_html(context, chart_url_prefix=chart_url_prefix)
    pdf_path = render_pdf(context)
    return html_path, pdf_path, context
