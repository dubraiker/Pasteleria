from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Pateleria.database import get_db

router = APIRouter()

class ProductoSchema(BaseModel):
    nombre: str
    categoria: str
    cantidad: int
    fecha_caducidad: str
    ubicacion_estante: str

@router.get("/")
def listar_inventario(db: Session = Depends(get_db)):
    return [
        {"id": 1, "nombre": "Pastel de Chocolate", "cantidad": 5, "estado": "Óptimo", "fecha_caducidad": "2026-10-12"},
        {"id": 2, "nombre": "Tarta de Fresas", "cantidad": 2, "estado": "Próximo a vencer", "fecha_caducidad": "2026-10-08"}
    ]

@router.post("/")
def registrar_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    return {"mensaje": "Producto registrado en inventario", "producto": producto}