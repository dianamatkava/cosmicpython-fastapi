from typing import Self, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.orders.adapters.repository.order_repository import OrderRepository
from src.settings import get_settings
from src.shared.repository import AbstractRepository
from src.shared.uow import AbstractUnitOfWork

settings = get_settings()

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(settings.DB_URL))


class OrderUnitOfWork(AbstractUnitOfWork):
    """
    Context Manager for adapters operations.
    The Unit of Work pattern manages adapters changes as a single atomic transaction.
    Manages session life cycle.
    """

    order_repo: OrderRepository

    def __init__(
        self,
        session_factory=DEFAULT_SESSION_FACTORY,
        order_repo: Type[AbstractRepository] = OrderRepository,
    ):
        self.session_factory = session_factory
        self.order_repo_cls = order_repo

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.order_repo = self.order_repo_cls(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def flush(self):
        self.session.flush()

    def collect_events(self):
        raise NotImplementedError

    def publish_events(self):
        raise NotImplementedError
