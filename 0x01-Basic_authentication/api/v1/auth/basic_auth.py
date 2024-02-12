#!/usr/bin/env python3
"""Module for the BasicAuth class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class that implements basic authentication."""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts the string after 'Basic '"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        prefix = 'Basic '
        if not authorization_header.startswith(prefix):
            return None
        return authorization_header[len(prefix):]
