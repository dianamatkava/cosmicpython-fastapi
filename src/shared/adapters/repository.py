import abc
from typing import Generic, TypeVar, List

from sqlalchemy.orm import Session

T = TypeVar("T")


class AbstractRepository(abc.ABC, Generic[T]):
    session: Session

    @abc.abstractmethod
    def add(self, obj: T): ...
    @abc.abstractmethod
    def get(self, ref) -> T: ...
    @abc.abstractmethod
    def list(self) -> List[T]: ...
    @abc.abstractmethod
    def delete(self, ref, *args, **kwargs): ...
