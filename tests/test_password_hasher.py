from src.secure_service_with_tdd.interfaces import PasswordHasher


def test_hash_different_from_original(password_hasher: PasswordHasher):
    password = "correct_secure_password"
    hashed = password_hasher.hash_password(password)
    assert hashed != password


def test_verify_password_success(password_hasher: PasswordHasher):
    password = "correct_secure_password"
    hashed = password_hasher.hash_password(password)

    assert password_hasher.verify_password(password, hashed) is True


def test_verify_password_failure(password_hasher: PasswordHasher):
    password = "correct_secure_password"
    hashed = password_hasher.hash_password(password)

    assert password_hasher.verify_password("wrong_password", hashed) is False


def test_salts_are_unique(password_hasher: PasswordHasher):
    password = "same_password"
    hash_one = password_hasher.hash_password(password)
    hash_two = password_hasher.hash_password(password)

    assert hash_one != hash_two
