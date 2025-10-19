import abc
from typing import List, Union

from src.shared.domain.events import Event, Command

Message = Union[Event, Command]


class AbstractMessageBus(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def handle(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def handle_event(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def handle_command(self, *args, **kwargs):
        pass


class MessageBus(AbstractMessageBus):

    def __init__(self, events_mapping: List, command_mapping) -> None:
        pass

    def handle(self, message: Message):

        if isinstance(message, Event):
            self.handle_event(event=message)
        elif isinstance(message, Command):
            self.handle_command(command=message)

    def handle_event(self, event: Event) -> None:
        pass

    def handle_command(self, command: Command) -> None:
        pass
