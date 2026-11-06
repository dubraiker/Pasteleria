from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.iot import (
    DispositivoIoTCreate, DispositivoIoTResponse,
    LecturaSensorCreate, LecturaSensorResponse,
    AlertaEmergenciaCreate, AlertaEmergenciaResponse
)
from app.repositories.iot_repo import IoTRepository

router = APIRouter(prefix="/api/iot", tags=["IoT & Alertas"])
repo = IoTRepository()

# --- DISPOSITIVOS ESP32 ---
@router.post("/dispositivos", status_code=status.HTTP_201_CREATED)
def registrar_dispositivo(dispositivo: DispositivoIoTCreate):
    nuevo_id = repo.registrar_dispositivo(dispositivo)
    return {"mensaje": "Dispositivo registrado con éxito", "id": nuevo_id}

@router.get("/dispositivos", response_model=List[DispositivoIoTResponse])
def listar_dispositivos():
    return repo.listar_dispositivos()

# --- TELEMETRÍA DE SENSORES ---
@router.post("/telemetria", status_code=status.HTTP_201_CREATED)
def registrar_telemetria(lectura: LecturaSensorCreate):
    nuevo_id = repo.registrar_lectura(lectura)
    return {"mensaje": "Lectura de sensor registrada", "id": nuevo_id}

@router.get("/dispositivos/{id_dispositivo}/lecturas", response_model=List[LecturaSensorResponse])
def consultar_lecturas_dispositivo(id_dispositivo: int, limite: int = 10):
    return repo.obtener_ultimas_lecturas(id_dispositivo, limite)

# --- ALERTAS DE EMERGENCIA ---
@router.post("/alertas", status_code=status.HTTP_201_CREATED)
def registrar_alerta(alerta: AlertaEmergenciaCreate):
    nuevo_id = repo.crear_alerta(alerta)
    return {"mensaje": "Alerta de emergencia registrada", "id": nuevo_id}

@router.get("/alertas/pendientes", response_model=List[AlertaEmergenciaResponse])
def listar_alertas_pendientes():
    return repo.obtener_alertas_pendientes()

@router.put("/alertas/{alerta_id}/atender")
def atender_alerta(alerta_id: int, id_usuario: int):
    exito = repo.atender_alerta(alerta_id, id_usuario)
    if not exito:
        raise HTTPException(status_code=404, detail="Alerta no encontrada o ya atendida")
    return {"mensaje": "Alerta marcada como atendida exitosamente"}