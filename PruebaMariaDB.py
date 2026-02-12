from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel,Field,Session,select
from db import engine #Archivo de la conexion a la bd

#El SQLModel es las creacion de la tabla, lo que en c# son las entidades, lo que lo diferencia entre las restricciones del campo y 
#que ea una tabla es el "Table=True".

class Usuario(SQLModel, table = True): 
      id: int |  None = Field(default = None, primary_key= True)
      Nombre: str
      Apellido_P: str
      Numero: str

#definimos la funcion para crear las tablas. 
def createTable(): 
    SQLModel.metadata.create_all(engine)

def getSession(): 
    with Session(engine) as session: 
         yield session

SessionDep = Annotated [Session, Depends(getSession)]

app = FastAPI()

#el startup manda a crear las tablas/db si es que no existen.
@app.on_event("startup")
def on_startup():
    createTable()

#En esta funcion vamos a anadir un nuevo registro en la tabla.
@app.post("/usuarios/")
def crearUsuario(usuario: Usuario, session: SessionDep) -> Usuario:
   session.add(usuario)
   session.commit()
   session.refresh(usuario)
   return Usuario

#Esta funcion es para leer los registros que existen en la tabla de usuarios.
@app.get("/usuarios/")
def leerUsuarios(session: SessionDep,
                 offset:int = 0,
                 limit: Annotated[int, Query(le=100)] = 100,
) -> list[Usuario]:
     usuarios = session.exec(select(Usuario).offset(offset).limit(limit)).all()
     return usuarios

#Funcion para actualizar los registros. 

@app.patch("/usuario/{usuario_id}", response_model = Usuario)
def update_usuario(usuario_id: int, DatosUser: Usuario, session: SessionDep):
    db_usuario = session.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code= 404, detail = "Usuario inexistente.")


    data_user = DatosUser.model_dump(exclude_unset = True)
    db_usuario.sqlmodel_update(data_user)

    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario

#Funcion que para leer solo un registro buscandolo por el ID.
@app.get("/usuarios/{usuarios_id}")
def leerUid(usuario_id: int, session: SessionDep) -> Usuario:
    usuario = session.get(Usuario, usuario_id)
    if not usuario:

        raise HTTPException(status_code = 404, detail= "usuario no encontrado")
    return usuario

#funcion para eliminar registros
@app.delete("/usuario/{usuario_id}")
def eliminarUsuario(usuario_id: int, session: SessionDep): 
    usuario = session.get(Usuario, usuario_id)
    if not Usuario: 
        raise HTTPException(status_code = 404, detail = "Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return {"ok": True}


