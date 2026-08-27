# ==========================================
# WATCHBYTE API AUTHORIZATION
# ==========================================

from modules.authentication.session_manager import validate_session


def authorize_session(session_token):
    """
    Validate a session token for protected API access.

    Returns the session information when valid,
    otherwise returns None.
    """

    if not isinstance(session_token, str):
        return None

    session_token = session_token.strip()

    if not session_token:
        return None

    session = validate_session(session_token)

    if not session.get("valid"):
        return None

    return session


def is_authorized(session_token):
    """
    Return True when the supplied session token is valid.
    """

    return authorize_session(session_token) is not None