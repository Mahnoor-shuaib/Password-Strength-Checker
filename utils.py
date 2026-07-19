import hmac
import hashlib


def secure_compare(a, b):
    """Constant-time string comparison to prevent timing attacks"""
    return hmac.compare_digest(a.encode(), b.encode())


def hash_password(password):
    """Hash password for secure storage (not used in this project)"""
    return hashlib.sha256(password.encode()).hexdigest()


def clear_variable(var):
    """Safely clear variable from memory"""
    try:
        del var
    except:
        pass