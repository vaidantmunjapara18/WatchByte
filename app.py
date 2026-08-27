from modules.security.security_headers import apply_security_headers
from modules.security.csrf import (
    generate_csrf_token,
    verify_csrf_token
)
from modules.security.input_validation import (
    validate_text,
    validate_integer,
    validate_username
)
from modules.security.request_limits import (
    is_request_size_allowed,
    get_max_request_size
)
from modules.security.file_validation import (
    is_valid_filename,
    validate_file_stream
)
from modules.security.authorization import authorize_session
from modules.security.error_handler import get_safe_error_message
from modules.security.error_handler import (
    get_safe_error_message,
    get_client_error_message
)
from modules.security.request_id import get_request_id
from flask import Flask, render_template, request, jsonify
from modules.cryptography.aes import encrypt_aes, decrypt_aes
from modules.cryptography.des import encrypt_des, decrypt_des
from modules.cryptography.rsa import (
    generate_rsa_keys,
    encrypt_rsa,
    decrypt_rsa
)
from modules.integrity.hash import sha256_hash
from modules.integrity.hmac import hmac_sha256
from modules.integrity.file_hash import calculate_file_sha256
from modules.authentication.auth import register_user, login_user
from modules.network.network_engine import analyze_network_request
from modules.logs.logger import (
    log_info,
    log_warning,
    log_block,
    add_log,
    get_logs,
    clear_logs
)
from modules.authentication.captcha import (
    generate_captcha,
    verify_captcha
)
from modules.authentication.rate_limiter import (
    check_rate_limit,
    record_failed_attempt,
    reset_attempts
)
from modules.authentication.account_lockout import (
    is_locked,
    record_failed_login,
    reset_failed_logins,
    get_lockout_status
)
from modules.authentication.session_manager import (
    create_session,
    validate_session,
    destroy_session,
    get_active_sessions
)

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = get_max_request_size()

@app.errorhandler(413)
def handle_request_too_large(error):
    return jsonify({
        "success": False,
        "error": "Request is too large. Maximum allowed size is 1 MB."
    }), 413

@app.after_request
def add_security_headers(response):
    response = apply_security_headers(response)
    response.headers["X-Request-ID"] = get_request_id()
    return response
def get_client_ip():
    """
    Get the client's IP address from the current Flask request.
    """

    return request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/aes", methods=["POST"])
def aes_operation():
    try:
        data = request.get_json()

        operation = data.get("operation")
        key = data.get("key", "")
        text = data.get("text", "")

        if not key:
            return jsonify({
                "success": False,
                "error": "Please enter an AES key."
            }), 400

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter text."
            }), 400

        if len(key) not in [16, 24, 32]:
            return jsonify({
                "success": False,
                "error": "AES key must be exactly 16, 24, or 32 characters."
            }), 400

        if operation == "encrypt":
            result = encrypt_aes(text, key)

        elif operation == "decrypt":
            result = decrypt_aes(text, key)

        else:
            return jsonify({
                "success": False,
                "error": "Invalid operation."
            }), 400

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as error:
        if getattr(error, "code", None) == 413:
            return jsonify({
                "success": False,
                "error": "Request is too large. Maximum allowed size is 1 MB."
            }), 413

        return jsonify({
            "success": False,
            "error": get_safe_error_message(error)
        }), 500

@app.route("/api/des", methods=["POST"])
def des_operation():
    try:
        data = request.get_json()

        operation = data.get("operation")
        key = data.get("key", "")
        text = data.get("text", "")

        if not key:
            return jsonify({
                "success": False,
                "error": "Please enter a DES key."
            }), 400

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter text."
            }), 400

        if len(key) != 8:
            return jsonify({
                "success": False,
                "error": "DES key must be exactly 8 characters."
            }), 400

        if operation == "encrypt":
            result = encrypt_des(text, key)

        elif operation == "decrypt":
            result = decrypt_des(text, key)

        else:
            return jsonify({
                "success": False,
                "error": "Invalid operation."
            }), 400

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception:
        return jsonify({
            "success": False,
            "error": "Decryption failed. Check the key and encrypted data."
        }), 400
