from abc import ABC, abstractmethod

from src.secure_service_with_tdd.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def save_new_user(self, user: User) -> None: ...


class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, original_password: str) -> str: ...

    @abstractmethod
    def verify_password(self, original_password: str, password_hash: str) -> bool: ...
