"""deprecated"""
#  Declarative Base

from sqlalchemy import Column, Integer, String, Table, MetaData, DateTime

from sqlalchemy.orm import mapper
from src.models.allocation import OrderLineModel, OrderModel, BatchModel, CustomerModel, ProductModel

metadata = MetaData()

customer = Table(
    'customer',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('address', String(255), nullable=False),
    Column('name', String(255), nullable=False),
)

product = Table(
    'product',
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("sku", String(255), unique=True),
)

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('product', Integer, nullable=False),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255))
)

batch = Table(
    'batch',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('product', Integer),
    Column('eta', DateTime, nullable=True)
)


# Inverting Database Dependency from Domain model
# explicit mapper for how to convert between the schema and our domain model,
# what SQLAlchemy calls a classical mapping:
def start_mappers():
    order_lines_mapper = mapper(OrderLineModel, order_lines)
    orders_mapper = mapper(OrderModel, order_lines)
    customer_mapper = mapper(CustomerModel, order_lines)
    product_mapper = mapper(ProductModel, order_lines)
    batch_mapper = mapper(BatchModel, order_lines)

