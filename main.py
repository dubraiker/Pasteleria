from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.rutas_inventario import router as inventario_router
from app.api.rutas_iot import router as iot_router
from app.api.rutas_seguridad import router as seguridad_router

app = FastAPI(
    title="API Sistema de Gestión - Pastelería IoT",
    version="1.0.0"
)


origins = [
    "http://localhost:4200",     
    "https://pasteleria-fronted.vercel.app",   
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.include_router(
    seguridad_router,
    prefix="/api"
)

app.include_router(
    inventario_router,
    prefix="/api"
)

app.include_router(iot_router)