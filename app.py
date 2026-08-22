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


app = Flask(__name__)


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
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

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
            "error": str(error)
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
            "error": str(error)
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
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

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
                    "Authentication"
                )
            )

            return jsonify(result), 400


        add_log(
            log_info(
                f"User '{username}' registered successfully.",
                "Authentication"
            )
        )

        return jsonify(result), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
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
            "error": str(error)
        }), 400

@app.route("/api/network/analyze", methods=["POST"])
def analyze_network():
    try:
        data = request.get_json()

        source_ip = data.get("source_ip", "").strip()
        destination_port = data.get("destination_port")
        protocol = data.get("protocol", "").strip()
        connection_attempts = data.get("connection_attempts")

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
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

# ==========================================
# SECURITY LOG API
# ==========================================

@app.route("/api/logs", methods=["GET"])
def get_security_logs():

    return jsonify({
        "success": True,
        "logs": get_logs()
    })


@app.route("/api/logs", methods=["POST"])
def create_security_log():

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
            "error": str(error)
        }), 400


@app.route("/api/logs/clear", methods=["POST"])
def clear_security_logs():

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
                    "CAPTCHA"
                )
            )

        else:

            add_log(
                log_warning(
                    "CAPTCHA verification failed.",
                    "CAPTCHA"
                )
            )

        return jsonify({
            "success": True,
            "verified": verified
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

if __name__ == "__main__":
    app.run(debug=True)