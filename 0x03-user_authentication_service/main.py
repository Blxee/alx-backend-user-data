#!/usr/bin/env python3
"""Module for testing the api routes."""
import requests


def register_user(email, passwd):
    """Test register user."""
    response = requests.post('localhost:5000/users',
                             data={'email': email, 'password': passwd})
    assert response.json() == {'email': email, 'message': 'user created'}
    response = requests.post('localhost:5000/users',
                             data={'email': email, 'password': passwd})
    assert response.json() == {'message': 'email already registered'}


def log_in_wrong_password(email, new_passwd):
    """Test login with wrong password."""
    response = requests.post('localhost:5000/sessions',
                             data={'email': email, 'password': new_passwd})
    assert response.status_code == 401


def profile_unlogged():
    """Test profile route no login."""
    response = requests.get('localhost:5000/profile')
    assert response.status_code == 403


def log_in(email, passwd):
    """log in user."""
    response = requests.post('localhost:5000/sessions',
                             data={'email': email, 'password': passwd})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'logged in'}
    return response.cookies.get('session_id')


def profile_logged(session_id):
    """test profile route with login."""
    response = requests.get('localhost:5000/profile',
                            cookies={'session_id': session_id})
    assert response.status_code == 200


def log_out(session_id):
    """Test log out user."""
    response = requests.delete('localhost:5000/logout',
                               cookies={'session_id': session_id})
    assert response.status_code == 200


def reset_password_token(email):
    """Test reset user password."""
    response = requests.post('localhost:5000/reset_password',
                             data={'email': email})
    assert response.status_code == 200
    return response.json().get('reset_token')


def update_password(email, reset_token, new_passwd):
    """Test reset user password."""
    response = requests.put('localhost:5000/reset_password',
                            data={'email': email,
                                  'reset_token': reset_token,
                                  'new_password': new_passwd})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
