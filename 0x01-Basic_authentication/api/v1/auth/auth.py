#!/usr/bin/env python3
"""Module for the Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns whether a path requires authorization."""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns the auth header."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the auth user from a request."""
        return None
