import os


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


class NotificationSettings:
    api_key = "123456789"


class DatabaseSettings:
    BASE_APP_URL = os.getenv("BASE_APP_URL", "http://127.0.0.1:8000")
    DB_URL = os.getenv(
        "DB_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
    )


class Settings:
    MESSAGING_CLIENT = MessagingClientSettings
    MEM_STORAGE_CLIENT = MemStoreSettings
    NOTIFICATION_CLIENT = NotificationSettings
    DATABASE_SETTINGS = DatabaseSettings
