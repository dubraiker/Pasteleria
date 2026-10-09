from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Pateleria.database import get_db
from Pateleria.models.inventario_models import Producto 
from Pateleria.schemas.producto_schemas import ProductoCreate
from Pateleria.core.dependencies import requerir_roles

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(requerir_roles(["administrador", "operador"]))])
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo producto en la base de datos de Neon DB."""
    
    datos_producto = producto.model_dump() if hasattr(producto, "model_dump") else producto.dict()
    
    
    nuevo_producto = Producto(**datos_producto)
    
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    
    return {
        "mensaje": "Producto registrado en el inventario exitosamente",
        "producto": nuevo_producto
    }


@router.get("/")
def listar_inventario(db: Session = Depends(get_db)):
    """Obtiene el listado real de productos desde Neon PostgreSQL."""
    productos = db.query(Producto).all()
    return productos