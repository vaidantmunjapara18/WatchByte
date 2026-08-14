from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import base64


def encrypt_aes(plaintext, key):
    """
    Encrypt plaintext using AES-CBC.
    Returns Base64 encoded ciphertext and IV.
    """

    # Convert text and key to bytes
    plaintext_bytes = plaintext.encode("utf-8")
    key_bytes = key.encode("utf-8")

    # AES requires a 16, 24, or 32 byte key
    if len(key_bytes) not in [16, 24, 32]:
        raise ValueError("AES key must be exactly 16, 24, or 32 characters.")

    # Create random initialization vector
    iv = os.urandom(16)

    # Add PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext_bytes)
    padded_data += padder.finalize()

    # Create AES cipher
    cipher = Cipher(
        algorithms.AES(key_bytes),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded_data)
    ciphertext += encryptor.finalize()

    # Combine IV + ciphertext
    result = iv + ciphertext

    # Convert to Base64 for display/storage
    return base64.b64encode(result).decode("utf-8")


def decrypt_aes(encrypted_data, key):
    """
    Decrypt Base64 encoded AES-CBC data.
    """

    key_bytes = key.encode("utf-8")

    if len(key_bytes) not in [16, 24, 32]:
        raise ValueError("AES key must be exactly 16, 24, or 32 characters.")

    # Decode Base64
    encrypted_bytes = base64.b64decode(encrypted_data)

    # Extract IV and ciphertext
    iv = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:]

    # Create AES cipher
    cipher = Cipher(
        algorithms.AES(key_bytes),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext)
    padded_data += decryptor.finalize()

    # Remove PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()

    plaintext_bytes = unpadder.update(padded_data)
    plaintext_bytes += unpadder.finalize()

    return plaintext_bytes.decode("utf-8")