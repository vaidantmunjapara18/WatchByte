# ==========================================
# WATCHBYTE PASSWORD POLICY
# ==========================================

import re


MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 128


def validate_password(password):
    """
    Validate password strength.

    Requirements:
    - 12 to 128 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """

    if not isinstance(password, str):
        return False

    if len(password) < MIN_PASSWORD_LENGTH:
        return False

    if len(password) > MAX_PASSWORD_LENGTH:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[^A-Za-z0-9]", password):
        return False

    return True


def get_password_policy():
    """
    Return the password policy requirements.
    """

    return {
        "min_length": MIN_PASSWORD_LENGTH,
        "max_length": MAX_PASSWORD_LENGTH,
        "uppercase_required": True,
        "lowercase_required": True,
        "digit_required": True,
        "special_character_required": True,
    }