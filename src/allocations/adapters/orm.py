"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, Table, MetaData, ForeignKey
from sqlalchemy.orm import registry, relationship

from src.allocations.domain import OrderLineModel
from src.allocations.domain.batch_domain_model import BatchModel
from src.inventory.adapters.orm import batches
from src.orders.adapters.orm import order_lines

metadata = MetaData()

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id"), unique=True),
    Column("batch_id", ForeignKey("batches.id")),
)


mapper_registry = (
    registry()
)  # contains the info about how to map db tables to python models


def start_mappers():
    # Inverting Database Dependency ORM from Domain model
    # Following is the configuration for how to convert between the schema and domain model
    lines_mapper = mapper_registry.map_imperatively(OrderLineModel, order_lines)
    mapper_registry.map_imperatively(
        BatchModel,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,  # Maps to OrderLineModel
                secondary=allocations,  # Through the 'allocations' join table
                collection_class=set,  # Allocations are stored in a set
            ),
        },
    )
