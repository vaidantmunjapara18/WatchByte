# ==========================================
# WATCHBYTE FIREWALL
# ==========================================


def check_firewall_rule(source_ip, destination_port, protocol):
    """
    Check a network request against basic firewall rules.
    """

    # Block SSH from unknown/public sources
    if destination_port == 22 and protocol.lower() == "tcp":
        return {
            "action": "BLOCK",
            "reason": "SSH traffic is blocked by the firewall."
        }

    # Allow standard HTTPS traffic
    if destination_port == 443 and protocol.lower() == "tcp":
        return {
            "action": "ALLOW",
            "reason": "HTTPS traffic is allowed."
        }

    # Allow standard HTTP traffic
    if destination_port == 80 and protocol.lower() == "tcp":
        return {
            "action": "ALLOW",
            "reason": "HTTP traffic is allowed."
        }

    # Default rule
    return {
        "action": "BLOCK",
        "reason": "Traffic does not match an allowed firewall rule."
    }