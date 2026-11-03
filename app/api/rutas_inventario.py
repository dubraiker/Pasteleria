from fastapi import APIRouter, HTTPException, status
from app.models.inventario import ProductoCreate
from app.repositories.inventario_repo import InventarioRepository

router = APIRouter(prefix="/productos", tags=["Gestión de Productos e Inventario"])
repo = InventarioRepository()

@router.get("/")
def listar_productos():
    return repo.obtener_todos_productos()

@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    producto = repo.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    nuevo_id = repo.crear_producto(producto)
    return {"mensaje": "Producto registrado exitosamente", "id": nuevo_id}

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int):
    exito = repo.desactivar_producto(producto_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto desactivado correctamente (Eliminación Lógica)"}