#!/usr/bin/env python3
"""Main tasks module."""
import logging
import re


def filter_datum(fields: list[str], redaction: str, message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    pattern = rf'(({"|".join(fields)})=)[^{separator}]*'
    return re.sub(pattern, rf'\1{redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
