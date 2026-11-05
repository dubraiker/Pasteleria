from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.models.seguridad import UsuarioCreate, UsuarioResponse, UsuarioRegistroCliente
from app.repositories.seguridad_repo import SeguridadRepository
from app.core.database import get_db

router = APIRouter(prefix="/usuarios", tags=["Gestión de Usuarios y Seguridad"])
repo = SeguridadRepository()

class UsuarioUpdateSchema(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    id_perfil: int
    estado: Optional[bool] = True

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_cliente(datos: UsuarioRegistroCliente):
    usuario_dto = UsuarioCreate(
        id_perfil=3,
        nombre=datos.nombre,
        apellido=datos.apellido,
        correo=datos.correo,
        password=datos.password
    )
    nuevo_id = repo.crear(usuario_dto)
    return {"mensaje": "Cuenta de cliente creada exitosamente", "id": nuevo_id}

@router.post("/admin/crear", status_code=status.HTTP_201_CREATED)
def crear_usuario_administrativo(usuario: UsuarioCreate):
    nuevo_id = repo.crear(usuario)
    return {"mensaje": "Usuario registrado exitosamente por el administrador", "id": nuevo_id}

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios():
    return repo.obtener_todos()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int):
    usuario = repo.obtener_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdateSchema, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM usuario WHERE id = %s", (usuario_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cursor.execute("""
        UPDATE usuario 
        SET nombre = %s, apellido = %s, correo = %s, id_perfil = %s, estado = %s
        WHERE id = %s
    """, (datos.nombre, datos.apellido, datos.correo, datos.id_perfil, datos.estado, usuario_id))
    db.commit()
    return {"mensaje": "Usuario actualizado correctamente"}

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    exito = repo.desactivar(usuario_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario desactivado correctamente (Borrado Lógico)"}

