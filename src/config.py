class MessagingClientSettings:
    host = "localhost"
    port = 5672
    virtual_host = "rabbitmq"
    user = "rabbitmq"
    password = "rabbitmq"
    prefetch_count = 10


class MemStoreSettings:
    host = "localhost"
    port = 6379
    user = "default"
    password = "rabbitmq"


class Settings:
    MESSAGING_CLIENT = MessagingClientSettings
    MEM_STORAGE = MemStoreSettings
