from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

class Login(BaseModel):
    login: str
    passwd: str

users:dict= {}

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root (request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.post("/users", response_class=HTMLResponse)
async def cria_usuario(request: Request):
    data = await request.json()
    
    login = data.get("login")
    senha = data.get("senha")
    print(login, senha, users)

    users[login] = senha
    return JSONResponse(content={
        "message": "Usuário adicionado",
    })

@app.get("/login", response_class=HTMLResponse)
def plataformas(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def testarLogin(request: Request):
    data = await request.json()
    user = data.get("login")
    senha = data.get("senha")
    print(user, senha, users)
    if (user in users and users[user] == senha):
        return templates.TemplateResponse(request, "logged.html", {"request": request})
    else:
        return JSONResponse(content={
            "message": "Login ou senha invalidos"
        })
