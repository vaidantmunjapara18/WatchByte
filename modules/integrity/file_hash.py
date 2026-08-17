import hashlib


def calculate_file_sha256(file_path):
    """
    Calculate the SHA-256 hash of a file.

    Reads the file in chunks so large files
    do not need to be loaded completely into memory.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            chunk = file.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()