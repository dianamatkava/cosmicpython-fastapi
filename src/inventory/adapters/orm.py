"""Classical (imperative) mapping."""

from sqlalchemy import Column, Integer, String, Table, Date, ForeignKey

from src.adapters.db_metadata import metadata

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


product_aggregate = Table(
    "product_aggregates",
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
        doc="Version number for consistency boundaries",
    ),
)
