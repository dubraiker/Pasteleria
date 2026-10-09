from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from Pateleria.database import Base

class Producto(Base):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)
    categoria_id = Column(Integer, nullable=True)
    estado = Column(Boolean, default=True)
    creado = Column(DateTime, default=datetime.utcnow)
    actualizado = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)