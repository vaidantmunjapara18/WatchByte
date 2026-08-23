# ==========================================
# WATCHBYTE PASSWORD SECURITY
# ==========================================

import hashlib
import secrets


def hash_password(password):
    """
    Create a secure password hash using
    PBKDF2-HMAC-SHA256 with a random salt.
    """

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000
    )

    return (
        salt.hex(),
        password_hash.hex()
    )


def verify_password(password, salt_hex, password_hash_hex):
    """
    Verify a password against its stored salt
    and password hash.
    """

    salt = bytes.fromhex(salt_hex)

    expected_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000
    )

    return secrets.compare_digest(
        expected_hash.hex(),
        password_hash_hex
    )
