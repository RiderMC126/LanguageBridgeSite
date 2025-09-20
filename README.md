# 🌍 LanguageBridgeSite

**LanguageBridgeSite** — это веб-приложение-чата на **FastAPI**, которое автоматически переводит сообщения так, чтобы получатель всегда читал их на своём языке.

---

## 🎯 Основная идея

- Регистрация с выбором языка.
- Сообщения автоматически переводятся на язык получателя.
- Отправитель всегда видит оригинал, а не перевод.
- Чат работает в реальном времени через **WebSocket**.

---

## 🔧 Технологии

| Компонент | Используется |
|-----------|--------------|
| Язык | Python 3.x |
| Веб-фреймворк | FastAPI |
| WebSocket | Uvicorn |
| Перевод | [deep-translator](https://pypi.org/project/deep-translator/) |
| БД | PostgreSQL + asyncpg |
| Фронтенд | HTML, CSS, JavaScript |
| Сервер | Nginx / ngrok (для внешнего доступа) |

---

## 🚀 Установка

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/RiderMC126/LanguageBridgeSite.git
   cd LanguageBridgeSite
   ```
2. Создать и активировать виртуальное окружение:
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   source venv/bin/activate  # Linux / macOS
   ```
  
3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Настроить "config.py".
5. Запустить сервер:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   


   
