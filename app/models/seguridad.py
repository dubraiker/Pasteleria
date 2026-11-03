from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UsuarioRegistroCliente(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    password: str


class UsuarioBase(BaseModel):
    id_perfil: int
    nombre: str
    apellido: str
    correo: EmailStr
    foto_perfil_url: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str
    embedding_facial: Optional[List[float]] = None

# --- AGREGAR ESTA CLASE QUE FALTABA ---
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    id_perfil: Optional[int] = None
    foto_perfil_url: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    estado: bool
    perfil_nombre: Optional[str] = None
    creado: datetime
    actualizado: datetime

    class Config:
        from_attributes = True