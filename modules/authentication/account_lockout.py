# ==========================================
# WATCHBYTE ACCOUNT LOCKOUT
# ==========================================

import time


MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes


failed_attempts = {}


def is_locked(username):
    """
    Check whether an account is currently locked.
    """

    if username not in failed_attempts:
        return False

    attempts, locked_until = failed_attempts[username]

    if locked_until is None:
        return False

    if time.time() < locked_until:
        return True

    # Lockout expired
    failed_attempts[username] = (0, None)

    return False


def record_failed_login(username):
    """
    Record a failed login attempt.
    Lock the account after the maximum attempts.
    """

    attempts, locked_until = failed_attempts.get(
        username,
        (0, None)
    )

    attempts += 1

    if attempts >= MAX_FAILED_ATTEMPTS:

        locked_until = time.time() + LOCKOUT_DURATION

    failed_attempts[username] = (
        attempts,
        locked_until
    )

    return {
        "attempts": attempts,
        "locked": locked_until is not None
    }


def reset_failed_logins(username):
    """
    Reset failed login attempts after
    successful authentication.
    """

    failed_attempts.pop(username, None)


def get_lockout_status(username):
    """
    Return the current lockout status.
    """

    locked = is_locked(username)

    attempts, locked_until = failed_attempts.get(
        username,
        (0, None)
    )

    remaining = 0

    if locked_until is not None:
        remaining = max(
            0,
            int(locked_until - time.time())
        )

    return {
        "locked": locked,
        "attempts": attempts,
        "remaining_seconds": remaining
    }