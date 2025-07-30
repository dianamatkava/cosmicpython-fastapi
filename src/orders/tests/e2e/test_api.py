"""
Test API that performs end-to-end testing of the API routers by verifying core domain functionality using:
 - production-like unit-of-work
 - postgres-test adapters and session
Also validates the REST API contract by ensuring correct response codes, error handling, and response structures.
"""

from src.settings import get_settings

settings = get_settings()
