from fastapi.staticfiles import StaticFiles
import os

from database import create_db_and_tables, engine
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import *
from sqlmodel import Session, col, select

app = FastAPI()



jogos = []

templates = Jinja2Templates(directory="templates")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

def buscar_jogos(busca):
    with Session(engine) as session:
        query = select(Jogo).where(col(Jogo.nome).contains(busca)).order_by(Jogo.nome)
        return session.exec(query).all()
    
@app.get("/lista", response_class=HTMLResponse)
def lista(request: Request, busca: str | None=''):
    jogos = buscar_jogos(busca)
    return templates.TemplateResponse(request, "lista.html", {"jogos": jogos})


@app.get("/busca", response_class=HTMLResponse)
def busca(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/adicionarJogo")
def novoJogo(request: Request):
    return templates.TemplateResponse(request, "options.html")