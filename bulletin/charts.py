import matplotlib

matplotlib.use("Agg")  # без GUI — рендер прямо в файл
import matplotlib.pyplot as plt
from pathlib import Path


def render_trend_chart(history: list[dict], out_path: Path) -> Path:
    weeks = [h["week_start"].strftime("%d.%m") for h in history]
    revenue = [h["revenue"] for h in history]

    plt.figure(figsize=(7, 3))
    plt.plot(weeks, revenue, marker="o", linewidth=2, color="#2563eb")
    plt.fill_between(range(len(weeks)), revenue, color="#2563eb", alpha=0.08)
    plt.title("Динамика выручки, последние недели")
    plt.xticks(rotation=30, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path
