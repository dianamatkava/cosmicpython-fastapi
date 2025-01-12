import os

import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from cruds.product_crud import ProductCrud
from services.batch_service import BatchService


@pytest.fixture(scope="session")
def engine():
    sqlite_file_name = "database.testing.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=True)

    yield engine

    SQLModel.metadata.drop_all(engine)
    if os.path.exists(sqlite_file_name):  # Delete the SQLite file
        os.remove(sqlite_file_name)


@pytest.fixture(scope="session", autouse=True)
def setup_database(engine):
    SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="function")
def session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name='batch_service')
def get_batch_service():
    return BatchService()


@pytest.fixture(name="product_crud")
def get_product_crud(session):
    return ProductCrud(session)

