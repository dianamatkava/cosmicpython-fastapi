from datetime import datetime

from pydantic import BaseModel


class DomainEvent(BaseModel):
    """
    Events are immutable, historical facts indicating that a state change has occurred.
    They are broadcast using a publish-subscribe model, and the sender doesn't know
    who the recipients are.
    """

    _routing_key: str = "Unknown"
    _aggregate_type: str = "Generic"
    aggregate_id: str = "NaN"
    occurred_on: datetime = datetime.utcnow()

    @property
    def routing_key(self):
        return self._routing_key

    @property
    def aggregate_type(self):
        return self._aggregate_type


class Event(DomainEvent):
    pass


class Command(DomainEvent):
    pass
