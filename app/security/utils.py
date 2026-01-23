from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return generate_password_hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return check_password_hash(password_hash, password)
