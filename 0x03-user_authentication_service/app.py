#!/usr/bin/env python3
"""Module of the main ."""
from auth import Auth
from flask import Flask, jsonify, request


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
