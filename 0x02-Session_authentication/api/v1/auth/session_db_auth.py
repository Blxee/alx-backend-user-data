#!/usr/bin/env python3
"""Module for SessionDBAuth class."""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Class declaration for SessionDBAuth."""

    def create_session(self, user_id=None):
        """Creates a new session for a user id."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_session = UserSession(user_id=user_id,
                                        session_id=session_id)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves a user id from a session id."""
        user_id = super().user_id_for_session_id(session_id)
        return user_id

    def destroy_session(self, request=None):
        """Removes the session associated with the user."""
        destroy = super().destroy_session(request)
        if destroy:
            self.user_session.remove()
        return destroy
