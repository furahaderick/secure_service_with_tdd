import pytest

from src.secure_service_with_tdd.password_hasher import BcryptPasswordHasher


@pytest.fixture
def hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher(rounds=4)


def test_hash_different_from_original(hasher: BcryptPasswordHasher):
    password = "correct_secure_password"
    hashed = hasher.hash_password(password)
    assert hashed != password


def test_verify_password_success(hasher: BcryptPasswordHasher):
    password = "correct_secure_password"
    hashed = hasher.hash_password(password)

    assert hasher.verify_password(password, hashed) is True


def test_verify_password_failure(hasher: BcryptPasswordHasher):
    password = "correct_secure_password"
    hashed = hasher.hash_password(password)

    assert hasher.verify_password("wrong_password", hashed) is False


def test_salts_are_unique(hasher: BcryptPasswordHasher):
    password = "same_password"
    hash_one = hasher.hash_password(password)
    hash_two = hasher.hash_password(password)

    assert hash_one != hash_two
