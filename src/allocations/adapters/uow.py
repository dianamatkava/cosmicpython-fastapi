import abc
from typing import Self, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.allocations.adapters.repository import (
    AbstractRepository,
    ProductStockRepository,
)
from src.settings import get_settings

settings = get_settings()

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(settings.DB_URL))


class AbstractUnitOfWork(abc.ABC):
    batch_repo: AbstractRepository

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):  # enherited methods
        pass

    @abc.abstractmethod  # enforce method overwrites
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory=DEFAULT_SESSION_FACTORY,
        batch_repo: Type[AbstractRepository] = ProductStockRepository,
    ):
        self.session_factory = session_factory
        self._batch_repo_cls = batch_repo
        self.batch_repo: AbstractRepository

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.batch_repo = self._batch_repo_cls(session=self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
