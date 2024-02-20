#!/usr/bin/env python3
"""Module for user authentication."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Generates a password hash."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user to the database."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except (InvalidRequestError, NoResultFound):
            hashed = _hash_password(password).decode()
            user = self._db.add_user(email, hashed)
            return user
