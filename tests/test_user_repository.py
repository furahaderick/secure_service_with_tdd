import pytest

from src.secure_service_with_tdd.user import User
from src.secure_service_with_tdd.repository import InMemoryUserRepository


@pytest.fixture
def user_repo():
    """Provides a fresh users store for each test"""
    return InMemoryUserRepository()


def test_save_and_get_new_user_by_username(user_repo: InMemoryUserRepository):
    user = User(1, "Alice", "my_hashed_password_123")
    user_repo.save_new_user(user)
    retrieved_user = user_repo.get_user_by_username("Alice")

    assert retrieved_user == user


def test_user_not_found(user_repo: InMemoryUserRepository):
    retrieved_user = user_repo.get_user_by_username("Bob")
    assert retrieved_user is None
