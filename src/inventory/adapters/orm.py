"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, String, Table, MetaData, Date, ForeignKey
from sqlalchemy.orm import registry

from src.allocations.domain import batch_domain_model as domain

metadata = MetaData()


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
    Column("sku", ForeignKey("product_aggregates.sku"), doc="Reference to a product"),
    Column(
        "eta",
        Date,
        nullable=True,
        doc="Batches have an ETA if they are currently shipping",
    ),
    Column("_purchased_quantity", Integer, nullable=False, doc="Total quantity"),
)


mapper_registry = (
    registry()
)  # contains the info about how to map db tables to python models


def start_mappers():
    # Inverting Database Dependency ORM from Domain model
    # Following is the configuration for how to convert between the schema and domain model

    mapper_registry.map_imperatively(
        domain.BatchModel,
        batches,
    )
