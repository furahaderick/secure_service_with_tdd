from unittest.mock import Mock

import pytest

from src.secure_service_with_tdd.interfaces import PasswordHasher
from src.secure_service_with_tdd.service import UserService
from src.secure_service_with_tdd.exceptions import (
    InvalidPasswordException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


def test_register_user_successfully(user_service, user_repo):
    user = user_service.register_user(
        user_id=1,
        username="alice",
        password="securepassword",
    )

    assert user.username == "alice"
    assert user.password_hash != "securepassword"
    assert user_repo.get_user_by_username("alice") == user


def test_register_user_rejects_short_password(user_service, user_repo):
    with pytest.raises(InvalidPasswordException):
        user_service.register_user(
            user_id=1,
            username="alice",
            password="short",
        )

    assert user_repo.get_user_by_username("alice") is None


def test_register_user_rejects_existing_username(user_service):
    user_service.register_user(
        user_id=1,
        username="alice",
        password="securepassword",
    )

    with pytest.raises(UserAlreadyExistsException):
        user_service.register_user(
            user_id=2,
            username="alice",
            password="anothersecurepassword",
        )


def test_registered_password_is_hashed(user_service, user_repo, password_hasher):
    password = "securepassword"

    user_service.register_user(
        user_id=1,
        username="alice",
        password=password,
    )

    stored_user = user_repo.get_user_by_username("alice")

    assert stored_user is not None
    assert stored_user.password_hash != password
    assert password_hasher.verify_password(password, stored_user.password_hash)


def test_invalid_registration_does_not_save_user(user_service, user_repo):
    with pytest.raises(InvalidPasswordException):
        user_service.register_user(
            user_id=1,
            username="alice",
            password="short",
        )

    assert user_repo.users == {}


def test_existing_username_does_not_overwrite_user(user_service, user_repo):
    original_user = user_service.register_user(
        user_id=1,
        username="alice",
        password="securepassword",
    )

    with pytest.raises(UserAlreadyExistsException):
        user_service.register_user(
            user_id=2,
            username="alice",
            password="anothersecurepassword",
        )

    assert user_repo.get_user_by_username("alice") == original_user
    assert len(user_repo.users) == 1


def test_register_user_hashes_supplied_password(user_repo):
    password_hasher = Mock(spec=PasswordHasher)
    password_hasher.hash_password.return_value = "hashed_password"

    service = UserService(
        user_repo=user_repo,
        password_hasher=password_hasher,
    )

    user = service.register_user(
        user_id=1,
        username="alice",
        password="securepassword",
    )

    password_hasher.hash_password.assert_called_once_with("securepassword")

    assert user.password_hash == "hashed_password"
    assert user_repo.get_user_by_username("alice").password_hash == ("hashed_password")


def test_login_successfully(user_service):
    user_service.register_user(
        user_id=1,
        username="alice",
        password="securepassword",
    )

    user = user_service.login("alice", "securepassword")

    assert user is not None
    assert user.username == "alice"


def test_login_unknown_username_raises_exception(user_service):
    with pytest.raises(UserNotFoundException):
        user_service.login("unknown", "securepassword")


def test_login_wrong_password_raises_exception(user_service):
    user_service.register_user(
        user_id=1,
        username="alice",
        password="securepassword",
    )

    with pytest.raises(InvalidPasswordException):
        user_service.login("alice", "wrongpassword")


def test_login_verifies_supplied_password_against_stored_hash(
    user_repo,
):
    password_hasher = Mock(spec=PasswordHasher)
    password_hasher.hash_password.return_value = "stored_hash"
    password_hasher.verify_password.return_value = True

    service = UserService(
        user_repo=user_repo,
        password_hasher=password_hasher,
    )

    service.register_user(1, "alice", "securepassword")
    password_hasher.verify_password.reset_mock()

    service.login("alice", "supplied-password")

    password_hasher.verify_password.assert_called_once_with(
        "supplied-password",
        "stored_hash",
    )


def test_login_does_not_verify_password_for_unknown_user(user_repo):
    password_hasher = Mock(spec=PasswordHasher)

    service = UserService(
        user_repo=user_repo,
        password_hasher=password_hasher,
    )

    with pytest.raises(UserNotFoundException):
        service.login("unknown", "securepassword")

    password_hasher.verify_password.assert_not_called()


def test_failed_login_does_not_return_user(user_service):
    user_service.register_user(
        user_id=1,
        username="alice",
        password="securepassword",
    )

    with pytest.raises(InvalidPasswordException):
        user_service.login("alice", "wrongpassword")
