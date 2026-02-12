from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import SQLModel,Field,Session,select
from db import SessionDep #Archivo de la conexion a la bd
from models import Usuario

router = APIRouter(prefix = "/usuarios", tags=["Usuarios"])

#En esta funcion vamos a anadir un nuevo registro en la tabla.
@router.post("/", response_model = Usuario)
def crearUsuario(usuario: Usuario, session: SessionDep):
   session.add(usuario)
   session.commit()
   session.refresh(usuario)
   return usuario

#Esta funcion es para leer los registros que existen en la tabla de usuarios.
@router.get("/", response_model = list[Usuario])
def leerUsuarios(session: SessionDep,
                 offset:int = 0,
                 limit: Annotated[int, Query(le=100)] = 100):
     usuarios = session.exec(select(Usuario).offset(offset).limit(limit)).all()
     return usuarios

#Funcion para actualizar los registros. 

@router.patch("/{usuario_id}", response_model = Usuario)
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
@router.get("/{usuarios_id}", response_model = Usuario)
def leerUid(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code = 404, detail= "usuario no encontrado")
    return usuario

#funcion para eliminar registros
@router.delete("/{usuario_id}")
def eliminarUsuario(usuario_id: int, session: SessionDep): 
    usuario = session.get(Usuario, usuario_id)
    if not Usuario: 
        raise HTTPException(status_code = 404, detail = "Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return {"ok": True}
