import json
from fastapi import HTTPException, status
from app.core.database import Database
from app.core.security import get_password_hash
from app.models.seguridad import UsuarioCreate, UsuarioUpdate

class UsuarioRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        """Retorna solo usuarios activos (Borrado Lógico) sin expone la contraseña"""
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        cursor = conn.cursor()
        query = """
            SELECT u.id, u.id_perfil, u.nombre, u.apellido, u.correo, 
                   u.foto_perfil_url, u.estado, u.creado, u.actualizado,
                   p.nombre as perfil_nombre
            FROM usuario u
            JOIN perfil p ON u.id_perfil = p.id
            WHERE u.estado = TRUE
            ORDER BY u.id ASC;
        """
        cursor.execute(query)
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def obtener_por_id(self, usuario_id: int):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        cursor = conn.cursor()
        query = """
            SELECT id, id_perfil, nombre, apellido, correo, foto_perfil_url, estado, creado, actualizado
            FROM usuario
            WHERE id = %s AND estado = TRUE;
        """
        cursor.execute(query, (usuario_id,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def crear(self, usuario: UsuarioCreate):
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        
        # Encriptar la contraseña antes de guardarla
        hashed_password = get_password_hash(usuario.password)
        
        # Convertir el vector facial a JSONB si está presente
        embedding_json = json.dumps(usuario.embedding_facial) if usuario.embedding_facial else None

        cursor = conn.cursor()
        query = """
            INSERT INTO usuario (id_perfil, nombre, apellido, correo, password_hash, embedding_facial, foto_perfil_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        try:
            cursor.execute(query, (
                usuario.id_perfil,
                usuario.nombre,
                usuario.apellido,
                usuario.correo,
                hashed_password,
                embedding_json,
                usuario.foto_perfil_url
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
                detail=f"Error al registrar usuario (verifique si el correo ya existe): {str(e)}"
            )

    def desactivar(self, usuario_id: int):
        """Borrado Lógico: Cambia estado a FALSE"""
        conn = self.db.get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la BD")
        cursor = conn.cursor()
        query = "UPDATE usuario SET estado = FALSE WHERE id = %s RETURNING id;"
        cursor.execute(query, (usuario_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None