# WatchByte

## Cybersecurity Learning & Demonstration Platform

WatchByte is a modular, web-based cybersecurity learning and demonstration platform developed with Python, Flask, HTML, CSS, and JavaScript. It brings together practical demonstrations of cryptography, data integrity, authentication security, network security, CAPTCHA/bot protection, session management, CSRF protection, authorization, and security logging in one application.

### Academic & Portfolio Purpose

WatchByte is designed for:

- **Academic demonstration:** explaining cybersecurity concepts through interactive features.
- **GitHub portfolio:** demonstrating practical implementation, modular architecture, defensive programming, and security awareness.

> **Important:** WatchByte is an educational/security demonstration project. Some storage and deployment mechanisms are intentionally simplified and require further hardening before production use.

## Features

### Cryptography Lab

WatchByte includes:

- **AES** — modern symmetric encryption demonstration.
- **DES** — legacy symmetric encryption included for educational comparison. DES is obsolete for modern secure systems.
- **RSA** — 2048-bit public/private key generation with RSA-OAEP encryption/decryption.
- **Diffie-Hellman** — 2048-bit key-agreement demonstration where Alice and Bob independently derive the same shared secret.

Diffie-Hellman is key agreement, not direct message encryption. The current demonstration verifies that both derived secrets match without returning the raw shared secret or private keys to the browser.

### Integrity Lab

- **SHA-256** — one-way cryptographic hashing.
- **HMAC-SHA256** — message integrity/authentication using a secret key.
- **File SHA-256** — file integrity verification.

### Authentication Security

- Password policy: 12–128 characters.
- Uppercase, lowercase, digit, and special-character requirements.
- PBKDF2-HMAC-SHA256 password derivation.
- Random 16-byte password salt.
- 100,000 PBKDF2 iterations.
- Generic invalid-credential responses.
- Rate limiting.
- Failed-login tracking.
- Account lockout.

### CAPTCHA / Bot Protection

- Server-side CAPTCHA generation.
- Challenge identifiers.
- Server-side verification.
- Case-insensitive comparison and whitespace trimming.
- Single-use challenge behavior.
- Regeneration after failed verification.
- Security logging of successful and failed verification.

API endpoints:

```text
GET  /api/captcha/generate
POST /api/captcha/verify
```

### Session Management & Authorization

The project provides:

- Secure random session tokens.
- Session validation.
- Session expiration.
- Logout/session destruction.
- Active-session tracking.
- Centralized `authorize_session()` protection for protected APIs.

### CSRF Protection

The CSRF module provides:

- Cryptographically secure token generation.
- Token storage and lifetime checking.
- Constant-time comparison.
- Expiration handling.
- Token removal.

Current token lifetime: **30 minutes**.

### Network Security

The network security area demonstrates:

- Network request analysis.
- Firewall decision logic.
- IDS-style alerting.
- Source IP, port, protocol, and attempt analysis.

### Security Logging

Structured security events contain:

- Timestamp.
- Level.
- Event.
- Source.
- IP address.

Supported levels include `INFO`, `WARNING`, and `BLOCK`.

The current in-memory log store is limited to 1,000 events.

### Log Sanitization

Sensitive fields are redacted before being placed in log messages, including:

- password
- passwd
- session_token
- csrf_token
- captcha
- captcha_token
- secret
- private_key
- encryption_key

Sensitive values are replaced with `[REDACTED]`.

### XSS-Safe Log Rendering

Security-log values are rendered through DOM APIs such as `textContent` rather than inserting server-controlled values directly through `innerHTML`.

This treats log content as untrusted data and reduces the risk of malicious log entries becoming executable HTML/script content.

### Application Security

WatchByte also contains:

- Security HTTP headers.
- Input validation.
- Username/text/integer validation.
- File-name and file-stream validation.
- Request-size limits.
- Safe client-facing error handling.
- Request IDs.
- Protected security-log APIs.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend |
| Flask | Web framework/API |
| HTML5 | UI structure |
| CSS3 | Styling |
| JavaScript | Frontend interaction |
| `cryptography` | Cryptographic primitives including AES/DH |
| PyCryptodome | RSA/DES implementation used by the project |
| Git | Version control |
| GitHub | Repository/collaboration |

## Architecture

```text
Browser
   |
   v
Flask Application (app.py)
   |
   +-----------------------------+
   |                             |
   v                             v
Security Modules              Feature Modules
   |                             |
Validation                  Cryptography
Authorization              Authentication
CSRF                        Integrity
Headers                     Network
Request Limits              Logging
Error Handling
```

The application keeps feature-specific and security-specific logic in modules instead of placing everything directly in `app.py`.

## Project Structure

