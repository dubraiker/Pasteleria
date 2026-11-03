from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- DISPOSITIVO IOT (ESP32) ---
class DispositivoIoTBase(BaseModel):
    nombre: str
    codigo_mac: str
    ubicacion: str

class DispositivoIoTCreate(DispositivoIoTBase):
    pass

class DispositivoIoTResponse(DispositivoIoTBase):
    id: int
    estado_conexion: bool
    estado: bool
    creado: datetime
    actualizado: datetime

    class Config:
        from_attributes = True

# --- LECTURA DE SENSORES (DHT22 / PIR) ---
class LecturaSensorCreate(BaseModel):
    id_dispositivo: int
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    movimiento_detectado: Optional[bool] = False

class LecturaSensorResponse(LecturaSensorCreate):
    id: int
    estado: bool
    creado: datetime
    actualizado: datetime

    class Config:
        from_attributes = True

# --- ALERTAS DE EMERGENCIA ---
class AlertaEmergenciaCreate(BaseModel):
    id_dispositivo: int
    id_tipo_alerta: int
    mensaje: str

class AlertaEmergenciaResponse(BaseModel):
    id: int
    id_dispositivo: int
    id_tipo_alerta: int
    id_usuario_atencion: Optional[int] = None
    mensaje: str
    atendida: bool
    fecha_atencion: Optional[datetime] = None
    dispositivo_nombre: Optional[str] = None
    tipo_alerta_nombre: Optional[str] = None
    nivel_riesgo: Optional[str] = None
    creado: datetime

    class Config:
        from_attributes = True