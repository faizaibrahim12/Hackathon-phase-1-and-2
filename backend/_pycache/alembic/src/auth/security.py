"""Password hashing and security utilities"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string
    """
    # Truncate password to 72 bytes to comply with bcrypt limitations
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')

    # Convert password to bytes if it's not already
    if isinstance(password, str):
        password = password.encode('utf-8')

    # Generate salt and hash the password
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password, salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain text password against hashed password

    Args:
        plain_password: Plain text password from user
        hashed_password: Hashed password from database

    Returns:
        True if passwords match, False otherwise
    """
    # Convert strings to bytes if they're not already
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_password, hashed_password)
