# ==========================================
# WATCHBYTE RATE LIMITER
# ==========================================

from time import time


# Store login attempts by identifier
_attempts = {}


# Maximum failed attempts allowed
MAX_ATTEMPTS = 5


# Time window in seconds
WINDOW_SECONDS = 60


def check_rate_limit(identifier):
    """
    Check whether an identifier is allowed
    to make another authentication attempt.
    """

    current_time = time()

    attempts = _attempts.get(identifier, [])


    # Keep only attempts inside the time window
    attempts = [
        attempt
        for attempt in attempts
        if current_time - attempt < WINDOW_SECONDS
    ]


    _attempts[identifier] = attempts


    if len(attempts) >= MAX_ATTEMPTS:

        return {
            "allowed": False,
            "attempts": len(attempts),
            "remaining": 0
        }


    return {
        "allowed": True,
        "attempts": len(attempts),
        "remaining": MAX_ATTEMPTS - len(attempts)
    }


def record_failed_attempt(identifier):
    """
    Record a failed authentication attempt.
    """

    current_time = time()

    if identifier not in _attempts:

        _attempts[identifier] = []


    _attempts[identifier].append(current_time)


def reset_attempts(identifier):
    """
    Reset failed attempts after successful authentication.
    """

    _attempts.pop(identifier, None)