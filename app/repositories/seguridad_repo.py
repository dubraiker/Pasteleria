
import json

from fastapi import HTTPException, status

from app.core.database import Database
from app.core.security import get_password_hash
from app.models.seguridad import UsuarioCreate


class SeguridadRepository:  
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        """Retorna usuarios activos sin exponer contraseñas."""
        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la BD"
            )

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    u.id,
                    u.id_perfil,
                    u.nombre,
                    u.apellido,
                    u.correo,
                    u.foto_perfil_url,
                    u.estado,
                    u.creado,
                    u.actualizado,
                    p.nombre AS perfil_nombre
                FROM usuario u
                INNER JOIN perfil p ON u.id_perfil = p.id
                WHERE u.estado = TRUE
                ORDER BY u.id ASC;
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            conn.close()

    def obtener_por_id(self, usuario_id: int):
        """Busca un usuario activo por su ID."""
        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la BD"
            )

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    id,
                    id_perfil,
                    nombre,
                    apellido,
                    correo,
                    foto_perfil_url,
                    estado,
                    creado,
                    actualizado
                FROM usuario
                WHERE id = %s AND estado = TRUE;
            """

            cursor.execute(query, (usuario_id,))
            return cursor.fetchone()

        finally:
            conn.close()

    def obtener_por_correo(self, correo: str):
        """Busca un usuario activo para autenticación."""
        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la BD"
            )

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    id,
                    id_perfil,
                    nombre,
                    apellido,
                    correo,
                    password_hash,
                    estado
                FROM usuario
                WHERE correo = %s AND estado = TRUE;
            """

            cursor.execute(query, (correo,))
            return cursor.fetchone()

        finally:
            conn.close()

    def crear(self, usuario: UsuarioCreate):
        """Registra un usuario con contraseña cifrada."""
        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la BD"
            )

        hashed_password = get_password_hash(usuario.password)

        embedding_json = (
            json.dumps(usuario.embedding_facial)
            if usuario.embedding_facial
            else None
        )

        try:
            cursor = conn.cursor()

            query = """
                INSERT INTO usuario (
                    id_perfil,
                    nombre,
                    apellido,
                    correo,
                    password_hash,
                    embedding_facial,
                    foto_perfil_url
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """

            cursor.execute(
                query,
                (
                    usuario.id_perfil,
                    usuario.nombre,
                    usuario.apellido,
                    usuario.correo,
                    hashed_password,
                    embedding_json,
                    usuario.foto_perfil_url
                )
            )

            nuevo_id = cursor.fetchone()["id"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            conn.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al registrar usuario: {str(e)}"
            )

        finally:
            conn.close()

    def desactivar(self, usuario_id: int):
        """Desactiva un usuario mediante borrado lógico."""
        conn = self.db.get_connection()

        if not conn:
            raise HTTPException(
                status_code=500,
                detail="Error de conexión a la BD"
            )

        try:
            cursor = conn.cursor()

            query = """
                UPDATE usuario
                SET estado = FALSE
                WHERE id = %s AND estado = TRUE
                RETURNING id;
            """

            cursor.execute(query, (usuario_id,))
            eliminado = cursor.fetchone()

            conn.commit()

            return eliminado is not None

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
