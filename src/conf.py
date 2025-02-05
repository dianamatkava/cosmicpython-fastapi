from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from src.adapters.repository import BatchRepository
from src.services.batch_service import BatchService

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_batch_service(session: Session) -> BatchService:
    return BatchService(
        session=session,
        batch_repository=BatchRepository(session)
    )