@app.route("/api/rsa/generate", methods=["POST"])
def rsa_generate_keys():
    try:
        public_key, private_key = generate_rsa_keys()

        return jsonify({
            "success": True,
            "public_key": public_key,
            "private_key": private_key
        })

    except Exception:
        return jsonify({
            "success": False,
            "error": "Unable to generate RSA keys."
        }), 500


@app.route("/api/rsa", methods=["POST"])
def rsa_operation():
    try:
        data = request.get_json()

        operation = data.get("operation")
        key = data.get("key", "")
        text = data.get("text", "")

        if not key:
            return jsonify({
                "success": False,
                "error": "Please provide an RSA key."
            }), 400

        if not text.strip():
            return jsonify({
                "success": False,
                "error": "Please enter some text."
            }), 400

        if operation == "encrypt":
            result = encrypt_rsa(text, key)

        elif operation == "decrypt":
            result = decrypt_rsa(text, key)

        else:
            return jsonify({
                "success": False,
                "error": "Invalid RSA operation."
            }), 400

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception:
        return jsonify({
            "success": False,
            "error": "RSA operation failed. Check the key and encrypted data."
        }), 400

@app.route("/api/hash", methods=["POST"])
def hash_operation():
    try:
        data = request.get_json()

        text = data.get("text", "")

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter some text."
            }), 400

        result = sha256_hash(text)

        return jsonify({
            "success": True,
            "algorithm": "SHA-256",
            "result": result
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": get_client_error_message(error)
        }), 400

@app.route("/api/hmac", methods=["POST"])
def hmac_operation():
    try:
        data = request.get_json()

        text = data.get("text", "")
        key = data.get("key", "")

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter some text."
            }), 400

        if not key:
            return jsonify({
                "success": False,
                "error": "Please enter a secret key."
            }), 400

        result = hmac_sha256(text, key)

        return jsonify({
            "success": True,
            "algorithm": "HMAC-SHA256",
            "result": result
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": get_client_error_message(error)
        }), 400

@app.route("/api/file-hash", methods=["POST"])
def file_hash_operation():
    try:
        if "file" not in request.files:
            return jsonify({
                "success": False,
                "error": "Please select a file."
            }), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "success": False,
                "error": "Please select a file."
            }), 400

        # ==========================================
        # FILE UPLOAD SECURITY VALIDATION
        # ==========================================

        if not is_valid_filename(file.filename):
            return jsonify({
                "success": False,
                "error": "Invalid filename."
            }), 400


        if not validate_file_stream(file.stream):
            return jsonify({
                "success": False,
                "error": "Uploaded file is too large. Maximum allowed size is 5 MB."
            }), 413

        # Save the uploaded file temporarily
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        try:
            result = calculate_file_sha256(temp_path)

        finally:
            os.remove(temp_path)

        return jsonify({
            "success": True,
            "algorithm": "SHA-256",
            "filename": file.filename,
            "hash": result
        })

    except Exception as error:
        if getattr(error, "code", None) == 413:
            return jsonify({
                "success": False,
                "error": "Uploaded file is too large. Maximum allowed size is 5 MB."
            }), 413

        return jsonify({
            "success": False,
            "error": get_safe_error_message(error)
        }), 500

