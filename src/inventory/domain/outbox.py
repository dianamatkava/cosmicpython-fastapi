"""Contains 'pure' business logic models."""

import json
from datetime import datetime

from src.shared.adapters.orm import OutboxStatus


class OutBoxModel:
    aggregate_type: str
    aggregate_id: str
    routing_key: str
    body: json
    retry_count: int
    status: OutboxStatus
    created_at: datetime

    def __init__(
        self,
        aggregate_type: str,
        aggregate_id: str,
        routing_key: str,
        body: json,
    ):
        self.aggregate_type = aggregate_type
        self.aggregate_id = aggregate_id
        self.routing_key = routing_key
        self.body = body

    def __str__(self):
        return f"{self.routing_key} {self.body}"
