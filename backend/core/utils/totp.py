import pyotp

def generate_mfa_secret():
    return pyotp.random_base32()

def verify_totp(secret, token):
    if not secret:
        return False
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
