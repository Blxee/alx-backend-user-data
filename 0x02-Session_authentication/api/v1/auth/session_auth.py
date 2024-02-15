#!/usr/bin/env python3
"""Module for the SessionAuth class."""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class for handling session based authentication."""
    lastest_instance = None
    user_id_by_session_id = {}

    def __init__(self):
        SessionAuth.lastest_instance = self
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session for a user id."""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a user id from a session id."""
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieves the current session auth user."""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Removes the session associated with the user."""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
