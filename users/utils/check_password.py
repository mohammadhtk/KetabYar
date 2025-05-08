import re
from rest_framework.exceptions import ValidationError

def is_valid_password(password):
    """
    Return True if `password` is at least 8 characters long and contains
    at least one lowercase letter, one uppercase letter, and one digit.
    """
    return (
        len(password) >= 8 and
        bool(re.search(r'[a-z]', password)) and
        bool(re.search(r'[A-Z]', password)) and
        bool(re.search(r'[0-9]', password))
    )

def check_repeat_password(password, password_confirm):
    """
    Raise a ValidationError if passwords don’t match or don’t meet complexity rules.
    Uses `is_valid_password` internally.
    """
    if password != password_confirm:
        raise ValidationError("Passwords do not match.")

    if not is_valid_password(password):
        raise ValidationError(
            "Password must be at least 8 characters long and contain "
            "at least one lowercase letter, one uppercase letter, and one digit."
        )
    return True
