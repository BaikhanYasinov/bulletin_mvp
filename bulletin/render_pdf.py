from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from . import config


def _money(v: int) -> str:
    return f"{v:,} ₽".replace(",", " ")


def render_pdf(context: dict) -> Path:
    out_path = config.OUTPUT_DIR / f"bulletin_{context['period_tag']}.pdf"
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleRu", parent=styles["Title"], fontSize=18)
    normal = styles["Normal"]
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], spaceBefore=12)
    alert_style = ParagraphStyle("Alert", parent=normal, textColor=colors.HexColor("#b91c1c"))

    story = [
        Paragraph(context["title"], title_style),
        Paragraph(
            f"Период: {context['period_start']} – {context['period_end']} · "
            f"Сформировано: {context['generated_at']}",
            normal,
        ),
        Spacer(1, 10),
    ]

    for a in context["alerts"]:
        story.append(Paragraph(f"⚠ {a}", alert_style))
    if context["alerts"]:
        story.append(Spacer(1, 8))

    kpis = context["kpis"]
    kpi_rows = [
        ["Показатель", "Значение", "Δ к прошлой неделе"],
        ["Выручка", _money(kpis["revenue"]), f"{kpis['revenue_delta']:+.1f}%"],
        ["Заказы", str(kpis["orders"]), f"{kpis['orders_delta']:+.1f}%"],
        ["Конверсия", f"{kpis['conversion']}%", f"{kpis['conversion_delta']:+.1f}%"],
        ["Средний чек", _money(kpis["avg_check"]), f"{kpis['avg_check_delta']:+.1f}%"],
    ]
    kpi_table = Table(kpi_rows, colWidths=[60 * mm, 50 * mm, 50 * mm])
    kpi_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story += [Paragraph("Ключевые показатели", h2), kpi_table, Spacer(1, 14)]

    story += [
        Paragraph("Динамика выручки", h2),
        Image(str(context["chart_path"]), width=160 * mm, height=68 * mm),
        Spacer(1, 10),
    ]

    prod_rows = [["Объект", "Выручка", "Рост"]] + [
        [p["name"], _money(p["revenue"]), f"{p['growth']:+.1f}%"] for p in context["top_products"]
    ]
    prod_table = Table(prod_rows, colWidths=[60 * mm, 50 * mm, 50 * mm])
    prod_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story += [Paragraph("Топ-5 объектов по выручке", h2), prod_table]

    doc.build(story)
    return out_path
