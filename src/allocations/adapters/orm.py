"""Classical mapping."""

from sqlalchemy import Column, Integer, String, Table, MetaData, Date, ForeignKey
from sqlalchemy.orm import registry, relationship
from src.allocations.domain import batch_domain_model as domain

metadata = MetaData()

product = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "sku", String(255), unique=True, doc="Assigned by vendor, manufacturer, or ERP"
    ),
)

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("order_id", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "reference",
        String(255),
        unique=True,
        doc="Purchasing team (upstream ERP/PO system) assigns a batch/PO-number",
    ),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id"), unique=True),
    Column("batch_id", ForeignKey("batches.id")),
)


mapper_registry = registry()


def start_mappers():
    # Inverting Database Dependency from Domain model
    # explicit mapper for how to convert between the schema and our domain model,
    # what SQLAlchemy calls a classical mapping:

    lines_mapper = mapper_registry.map_imperatively(domain.OrderLineModel, order_lines)
    mapper_registry.map_imperatively(
        domain.BatchModel,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,  # Maps to OrderLineModel
                secondary=allocations,  # Through the 'allocations' join table
                collection_class=set,  # Allocations are stored in a set
            ),
        },
    )
