# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
poetry install

# Run all tests
poetry run pytest

# Run a single test file or test
poetry run pytest src/orders/tests/unit/test_order_model.py
poetry run pytest src/orders/tests/unit/test_order_model.py::test_function_name

# Type checking
poetry run mypy .

# Linting
poetry run ruff check .
poetry run ruff check . --fix

# Formatting
poetry run ruff format

# Run dev server
poetry run uvicorn src.app:create_app --reload
```

Tests load environment variables from `src/.env.test` automatically via `pytest-dotenv`.

## Architecture

This is a **DDD / Clean Architecture** warehouse allocation service with two bounded contexts: **Inventory** (batches, products, allocations) and **Orders** (customer orders and order lines).

### Layer Structure (innermost to outermost)

Each bounded context (`src/inventory/`, `src/orders/`) follows the same four-layer layout:

1. **`domain/`** — Pure Python business logic. No framework imports. Contains models, domain events (`events.py`), and commands (`commands.py`). This layer has zero dependencies on anything outside `shared/domain/`.

2. **`adapters/`** — Infrastructure implementations:
   - `orm.py`: SQLAlchemy classical mapping (tables defined separately from domain models)
   - `repository.py`: Concrete implementations of `AbstractRepository[T]`
   - `uow.py`: Unit of Work wrapping SQLAlchemy session lifecycle
   - `rabbitmq_callback*.py`: Message handlers for incoming RabbitMQ messages

3. **`services/`** — Orchestration layer. Calls repositories via UoW, raises/handles domain events, translates between DTOs and domain models. Contains `messagebus.py` and `event_handlers.py`.

4. **`routes/`** — FastAPI routers. Pydantic schemas in `schemas/`, exception handlers in `exceptions/`.

### Shared Infrastructure

- `src/shared/domain/events.py` — Base `Event`, `Command`, `DomainEvent` classes
- `src/shared/adapters/uow.py` — `AbstractUnitOfWork` protocol
- `src/shared/adapters/repository.py` — `AbstractRepository[T]` generic
- `src/database/` — SQLAlchemy metadata and ORM mapper setup
- `src/adapters/` — External clients: RabbitMQ (`rabbitmqclient.py`), Redis (`redisclient.py`), Twilio email

### Key Patterns

**Unit of Work**: All service methods receive a UoW instance as a parameter. The UoW wraps the SQLAlchemy session and exposes repositories as attributes. Always used as a context manager (`async with uow:`).

**Repository**: Repositories extend `AbstractRepository[T]`. They never expose the session directly — callers interact through the UoW.

**Domain Events**: Domain models append events to `self.events`. The message bus in `services/messagebus.py` drains these events after each operation and dispatches them to registered handlers.

**Outbox Pattern**: The `OutBoxModel` in `src/inventory/domain/outbox.py` persists events to DB before publishing to RabbitMQ, ensuring at-least-once delivery.

**Bootstrap / DI**: `src/bootstrap.py` wires together all dependencies (UoW, message bus, external clients) as a singleton. Routes receive injected dependencies rather than constructing them.

### Data Flow

```
Client → FastAPI Router → Service (via UoW) → Repository → SQLAlchemy → PostgreSQL
                                    ↓
                              Domain Events
                                    ↓
                            Outbox → RabbitMQ
                                    ↓
                           RabbitMQ Callbacks → Event Handlers
```

### Test Structure

Each bounded context has three test layers under `tests/`:
- `unit/` — Domain logic only, no DB or network
- `intergation/` (note: typo in directory name) — Hits real DB via `conftest.py` fixtures
- `contract/` — Full API contract tests via HTTP client

Root `src/conftest.py` provides shared fixtures: database sessions, test client, and factory helpers.
