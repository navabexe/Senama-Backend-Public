import random
import string


def generate_otp(length: int = 6) -> str:
    return ''.join(random.choice(string.digits) for _ in range(length))
