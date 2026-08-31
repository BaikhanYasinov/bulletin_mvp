from datetime import date

from . import config
from .charts import render_trend_chart
from .data_source import get_weekly_kpis


def build_bulletin(reference_date: date | None = None) -> dict:
    """Собирает единый контекст с данными, который используют оба рендерера (HTML и PDF)."""
    data = get_weekly_kpis(reference_date, weeks_history=config.WEEKS_HISTORY)

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    period_tag = data["period_start"].strftime("%Y-%m-%d")
    chart_path = config.OUTPUT_DIR / f"chart_{period_tag}.png"
    render_trend_chart(data["history"], chart_path)

    return {
        "title": config.BULLETIN_TITLE,
        "period_start": data["period_start"].strftime("%d.%m.%Y"),
        "period_end": data["period_end"].strftime("%d.%m.%Y"),
        "generated_at": date.today().strftime("%d.%m.%Y"),
        "kpis": data["kpis"],
        "top_products": data["top_products"],
        "alerts": data["alerts"],
        "chart_path": chart_path,
        "period_tag": period_tag,
    }