@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    try:
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username:
            return jsonify({
                "success": False,
                "error": "Please enter a username."
            }), 400

        if not validate_username(username):
            return jsonify({
                "success": False,
                "error": "Username must be 3-32 characters, start with a letter, and contain only letters, numbers, underscores, or hyphens."
            }), 400

        if not password:
            return jsonify({
                "success": False,
                "error": "Please enter a password."
            }), 400

        result = register_user(username, password)

        if not result["success"]:

            add_log(
                log_warning(
                    f"User registration failed for '{username}'.",
                    "Authentication",
                    get_client_ip()
                )
            )

            return jsonify(result), 400


        add_log(
            log_info(
                f"User '{username}' registered successfully.",
                "Authentication",
                get_client_ip()
            )
        )

        return jsonify(result), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "error": get_client_error_message(error)
        }), 400


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    try:
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username:
            return jsonify({
                "success": False,
                "error": "Please enter a username."
            }), 400

        if not password:
            return jsonify({
                "success": False,
                "error": "Please enter a password."
            }), 400

        # ==========================================
        # ACCOUNT LOCKOUT CHECK
        # ==========================================

        if is_locked(username):

            lockout_status = get_lockout_status(username)

            add_log(
                log_block(
                    f"Login blocked: account '{username}' is locked.",
                    "Account Lockout",
                    get_client_ip()
                )
            )

            return jsonify({
                "success": False,
                "message": "Account is temporarily locked. Please try again later.",
                "account_locked": True,
                "remaining_seconds": lockout_status["remaining_seconds"]
            }), 423

        # ==========================================
        # RATE LIMIT CHECK
        # ==========================================

        rate_status = check_rate_limit(username)

        if not rate_status["allowed"]:

            add_log(
                log_block(
                    f"Login blocked: too many failed attempts for '{username}'.",
                    "Rate Limiter",
                    get_client_ip()
                )
            )
            return jsonify({
                "success": False,
                "message": "Too many failed login attempts. Please try again later.",
                "rate_limited": True
            }), 429


        # ==========================================
        # AUTHENTICATION
        # ==========================================

        result = login_user(username, password)


        if not result["success"]:

            # Record failure for the existing rate limiter
            record_failed_attempt(username)

            # Record failure for account lockout
            lockout_result = record_failed_login(username)

            if lockout_result["locked"]:

                add_log(
                    log_block(
                        f"Account '{username}' locked after repeated failed logins.",
                        "Account Lockout",
                        get_client_ip()
                    )
                )

                return jsonify({
                    "success": False,
                    "message": "Account is temporarily locked. Please try again later.",
                    "account_locked": True,
                    "remaining_seconds": get_lockout_status(username)["remaining_seconds"]
                }), 423


            add_log(
                log_warning(
                    f"Login failed for user '{username}'.",
                    "Authentication",
                    get_client_ip()
                )
            )

            return jsonify(result), 401


        # ==========================================
        # SUCCESSFUL LOGIN
        # ==========================================

        # Reset rate limiter
        reset_attempts(username)

        # Reset account lockout
        reset_failed_logins(username)

        # Create secure session
        session_token = create_session(username)

        add_log(
            log_info(
                f"Session created for user '{username}'.",
                "Session Manager",
                get_client_ip()
            )
        )

        add_log(
            log_info(
                f"User '{username}' logged in successfully.",
                "Authentication",
                get_client_ip()
            )
        )

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "session_token": session_token
        }), 200


    except Exception as error:

        return jsonify({
            "success": False,
           "error": get_client_error_message(error) 
        }), 400 
    try:
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username:
            return jsonify({
                "success": False,
                "error": "Please enter a username."
            }), 400

        if not password:
            return jsonify({
                "success": False,
                "error": "Please enter a password."
            }), 400

        result = login_user(username, password)

        if not result["success"]:

            add_log(
                log_warning(
                    f"Login failed for user '{username}'.",
                    "Authentication"
                )
            )

            return jsonify(result), 401


        add_log(
            log_info(
                f"User '{username}' logged in successfully.",
                "Authentication"
            )
        )

        return jsonify(result), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "error": get_client_error_message(error)
        }), 400

