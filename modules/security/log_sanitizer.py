# ==========================================
# WATCHBYTE LOG SANITIZER
# ==========================================

import re


SENSITIVE_FIELDS = {
    "password",
    "passwd",
    "session_token",
    "csrf_token",
    "captcha",
    "captcha_token",
    "secret",
    "private_key",
    "encryption_key",
}


def sanitize_log_message(message):
    """
    Remove sensitive key/value data from a log message.
    """

    if not isinstance(message, str):
        return "[REDACTED]"

    sanitized = message

    for field in SENSITIVE_FIELDS:
        pattern = rf"({re.escape(field)}\s*[:=]\s*)([^,\s]+)"
        sanitized = re.sub(
            pattern,
            r"\1[REDACTED]",
            sanitized,
            flags=re.IGNORECASE
        )

    return sanitized