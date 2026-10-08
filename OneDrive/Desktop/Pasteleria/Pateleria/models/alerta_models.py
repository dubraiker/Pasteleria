from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Alerta(Base):
    __tablename__ = "alerta"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    mensaje = Column(String)
    tipo = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    resolvida = Column(Boolean, default=False)