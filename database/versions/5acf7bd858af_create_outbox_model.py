"""Create outbox model

Revision ID: 5acf7bd858af
Revises: ae142dca3487
Create Date: 2025-10-04 15:21:46.388932

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5acf7bd858af"
down_revision: Union[str, None] = "ae142dca3487"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define your constraint SQL here
OUTBOX_STATUS_VALUES = "'NEW', 'SENT', 'FAILED', 'ARCHIVED'"
OUTBOX_STATUS_CONSTRAINT_SQL = f"status IN ({OUTBOX_STATUS_VALUES})"

CHECK_SQL = "ALTER TABLE outbox ADD CONSTRAINT ck_outbox_status_valid CHECK (status IN ('NEW', 'SENT', 'FAILED', 'ARCHIVED'))"


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("ck_outbox_status_valid", "outbox", type_="check")
    op.execute(CHECK_SQL)


def downgrade() -> None:
    """Downgrade schema (revert to previous constraint state)."""
    op.drop_constraint("ck_outbox_status_valid", "outbox", type_="check")
