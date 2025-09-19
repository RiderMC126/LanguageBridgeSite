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


# Start application
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)