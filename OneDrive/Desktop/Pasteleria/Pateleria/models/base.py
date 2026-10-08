from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class Base:
    id = Column(Integer, primary_key=True, index=True)
    estado = Column(Boolean, default=True)
    creado = Column(DateTime, default=datetime.utcnow)
    actualizado = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)