from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


ALGORITHM = "HS256"


def hash_password(password: str) -> str:

    return password_hash.hash(password)


def verify_password(plain_pass: str, hashed_pass: str) -> bool:

    return password_hash.verify(plain_pass, hashed_pass)
