from typing import Self, Type, List, Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.inventory.adapters.repositories.batch_repository import BatchRepository
from src.inventory.adapters.repositories.outbox_repository import OutboxRepository
from src.inventory.adapters.repositories.product_repository import (
    ProductAggregateRepository,
)
from src.inventory.domain.commands import Command
from src.shared.domain.events import DomainEvent
from src.inventory.domain.outbox import OutBoxModel
from src.orders.adapters.repository.order_line_repository import OrderLineRepository
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
        batch_repo: Type[AbstractRepository] = BatchRepository,
        outbox_repo: Type[AbstractRepository] = OutboxRepository,
    ) -> None:
        self.session_factory = session_factory
        self.product_aggregate_repo_cls = product_aggregate_repo
        self.order_line_repo_cls = order_line_repo
        self.batch_repo_cls = batch_repo
        self.outbox_repo_cls = outbox_repo

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.product_aggregate_repo: ProductAggregateRepository = (
            self.product_aggregate_repo_cls(self.session)
        )
        self.order_line_repo: OrderLineRepository = self.order_line_repo_cls(
            self.session
        )
        self.batch_repo: BatchRepository = self.batch_repo_cls(self.session)
        self.outbox_repo: OutboxRepository = self.outbox_repo_cls(self.session)
        return super().__enter__()

    def __exit__(self, *args) -> None:
        super().__exit__(*args)

    def rollback(self) -> None:
        self.session.rollback()

    def flush(self) -> None:
        self.session.flush()

    def commit(self) -> None:
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

    def collect_events(self) -> List[Union[DomainEvent, Command]]:
        events: List[Union[DomainEvent, Command]] = []
        for product in self.product_aggregate_repo.seen:
            while product.events:
                events.append(product.events.pop(0))
        return events