@app.route("/api/network/analyze", methods=["POST"])
def analyze_network():
    try:
        data = request.get_json()

        source_ip = data.get("source_ip", "").strip()
        destination_port = data.get("destination_port")
        protocol = data.get("protocol", "").strip()
        connection_attempts = data.get("connection_attempts")

        # ==========================================
        # INPUT VALIDATION
        # ==========================================

        if not validate_text(source_ip, 1, 45):
            return jsonify({
                "success": False,
                "error": "Invalid source IP address."
            }), 400


        if not validate_integer(destination_port, 1, 65535):
            return jsonify({
                "success": False,
                "error": "Destination port must be between 1 and 65535."
            }), 400


        if not validate_text(protocol, 1, 20):
            return jsonify({
                "success": False,
                "error": "Invalid protocol."
            }), 400


        if not validate_integer(connection_attempts, 0, 1000000):
            return jsonify({
                "success": False,
                "error": "Connection attempts must be a valid number."
            }), 400

        if not source_ip:
            return jsonify({
                "success": False,
                "error": "Please enter a source IP address."
            }), 400

        if destination_port is None:
            return jsonify({
                "success": False,
                "error": "Please enter a destination port."
            }), 400

        if not protocol:
            return jsonify({
                "success": False,
                "error": "Please enter a protocol."
            }), 400

        if connection_attempts is None:
            return jsonify({
                "success": False,
                "error": "Please enter connection attempts."
            }), 400

        result = analyze_network_request(
            source_ip,
            int(destination_port),
            protocol,
            int(connection_attempts)
        )
        # ==========================================
        # SECURITY LOGGING
        # ==========================================

        # Firewall event
        if result["firewall"]["action"] == "BLOCK":

            add_log(
                log_block(
                    result["firewall"]["reason"],
                    "Firewall"
                )
            )

        else:

            add_log(
                log_info(
                    result["firewall"]["reason"],
                    "Firewall"
                )
            )


        # IDS event
        if result["ids"]["alert"]:

            for alert in result["ids"]["alerts"]:

                add_log(
                    log_warning(
                        alert,
                        "IDS"
                    )
                )

        return jsonify({
            "success": True,
            "result": result
        }), 200

    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Port and connection attempts must be numbers."
        }), 400

    except Exception as error:
        if getattr(error, "code", None) == 413:
            return jsonify({
                "success": False,
                "error": "Request is too large. Maximum allowed size is 1 MB."
            }), 413

        return jsonify({
            "success": False,
            "error": get_client_error_message(error)
        }), 400

# ==========================================
# SECURITY LOG API
# ==========================================

@app.route("/api/logs", methods=["GET"])
def get_security_logs():

    session_token = request.headers.get("Authorization", "")

    if session_token.startswith("Bearer "):
        session_token = session_token[7:]

    session = authorize_session(session_token)

    if session is None:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "logs": get_logs()
    })


@app.route("/api/logs", methods=["POST"])
def create_security_log():

        session_token = request.headers.get("Authorization", "")

        if session_token.startswith("Bearer "):
            session_token = session_token[7:]

        session = authorize_session(session_token)

        if session is None:
            return jsonify({
                "success": False,
                "error": "Authentication required."
            }), 401

        try:

            data = request.get_json()

            level = data.get("level", "").strip().upper()
            event = data.get("event", "").strip()
            source = data.get("source", "WatchByte").strip()

            if not level:
                return jsonify({
                    "success": False,
                    "error": "Log level is required."
                }), 400

            if not event:
                return jsonify({
                    "success": False,
                    "error": "Log event is required."
                }), 400

            if level == "INFO":

                log = log_info(event, source)

            elif level == "WARNING":

                log = log_warning(event, source)

            elif level == "BLOCK":

                log = log_block(event, source)

            else:

                return jsonify({
                    "success": False,
                    "error": "Invalid log level."
                }), 400

            add_log(log)

            return jsonify({
                "success": True,
                "log": log
            }), 201

        except Exception as error:

            return jsonify({
                "success": False,
                "error": get_client_error_message(error)
            }), 400


@app.route("/api/logs/clear", methods=["POST"])
def clear_security_logs():

    session_token = request.headers.get("Authorization", "")

    if session_token.startswith("Bearer "):
        session_token = session_token[7:]

    session = authorize_session(session_token)

    if session is None:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    clear_logs()

    return jsonify({
        "success": True,
        "message": "Security logs cleared successfully."
    })

