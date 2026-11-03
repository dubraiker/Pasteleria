from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.core.database import Database
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class LoginRequest(BaseModel):
    correo: EmailStr
    password: str

@router.post("/login")
def login(datos: LoginRequest):
    db = Database()
    conn = db.get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión a la BD")
    
    cursor = conn.cursor()
    query = """
        SELECT u.id, u.correo, u.password_hash, u.estado, p.nombre as rol
        FROM usuario u
        JOIN perfil p ON u.id_perfil = p.id
        WHERE u.correo = %s AND u.estado = TRUE;
    """
    cursor.execute(query, (datos.correo,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario or not verify_password(datos.password, usuario["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    # Token JWT con ID, correo y ROL
    access_token = create_access_token(
        data={"sub": str(usuario["id"]), "correo": usuario["correo"], "rol": usuario["rol"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario["id"],
            "correo": usuario["correo"],
            "rol": usuario["rol"]
        }
    }