from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from Pateleria.database import get_db
from Pateleria.schemas.auth_schemas import UsuarioCreate, TokenResponse
from Pateleria.core.security import obtener_password_hash, verificar_password, crear_access_token
from Pateleria.models.auth_models import Usuario
from Pateleria.core.dependencies import requerir_roles

router = APIRouter()


@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya se encuentra registrado."
        )

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password_hash=obtener_password_hash(usuario.password),
        rol=usuario.rol
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario registrado exitosamente en la base de datos",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "rol": nuevo_usuario.rol
    }


@router.post("/login", response_model=TokenResponse)
def login_usuario(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Permite autenticarse enviando el usuario/correo y contraseña desde el formulario de Swagger o cliente OAuth2."""
    # En Swagger, el correo ingresado llega en form_data.username
    db_usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not db_usuario or not verificar_password(form_data.password, db_usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = crear_access_token(data={"sub": db_usuario.email, "rol": db_usuario.rol})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/usuarios", dependencies=[Depends(requerir_roles(["administrador"]))])
def listar_usuarios(db: Session = Depends(get_db)):
    """Lista todos los usuarios registrados (Solo accesible por administradores)"""
    usuarios = db.query(Usuario).all()
    return [
        {
            "id": u.id,
            "nombre": u.nombre,
            "email": u.email,
            "rol": u.rol,
            "creado": u.creado
        } for u in usuarios
    ]