import hashlib


def sha256_hash(text):
    """
    Generate a SHA-256 hash for the given text.

    Returns the hash as a hexadecimal string.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()