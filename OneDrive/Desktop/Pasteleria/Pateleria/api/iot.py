from fastapi import APIRouter, Depends, status
from Pateleria.models.iot_models import LecturaIoT
from sqlalchemy.orm import Session
from Pateleria.database import get_db
from pydantic import BaseModel
from Pateleria.database import get_db
from Pateleria.core.dependencies import requerir_roles
from Pateleria.models.iot_models import LecturaIoT  

router = APIRouter()

class MetricaLectura(BaseModel):
    sensor_id: str
    temperatura: float
    humedad: float


@router.post(
    "/lecturas",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requerir_roles(["administrador", "sensor"]))]
)
def registrar_lectura(lectura: MetricaLectura, db: Session = Depends(get_db)):
    """Registra telemetría IoT, evalúa rangos críticos y guarda en PostgreSQL (Neon DB)."""
    alerta = False
    mensaje_alerta = "Condiciones normales"
    
    if lectura.temperatura > 8.0 or lectura.temperatura < 2.0:
        alerta = True
        mensaje_alerta = "¡ALERTA! Temperatura fuera del rango óptimo de conservación (2°C - 8°C)"
    
    # Crear registro en la base de datos
    nueva_lectura = LecturaIoT(
        sensor_id=lectura.sensor_id,
        temperatura=lectura.temperatura,
        humedad=lectura.humedad,
        alerta=alerta,
        mensaje=mensaje_alerta
    )
    
    db.add(nueva_lectura)
    db.commit()
    db.refresh(nueva_lectura)
    
    return {
        "id": nueva_lectura.id,
        "sensor_id": nueva_lectura.sensor_id,
        "temperatura": nueva_lectura.temperatura,
        "humedad": nueva_lectura.humedad,
        "alerta": nueva_lectura.alerta,
        "mensaje": nueva_lectura.mensaje,
        "creado": nueva_lectura.creado
    }


@router.get("/estado")
def obtener_estado_sensores(db: Session = Depends(get_db)):
    """Obtiene el historial de lecturas de sensores directo desde la base de datos."""
    lecturas = db.query(LecturaIoT).all()
    return lecturas