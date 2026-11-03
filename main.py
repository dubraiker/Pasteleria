from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación directa de los módulos de la carpeta app/api
from app.api import rutas_inventario, rutas_seguridad, rutas_iot
from app.api import auth  # Asegúrate de que el archivo exista en app/api/auth.py

app = FastAPI(
    title="API Sistema Inteligente de Pastelería & Seguridad IoT",
    description="Backend modular para monitoreo ambiental, conteo automatizado mediante YOLO y control facial",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Integración de routers modulares
app.include_router(auth.router, prefix="/api")
app.include_router(rutas_inventario.router, prefix="/api")
app.include_router(rutas_seguridad.router, prefix="/api")
app.include_router(rutas_iot.router, prefix="/api")

@app.get("/")
def estado_api():
    return {"mensaje": "La API del sistema se encuentra en línea y funcional"}