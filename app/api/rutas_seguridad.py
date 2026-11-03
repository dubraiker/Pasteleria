from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.seguridad import UsuarioCreate, UsuarioResponse, UsuarioRegistroCliente
from app.repositories.seguridad_repo import UsuarioRepository

router = APIRouter(prefix="/usuarios", tags=["Gestión de Usuarios y Seguridad"])
repo = UsuarioRepository()

# 1. Endpoint Público para Clientes (id_perfil = 3 automático)
@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_cliente(datos: UsuarioRegistroCliente):
    usuario_dto = UsuarioCreate(
        id_perfil=3,  # Se asigna automáticamente el rol Cliente
        nombre=datos.nombre,
        apellido=datos.apellido,
        correo=datos.correo,
        password=datos.password
    )
    nuevo_id = repo.crear(usuario_dto)
    return {"mensaje": "Cuenta de cliente creada exitosamente", "id": nuevo_id}

# 2. Endpoint Administrativo para crear cualquier tipo de Usuario (Admin/Pastelero/Cliente)
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

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    exito = repo.desactivar(usuario_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario desactivado correctamente (Borrado Lógico)"}