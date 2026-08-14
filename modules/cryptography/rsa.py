from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def generate_rsa_keys():
    """
    Generate a 2048-bit RSA public/private key pair.
    """

    key = RSA.generate(2048)

    private_key = key.export_key().decode("utf-8")
    public_key = key.publickey().export_key().decode("utf-8")

    return public_key, private_key


def encrypt_rsa(plaintext, public_key):
    """
    Encrypt plaintext using the RSA public key.
    Uses RSA-OAEP padding.
    """

    key = RSA.import_key(public_key)

    cipher = PKCS1_OAEP.new(key)

    plaintext_bytes = plaintext.encode("utf-8")

    encrypted_data = cipher.encrypt(plaintext_bytes)

    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt_rsa(encrypted_data, private_key):
    """
    Decrypt Base64 encoded RSA-OAEP data
    using the RSA private key.
    """

    key = RSA.import_key(private_key)

    cipher = PKCS1_OAEP.new(key)

    encrypted_bytes = base64.b64decode(encrypted_data)

    decrypted_data = cipher.decrypt(encrypted_bytes)

    return decrypted_data.decode("utf-8")