# ==========================================
# WATCHBYTE INTRUSION DETECTION SYSTEM
# ==========================================


def detect_suspicious_activity(
    source_ip,
    destination_port,
    protocol,
    connection_attempts
):
    """
    Detect basic suspicious network activity.
    """

    alerts = []

    # Detect excessive connection attempts
    if connection_attempts >= 5:
        alerts.append(
            "Possible brute-force or scanning activity detected."
        )

    # Detect suspicious Telnet traffic
    if destination_port == 23 and protocol.lower() == "tcp":
        alerts.append(
            "Telnet traffic detected."
        )

    # Detect suspicious FTP traffic
    if destination_port == 21 and protocol.lower() == "tcp":
        alerts.append(
            "FTP traffic detected."
        )

    if alerts:
        return {
            "alert": True,
            "source_ip": source_ip,
            "alerts": alerts
        }

    return {
        "alert": False,
        "source_ip": source_ip,
        "alerts": []
    }