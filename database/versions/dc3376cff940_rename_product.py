"""rename product

Revision ID: dc3376cff940
Revises: d20d049c31a3
Create Date: 2025-09-13 18:08:23.606205

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "dc3376cff940"
down_revision: Union[str, None] = "d20d049c31a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
