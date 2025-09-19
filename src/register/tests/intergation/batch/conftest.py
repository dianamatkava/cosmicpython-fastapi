import pytest
from sqlalchemy.orm import Session

from src.register.adapters.repositories.batch_repository import BatchRepository


@pytest.fixture(name="batch_repository")
def get_batch_repository(session: Session) -> BatchRepository:
    return BatchRepository(session)
