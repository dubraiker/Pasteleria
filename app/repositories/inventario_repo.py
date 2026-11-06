
from fastapi import HTTPException, status

from app.core.database import Database
from app.models.inventario import ProductoCreate


class InventarioRepository:

    def __init__(self):
        self.db = Database()

    # Obtener todos los productos activos
    def obtener_todos_productos(self):

        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la base de datos"
            )

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM producto
                WHERE estado = TRUE
                ORDER BY id ASC;
            """)

            productos = cursor.fetchall()

            return productos

        finally:
            conn.close()

    # Obtener producto por ID
    def obtener_producto_por_id(self, producto_id: int):

        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la base de datos"
            )

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM producto
                WHERE id = %s AND estado = TRUE;
            """, (producto_id,))

            producto = cursor.fetchone()

            return producto

        finally:
            conn.close()

    # Crear producto
    def crear_producto(self, producto: ProductoCreate):

        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la base de datos"
            )

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO producto (
                    id_categoria,
                    nombre,
                    descripcion,
                    precio,
                    etiqueta_yolo
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                producto.id_categoria,
                producto.nombre,
                producto.descripcion,
                producto.precio,
                producto.etiqueta_yolo
            ))

            nuevo_id = cursor.fetchone()['id']

            conn.commit()

            return nuevo_id

        except Exception as e:

            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail=f"Error al crear el producto: {str(e)}"
            )

        finally:
            conn.close()

    # Actualizar producto
    def actualizar_producto(
        self,
        producto_id: int,
        producto: ProductoCreate
    ):

        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la base de datos"
            )

        try:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE producto
                SET
                    id_categoria = %s,
                    nombre = %s,
                    descripcion = %s,
                    precio = %s,
                    etiqueta_yolo = %s
                WHERE id = %s AND estado = TRUE
                RETURNING id;
            """, (
                producto.id_categoria,
                producto.nombre,
                producto.descripcion,
                producto.precio,
                producto.etiqueta_yolo,
                producto_id
            ))

            actualizado = cursor.fetchone()

            if actualizado is None:
                conn.rollback()
                return False

            conn.commit()

            return True

        except Exception as e:

            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail=f"Error al actualizar el producto: {str(e)}"
            )

        finally:
            conn.close()

    # Desactivar producto
    def desactivar_producto(self, producto_id: int):

        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la base de datos"
            )

        try:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE producto
                SET estado = FALSE
                WHERE id = %s AND estado = TRUE
                RETURNING id;
            """, (producto_id,))

            eliminado = cursor.fetchone()

            if eliminado is None:
                conn.rollback()
                return False

            conn.commit()

            return True

        except Exception as e:

            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail=f"Error al desactivar el producto: {str(e)}"
            )

        finally:
            conn.close()
