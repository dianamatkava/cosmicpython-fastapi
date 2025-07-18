"""Declarative mapping."""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, registry, DeclarativeBase

# Base = declarative_base()  # implicitly creates a registry() behind the scenes, return DeclarativeBase class


reg = registry()


# Modern way, explicitly create and manage the registry
class Base(DeclarativeBase):
    registry = reg


# @mapper_registry.mapped
# class Product:
class Product(Base):
    __tablename__ = "product"

    sku = Column(Integer, primary_key=True)
    version_number = Column(Integer)


class OrderLine(Base):
    __tablename__ = "order_line"

    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Integer(String(250))
    order_id = Column(Integer, ForeignKey("order.id"))


class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer, primary_key=True)
    ref = Column(Integer, primary_key=True)
    product = relationship(Product)
    sku = Column(DateTime(), nullable=True)
