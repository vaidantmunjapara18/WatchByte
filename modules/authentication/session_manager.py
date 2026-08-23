# ==========================================
# WATCHBYTE SESSION MANAGER
# ==========================================

import secrets
from time import time


# Store active sessions
_sessions = {}


# Session lifetime: 30 minutes
SESSION_TIMEOUT = 30 * 60


def create_session(username):
    """
    Create a new secure session for a user.
    """

    session_token = secrets.token_urlsafe(32)

    _sessions[session_token] = {
        "username": username,
        "created_at": time(),
        "last_activity": time()
    }

    return session_token


def validate_session(session_token):
    """
    Validate an existing session.
    """

    if not session_token:
        return {
            "valid": False,
            "username": None
        }


    session = _sessions.get(session_token)

    if not session:
        return {
            "valid": False,
            "username": None
        }


    current_time = time()

    # Check session timeout
    if current_time - session["last_activity"] >= SESSION_TIMEOUT:

        _sessions.pop(session_token, None)

        return {
            "valid": False,
            "username": None
        }


    # Update activity timestamp
    session["last_activity"] = current_time


    return {
        "valid": True,
        "username": session["username"]
    }


def destroy_session(session_token):
    """
    Destroy an active session.
    """

    if session_token in _sessions:

        _sessions.pop(session_token)

        return True


    return False


def get_active_sessions():
    """
    Return the number of active sessions.
    """

    return len(_sessions)