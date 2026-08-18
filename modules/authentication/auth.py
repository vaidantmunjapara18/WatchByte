from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """
    Securely hash a password.
    """
    return generate_password_hash(password)


def verify_password(password, password_hash):
    """
    Verify a password against its stored hash.
    """
    return check_password_hash(password_hash, password)

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

    password_hash = hash_password(password)

    users[username] = {
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

    password_hash = users[username]["password_hash"]

    if verify_password(password, password_hash):

        return {
            "success": True,
            "message": "Login successful."
        }

    return {
        "success": False,
        "message": "Invalid username or password."
    }