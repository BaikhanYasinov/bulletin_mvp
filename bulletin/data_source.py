"""
Источник данных для бюллетеня.

Сейчас — генератор моковых данных, реалистично имитирующий недельные
KPI интернет-магазина (выручка, заказы, конверсия, средний чек, топ-товары).

В проде функцию get_weekly_kpis() нужно заменить на реальный запрос
к хранилищу/BI-системе (SQL, REST API, OLAP-куб и т.п.), сохранив
ту же структуру возвращаемых данных — тогда generator.py, рендеры
и шаблон менять не придётся.
"""

import random
from datetime import date, timedelta


def _week_start(d: date | None = None) -> date:
    d = d or date.today()
    return d - timedelta(days=d.weekday())


def get_weekly_kpis(reference_date: date | None = None, weeks_history: int = 8) -> dict:
    ref = _week_start(reference_date)

    # Сид от номера недели — данные одной и той же недели всегда одинаковые
    # (удобно для повторных прогонов и тестов), но меняются от недели к неделе.
    random.seed(ref.isocalendar()[1] + ref.year * 100)

    history = []
    base_revenue = 1_200_000
    for i in range(weeks_history, 0, -1):
        wk_start = ref - timedelta(weeks=i - 1)
        noise = random.uniform(-0.12, 0.15)
        trend = 1 + 0.01 * (weeks_history - i)  # лёгкий рост во времени
        revenue = base_revenue * trend * (1 + noise)
        orders = int(revenue / random.uniform(2800, 3400))
        conversion = round(random.uniform(1.8, 3.4), 2)
        history.append(
            {
                "week_start": wk_start,
                "revenue": round(revenue),
                "orders": orders,
                "conversion": conversion,
                "avg_check": round(revenue / orders),
            }
        )

    current, previous = history[-1], history[-2]

    def delta_pct(cur, prev):
        return round((cur - prev) / prev * 100, 1) if prev else 0.0

    kpis = {
        "revenue": current["revenue"],
        "revenue_delta": delta_pct(current["revenue"], previous["revenue"]),
        "orders": current["orders"],
        "orders_delta": delta_pct(current["orders"], previous["orders"]),
        "conversion": current["conversion"],
        "conversion_delta": delta_pct(current["conversion"], previous["conversion"]),
        "avg_check": current["avg_check"],
        "avg_check_delta": delta_pct(current["avg_check"], previous["avg_check"]),
    }

    products = [
        {
            "name": f"Объект {chr(65 + i)}",
            "revenue": int(random.uniform(50_000, 300_000)),
            "growth": round(random.uniform(-20, 40), 1),
        }
        for i in range(5)
    ]
    products.sort(key=lambda p: -p["revenue"])

    alerts = []
    if kpis["conversion_delta"] < -10:
        alerts.append(f"Конверсия упала на {abs(kpis['conversion_delta'])}% к прошлой неделе")
    if kpis["revenue_delta"] < -15:
        alerts.append(f"Выручка снизилась на {abs(kpis['revenue_delta'])}% — требуется внимание")
    if kpis["revenue_delta"] > 20:
        alerts.append(f"Рекордный рост выручки: +{kpis['revenue_delta']}%")

    return {
        "period_start": current["week_start"],
        "period_end": current["week_start"] + timedelta(days=6),
        "kpis": kpis,
        "history": history,
        "top_products": products,
        "alerts": alerts,
    }
