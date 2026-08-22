# ==========================================
# WATCHBYTE NETWORK SECURITY ENGINE
# ==========================================

from modules.network.firewall import check_firewall_rule
from modules.network.ids import detect_suspicious_activity


def analyze_network_request(
    source_ip,
    destination_port,
    protocol,
    connection_attempts
):
    """
    Analyze a simulated network request using
    both the firewall and IDS.
    """

    # Run firewall check
    firewall_result = check_firewall_rule(
        source_ip,
        destination_port,
        protocol
    )

    # Run IDS check
    ids_result = detect_suspicious_activity(
        source_ip,
        destination_port,
        protocol,
        connection_attempts
    )

    # Final security decision
    if firewall_result["action"] == "BLOCK":
        final_action = "BLOCK"

    elif ids_result["alert"]:
        final_action = "ALERT"

    else:
        final_action = "ALLOW"

    return {
        "source_ip": source_ip,
        "destination_port": destination_port,
        "protocol": protocol,
        "connection_attempts": connection_attempts,
        "firewall": firewall_result,
        "ids": ids_result,
        "final_action": final_action
    }