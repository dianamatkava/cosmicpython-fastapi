from typing import Self, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.allocations.adapters.repository import ProductAggregateRepository
from src.orders.adapters.repository import OrderLineRepository
from src.settings import get_settings
from src.shared.repository import AbstractRepository
from src.shared.uow import AbstractUnitOfWork

settings = get_settings()

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(settings.DB_URL, echo=True))


class ProductAggregateUnitOfWork(AbstractUnitOfWork):
    """
    Context Manager for adapters operations.
    The Unit of Work pattern manages adapters changes as a single atomic transaction.
    Manages session life cycle.
    """

    def __init__(
        self,
        session_factory=DEFAULT_SESSION_FACTORY,
        product_aggregate_repo: Type[AbstractRepository] = ProductAggregateRepository,
        order_line_repo: Type[AbstractRepository] = OrderLineRepository,
    ):
        self.session_factory = session_factory
        self.product_aggregate_repo_cls = product_aggregate_repo
        self.order_line_repo_cls = order_line_repo

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.product_aggregate_repo: ProductAggregateRepository = (
            self.product_aggregate_repo_cls(self.session)
        )
        self.order_line_repo: OrderLineRepository = self.order_line_repo_cls(
            self.session
        )
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def rollback(self):
        self.publish_events()
        self._rollback()

    def _rollback(self):
        self.session.rollback()

    def commit(self):
        self.publish_events()
        self._commit()

    def _commit(self):
        self.session.commit()

    def collect_events(self):
        events = []
        for product in self.product_aggregate_repo.seen:
            while product.events:
                events.append(product.events.pop(0))
        return events

    def publish_events(self):
        from src.allocations.services.messagebus import dispatch

        for product in self.product_aggregate_repo.seen:
            dispatch(product.events)
