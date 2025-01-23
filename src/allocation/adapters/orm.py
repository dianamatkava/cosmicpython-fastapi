from sqlalchemy import Column, Integer, String, Table, MetaData, DateTime, ForeignKey
from sqlalchemy.orm import registry, relationship

from src.allocation.domain import model

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
    Column("product_id", ForeignKey("product.id")),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255))
)

batches = Table(
    'batches',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column("product_id", ForeignKey("product.id")),
    Column('eta', DateTime, nullable=True)
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


mapper_registry = registry()

# Inverting Database Dependency from Domain model
# explicit mapper for how to convert between the schema and our domain model,
# what SQLAlchemy calls a classical mapping:

lines_mapper = mapper_registry.map_imperatively(model.OrderLineModel, order_lines)
product_mapper = mapper_registry.map_imperatively(model.ProductModel, product)
mapper_registry.map_imperatively(
    model.BatchModel,
    batches,
    properties={
        "_allocations": relationship(
            lines_mapper,  # Maps to OrderLineModel
            secondary=allocations,  # Through the 'allocations' join table
            collection_class=set,  # Allocations are stored in a set
        ),
    },
)

