# ==========================================
# WATCHBYTE CAPTCHA / BOT PROTECTION
# ==========================================

import secrets
import string
import time


# Store active CAPTCHA challenges
_captcha_challenges = {}


# CAPTCHA lifetime: 2 minutes
CAPTCHA_TIMEOUT = 120


def generate_captcha(length=6):
    """
    Generate a random CAPTCHA challenge.

    Returns a challenge ID and the CAPTCHA text.
    The actual answer is stored server-side.
    """

    characters = string.ascii_uppercase + string.digits

    captcha = "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

    challenge_id = secrets.token_urlsafe(32)

    _captcha_challenges[challenge_id] = {
        "answer": captcha,
        "created_at": time.time()
    }

    return challenge_id, captcha


def verify_captcha(challenge_id, submitted):
    """
    Verify a CAPTCHA answer against the
    server-side stored challenge.
    """

    if not challenge_id or not submitted:
        return False

    challenge = _captcha_challenges.get(challenge_id)

    if not challenge:
        return False

    # Expire old CAPTCHA challenges
    if time.time() - challenge["created_at"] >= CAPTCHA_TIMEOUT:

        _captcha_challenges.pop(challenge_id, None)

        return False

    expected = challenge["answer"]

    verified = (
        expected.upper()
        == submitted.strip().upper()
    )

    # CAPTCHA challenges are single-use
    _captcha_challenges.pop(
        challenge_id,
        None
    )

    return verified