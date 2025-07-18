"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, String, Table, MetaData, Date, ForeignKey
from sqlalchemy.orm import registry, relationship
from src.allocations.domain import batch_domain_model as domain

metadata = MetaData()

product_aggregate = Table(
    "product_aggregates",
    metadata,
    Column(
        "sku",
        String(255),
        primary_key=True,
        doc="Product identifier assigned by vendor, manufacturer, or ERP",
    ),
    Column("version_number", Integer, doc="Version number for consistency boundaries"),
)


order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String(255)),
    Column("sku", String(255), doc="Reference to an product"),
    Column("qty", Integer, nullable=False),
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
    Column("sku", ForeignKey("product_aggregates.sku"), doc="Reference to a product"),
    Column(
        "eta",
        Date,
        nullable=True,
        doc="Batches have an ETA if they are currently shipping",
    ),
    Column("_purchased_quantity", Integer, nullable=False, doc="Total quantity"),
)

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

    lines_mapper = mapper_registry.map_imperatively(domain.OrderLineModel, order_lines)
    batch_mapper = mapper_registry.map_imperatively(
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

    mapper_registry.map_imperatively(
        domain.ProductAggregate,
        product_aggregate,
        properties={
            "_batches": relationship(
                batch_mapper,  # Maps to BatchModel
                back_populates="batches",  # Through the 'batches' join table
                collection_class=set,  # Batches are stored in a set
            ),
        },
    )
