from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from passlib.exc import UnknownHashError

#
from app.core.database import get_db
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str


@router.post("/login")
def login(datos: LoginRequest, db=Depends(get_db)):
    cursor = db.cursor()
    correo_limpio = datos.correo.lower().strip()

    
    cursor.execute(
        """
        SELECT u.id, u.nombre, u.apellido, u.correo, u.password_hash, u.id_perfil, u.estado,
               p.nombre AS nombre_perfil
        FROM usuario u
        INNER JOIN perfil p ON u.id_perfil = p.id
        WHERE LOWER(u.correo) = %s AND u.estado = TRUE
    """,
        (correo_limpio,),
    )

    usuario = cursor.fetchone()

    # 2. Validar existencia del usuario
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o cuenta inactiva",
        )

   
    try:
        es_valida = verify_password(datos.password, usuario["password_hash"])
    except UnknownHashError:
        es_valida = False

    if not es_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o cuenta inactiva",
        )

    
    cursor.execute(
        """
        SELECT m.nombre, m.ruta, m.icono
        FROM modulos m
        INNER JOIN modulos_x_rol mxr ON m.id = mxr.id_modulo
        WHERE mxr.id_rol = %s AND mxr.estado = TRUE AND m.estado = TRUE
    """,
        (usuario["id_perfil"],),
    )

    modulos_usuario = cursor.fetchall()

   
    token_jwt = create_access_token({"sub": usuario["correo"]})

    return {
        "access_token": token_jwt,
        "token_type": "bearer",
        "usuario": {
            "id": usuario["id"],
            "nombre": f"{usuario['nombre']} {usuario['apellido']}",
            "correo": usuario["correo"],
            "rol": usuario["nombre_perfil"],
            "modulos": modulos_usuario,
        },
    }