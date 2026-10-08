from pydantic import BaseModel
from typing import Optional

class DispositivoIotCreate(BaseModel):
    nombre: str
    tipo: str

class DispositivoIotOut(BaseModel):
    id: int
    nombre: str
    tipo: str
    activo: bool

    class Config:
        from_attributes = True

class LecturaSensorCreate(BaseModel):
    dispositivo_id: int
    valor: str

class LecturaSensorOut(BaseModel):
    id: int
    dispositivo_id: int
    valor: str
    fecha_lectura: str

    class Config:
        from_attributes = True