from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config


def render_html(context: dict, chart_url_prefix: str = "") -> Path:
    """
    chart_url_prefix: во что подставлять перед именем файла графика.
      - "" (по умолчанию) — файл открывается напрямую (file://), картинка лежит рядом.
      - "/output/" — используется во Flask-приложении, где картинки отдаются отдельным роутом.
    """
    env = Environment(
        loader=FileSystemLoader(str(Path(__file__).parent / "templates")),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("bulletin.html")
    chart_filename = f"{chart_url_prefix}{context['chart_path'].name}"
    html = template.render(**context, chart_filename=chart_filename)

    out_path = config.OUTPUT_DIR / f"bulletin_{context['period_tag']}.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path
