# ==========================================
# WATCHBYTE DIFFIE-HELLMAN KEY EXCHANGE
# ==========================================

from cryptography.hazmat.primitives.asymmetric import dh


def generate_dh_parameters():
    """
    Generate Diffie-Hellman parameters.

    Uses a 2048-bit MODP-style DH parameter set.
    """

    parameters = dh.generate_parameters(
        generator=2,
        key_size=2048
    )

    return parameters


def generate_dh_key_pair(parameters):
    """
    Generate a private/public key pair
    using the supplied Diffie-Hellman parameters.
    """

    private_key = parameters.generate_private_key()

    public_key = private_key.public_key()

    return private_key, public_key


def generate_shared_secret(private_key, peer_public_key):
    """
    Derive a shared secret using the local private key
    and the other party's public key.
    """

    return private_key.exchange(peer_public_key)