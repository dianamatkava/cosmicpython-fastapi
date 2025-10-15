import abc

from src.config import NotificationSettings


class NotificationClient(abc.ABC):
    @abc.abstractmethod
    def __init__(self, config: NotificationSettings):
        pass

    @abc.abstractmethod
    def send(self, *args):
        pass

    @abc.abstractmethod
    def shutdown(self, *args):
        pass


class TwilioClient(NotificationClient):
    def __init__(self, config: NotificationSettings):
        pass

    def send(self, *args):
        print("SENDING EMAIL:", *args)

    def shutdown(self):
        print("Notification client connection closed")
