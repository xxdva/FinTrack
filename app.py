"""FinTrack — персональный финансовый ассистент (фронтенд по макету из Figma).

Запуск:
    pip install -r requirements.txt
    python app.py
и открыть http://127.0.0.1:8000
"""
from flask import Flask, render_template

app = Flask(__name__)

USER_NAME = "Ильяс"

NAV = [
    {"endpoint": "dashboard", "title": "Главная"},
    {"endpoint": "operations", "title": "Операции"},
    {"endpoint": "budgets", "title": "Бюджеты и цели"},
    {"endpoint": "reports", "title": "Отчёты"},
    {"endpoint": "settings", "title": "Настройки"},
]

# Демо-данные (только для отображения интерфейса)
OPERATIONS = [
    {"id": 1, "date": "25.10.2026", "type": "Доход", "category": "Стипендия", "amount": "+60 000", "account": "Kaspi Gold", "comment": "Стипендия за октябрь"},
    {"id": 2, "date": "24.10.2026", "type": "Расход", "category": "Продукты", "amount": "-12 400", "account": "Kaspi Gold", "comment": "Magnum"},
    {"id": 3, "date": "23.10.2026", "type": "Расход", "category": "Транспорт", "amount": "-3 500", "account": "Наличные", "comment": "Проездной Astana Bus"},
    {"id": 4, "date": "22.10.2026", "type": "Расход", "category": "Кафе", "amount": "-4 800", "account": "Kaspi Gold", "comment": "Кофе и обед"},
    {"id": 5, "date": "20.10.2026", "type": "Доход", "category": "Подработка", "amount": "+45 000", "account": "Halyk", "comment": "Фриланс, вёрстка"},
    {"id": 6, "date": "19.10.2026", "type": "Расход", "category": "Связь", "amount": "-3 990", "account": "Kaspi Gold", "comment": "Интернет"},
    {"id": 7, "date": "17.10.2026", "type": "Расход", "category": "Учёба", "amount": "-25 000", "account": "Halyk", "comment": "Онлайн-курс"},
    {"id": 8, "date": "15.10.2026", "type": "Расход", "category": "Развлечения", "amount": "-7 200", "account": "Наличные", "comment": "Кино и боулинг"},
]

CATEGORY_BARS = [
    {"name": "Учёба", "value": 25.0, "color": "accent"},
    {"name": "Одежда", "value": 18.5, "color": "warning"},
    {"name": "Продукты", "value": 12.4, "color": "neutral-bar"},
    {"name": "Развлечения", "value": 7.2, "color": "expense"},
    {"name": "Кафе", "value": 4.8, "color": "light-bar"},
]

NOTICES = [
    {"text": "Бюджет «Кафе» израсходован на 85%", "color": "warning"},
    {"text": "Цель «Ноутбук»: накоплено 62%", "color": "income"},
    {"text": "Завтра платёж: интернет 3 990 ₸", "color": "accent"},
]

LIMITS = [
    {"name": "Продукты", "spent": "12 400", "limit": "30 000", "percent": 41},
    {"name": "Кафе", "spent": "4 800", "limit": "5 600", "percent": 86},
    {"name": "Транспорт", "spent": "3 500", "limit": "8 000", "percent": 44},
    {"name": "Развлечения", "spent": "7 200", "limit": "10 000", "percent": 72},
    {"name": "Связь", "spent": "3 990", "limit": "4 000", "percent": 100},
]

GOALS = [
    {"name": "Ноутбук", "saved": "310 000", "target": "500 000", "percent": 62},
    {"name": "Поездка в Алматы", "saved": "45 000", "target": "120 000", "percent": 37},
    {"name": "Резервный фонд", "saved": "90 000", "target": "300 000", "percent": 30},
]

# Высоты столбцов в px — как в макете
MONTHS = [
    {"name": "Июль", "income": 154, "expense": 128},
    {"name": "Авг", "income": 187, "expense": 134},
    {"name": "Сен", "income": 209, "expense": 158},
    {"name": "Окт", "income": 264, "expense": 165},
]

CATEGORIES = ["Продукты", "Транспорт", "Кафе", "Связь", "Учёба", "Одежда", "Развлечения"]
ACCOUNTS = ["Kaspi Gold", "Halyk", "Наличные"]


@app.context_processor
def inject_globals():
    return {"nav": NAV, "user_name": USER_NAME}


@app.route("/")
def dashboard():
    max_value = max(bar["value"] for bar in CATEGORY_BARS)
    return render_template(
        "dashboard.html",
        window_title="Главное окно",
        active="dashboard",
        bars=CATEGORY_BARS,
        max_value=max_value,
        notices=NOTICES,
        recent=OPERATIONS[:3],
    )


@app.route("/operations")
def operations():
    return render_template(
        "operations.html",
        window_title="Просмотр и поиск",
        active="operations",
        operations=OPERATIONS,
        categories=CATEGORIES,
    )


@app.route("/operations/new")
def add_operation():
    return render_template(
        "add.html",
        window_title="Добавление операции",
        active="operations",
        categories=CATEGORIES,
        accounts=ACCOUNTS,
    )


@app.route("/operations/<int:op_id>/edit")
def edit_operation(op_id):
    op = next((o for o in OPERATIONS if o["id"] == op_id), OPERATIONS[1])
    return render_template(
        "edit.html",
        window_title="Редактирование операции",
        active="operations",
        op=op,
        categories=CATEGORIES,
        accounts=ACCOUNTS,
    )


@app.route("/budgets")
def budgets():
    return render_template(
        "budgets.html",
        window_title="Бюджеты и цели",
        active="budgets",
        limits=LIMITS,
        goals=GOALS,
    )


@app.route("/reports")
def reports():
    return render_template(
        "reports.html",
        window_title="Отчёты",
        active="reports",
        months=MONTHS,
    )


@app.route("/settings")
def settings():
    return render_template(
        "settings.html",
        window_title="Настройки",
        active="settings",
        categories=CATEGORIES,
        accounts=ACCOUNTS,
    )


if __name__ == "__main__":
    # порт 5000 на macOS занят AirPlay Receiver
    app.run(debug=True, port=8000)
