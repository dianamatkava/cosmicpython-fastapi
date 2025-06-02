# The Repository pattern is an abstraction over persistent storage
import abc
from typing import List

from sqlalchemy.orm import Session

from src.allocations.domain import batch_domain_model as domain


class AbstractRepository(abc.ABC):
    session: Session

    @abc.abstractmethod
    def __init__(self, session: Session):
        self.session = session

    @abc.abstractmethod
    def add(self, batch: domain.BatchModel):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> domain.BatchModel:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[domain.BatchModel]:
        raise NotImplementedError


class BatchRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, reference: str) -> domain.BatchModel:
        return (
            self.session.query(domain.BatchModel).filter_by(reference=reference).one()
        )

    def add(self, batch: domain.BatchModel) -> None:
        self.session.add(batch)

    def list(self) -> List[domain.BatchModel]:
        return self.session.query(domain.BatchModel).all()

    def delete(self, reference: str) -> None:
        self.session.query(domain.BatchModel).filter_by(reference=reference).delete()
