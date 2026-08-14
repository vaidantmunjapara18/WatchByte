from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import base64


def encrypt_des(plaintext, key):
    """
    Encrypt plaintext using DES-CBC.
    Returns Base64 encoded IV + ciphertext.
    """

    key_bytes = key.encode("utf-8")

    # DES requires exactly 8 bytes
    if len(key_bytes) != 8:
        raise ValueError("DES key must be exactly 8 characters.")

    plaintext_bytes = plaintext.encode("utf-8")

    # Generate a random 8-byte IV
    iv = os.urandom(8)

    # Create DES cipher
    cipher = DES.new(key_bytes, DES.MODE_CBC, iv)

    # PKCS7 padding
    padded_data = pad(plaintext_bytes, DES.block_size)

    # Encrypt
    ciphertext = cipher.encrypt(padded_data)

    # Store IV together with ciphertext
    result = iv + ciphertext

    # Base64 for easy display
    return base64.b64encode(result).decode("utf-8")


def decrypt_des(encrypted_data, key):
    """
    Decrypt Base64 encoded DES-CBC data.
    """

    key_bytes = key.encode("utf-8")

    if len(key_bytes) != 8:
        raise ValueError("DES key must be exactly 8 characters.")

    # Decode Base64
    encrypted_bytes = base64.b64decode(encrypted_data)

    # Extract IV and ciphertext
    iv = encrypted_bytes[:8]
    ciphertext = encrypted_bytes[8:]

    # Create DES cipher
    cipher = DES.new(key_bytes, DES.MODE_CBC, iv)

    # Decrypt
    padded_data = cipher.decrypt(ciphertext)

    # Remove padding
    plaintext_bytes = unpad(padded_data, DES.block_size)

    return plaintext_bytes.decode("utf-8")