from datetime import datetime, date
from uuid import UUID


def json_converter(obj):
    """
    Converts objects that are not natively JSON serializable.
    """
    if isinstance(obj, datetime) or isinstance(obj, date):
        return obj.isoformat()

    if isinstance(obj, UUID):
        return str(obj)

    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
