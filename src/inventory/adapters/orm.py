"""Classical (imperative) mapping."""

from enum import StrEnum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Date,
    ForeignKey,
    Boolean,
    CheckConstraint,
)

from src.database.metadata import metadata


class UnitOfMeasure(StrEnum):
    """
    Defines the valid units of measure for a product.
    Using (str, Enum) allows string-like comparison and serialization.
    """

    EACH = "EACH"
    KG = "KG"
    BOX = "BOX"
    LITER = "LITER"


UOM_VALUES = [e.value for e in UnitOfMeasure]
quoted_values_list = ", ".join([f"'{v}'" for v in UOM_VALUES])
UOM_CONSTRAINT_SQL = f"unit_of_measure IN ({quoted_values_list})"


allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", ForeignKey("order_lines.id"), unique=True),
    Column("batch_id", ForeignKey("batches.id")),
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
    Column("sku", ForeignKey("product.sku"), doc="Reference to a product"),
    Column(
        "eta",
        Date,
        nullable=True,
        doc="Batches have an ETA if they are currently shipping",
    ),
    Column("_purchased_quantity", Integer, nullable=False, doc="Total quantity"),
)


product = Table(
    "product",
    metadata,
    Column(
        "sku",
        String(255),
        primary_key=True,
        doc="Product identifier assigned by vendor, manufacturer, or ERP",
    ),
    Column(
        "version_number",
        Integer,
        default=0,
        doc="Version number (fence token) for OCC",
    ),
    Column("name", String(255), nullable=False),
    Column("unit_of_measure", String(50), nullable=False),
    Column("is_active", Boolean, default=False),
    CheckConstraint(UOM_CONSTRAINT_SQL, name="ck_product_unit_of_measure_valid"),
)
