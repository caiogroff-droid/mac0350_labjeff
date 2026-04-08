from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    idade: int

users = []

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request, "response.html", {"request": request})


@app.post("/users")
async def create_user(request: Request):
    data = await request.json()
    
    user = {
        "nome": data.get("nome"),
        "idade": data.get("idade")
    }

    users.append(user)

    return JSONResponse(content={
        "message": "Usuário adicionado",
        "user": user,
        "total": len(users)
    })


@app.get("/users")
async def get_users(index: Optional[int] = Query(None)):
    if index is not None:
        if 0 <= index < len(users):
            return JSONResponse(content=users[index])
        return JSONResponse(content={"error": "Índice inválido"}, status_code=400)

    return JSONResponse(content=users)


@app.delete("/users")
async def delete_users():
    users.clear()
    return JSONResponse(content={"message": "Lista de usuários apagada"})