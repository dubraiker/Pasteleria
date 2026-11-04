from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.repositories.seguridad_repo import SeguridadRepository
from app.core.security import crear_token_acceso, verificar_password, obtener_password_hash

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

class LoginSchema(BaseModel):
    correo: EmailStr
    password: str

class RegistroSchema(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    password: str
    id_rol: int = 3  # Rol por defecto: Cliente

@router.post("/login")
def login(datos: LoginSchema):
    repo = SeguridadRepository()
    usuario = repo.obtener_usuario_por_correo(datos.correo)
    
    if not usuario or not verificar_password(datos.password, usuario["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    token = crear_token_acceso(data={"sub": usuario["correo"], "id_usuario": usuario["id_usuario"]})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario
    }

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_cliente(datos: RegistroSchema):
    repo = SeguridadRepository()
    
    # Verificar si el correo ya existe
    if repo.obtener_usuario_por_correo(datos.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya se encuentra registrado"
        )
    
    password_hash = obtener_password_hash(datos.password)
    nuevo_usuario = repo.crear_usuario(
        nombre=datos.nombre,
        apellido=datos.apellido,
        correo=datos.correo,
        password_hash=password_hash,
        id_rol=datos.id_rol
    )
    
    return {"mensaje": "Usuario registrado exitosamente", "usuario": nuevo_usuario}