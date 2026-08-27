import re

# ==========================================
# WATCHBYTE INPUT VALIDATION
# ==========================================

def is_non_empty_string(value):
    """
    Check whether a value is a non-empty string.
    """

    return isinstance(value, str) and bool(value.strip())


def is_valid_length(value, minimum=1, maximum=10000):
    """
    Check whether a string is within the allowed length.
    """

    if not isinstance(value, str):
        return False

    return minimum <= len(value) <= maximum


def validate_text(value, minimum=1, maximum=10000):
    """
    Validate text input.
    """

    return (
        is_non_empty_string(value)
        and is_valid_length(value, minimum, maximum)
    )


def validate_integer(value, minimum=None, maximum=None):
    """
    Validate an integer and optional range.
    """

    if isinstance(value, bool) or not isinstance(value, int):
        return False

    if minimum is not None and value < minimum:
        return False

    if maximum is not None and value > maximum:
        return False

    return True

def validate_username(username):
    """
    Validate a WatchByte username.

    Requirements:
    - 3 to 32 characters
    - Starts with a letter
    - Contains only letters, numbers, underscores, and hyphens
    """

    if not isinstance(username, str):
        return False

    if not 3 <= len(username) <= 32:
        return False

    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", username))  