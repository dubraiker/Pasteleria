from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from Pateleria.core.security import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

def requerir_roles(roles_permitidos: list[str]):
    """Dependencia para validar si el rol del usuario tiene permiso."""
    def verificador_rol(usuario_actual: dict = Depends(obtener_usuario_actual)):
        rol_usuario = usuario_actual.get("rol")
        if rol_usuario not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: Se requiere alguno de estos roles {roles_permitidos}"
            )
        return usuario_actual
    return verificador_rol