```text
WatchByte/
├── app.py
├── README.md
├── modules/
│   ├── authentication/
│   │   ├── auth.py
│   │   ├── captcha.py
│   │   ├── password_security.py
│   │   ├── rate_limiter.py
│   │   ├── account_lockout.py
│   │   └── session_manager.py
│   ├── cryptography/
│   │   ├── aes.py
│   │   ├── des.py
│   │   ├── rsa.py
│   │   └── diffie_hellman.py
│   ├── integrity/
│   │   ├── hash.py
│   │   ├── hmac.py
│   │   └── file_hash.py
│   ├── network/
│   │   ├── network_engine.py
│   │   └── firewall.py
│   ├── security/
│   │   ├── authorization.py
│   │   ├── csrf.py
│   │   ├── input_validation.py
│   │   ├── request_limits.py
│   │   ├── file_validation.py
│   │   ├── password_policy.py
│   │   ├── security_headers.py
│   │   ├── log_sanitizer.py
│   │   ├── error_handler.py
│   │   └── request_id.py
│   └── logs/
│       └── logger.py
├── static/
│   ├── js/
│   │   └── app.js
│   └── style.css
└── templates/
    ├── index.html
    └── dashboard.html
```

## Security Model

WatchByte follows a layered-security approach:

1. **Input layer** — validate input, files, integers, usernames, and request size.
2. **Authentication layer** — password policy, password hashing, CAPTCHA, rate limiting, and account lockout.
3. **Session layer** — secure session tokens, validation, expiration, logout, and authorization.
4. **Request-protection layer** — CSRF tokens, security headers, request IDs, and size limits.
5. **Monitoring layer** — structured logs, security levels, IP information, and redaction.
6. **Frontend layer** — safe rendering of untrusted log data.

## Installation & Running

### Clone

```bash
git clone https://github.com/vaidantmunjapara18/WatchByte.git
cd WatchByte
```

### Virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Dependencies

Install the packages required by the repository's dependency configuration. The current implementation uses Flask, `cryptography`, PyCryptodome, and `requests` for HTTP testing.

### Run

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Testing

Basic Python syntax checks:

```powershell
python -m py_compile app.py
python -m py_compile modules\authentication\captcha.py
python -m py_compile modules\cryptography\diffie_hellman.py
```

Git validation:

```powershell
git diff --check
```

The development process also included API checks for malformed requests, CAPTCHA success/reuse behavior, session/authorization behavior, and Diffie-Hellman verification.

## Recommended Faculty Demonstration

1. Introduce the problem, objectives, and architecture.
2. Demonstrate AES, DES, RSA, and Diffie-Hellman.
3. Demonstrate SHA-256, HMAC, and file hashing.
4. Demonstrate registration, password policy, CAPTCHA, rate limiting, and lockout.
5. Demonstrate sessions and authorization.
6. Demonstrate CSRF, headers, validation, and request limits.
7. Demonstrate network analysis and IDS/firewall decisions.
8. Demonstrate security logs and sensitive-data redaction.
9. Explain XSS-safe log rendering.
10. Finish with limitations and future improvements.

## Limitations

The current version is primarily an educational platform:

- Users are stored in memory.
- Sessions are stored in memory.
- CSRF state is stored in memory.
- CAPTCHA state is application-managed.
- Security logs are stored in memory.
- Production database and deployment architecture are not yet implemented.
- DES is intentionally retained for educational comparison.
- Diffie-Hellman requires authentication in a real protocol to prevent man-in-the-middle attacks.
- Automated security-test coverage can be expanded.

These limitations are documented intentionally to distinguish an academic demonstration from a production security system.

## Future Improvements

Potential future work:

- Database-backed users.
- Persistent sessions and security logs.
- Role-based access control.
- Password change/reset.
- Email verification.
- Automated unit/integration/security tests.
- Dependency vulnerability scanning.
- CI/CD security checks.
- Production-grade key management.
- Authenticated key exchange.
- Improved cryptographic visualizations.
- Advanced dashboard analytics.
- Containerized production deployment.

## Team Presentation Allocation

### Member 1 — Cryptography
AES, DES, RSA, Diffie-Hellman, symmetric vs asymmetric cryptography, key agreement.

### Member 2 — Authentication
Password policy, PBKDF2, salts, CAPTCHA, rate limiting, account lockout, sessions.

### Member 3 — Application Security
CSRF, authorization, security headers, input validation, request limits, XSS protection.

### Member 4 — Network & Monitoring
Firewall, IDS, network analysis, logging, log sanitization, dashboard.

## Conclusion

WatchByte demonstrates that cybersecurity is a combination of complementary controls rather than a single algorithm. The project combines:

**Cryptography + Integrity + Authentication + Authorization + Network Security + Application Security + Monitoring**

in one interactive educational platform.

## Repository

GitHub: https://github.com/vaidantmunjapara18/WatchByte

Current development checkpoint: **Diffie-Hellman key exchange added to the Cryptography Lab.**
