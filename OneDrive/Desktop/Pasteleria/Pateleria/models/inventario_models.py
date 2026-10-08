from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)

class Producto(Base):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)
    precio = Column(Integer)
    categoria_id = Column(Integer, ForeignKey("categoria.id"))
    activo = Column(Boolean, default=True)

class LoteInventario(Base):
    __tablename__ = "lote_inventario"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("producto.id"))
    cantidad = Column(Integer)
    fecha_vencimiento = Column(DateTime)