# ==========================================
# CAPTCHA API
# ==========================================

@app.route("/api/captcha/generate", methods=["GET"])
def generate_captcha_api():

    captcha = generate_captcha()

    return jsonify({
        "success": True,
        "captcha": captcha
    })


@app.route("/api/captcha/verify", methods=["POST"])
def verify_captcha_api():

    try:

        data = request.get_json()

        expected = data.get("expected", "")
        submitted = data.get("submitted", "")

        if not expected:
            return jsonify({
                "success": False,
                "error": "CAPTCHA challenge is required."
            }), 400

        if not submitted:
            return jsonify({
                "success": False,
                "error": "CAPTCHA answer is required."
            }), 400

        verified = verify_captcha(
            expected,
            submitted
        )

        # ==========================================
        # CAPTCHA SECURITY LOGGING
        # ==========================================

        if verified:

            add_log(
                log_info(
                    "CAPTCHA verification successful.",
                    "CAPTCHA",
                    get_client_ip()
                )
            )

        else:

            add_log(
                log_warning(
                    "CAPTCHA verification failed.",
                    "CAPTCHA",
                    get_client_ip()
                )
            )

        return jsonify({
            "success": True,
            "verified": verified
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": get_client_error_message(error)
        }), 400
# ==========================================
# CSRF PROTECTION API
# ==========================================

@app.route("/api/security/csrf", methods=["GET"])
def get_csrf_token():

    token = generate_csrf_token()

    return jsonify({
        "success": True,
        "csrf_token": token
    }), 200

# ==========================================
# SESSION MANAGEMENT API
# ==========================================

@app.route("/api/auth/session", methods=["POST"])
def validate_auth_session():

    try:

        data = request.get_json()

        session_token = data.get("session_token", "")

        if not session_token:
            return jsonify({
                "success": False,
                "error": "Session token is required."
            }), 400


        session = validate_session(session_token)


        if not session["valid"]:

            add_log(
                log_warning(
                    "Invalid or expired session attempted.",
                    "Session Manager"
                )
            )

            return jsonify({
                "success": False,
                "valid": False,
                "error": "Session is invalid or expired."
            }), 401


        return jsonify({
            "success": True,
            "valid": True,
            "username": session["username"]
        }), 200


    except Exception as error:

        return jsonify({
            "success": False,
            "error": get_client_error_message(error)
        }), 400

@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():

    try:

        data = request.get_json()

        session_token = data.get("session_token", "")

        csrf_token = data.get("csrf_token", "")

        # ==========================================
        # CSRF VALIDATION
        # ==========================================

        expected_csrf_token = request.headers.get("X-CSRF-Token")

        if not verify_csrf_token(expected_csrf_token, csrf_token):

            add_log(
                log_warning(
                    "CSRF validation failed during logout.",
                    "CSRF Protection"
                )
            )

            return jsonify({
                "success": False,
                "error": "Invalid or missing CSRF token."
            }), 403

        if not session_token:
            return jsonify({
                "success": False,
                "error": "Session token is required."
            }), 400


        destroyed = destroy_session(session_token)


        if not destroyed:
            return jsonify({
                "success": False,
                "message": "Session not found or already logged out."
            }), 404


        add_log(
            log_info(
                "User session terminated.",
                "Session Manager",
                get_client_ip()
            )
        )


        return jsonify({
            "success": True,
            "message": "Logout successful."
        }), 200


    except Exception as error:

        return jsonify({
            "success": False,
            "error": get_client_error_message(error)
        }), 400

@app.route("/api/auth/sessions", methods=["GET"])
def active_sessions():

    session_token = request.headers.get("Authorization", "")

    if session_token.startswith("Bearer "):
        session_token = session_token[7:]

    session = authorize_session(session_token)

    if session is None:
        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "active_sessions": get_active_sessions()
    }), 200

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=False)