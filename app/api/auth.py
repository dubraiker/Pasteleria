from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.repositories.seguridad_repo import SeguridadRepository
from app.core.security import crear_token_acceso, verificar_password

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


MODULOS_POR_PERFIL = {
    1: [ 
        {"nombre": "Usuarios y Roles", "ruta": "/admin/usuarios"},
        {"nombre": "Inventario General", "ruta": "/pastelero/inventario"},
        {"nombre": "Monitoreo IoT", "ruta": "/pastelero/alertas"}
    ],
    2: [  
        {"nombre": "Inventario & YOLO", "ruta": "/pastelero/inventario"},
        {"nombre": "Alertas Cocina", "ruta": "/pastelero/alertas"},
        {"nombre": "Sensores en Vivo", "ruta": "/pastelero/alertas-estado"}
    ],
    3: [  
        {"nombre": "Catálogo de Productos", "ruta": "/cliente/catalogo"},
        {"nombre": "Vitrina Pública", "ruta": "/cliente/catalogo-publico"}
    ]
}

class LoginSchema(BaseModel):
    correo: EmailStr
    password: str

@router.post("/login")
def login(datos: LoginSchema):
    repo = SeguridadRepository()
    usuario = repo.obtener_por_correo(datos.correo)
    
    if not usuario or not verificar_password(datos.password, usuario["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    id_perfil = usuario["id_perfil"]
    token = crear_token_acceso(data={"sub": usuario["correo"], "id_usuario": usuario["id"]})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"],
            "correo": usuario["correo"],
            "id_perfil": id_perfil,
            "modulos": MODULOS_POR_PERFIL.get(id_perfil, [])
        }
    }