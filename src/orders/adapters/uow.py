from typing import Self, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.inventory.adapters.repositories.product_repository import (
    ProductAggregateRepository,
)
from src.inventory.domain.outbox import OutBoxModel
from src.orders.adapters.repository.order_line_repository import OrderLineRepository
from src.orders.adapters.repository.order_repository import OrderRepository
from src.orders.adapters.repository.order_view_repository import OrderViewRepository
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

    order_repo: OrderRepository  # aggregate root
    order_view_repo: OrderViewRepository
    order_line_repo: OrderLineRepository
    product_repo: ProductAggregateRepository

    def __init__(
        self,
        session_factory=DEFAULT_SESSION_FACTORY,
        order_repo: Type[AbstractRepository] = OrderRepository,
        order_view_repo: Type[AbstractRepository] = OrderViewRepository,
        order_line_repo: Type[AbstractRepository] = OrderLineRepository,
        product_repo: Type[AbstractRepository] = ProductAggregateRepository,
    ):
        self.session_factory = session_factory
        self.order_repo_cls = order_repo
        self.order_view_repo_cls = order_view_repo
        self.order_line_repo_cls = order_line_repo
        self.product_repo_cls = product_repo

    def __enter__(self) -> Self:
        from src.service_manager import service_manager  # TODO: temp

        self.session: Session = self.session_factory()
        self.order_repo = self.order_repo_cls(self.session)
        self.order_view_repo = self.order_view_repo_cls(
            session=self.session, in_mem=service_manager.get_mem_storage_client()
        )
        self.order_line_repo = self.order_line_repo_cls(self.session)
        self.product_repo = self.product_repo_cls(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def rollback(self):
        self.session.rollback()

    def commit(self):
        events = self.collect_events()
        for event in events:
            outbox = OutBoxModel(
                aggregate_id=event.aggregate_id,
                aggregate_type=event.aggregate_type,
                routing_key=event.routing_key,
                body=event.model_dump_json(),
            )
            self.session.add(outbox)
        self.session.commit()

    def flush(self):
        self.session.flush()

    def collect_events(self):
        events = []
        for order in self.order_repo.seen:
            while order.events:
                events.append(order.events.pop())
        return events
