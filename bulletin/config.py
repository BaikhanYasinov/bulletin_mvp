"""
Конфигурация MVP.

позже стоит вынести в .env / переменные окружения
или в настройки конкретного получателя/проекта (если бюллетеней много).
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
STATE_FILE = BASE_DIR / "state.json"

# --- Расписание ---
# День недели рассылки: 0 = понедельник ... 6 = воскресенье
SCHEDULE_WEEKDAY = 0
SCHEDULE_HOUR = 9  # используется как справочное значение для cron/планировщика ОС

# --- Получатели (заглушка на будущее; в MVP реально никуда не отправляем) ---
RECIPIENTS = [
    "ceo@example.com",
    "sales-team@example.com",
]

# --- Контент ---
BULLETIN_TITLE = "Еженедельный бюллетень: продажи и клиенты"
WEEKS_HISTORY = 8  # сколько недель истории показывать на графике тренда
