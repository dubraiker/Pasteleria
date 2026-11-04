from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.database import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

class UsuarioUpdateSchema(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    id_perfil: int
    estado: bool

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