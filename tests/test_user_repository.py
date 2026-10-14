from src.secure_service_with_tdd.user import User
from src.secure_service_with_tdd.interfaces import UserRepository


def test_save_and_get_new_user_by_username(user_repo: UserRepository):
    user = User(1, "Alice", "my_hashed_password_123")
    user_repo.save_new_user(user)
    retrieved_user = user_repo.get_user_by_username("Alice")

    assert retrieved_user == user


def test_user_not_found(user_repo: UserRepository):
    retrieved_user = user_repo.get_user_by_username("Bob")
    assert retrieved_user is None
