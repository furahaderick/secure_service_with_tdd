import logging

from src.secure_service_with_tdd.exceptions import (
    InvalidPasswordException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.secure_service_with_tdd.interfaces import PasswordHasher, UserRepository
from src.secure_service_with_tdd.user import User

logger = logging.getLogger(__name__)


class UserService:
    MIN_PASSWORD_LENGTH = 8

    def __init__(
        self, user_repo: UserRepository, password_hasher: PasswordHasher
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def register_user(self, user_id: int, username: str, password: str) -> User:
        """Registers a new user and stores only their password hash."""

        if len(password) < self.MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException(
                f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters long."
            )

        if self.user_repo.get_user_by_username(username) is not None:
            logger.warning(
                "User registration rejected",
                extra={
                    "event": "registration_rejected",
                    "reason": "duplicate_username",
                    "username": username,
                },
            )
            raise UserAlreadyExistsException(f"User '{username}' already exists.")

        password_hash = self.password_hasher.hash_password(password)

        user = User(
            id=user_id,
            username=username,
            password_hash=password_hash,
        )

        self.user_repo.save_new_user(user)

        logger.info(
            "User registered successfully",
            extra={
                "event": "registration_success",
                "user_id": user.id,
                "username": user.username,
            },
        )

        return user

    def login(self, username: str, password: str) -> User:
        """Authenticates a user and returns the authenticated user."""

        user = self.user_repo.get_user_by_username(username)

        if user is None:
            logger.warning(
                "User authentication failed",
                extra={
                    "event": "authentication_failure",
                    "reason": "user_not_found",
                    "username": username,
                },
            )
            raise UserNotFoundException(f"User '{username}' was not found.")

        if not self.password_hasher.verify_password(password, user.password_hash):
            logger.warning(
                "User authentication failed",
                extra={
                    "event": "authentication_failure",
                    "reason": "invalid_password",
                    "user_id": user.id,
                    "username": user.username,
                },
            )
            raise InvalidPasswordException("Invalid password.")

        logger.info(
            "User authenticated successfully",
            extra={
                "event": "authentication_success",
                "user_id": user.id,
                "username": user.username,
            },
        )

        return user
