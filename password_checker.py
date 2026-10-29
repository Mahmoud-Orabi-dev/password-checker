import math
import secrets
import string
import sys

COMMON = {"123456", "password", "12345678", "qwerty", "123456789", "111111", "abc123", "password1", "iloveyou", "admin"}


def rate_password(pw):
    if pw.lower() in COMMON:
        return "VERY WEAK", 0.0, ["This is one of the most common passwords"]

    pool = 0
    tips = []
    if any(c.islower() for c in pw):
        pool += 26
    else:
        tips.append("Add lowercase letters")
    if any(c.isupper() for c in pw):
        pool += 26
    else:
        tips.append("Add uppercase letters")
    if any(c.isdigit() for c in pw):
        pool += 10
    else:
        tips.append("Add numbers")
    if any(c in string.punctuation for c in pw):
        pool += 32
    else:
        tips.append("Add symbols")
    if len(pw) < 12:
        tips.append("Use at least 12 characters")

    entropy = len(pw) * math.log2(pool) if pool else 0.0

    if entropy < 40:
        label = "WEAK"
    elif entropy < 60:
        label = "MEDIUM"
    elif entropy < 80:
        label = "STRONG"
    else:
        label = "VERY STRONG"
    return label, entropy, tips


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "generate":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 16
        print(generate_password(n))
    elif len(sys.argv) >= 2:
        label, bits, tips = rate_password(sys.argv[1])
        print("Strength:", label, "(" + str(round(bits, 1)) + " bits)")
        for t in tips:
            print(" -", t)
    else:
        print("Usage: python password_checker.py <password>")
        print("   or: python password_checker.py generate [length]")
