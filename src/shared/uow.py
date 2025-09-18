import abc
from typing import Self, TypeVar


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):  # inherited methods
        self.rollback()

    @abc.abstractmethod  # enforce method overwrites
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def collect_events(self):
        raise NotImplementedError


TRepos = TypeVar("TRepos", bound=AbstractUnitOfWork)
