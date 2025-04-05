from typing import Annotated, Any

from fastapi import Depends
from sqlmodel import SQLModel

from src.adapters.uow import engine, UnitOfWork
from src.services.batch_service import BatchService


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork()


def get_batch_service(uof: Annotated[Any, Depends(get_unit_of_work)]) -> BatchService:
    return BatchService(uof=uof)


