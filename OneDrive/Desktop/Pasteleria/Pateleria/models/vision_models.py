from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Pateleria.database import Base

class CamaraIA(Base):
    __tablename__ = "camaras_ia"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    ubicacion = Column(String)
    estado = Column(String, default="activa")

    detecciones = relationship("DeteccionConteo", back_populates="camara")

class DeteccionConteo(Base):
    __tablename__ = "detecciones_conteo"

    id = Column(Integer, primary_key=True, index=True)
    camara_id = Column(Integer, ForeignKey("camaras_ia.id"))
    producto_detectado = Column(String)
    cantidad_detectada = Column(Integer)
    nivel_confianza = Column(Float)
    fecha_deteccion = Column(DateTime, default=datetime.utcnow)

    camara = relationship("CamaraIA", back_populates="detecciones")