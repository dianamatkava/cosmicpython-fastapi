from enum import StrEnum

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    JSON,
    CheckConstraint,
    DateTime,
    func,
)

from src.database.metadata import metadata


class OutboxStatus(StrEnum):
    NEW = "NEW"
    SENT = "SENT"
    FAILED = "FAILED"


OUTBOX_STATUS_VALUES = ", ".join([f"'{v}'" for v in [e.value for e in OutboxStatus]])
OUTBOX_STATUS_CONSTRAINT_SQL = f"status IN ({OUTBOX_STATUS_VALUES})"


outbox = Table(
    "outbox",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("aggregate_type", String(255), nullable=False),  # Order, Allocation
    Column(
        "aggregate_id",
        String(255),
        nullable=False,
        doc="ID of the entity that generated the event",
    ),
    Column("routing_key", String(255), nullable=False),
    Column("body", JSON),
    Column("retry_count", Integer, nullable=False, default=0),
    Column("status", String(50), nullable=False, default=OutboxStatus.NEW),
    Column("created_at", DateTime, nullable=False, default=func.now()),
    CheckConstraint(OUTBOX_STATUS_CONSTRAINT_SQL, name="ck_outbox_status_valid"),
)
