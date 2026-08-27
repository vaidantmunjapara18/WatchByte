# ==========================================
# WATCHBYTE CSRF PROTECTION
# ==========================================

import secrets
import time


csrf_tokens = {}

MAX_CSRF_TOKENS = 1000
CSRF_TOKEN_LIFETIME = 1800


def generate_csrf_token():
    """
    Generate and store a secure random CSRF token.
    """

    token = secrets.token_urlsafe(32)

    if len(csrf_tokens) >= MAX_CSRF_TOKENS:
        oldest_token = min(
            csrf_tokens,
            key=csrf_tokens.get
        )
        csrf_tokens.pop(oldest_token, None)

    csrf_tokens[token] = time.time()

    return token

def verify_csrf_token(expected_token, submitted_token):
    """
    Verify that the submitted CSRF token is valid,
    matches the expected token, and has not expired.
    """

    if not expected_token or not submitted_token:
        return False

    if not secrets.compare_digest(
        expected_token,
        submitted_token
    ):
        return False

    created_at = csrf_tokens.get(submitted_token)

    if created_at is None:
        return False

    if time.time() - created_at > CSRF_TOKEN_LIFETIME:
        csrf_tokens.pop(submitted_token, None)
        return False

    return True
   
def remove_csrf_token(token):
    """
    Remove a CSRF token after it is no longer needed.
    """

    if token:
        csrf_tokens.pop(token, None)
