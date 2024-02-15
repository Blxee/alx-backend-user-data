#!/usr/bin/env python3
"""Module for the SessionExpAuth class."""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Declaration for the SessionExpAuth calss."""

    def __init__(self):
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0
        super().__init__()

    def create_session(self, user_id=None):
        """Creates a new session for a user id."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a user id from a session id."""
        if session_id is None or type(session_id) != str:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            return None
        if self.session_duration + session_dict.get('created_at') < timedelta():
            return None
        return session_dict.get('user_id')
