#!/usr/bin/env python3
"""Main tasks module."""
import logging
import mysql.connector
from os import environ
import re


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


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
        """Formats fields of record."""
        return filter_datum(self.fields, self.REDACTION, self.FORMAT % {
            'name': record.name, 'levelname': record.levelname,
            'asctime': record.asctime, 'message': record.msg}, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates a new logger for user_data."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Establishes a conection to mysql database and returns it."""
    user = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    database = environ.get('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(
        user=user, password=password, host=host, database=database
    )
