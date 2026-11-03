from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    etiqueta_yolo: str

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: Optional[int] = None
    estado: bool = True