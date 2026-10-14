from src.secure_service_with_tdd.user import User


class TestUser:

    def test_user_can_be_created_with_expected_fields(self):
        user = User(1, "Alice", "my_hashed_password_123")

        assert user.username == "Alice"
        assert user.password_hash == "my_hashed_password_123"

    def test_user_does_not_store_original_password(self):
        original_password = "my_secret_password"
        user = User(1, "Alice", "my_hashed_password_123")

        assert not hasattr(user, "password")
        assert user.password_hash != original_password
