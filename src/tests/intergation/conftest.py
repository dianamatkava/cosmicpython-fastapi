import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, clear_mappers, Session
from sqlalchemy_utils import database_exists, create_database
from starlette.testclient import TestClient

from src.adapters.orm import metadata, start_mappers
from src.adapters.repository import BatchRepository, AbstractRepository
from src.adapters.uow import UnitOfWork
from src.app import app
from src.services.batch_service import BatchService
from src.settings import get_settings

settings = get_settings()


@pytest.fixture(scope="session")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")  # in memory db, or sqlite://
    # create all tables
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def session(in_memory_db: Engine):
    start_mappers()
    connection = in_memory_db.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    clear_mappers()
