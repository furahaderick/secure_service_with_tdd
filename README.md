# Secure Service with TDD

A lightweight authentication module built with Test-Driven Development (TDD), providing secure user registration and login functionality with password hashing.

## Project Overview

This module implements a secure authentication service that handles user registration and login operations. It uses bcrypt for password hashing and follows dependency injection principles for testability.

## Features

- **User Registration**: Register new users with username and password validation
- **Password Hashing**: Secure password storage using bcrypt with configurable rounds
- **User Login**: Authenticate users with username and password verification
- **Custom Exceptions**:
   - `UserAlreadyExistsException` - Raised when attempting to register a duplicate username
   - `InvalidPasswordException` - Raised for passwords that are too short or incorrect
   - `UserNotFoundException` - Raised when attempting to login with a non-existent username

## Architecture

The project follows a layered architecture with clear separation of concerns:

- **UserService**: Core business logic for user registration and authentication. Validates passwords, checks for duplicate users, and coordinates between repository and password hasher.
- **UserRepository**: Abstract interface for data persistence. `InMemoryUserRepository` provides a simple in-memory implementation using a dictionary.
- **PasswordHasher**: Abstract interface for password operations. `BcryptPasswordHasher` implements bcrypt hashing with configurable cost rounds (default: 12).

## Installation

Install dependencies using Poetry:

```bash
poetry install
```

This installs the runtime dependency `bcrypt` and development tools including `pytest`, `pytest-mock`, and `coverage`.

## Usage

```python
from src.secure_service_with_tdd.service import UserService
from src.secure_service_with_tdd.repository import InMemoryUserRepository
from src.secure_service_with_tdd.password_hasher import BcryptPasswordHasher

# Create dependencies
user_repo = InMemoryUserRepository()
password_hasher = BcryptPasswordHasher(rounds=12)
user_service = UserService(user_repo, password_hasher)

# Register a user
user = user_service.register_user(
    user_id=1, username="alice", password="securepassword"
)

# Login
authenticated_user = user_service.login("alice", "securepassword")
```

## Testing

Run tests with pytest:

```bash
poetry run pytest
```

Generate coverage report:

```bash
poetry run coverage run -m pytest
poetry run coverage report
```

## Quality Checks

Pre-commit hooks are configured for code quality:

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run hooks manually
poetry run pre-commit run --all-files
```

The configured hooks include:

- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-added-large-files

## Security Notes

- **Password Hashing**: Uses bcrypt with 12 rounds by default, providing strong protection against brute-force attacks. Passwords are never stored in plain text.
- **In-Memory Storage**: The default `InMemoryUserRepository` stores data in memory only. All user data is lost when the application restarts. For production use, implement a persistent repository (e.g., MySQL database).
- **Password Validation**: Minimum password length is enforced (8 characters) to prevent weak passwords.
