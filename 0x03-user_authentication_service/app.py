#!/usr/bin/env python3
"""Module of the main ."""
from auth import Auth
from flask import Flask, abort, jsonify, request, redirect


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Root route definition."""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Route for creating a new user."""
    email = request.form['email']
    password = request.form['password']
    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Route for the user to login."""
    email = request.form['email']
    password = request.form['password']
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({'email': email, 'message': 'logged in'})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Route for the user to logout."""
    session_id = request.cookies['session_id']
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return ('', 403)
    AUTH.destroy_session(user.id)
    redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Route for the signed-in user profile."""
    session_id = request.cookies['session_id']
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return ('', 403)
    return jsonify({'email': user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """Route for getting a reset password token."""
    email = request.form['email']
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': token})
    except ValueError:
        return ('', 403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
