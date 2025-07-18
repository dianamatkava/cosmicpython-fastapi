import abc
from typing import Self, Type, Generic, TypeVar

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
    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):  # inherited methods
        pass

    @abc.abstractmethod  # enforce method overwrites
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


TRepos = TypeVar("TRepos", bound=AbstractUnitOfWork)


class AbstractAllocationsUnitOfWork(Generic[TRepos]):
    product_repo: Type[AbstractRepository]


class AllocationsUnitOfWork(AbstractUnitOfWork):
    """
    Context Manager for database operations.
    The Unit of Work pattern manages database changes as a single atomic transaction.
    Manages session life cycle.
    """

    def __init__(
        self,
        session_factory=DEFAULT_SESSION_FACTORY,
        product_repo: Type[AbstractRepository] = ProductStockRepository,
    ):
        self.session_factory = session_factory
        self._product_repo_cls = product_repo
        self.product_repo: AbstractRepository

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.product_repo = self._product_repo_cls(session=self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
