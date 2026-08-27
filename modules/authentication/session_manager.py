# ==========================================
# WATCHBYTE SESSION MANAGER
# ==========================================

import secrets
from time import time


# Store active sessions
_sessions = {}


# Session lifetime: 30 minutes
SESSION_TIMEOUT = 30 * 60

MAX_SESSIONS_PER_USER = 5

def create_session(username):
    """
    Create a new secure session for a user.

    If the user already has the maximum number of active
    sessions, revoke the oldest session first.
    """

    # Find all existing sessions for this user
    user_sessions = [
        (token, session)
        for token, session in _sessions.items()
        if session["username"] == username
    ]

    # Enforce maximum concurrent sessions
    if len(user_sessions) >= MAX_SESSIONS_PER_USER:
        oldest_token, _ = min(
            user_sessions,
            key=lambda item: item[1]["created_at"]
        )

        _sessions.pop(oldest_token, None)

    # Generate a new secure session token
    session_token = secrets.token_urlsafe(32)

    current_time = time()

    _sessions[session_token] = {
        "username": username,
        "created_at": current_time,
        "last_activity": current_time
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