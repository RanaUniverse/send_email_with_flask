"""
app/shared/security/otp_generate.py

This is for generating otp
"""

import random


def generate_otp() -> str:
    n = random.randint(
        a=100000,
        b=999999,
    )
    return str(n)
