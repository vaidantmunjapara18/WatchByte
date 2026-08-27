# ==========================================
# WATCHBYTE SECURITY LOGGER
# ==========================================

from datetime import datetime
from modules.security.log_sanitizer import sanitize_log_message


def create_log(
    level,
    event,
    source="WatchByte",
    ip_address=None
):
    """
    Create a structured security log entry.
    """

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level.upper(),
        "event": sanitize_log_message(event),
        "source": source,
        "ip_address": ip_address
    }


def log_info(
    event,
    source="WatchByte",
    ip_address=None
):
    return create_log(
        "INFO",
        event,
        source,
        ip_address
    )


def log_warning(
    event,
    source="WatchByte",
    ip_address=None
):
    return create_log(
        "WARNING",
        event,
        source,
        ip_address
    )


def log_block(
    event,
    source="WatchByte",
    ip_address=None
):
    return create_log(
        "BLOCK",
        event,
        source,
        ip_address
    )

# ==========================================
# SECURITY LOG STORAGE
# ==========================================

security_logs = []


def add_log(log):
    """
    Add a security log to the in-memory log list.
    """

    security_logs.append(log)

    return log


def get_logs():
    """
    Return all stored security logs.
    """

    return security_logs.copy()


def clear_logs():
    """
    Remove all stored security logs.
    """

    security_logs.clear()