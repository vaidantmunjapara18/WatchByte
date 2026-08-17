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
    
if __name__ == "__main__":
    app.run(debug=True)