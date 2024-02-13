#!/usr/bin/env python3
"""Module for the BasicAuth class"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar

from models.user import User


class BasicAuth(Auth):
    """BasicAuth class that implements basic authentication."""

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extracts the string after 'Basic '"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        prefix = 'Basic '
        if not authorization_header.startswith(prefix):
            return None
        return authorization_header[len(prefix):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 string."""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded = base64_authorization_header.encode()
            decoded = base64.b64decode(decoded)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user credentials from a string."""
        if decoded_base64_authorization_header is None:
            return None
        if type(decoded_base64_authorization_header) != str:
            return None
        if ':' not in decoded_base64_authorization_header:
            return None
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Returns a User instance from a username and a password."""
        if type(user_email) != str or type(user_pwd) != str:
            return None
        user_lst = User.search({'email': user_email})
        if len(user_lst) == 0:
            return None
        user = user_lst[0]
        if user.is_valid_password(user_pwd):
            return user
        else:
            return None
