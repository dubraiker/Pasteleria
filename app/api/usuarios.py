from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.core.database import get_db

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

class UsuarioUpdateSchema(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    id_perfil: int
    estado: bool

# 1. Endpoint GET para obtener la lista de usuarios (FALTABA ÉSTE)
@router.get("/")
def listar_usuarios(db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            u.id, 
            u.nombre, 
            u.apellido, 
            u.correo, 
            u.id_perfil, 
            p.nombre AS perfil_nombre, 
            u.estado AS activo
        FROM usuario u
        LEFT JOIN perfil p ON u.id_perfil = p.id
        ORDER BY u.id ASC
    """)
    filas = cursor.fetchall()
    
    # Si el cursor retorna tuplas, las mapeamos a diccionarios
    usuarios = []
    for fila in filas:
        if isinstance(fila, dict):
            usuarios.append(fila)
        else:
            usuarios.append({
                "id": fila[0],
                "nombre": fila[1],
                "apellido": fila[2],
                "correo": fila[3],
                "id_perfil": fila[4],
                "perfil_nombre": fila[5],
                "activo": fila[6]
            })
            
    return usuarios

# 2. Endpoint PUT para actualizar usuario
@router.put("/{id_usuario}")
def actualizar_usuario(id_usuario: int, datos: UsuarioUpdateSchema, db = Depends(get_db)):
    cursor = db.cursor()
    
    # Validar que el usuario exista
    cursor.execute("SELECT id FROM usuario WHERE id = %s", (id_usuario,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar en la base de datos
    cursor.execute("""
        UPDATE usuario 
        SET nombre = %s,
            apellido = %s,
            correo = %s,
            id_perfil = %s,
            estado = %s
        WHERE id = %s
    """, (datos.nombre, datos.apellido, datos.correo, datos.id_perfil, datos.estado, id_usuario))
    
    db.commit()
    return {"mensaje": "Usuario actualizado correctamente"}