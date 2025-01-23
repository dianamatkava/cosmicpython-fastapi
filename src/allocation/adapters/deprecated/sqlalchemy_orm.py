"""deprecated"""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    sku = Column(Integer, primary_key=True)
    name = Column(String(250))


class Customer(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    address = Column(String(250))


class Order(Base):
    id = Column(Integer, primary_key=True)
    customer = relationship(Customer)


class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Integer(String(250))
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)


class Batch(Base):
    id = Column(Integer, primary_key=True)
    ref = Column(Integer, primary_key=True)
    product = relationship(Product)
    sku = Column(DateTime(), nullable=True)


