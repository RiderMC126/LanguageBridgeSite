from fastapi import FastAPI, Request, Form, HTTPException, Depends, UploadFile, File, WebSocket
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
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


# Main Page
@app.get("/", response_class=HTMLResponse)
async def mainPage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "title": "MainPage"}
    )

# About Page
@app.get("/about", response_class=HTTPException)
async def aboutPage(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request,
         "title": "About"
         }
    )


# Start application
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)