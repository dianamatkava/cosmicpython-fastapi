import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.adapters.repository import AbstractRepository
from src.settings import get_settings

settings = get_settings()

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(settings.DB_URL)
)


class AbstractUnitOfWork(abc.ABC):

    batch_repo: AbstractRepository

    def __enter__(self) -> 'AbstractUnitOfWork':
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY, batch_repo=AbstractRepository):
        self.session_factory = session_factory
        self.batch_repo = batch_repo  # type: ignore

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.batch_repo = self.batch_repo(session=self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

