# app/security.py

from passlib.context import CryptContext

# Define the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)
