
from fastapi import APIRouter, HTTPException, status

from app.models.inventario import ProductoCreate
from app.repositories.inventario_repo import InventarioRepository

router = APIRouter(
    prefix="/productos",
    tags=["Inventario"]
)

repo = InventarioRepository()



@router.get("/")
def obtener_productos():

    try:
        return repo.obtener_todos_productos()

    except Exception as e:
        print(f"Error al obtener productos: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al obtener los productos"
        )



@router.get("/{producto_id}")
def obtener_producto(producto_id: int):

    producto = repo.obtener_producto_por_id(producto_id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return producto



@router.post("/")
def crear_producto(producto: ProductoCreate):

    try:
        nuevo_id = repo.crear_producto(producto)

        return {
            "id": nuevo_id,
            "mensaje": "Producto creado exitosamente"
        }

    except Exception as e:
        print(f"Error al crear producto: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    producto: ProductoCreate
):

    exito = repo.actualizar_producto(
        producto_id,
        producto
    )

    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto actualizado correctamente"
    }


# Desactivar un producto
@router.delete("/{producto_id}")
def desactivar_producto(producto_id: int):

    exito = repo.desactivar_producto(producto_id)

    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto desactivado correctamente"
    }
