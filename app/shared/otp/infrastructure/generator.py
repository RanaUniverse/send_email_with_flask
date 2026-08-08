"""
app/shared/otp/infrastructer/generator.py

Here i will have the logic to generate the otp
this values i will call in my send, executes and so on using the factory.py
"""

import random
import string


from ..interfaces.generator import OTPGenerator  # type: ignore


class LocalTestingOTPGenerator:
    def generate(
        self,
        length: int,
    ) -> str:
        return "111111"


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
