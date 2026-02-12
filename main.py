#es el punto de entrada y los registros de los routers/ deficinicion de las rutas. 

from fastapi import FastAPI
from sqlmodel import SQLModel
from db import engine
from routers import usuarios

app = FastAPI(title = "CRUD de usuarios.")

@app.on_event("startup")
def inicio():
    SQLModel.metadata.create_all(engine)

app.include_router(usuarios.router)

@app.get("/")
def root(): 
    return {"status": "Online"}

