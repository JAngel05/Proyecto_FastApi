#Archivo donde se encuentra el esquema de la tabl, para generacion de los datos y la validacion de los tipos. 
from sqlmodel import SQLModel,Field

class Usuario(SQLModel, table = True): 
      id: int |  None = Field(default = None, primary_key= True)
      Nombre: str
      Apellido_P: str
      Numero: str
