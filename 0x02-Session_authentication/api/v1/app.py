#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import (
    SessionAuth,
    login_view,
    logout_view
)
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


auth = None

if getenv('AUTH_TYPE') == 'basic_auth':
    auth = BasicAuth()
elif getenv('AUTH_TYPE') == 'session_auth':
    auth = SessionAuth()
elif getenv('AUTH_TYPE') == 'session_exp_auth':
    auth = SessionExpAuth()
elif getenv('AUTH_TYPE') == 'session_db_auth':
    auth = SessionDBAuth()
elif getenv('AUTH_TYPE') is not None:
    auth = Auth()


def handle_auth():
    """Function that runs before every request."""
    if auth is not None:
        exclude_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/',
        ]
        request.current_user = auth.current_user(request)
        if not auth.require_auth(request.path, exclude_paths):
            return
        if auth.authorization_header(request) is None:
            # and auth.session_cookie(request) is None
            abort(401)
        if auth.current_user(request) is None:
            abort(403)


app_views.before_request(handle_auth)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """Unauthorized handler"""
    res = jsonify({"error": "Unauthorized"})
    return (res, 401)


@app.errorhandler(403)
def forbidden(error):
    """Forbidden handler"""
    res = jsonify({"error": "Forbidden"})
    return (res, 403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
