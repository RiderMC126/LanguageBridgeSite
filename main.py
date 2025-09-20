from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
import asyncio
import sys
from config import *
from utils import translate_text
from db import *

# Initialization application
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
active_connections: dict[str, WebSocket] = {}

# Startup event для инициализации базы данных
@app.on_event("startup")
async def on_startup():
    await init_db()  

# ===========================
# Pages
# ===========================
@app.get("/", response_class=HTMLResponse)
async def mainPage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "MainPage"})

@app.get("/about", response_class=HTMLResponse)
async def aboutPage(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "title": "About"})

@app.get("/connect", response_class=HTMLResponse)
async def connectPage(request: Request):
    return templates.TemplateResponse("connect.html", {"request": request, "title": "Connect"})

@app.get("/chat", response_class=HTMLResponse)
async def chatPage(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "title": "Chat"})

# ===========================
# API
# ===========================
@app.post("/api/register")
async def api_register(data: dict):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    language = data.get("language", "en")
    if not username or not email or not password:
        return JSONResponse({"success": False, "message": "All fields are required!"})
    success, message = await register_user(username, email, password, language)
    return JSONResponse({"success": success, "message": message})

@app.post("/api/login")
async def api_login(data: dict):
    loginOrEmail = data.get("loginOrEmail")
    password = data.get("password")
    if not loginOrEmail or not password:
        return JSONResponse({"success": False, "message": "All fields are required!"})
    success, message = await authenticate_user(loginOrEmail, password)
    return JSONResponse({"success": success, "message": message})

@app.get("/api/users/search")
async def search_users(q: str, current: str):
    conn = await asyncpg.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    rows = await conn.fetch("""
        SELECT username FROM users
        WHERE username ILIKE $1 AND username != $2
        ORDER BY username ASC
        LIMIT 10
    """, f"%{q}%", current)
    await conn.close()
    return {"users": [r["username"] for r in rows]}

@app.get("/api/users/history")
async def users_with_history(current: str):
    conn = await asyncpg.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    rows = await conn.fetch("""
        SELECT DISTINCT u.username
        FROM users u
        JOIN messages m ON u.id = m.sender_id OR u.id = m.receiver_id
        WHERE u.username != $1 AND (m.sender_id = (SELECT id FROM users WHERE username=$1)
        OR m.receiver_id = (SELECT id FROM users WHERE username=$1))
    """, current)
    await conn.close()
    return {"users": [r["username"] for r in rows]}

@app.post("/api/messages")
async def send_message(data: dict):
    sender = data.get("sender")
    receiver = data.get("receiver")
    content = data.get("content")
    if not sender or not receiver or not content:
        return JSONResponse({"success": False, "message": "Missing fields"})

    conn = await asyncpg.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    sender_id = await conn.fetchval("SELECT id FROM users WHERE username=$1", sender)
    receiver_id = await conn.fetchval("SELECT id FROM users WHERE username=$1", receiver)
    await conn.execute("INSERT INTO messages(sender_id, receiver_id, content) VALUES($1,$2,$3)",
                       sender_id, receiver_id, content)
    await conn.close()
    return {"success": True}

@app.get("/api/messages/history")
async def messages_history(user1: str, user2: str):
    conn = await asyncpg.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    rows = await conn.fetch("""
        SELECT u.username as sender, m.content, m.created_at
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE (m.sender_id = (SELECT id FROM users WHERE username=$1) 
               AND m.receiver_id = (SELECT id FROM users WHERE username=$2))
           OR (m.sender_id = (SELECT id FROM users WHERE username=$2) 
               AND m.receiver_id = (SELECT id FROM users WHERE username=$1))
        ORDER BY m.created_at ASC
    """, user1, user2)
    await conn.close()
    return {"messages": [{"sender": r["sender"], "content": r["content"]} for r in rows]}

# ===========================
# WebSocket
# ===========================
async def send_translated(receiver: str, sender: str, content: str, receiver_lang: str, sender_lang: str):
    """Асинхронный перевод и отправка только получателю"""
    try:
        if receiver_lang != sender_lang:
            translated_content = await translate_text(content, receiver_lang)
        else:
            translated_content = content

        if receiver in active_connections:
            await active_connections[receiver].send_json({
                "sender": sender,
                "content": translated_content
            })
        # Сохраняем переведённое сообщение
        await save_message(sender, receiver, translated_content)
    except Exception as e:
        logger.error(f"Translation error: {e}")

@app.websocket("/ws/chat/{username}")
async def websocket_chat(websocket: WebSocket, username: str):
    await websocket.accept()
    active_connections[username] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            sender = data.get("sender")
            receiver = data.get("receiver")
            content = data.get("content")
            if not sender or not receiver or not content:
                continue

            # Сохраняем оригинал для отправителя
            await save_message(sender, receiver, content)

            # Отправляем оригинал отправителю мгновенно
            if sender in active_connections:
                await active_connections[sender].send_json({
                    "sender": sender,
                    "content": content
                })

            # Получаем языки пользователей
            conn = await asyncpg.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            receiver_lang = await conn.fetchval("SELECT language FROM users WHERE username=$1", receiver)
            sender_lang = await conn.fetchval("SELECT language FROM users WHERE username=$1", sender)
            await conn.close()

            # Асинхронно переводим и отправляем получателю
            asyncio.create_task(send_translated(receiver, sender, content, receiver_lang, sender_lang))

    except WebSocketDisconnect:
        active_connections.pop(username, None)
    except Exception as e:
        logger.error(f"{username} disconnected: {e}")
        active_connections.pop(username, None)

# ===========================
# Start application
# ===========================
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
