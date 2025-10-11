from abc import ABC, abstractmethod

from redis import Redis

from src.config import MemStoreSettings


class MemStorageClient(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_document(self, name: str) -> dict:
        pass

    @abstractmethod
    def create_document(self, name: str, data: dict) -> None:
        pass

    @abstractmethod
    def delete_document(self, name: str) -> None:
        pass

    @abstractmethod
    def shutdown(self):
        pass


class RedisClient(MemStorageClient):
    """
    Redis client as ultra-fast in memory data store

    Migration:
    Redis, as a schemaless, so requires application-side strategies for schema migration.
        1. The Multi-Version Application Approach (Tolerate Old Data Strategy)
        2. Full Data Re-Hydration (Rebuild from Source Strategy)
        3. In-Place/Manual Migration (Migration Script Strategy)
    """

    def __init__(self, config: MemStoreSettings):
        self.client = Redis(
            host=config.host,
            port=config.port,
            username=config.user,
            password=config.password,
            decode_responses=True,
        )

    def get_document(self, name: str) -> dict:
        return self.client.hgetall(name)

    def create_document(self, name: str, data: dict) -> None:
        self.client.hset(name=name, mapping=data)

    def delete_document(self, name: str) -> None:
        self.client.delete(name)

    def shutdown(self):
        self.client.close()
        self.client.connection_pool.disconnect()
