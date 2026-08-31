"""
Flask-прототип бюллетеня.

Роуты:
  GET  /                    — архив сформированных бюллетеней + кнопка "Сформировать сейчас"
  POST /generate             — генерирует новый бюллетень (HTML + PDF), редиректит на /
  GET  /bulletin/<period>    — открыть HTML-версию бюллетеня в браузере
  GET  /bulletin/<period>/pdf — скачать PDF-версию
  GET  /output/<filename>    — отдача статики (график PNG), нужна для встроенной картинки в HTML

Запуск:
  cd bulletin_mvp
  python3 app.py
  # затем открыть http://127.0.0.1:5000
"""

from flask import Flask, redirect, render_template, send_from_directory, url_for

from bulletin import config
from bulletin.actions import generate_now

app = Flask(__name__)


def _list_archive() -> list[dict]:
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    periods = sorted(
        {p.stem.replace("bulletin_", "") for p in config.OUTPUT_DIR.glob("bulletin_*.html")},
        reverse=True,
    )
    return [{"period": p} for p in periods]


@app.route("/")
def index():
    return render_template("index.html", items=_list_archive(), flash=None)


@app.route("/generate", methods=["POST"])
def generate():
    generate_now(chart_url_prefix="/output/")
    return redirect(url_for("index"))


@app.route("/bulletin/<period>")
def view_bulletin(period):
    filename = f"bulletin_{period}.html"
    if not (config.OUTPUT_DIR / filename).exists():
        return "Бюллетень не найден", 404
    return send_from_directory(config.OUTPUT_DIR, filename)


@app.route("/bulletin/<period>/pdf")
def download_pdf(period):
    filename = f"bulletin_{period}.pdf"
    if not (config.OUTPUT_DIR / filename).exists():
        return "Файл не найден", 404
    return send_from_directory(config.OUTPUT_DIR, filename, as_attachment=True)


@app.route("/output/<path:filename>")
def output_file(filename):
    return send_from_directory(config.OUTPUT_DIR, filename)


if __name__ == "__main__":
    app.run(debug=False, port=5000)
