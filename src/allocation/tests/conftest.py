import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from src.allocation.adapters.orm import metadata
from src.allocation.adapters.repository import SqlAlchemyRepository
from src.allocation.services.batch_service import BatchService


@pytest.fixture()
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture(name='batch_service')
def get_batch_service():
    return BatchService()


@pytest.fixture(name="sql_repository")
def get_sql_repository(session):
    return SqlAlchemyRepository(session)

