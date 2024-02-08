#!/usr/bin/env python3
"""Module for the last two tasks."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password."""
    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the a hash matches the password string."""
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password)
