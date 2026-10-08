from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class DispositivoIot(Base):
    __tablename__ = "dispositivo_iot"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    tipo = Column(String)
    activo = Column(Boolean, default=True)

class LecturaSensor(Base):
    __tablename__ = "lectura_sensor"

    id = Column(Integer, primary_key=True, index=True)
    dispositivo_id = Column(Integer, ForeignKey("dispositivo_iot.id"))
    valor = Column(String)
    fecha_lectura = Column(DateTime, default=datetime.utcnow)