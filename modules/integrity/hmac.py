import hmac
import hashlib


def hmac_sha256(text, key):
    """
    Generate an HMAC-SHA256 authentication code.

    Returns the HMAC as a hexadecimal string.
    """

    return hmac.new(
        key.encode("utf-8"),
        text.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()