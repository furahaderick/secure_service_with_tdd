from src.secure_service_with_tdd.user import User
from src.secure_service_with_tdd.interfaces import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: dict[int, User] = {}

    def get_user_by_username(self, username: str) -> User | None:
        """Finds a user by username. Returns None if not found."""
        return next((u for u in self.users.values() if u.username == username), None)

    def save_new_user(self, user: User) -> None:
        """Persists a user object in memory"""
        self.users[user.id] = user
