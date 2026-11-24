from fastapi.security.oauth2 import OAuth2PasswordBearer
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


ALGORITHM = "HS256"

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:

    return password_hash.hash(password)


def verify_password(plain_pass: str, hashed_pass: str) -> bool:

    return password_hash.verify(plain_pass, hashed_pass)
