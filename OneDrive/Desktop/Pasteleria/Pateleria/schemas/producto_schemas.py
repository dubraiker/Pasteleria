from pydantic import BaseModel
from typing import Optional

class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: int
    categoria_id: int

class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: int
    categoria_id: int
    activo: bool

    class Config:
        from_attributes = True

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True