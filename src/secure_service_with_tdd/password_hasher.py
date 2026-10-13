import bcrypt

from src.secure_service_with_tdd.interfaces import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self, rounds: int = 12) -> None:
        self.rounds = rounds

    def hash_password(self, original_password: str) -> str:
        """Hashes a plain-text password and returns the hash as a string"""

        password_bytes = original_password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode("utf-8")

    def verify_password(self, original_password: str, password_hash: str) -> bool:
        """Verifies if the original password matches the stored hash"""

        password_bytes = original_password.encode("utf-8")
        hash_bytes = password_hash.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hash_bytes)
