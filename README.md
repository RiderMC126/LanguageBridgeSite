# 🌐 LanguageBridgeSite

**LanguageBridgeSite** — это веб-приложение-чата, разработанное с использованием FastAPI, которое автоматически переводит сообщения, обеспечивая бесшовное общение между пользователями, говорящими на разных языках.

---

## 🚀 Описание

LanguageBridgeSite позволяет пользователям:

- **Регистрироваться** с выбором языка интерфейса.
- **Отправлять сообщения**, которые автоматически переводятся на язык получателя.
- **Видеть оригинальные сообщения**, сохраняя контекст и нюансы общения.
- **Общаться в реальном времени** благодаря использованию WebSocket.

---

## 🧩 Технологии

| Компонент        | Используется |
|------------------|--------------|
| Язык             | Python       |
| Веб-фреймворк    | FastAPI      |
| Шаблонизатор     | Jinja2       |
| База данных      | SQLite       |
| Асинхронность    | asyncio      |
| WebSocket        | Starlette    |
| Перевод          | Google Translate API |

---

## 📦 Установка и запуск

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
   


   
