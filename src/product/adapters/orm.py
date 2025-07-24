"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, String, Table, MetaData
from sqlalchemy.orm import registry

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


mapper_registry = (
    registry()
)  # contains the info about how to map db tables to python models


def start_mappers():
    # Inverting Database Dependency ORM from Domain model
    # Following is the configuration for how to convert between the schema and domain model

    mapper_registry.map_imperatively(
        ProductModel,
        product_aggregate,
    )
