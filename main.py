from fastapi import FastAPI, Request, Form, HTTPException, Depends, UploadFile, File, WebSocket
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
import asyncio
import sys
from config import *
from utils import *
from db import *


# Initialization application
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


# Startup event для инициализации базы данных
@app.on_event("startup")
async def on_startup():
    await init_db()  


# Main Page
@app.get("/", response_class=HTMLResponse)
async def mainPage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "title": "MainPage"}
    )

# About Page
@app.get("/about", response_class=HTMLResponse)
async def aboutPage(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request,
         "title": "About"
         }
    )

# Connect Page
@app.get("/connect", response_class=HTMLResponse)
async def connectPage(request: Request):
    return templates.TemplateResponse(
        "connect.html",
        {"request": request,
         "title": "Connect"
         }
    )

# API для регистрации
@app.post("/api/register")
async def api_register(data: dict):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        return JSONResponse({"success": False, "message": "All fields are required!"})
    success, message = await register_user(username, email, password)
    return JSONResponse({"success": success, "message": message})

# API для логина
@app.post("/api/login")
async def api_login(data: dict):
    loginOrEmail = data.get("loginOrEmail")
    password = data.get("password")
    if not loginOrEmail or not password:
        return JSONResponse({"success": False, "message": "All fields are required!"})
    success, message = await authenticate_user(loginOrEmail, password)
    return JSONResponse({"success": success, "message": message})



# Start application
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)