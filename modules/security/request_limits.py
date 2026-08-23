# ==========================================
# WATCHBYTE REQUEST SIZE PROTECTION
# ==========================================

MAX_REQUEST_SIZE = 1 * 1024 * 1024  # 1 MB


def is_request_size_allowed(content_length):
    """
    Check whether the request size is within the allowed limit.
    """

    if content_length is None:
        return True

    if not isinstance(content_length, int):
        return False

    return 0 <= content_length <= MAX_REQUEST_SIZE


def get_max_request_size():
    """
    Return the maximum allowed request size in bytes.
    """

    return MAX_REQUEST_SIZE