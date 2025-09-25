class MessagingClientSettings:
    host = "localhost"
    port = 5672
    virtual_host = 'rabbitmq'
    user = 'rabbitmq'
    password = 'rabbitmq'
    prefetch_count = 1


class Settings:
    MESSAGING_CLIENT = MessagingClientSettings
