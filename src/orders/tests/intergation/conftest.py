import pytest
from sqlalchemy.orm import Session

from src.orders.adapters.repository import OrderLineRepository


@pytest.fixture(name="order_line_repository")
def get_product_repository(session: Session) -> OrderLineRepository:
    return OrderLineRepository(session)
