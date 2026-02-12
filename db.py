from sqlmodel import Session, create_engine, Session as SessionType
from typing import Annotated, Generator
from fastapi import Depends

DATABASE_URL = "mysql+pymysql://jjesus:jjesus005@localhost/Usuarios"

engine=create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[SessionType, None, None]: 
    with Session(engine) as session: 
         yield session

SessionDep= Annotated[SessionType, Depends(get_session)]


def Conexion(): 
    try:
        with Session(engine) as session: 
             print("Conexion exitosa.")
    except Exception as e: 
       print(f"error: {e}")

if __name__ == "__main__":
   Conexion()
