# ==========================================
# WATCHBYTE CAPTCHA / BOT PROTECTION
# ==========================================

import random
import string


def generate_captcha(length=6):
    """
    Generate a random CAPTCHA challenge.
    """

    characters = string.ascii_uppercase + string.digits

    captcha = "".join(
        random.choices(characters, k=length)
    )

    return captcha


def verify_captcha(expected, submitted):
    """
    Verify the submitted CAPTCHA answer.
    """

    if not expected or not submitted:
        return False

    return expected.upper() == submitted.strip().upper()