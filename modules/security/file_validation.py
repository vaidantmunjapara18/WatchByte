# ==========================================
# WATCHBYTE FILE UPLOAD VALIDATION
# ==========================================

import os


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def is_valid_filename(filename):
    """
    Validate an uploaded filename.
    """

    if not isinstance(filename, str):
        return False

    filename = filename.strip()

    if not filename:
        return False

    # Prevent path traversal.
    if os.path.basename(filename) != filename:
        return False

    # Reject suspicious path characters.
    if "/" in filename or "\\" in filename:
        return False

    return True


def is_file_size_allowed(file_size):
    """
    Check whether the uploaded file is within the allowed size.
    """

    if not isinstance(file_size, int):
        return False

    return 0 <= file_size <= MAX_FILE_SIZE


def get_max_file_size():
    """
    Return the maximum allowed upload size.
    """

    return MAX_FILE_SIZE