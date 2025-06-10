# backend/app/core/security.py
from passlib.context import CryptContext

# Configuration for password hashing
# schemes: list of hashing algorithms to support
# deprecated: list of algorithms that are deprecated but can still be verified
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)