#!/usr/bin/env python3
"""Module for user authentication."""
from typing import Union
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Generates a password hash."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a random uuid."""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Returns whether the credentials are valid."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(),
                                  user.hashed_password.encode())
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Creates and returns a session id for a user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (InvalidRequestError, NoResultFound, ValueError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Returns the corresponding user from a session id."""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except (InvalidRequestError, NoResultFound):
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys session assossiated with user."""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Makes and returns a reset password token."""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password for a user using a reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed,
                                 reset_token=None)
        except Exception:
            raise ValueError
