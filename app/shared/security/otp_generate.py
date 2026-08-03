"""
app/shared/security/otp_generate.py

This is for generating otp
I make protocol so that later i can easily choose i will use to choose number or letters
as the otp and lenght i use to easily make this good
"""

import random
import string
from typing import Protocol


class OTPGenerator(Protocol):
    def generate(
        self,
        length: int,
    ) -> str: ...


class OTPNumberGenerator:
    def generate(
        self,
        length: int,
    ) -> str:
        # i will use another login in reality #TODO
        n = random.randint(
            a=100000,
            b=999999999999999999999999999999999999,
        )
        return str(n)[0:length]


class OTPAlphabetGenerator:
    def generate(
        self,
        length: int,
    ) -> str:
        LETTERS = string.ascii_uppercase
        s = "".join(random.choice(LETTERS) for _ in range(length))
        return s
