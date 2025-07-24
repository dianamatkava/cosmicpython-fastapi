from typing import Self, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.allocations.adapters.repository import BatchAllocationsRepository
from src.settings import get_settings
from src.shared.repository import AbstractRepository
from src.shared.uow import AbstractUnitOfWork

settings = get_settings()

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(settings.DB_URL))


class BatchAllocationsUnitOfWork(AbstractUnitOfWork):
    """
    Context Manager for database operations.
    The Unit of Work pattern manages database changes as a single atomic transaction.
    Manages session life cycle.
    """

    def __init__(
        self,
        session_factory=DEFAULT_SESSION_FACTORY,
        product_repo: Type[AbstractRepository] = BatchAllocationsRepository,
    ):
        self.session_factory = session_factory
        self.product_repo: product_repo

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
