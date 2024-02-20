#!/usr/bin/env python3
"""Module for user authentication."""
import bcrypt
from db import DB


def _hash_password(password: str) -> bytes:
    """Generates a password hash."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
