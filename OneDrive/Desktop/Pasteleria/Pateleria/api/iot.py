from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Pateleria.database import get_db

router = APIRouter()

class MetricaLectura(BaseModel):
    sensor_id: str
    temperatura: float
    humedad: float

@router.post("/lecturas")
def registrar_lectura(lectura: MetricaLectura, db: Session = Depends(get_db)):
    alerta = False
    mensaje_alerta = "Condiciones normales"
    
    if lectura.temperatura > 8.0 or lectura.temperatura < 2.0:
        alerta = True
        mensaje_alerta = "¡ALERTA! Temperatura fuera del rango óptimo de conservación (2°C - 8°C)"
        
    return {
        "sensor_id": lectura.sensor_id,
        "temperatura": lectura.temperatura,
        "humedad": lectura.humedad,
        "alerta": alerta,
        "mensaje": mensaje_alerta
    }

@router.get("/estado")
def obtener_estado_sensores(db: Session = Depends(get_db)):
    return {
        "sensor_camara_fria_1": {"temperatura": 4.5, "humedad": 65.0, "estado": "OK"},
        "sensor_exhibidor_1": {"temperatura": 5.2, "humedad": 60.0, "estado": "OK"}
    }