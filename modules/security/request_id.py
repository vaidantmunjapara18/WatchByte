# ==========================================
# WATCHBYTE REQUEST ID
# ==========================================

import secrets
from flask import g


def get_request_id():
    """
    Return the unique ID for the current request.

    A new ID is generated once per request and then
    reused throughout that request.
    """

    if not hasattr(g, "request_id"):
        g.request_id = secrets.token_hex(16)

    return g.request_id
