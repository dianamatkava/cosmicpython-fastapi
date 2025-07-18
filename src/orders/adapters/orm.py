"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, String, Table, MetaData
from sqlalchemy.orm import registry

from src.orders.domain import order_line_model as domain

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String(255)),
    Column("sku", String(255), doc="Reference to an product"),
    Column("qty", Integer, nullable=False),
)


mapper_registry = (
    registry()
)  # contains the info about how to map db tables to python models


def start_mappers():
    # Inverting Database Dependency ORM from Domain model
    # Following is the configuration for how to convert between the schema and domain model

    mapper_registry.map_imperatively(domain.OrderLineModel, order_lines)
