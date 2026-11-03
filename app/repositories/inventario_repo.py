from fastapi import HTTPException, status
from app.core.database import Database
from app.models.inventario import ProductoCreate

class InventarioRepository:
    def __init__(self):
       
        self.db = Database()

    def obtener_todos_productos(self):
        """Retorna solo productos activos (Borrado Lógico: estado = True)"""
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error de conexión a la base de datos"
            )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM producto WHERE estado = TRUE ORDER BY id ASC;")
        productos = cursor.fetchall()
        conn.close()
        return productos

    def obtener_producto_por_id(self, producto_id: int):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM producto WHERE id = %s AND estado = TRUE;", (producto_id,))
        producto = cursor.fetchone()
        conn.close()
        return producto

    def crear_producto(self, producto: ProductoCreate):
        """Inserta un nuevo producto en PostgreSQL"""
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        cursor = conn.cursor()
        query = """
            INSERT INTO producto (id_categoria, nombre, descripcion, precio, etiqueta_yolo)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """
        try:
            cursor.execute(query, (
                producto.id_categoria,
                producto.nombre,
                producto.descripcion,
                producto.precio,
                producto.etiqueta_yolo
            ))
            nuevo_id = cursor.fetchone()['id']
            conn.commit()
            conn.close()
            return nuevo_id
        except Exception as e:
            conn.rollback()
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear el producto: {str(e)}"
            )

    def desactivar_producto(self, producto_id: int):
        """Eliminación Lógica: Cambia el campo estado a FALSE"""
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        cursor = conn.cursor()
        query = "UPDATE producto SET estado = FALSE WHERE id = %s RETURNING id;"
        cursor.execute(query, (producto_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None