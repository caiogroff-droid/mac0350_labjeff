from typing import List, Optional
from fastapi.staticfiles import StaticFiles
import os

from database import create_db_and_tables, engine
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, col, select, Relationship, Field, SQLModel
from contextlib import asynccontextmanager

app = FastAPI()



jogos = []

templates = Jinja2Templates(directory="templates")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


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
    codigo: str = Field(index=True, unique=True)
    descricao: Optional[str] = None

    jogos: List["Jogo"] = Relationship(
        back_populates="plataforma",
        link_model=Disponibilidade,
    )

# @app.get("/jogos")
# def buscar_jogos_por_nome(nome: Optional[str]):
#     with Session(engine) as session:
#         if nome:
#             query = select(Jogo).where(Jogo.nome.contains(nome))
#             return session.exec(query).all()

#         query = select(Jogo)
#         return session.exec(query).all()
    
# @app.patch("/jogos/{id}")
# def atualizar_descricao(id: str, descricao: str):
#     with Session(engine) as session:
#         query = select(Jogo).where(Jogo.id == id)
#         jogo = session.exec(query).first()

#         if not jogo:
#             raise HTTPException(404, "jogo não encontrado")

#         jogo.descricao = descricao
#         session.add(jogo)
#         session.commit()
#         session.refresh(jogo)

#         return jogo
    
# @app.get("/plataforma/{codigo}")
# def buscar_plataforma(codigo: str):
#     with Session(engine) as session:
#         query = select(Plataforma).where(Plataforma.codigo == codigo)
#         return session.exec(query).first()

# @app.get("/plataforma/{codigo}/jogos")
# def jogos_da_plataforma(codigo: str):
#     with Session(engine) as session:
#         query = (
#             select(Jogo)
#             .join(Disponibilidade, Disponibilidade.jogo_id == Jogo.id)
#             .join(Plataforma, Disponibilidade.plataforma_id == Plataforma.id)
#             .where(Plataforma.codigo == codigo)
#         )

#         return session.exec(query).all()

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
def deletar_jogo(id: int):
    with Session(engine) as session:
        query = select(Jogo).where(Jogo.id == id)
        jogo = session.exec(query).first()
        if (not jogo):
            raise HTTPException(404, "Jogo não encontrado")
        session.delete(jogo)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) jogo(a) {jogo.nome} foi deletado(a)!</p>")
    
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


def buscar_jogos(busca):
    with Session(engine) as session:
        query = select(Jogo).where(col(Jogo.nome).contains(busca)).order_by(Jogo.nota.desc())  
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