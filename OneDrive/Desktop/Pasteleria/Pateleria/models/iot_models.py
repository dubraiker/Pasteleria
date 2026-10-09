from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from Pateleria.database import Base

class LecturaIoT(Base):
    __tablename__ = "lecturas_iot"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, nullable=False)
    temperatura = Column(Float, nullable=False)
    humedad = Column(Float, nullable=False)
    alerta = Column(Boolean, default=False)
    mensaje = Column(String, nullable=True)
    creado = Column(DateTime, default=datetime.utcnow)
    actualizado = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)