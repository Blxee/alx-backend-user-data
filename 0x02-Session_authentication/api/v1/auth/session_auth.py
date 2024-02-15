#!/usr/bin/env python3
"""Module for the SessionAuth class."""
from os import getenv
from flask import jsonify, request, abort
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from api.v1.views import app_views


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


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_view():
    """The login route."""
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    auth = SessionAuth.lastest_instance
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout_view():
    """The logout route."""
    auth = SessionAuth.lastest_instance
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
