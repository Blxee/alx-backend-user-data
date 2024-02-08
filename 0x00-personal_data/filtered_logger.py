#!/usr/bin/env python3
"""Main tasks module."""
import logging
import re


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    pattern = rf'(({"|".join(fields)})=)[^{separator}]*'
    return re.sub(pattern, rf'\1{redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION, self.FORMAT % {
            'name': record.name, 'levelname': record.levelname,
            'asctime': record.asctime, 'message': record.msg}, self.SEPARATOR)
