from typing import List

from src.shared.repository import AbstractRepository, T


class OutboxRepository(AbstractRepository):
    def add(self, obj: T):
        pass

    def get(self, ref) -> T:
        pass

    def list(self) -> List[T]:
        pass

    def delete(self, ref):
        pass
