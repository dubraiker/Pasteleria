from fastapi import FastAPI
from Pateleria.database import engine, Base
from Pateleria.api import auth, iot, productos, vision


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Inteligente de Gestión y Monitoreo de Inventario de Pasteles",
    description="Backend API con integración IoT (Temperatura/Humedad), Visión Artificial e Inventario de Productos.",
    version="1.0.0"
)

# Integración de routers por componentes del parcial
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(productos.router, prefix="/productos", tags=["Inventario y Productos"])
app.include_router(iot.router, prefix="/iot", tags=["Monitoreo IoT"])
app.include_router(vision.router, prefix="/vision", tags=["Visión Artificial"])

@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "sistema": "Sistema Inteligente de Pastelería Activo",
        "documentacion": "/docs"
    }