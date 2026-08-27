from modules.security.password_policy import validate_password
from modules.authentication.password_security import (
    hash_password,
    verify_password
)

# Temporary in-memory user storage
users = {}


def register_user(username, password):
    """
    Register a new user.
    """

    if username in users:
        return {
            "success": False,
            "message": "Username already exists."
        }

    if not validate_password(password):
        return {
            "success": False,
            "message": (
                "Password must be 12-128 characters and contain "
                "uppercase, lowercase, digit, and special character."
            )
        }

    salt, password_hash = hash_password(password)

    users[username] = {
        "salt": salt,
        "password_hash": password_hash
    }

    return {
        "success": True,
        "message": "User registered successfully."
    }
   
def login_user(username, password):
    """
    Authenticate an existing user.
    """

    if username not in users:
        return {
            "success": False,
            "message": "Invalid username or password."
        }

    user = users[username]

    salt = user["salt"]
    password_hash = user["password_hash"]

    if verify_password(password, salt, password_hash):
        return {
            "success": True,
            "message": "Login successful."
        }

    return {
        "success": False,
        "message": "Invalid username or password."
    }
    