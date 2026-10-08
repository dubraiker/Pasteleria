from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Pateleria.database import get_db
from Pateleria.schemas.auth_schemas import UsuarioCreate, UsuarioLogin, TokenResponse
from Pateleria.core.security import obtener_password_hash, verificar_password, crear_access_token

router = APIRouter()

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return {
        "mensaje": "Usuario registrado exitosamente",
        "email": usuario.email,
        "rol": usuario.rol
    }

@router.post("/login", response_model=TokenResponse)
def login_usuario(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    # Simulación de verificación para login
    token = crear_access_token(data={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}