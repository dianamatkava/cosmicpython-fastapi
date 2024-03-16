import re


PHONE_REGEX = r'^\+\d{9,13}$'
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_phone_number(phone_number):
    """Test"""
    match = re.match(PHONE_REGEX, phone_number)
    return bool(match)

def validate_email(phone_number):
    match = re.match(EMAIL_REGEX, phone_number)
    return bool(match)
