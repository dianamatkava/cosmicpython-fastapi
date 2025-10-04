from typing import List

from sqlalchemy.orm import Session

from src.inventory.adapters.orm import OutboxStatus
from src.inventory.domain.outbox import OutBoxModel
from src.shared.repository import AbstractRepository, T


class OutboxRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: T):
        raise NotImplementedError

    def get(self, ref) -> T:
        raise NotImplementedError

    def list(self) -> List[OutBoxModel]:
        return (
            self.session.query(OutBoxModel)
            .filter(OutBoxModel.status.in_([OutboxStatus.NEW, OutboxStatus.FAILED]))
            .order_by(OutBoxModel.created_at)
            .all()
        )

    def delete(self, ref):
        raise NotImplementedError
