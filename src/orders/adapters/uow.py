from typing import Self, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.orders.adapters.repository import OrderLineRepository
from src.settings import get_settings
from src.shared.repository import AbstractRepository
from src.shared.uow import AbstractUnitOfWork

settings = get_settings()

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(settings.DB_URL))


class OrderLineUnitOfWork(AbstractUnitOfWork):
    """
    Context Manager for adapters operations.
    The Unit of Work pattern manages adapters changes as a single atomic transaction.
    Manages session life cycle.
    """

    order_line_repo: OrderLineRepository

    def __init__(
        self,
        session_factory=DEFAULT_SESSION_FACTORY,
        order_line_repo: Type[AbstractRepository] = OrderLineRepository,
    ):
        self.session_factory = session_factory
        self.order_line_repo_cls = order_line_repo

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.order_line_repo = self.order_line_repo_cls(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
