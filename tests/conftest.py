import pytest

from src.secure_service_with_tdd.interfaces import PasswordHasher
from src.secure_service_with_tdd.password_hasher import BcryptPasswordHasher
from src.secure_service_with_tdd.repository import InMemoryUserRepository
from src.secure_service_with_tdd.service import UserService


@pytest.fixture
def password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher(rounds=4)


@pytest.fixture
def user_repo():
    """Provides a fresh users store for each test"""
    return InMemoryUserRepository()


@pytest.fixture
def user_service(user_repo, password_hasher):
    # Inject the mock/in-memory dependencies into the service for testing
    return UserService(user_repo=user_repo, password_hasher=password_hasher)
