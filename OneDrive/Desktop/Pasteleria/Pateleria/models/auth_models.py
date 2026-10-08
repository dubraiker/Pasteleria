from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nombre = Column(String)
    password_hash = Column(String)
    rol = Column(String)
    activo = Column(Boolean, default=True)

class Perfil(Base):
    __tablename__ = "perfil"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    descripcion = Column(String)

class Modulo(Base):
    __tablename__ = "modulo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)

class ModulosXRol(Base):
    __tablename__ = "modulosxrol"

    id = Column(Integer, primary_key=True, index=True)
    modulo_id = Column(Integer, ForeignKey("modulo.id"))
    rol = Column(String)