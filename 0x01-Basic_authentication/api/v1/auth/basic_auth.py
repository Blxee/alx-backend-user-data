#!/usr/bin/env python3
"""Module for the BasicAuth class"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 string base64_authorization_header."""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded = base64_authorization_header.encode()
            decoded = base64.b64decode(decoded)
            return decoded.decode('utf-8')
        except:
            return None
