class MessagingClientSettings:
    host = "localhost"
    port = 5672
    virtual_host = 'rabbitmq'
    user = 'rabbitmq'
    password = 'rabbitmq'
    prefetch_count = 10


class Settings:
    MESSAGING_CLIENT = MessagingClientSettings
