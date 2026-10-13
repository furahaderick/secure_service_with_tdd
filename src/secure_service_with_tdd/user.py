from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: int
    username: str
    password_hash: str
