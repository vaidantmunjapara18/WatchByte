from flask import Flask, render_template, request, jsonify
from modules.cryptography.aes import encrypt_aes, decrypt_aes
from modules.cryptography.des import encrypt_des, decrypt_des

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

if __name__ == "__main__":
    app.run(debug=True)