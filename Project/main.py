from typing import List, Optional
from fastapi.staticfiles import StaticFiles
import os

from database import create_db_and_tables, engine
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, col, select, Relationship, Field, SQLModel
from contextlib import asynccontextmanager


jogos = []

templates = Jinja2Templates(directory="templates")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

class Disponibilidade(SQLModel, table=True):
    jogo_id: Optional[int] = Field(
        default=None,
        foreign_key="jogo.id",
        primary_key=True,
    )
    plataforma_id: Optional[int] = Field(
        default=None,
        foreign_key="plataforma.id",
        primary_key=True,
    )

class Jogo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nome: str
    descricao: Optional[str] = None
    nota: Optional[int] = None

    plataforma: List["Plataforma"] = Relationship(
        back_populates="jogos",
        link_model=Disponibilidade,
    )
    
class Plataforma(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nome: str

    jogos: List["Jogo"] = Relationship(
        back_populates="plataforma",
        link_model=Disponibilidade,
    )

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request, "index.html")
    
@app.post("/novoJogo", response_class=HTMLResponse)
def criar_jogo(nome: str = Form(...), descricao: str = Form(None), nota: int = Form(None)):
    with Session(engine) as session:
        novo_jogo = Jogo(nome=nome, descricao=descricao, nota=nota)
        session.add(novo_jogo)
        session.commit()
        session.refresh(novo_jogo)
        return HTMLResponse(content=f"<p>✅ {novo_jogo.nome} foi adicionado!</p>")
    
@app.delete("/deletaJogo", response_class=HTMLResponse)
def deletar_jogo(id: int = Form(...)):
    with Session(engine) as session:
        query = select(Jogo).where(Jogo.id == id)
        jogo = session.exec(query).first()
        if (not jogo):
            raise HTTPException(404, "Jogo não encontrado")
        session.delete(jogo)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) jogo(a) {jogo.nome} foi deletado(a)!</p>")
    
@app.delete("/deletaTudo", response_class=HTMLResponse)
def deletar_tudo():
    with Session(engine) as session:
        query = select(Jogo)
        jogos = session.exec(query).all()
        for jogo in jogos:
            session.delete(jogo)
        session.commit()
        return HTMLResponse(content=f"<p>Todos os jogos foram deletados!</p>")
    
@app.put("/atualizaJogo", response_class=HTMLResponse)
def atualizar_jogo(
    id: int = Form(...), 
    nome: str = Form(None),
    descricao: str = Form(None),
    nota: int = Form(None)
):
    with Session(engine) as session:
        query = select(Jogo).where(Jogo.id == id)
        jogo = session.exec(query).first()
        
        if not jogo:
            raise HTTPException(404, "Jogo não encontrado")
        
        if nome:
            jogo.nome = nome
        if descricao:
            jogo.descricao = descricao
        if nota:
            jogo.nota = nota
            
        session.add(jogo)
        session.commit()
        session.refresh(jogo)
        return HTMLResponse(content=f"<p>✅ {jogo.nome} foi atualizado!</p>")
    
@app.post("/novaPlataforma", response_class=HTMLResponse)
def criar_plataforma(nome: str = Form(...)):
    with Session(engine) as session:
        nova_plataforma = Plataforma(nome=nome)
        session.add(nova_plataforma)
        session.commit()
        session.refresh(nova_plataforma)
        return HTMLResponse(content=f"<p>✅ {nova_plataforma.nome} foi adicionado!</p>")
    
@app.delete("/deletaPlataforma", response_class=HTMLResponse)
def deletar_plataforma(id: int = Form(...)):
    with Session(engine) as session:
        query = select(Plataforma).where(Plataforma.id == id)
        plataforma = session.exec(query).first()
        if (not plataforma):
            raise HTTPException(404, "Plataforma não encontrada")
        session.delete(plataforma)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) plataforma {plataforma.nome} foi deletado(a)!</p>")

@app.put("/atualizaPlataforma", response_class=HTMLResponse)
def atualizar_plataforma(
    id: int = Form(...), 
    nome: str = Form(None),
    codigo: str = Form(None),
    descricao: str = Form(None)
):
    with Session(engine) as session:
        query = select(Plataforma).where(Plataforma.id == id)
        plataforma = session.exec(query).first()
        
        if not plataforma:
            raise HTTPException(404, "Plataforma não encontrada")
        
        if nome:
            plataforma.nome = nome
        if codigo:
            plataforma.codigo = codigo
        if descricao:
            plataforma.descricao = descricao
            
        session.add(plataforma)
        session.commit()
        session.refresh(plataforma)
        return HTMLResponse(content=f"<p>✅ {plataforma.nome} foi atualizado!</p>")


def buscar_jogos(busca):
    with Session(engine) as session:
        query = select(Jogo).where(col(Jogo.nome).contains(busca)).order_by(Jogo.nota.desc())  
        return session.exec(query).all()
    
def buscar_plataformas(busca):
    with Session(engine) as session:
        query = select(Plataforma).where(col(Plataforma.nome).contains(busca)).order_by(Plataforma.nome)  
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

@app.get("/plataformas", response_class=HTMLResponse)
def plataformas(request: Request, busca: str | None=''):
    plataformas = buscar_plataformas(busca)
    return templates.TemplateResponse(request, "plataformas.html", {"plataformas": plataformas})

@app.get("/adicionarPlataforma")
def novaPlataforma(request: Request):
    return templates.TemplateResponse(request, "options_plataforma.html")