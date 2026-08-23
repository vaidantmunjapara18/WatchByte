# ==========================================
# WATCHBYTE SECURE ERROR HANDLING
# ==========================================

def get_safe_error_message(error, default_message="An internal error occurred."):
    """
    Return a safe error message without exposing
    internal application details.
    """

    if error is None:
        return default_message

    return default_message


def get_client_error_message(error):
    """
    Return a safe message for expected client-side errors.
    """

    if error is None:
        return "Invalid request."

    return "Invalid request."