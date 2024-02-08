#!/usr/bin/env python3
"""Main tasks module."""
import logging
import mysql.connector
from os import environ
import re
from typing import List


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated."""
    return re.sub(
        rf'(({"|".join(fields)})=)[^{separator}]*',
        rf'\1{redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Formats fields of record."""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


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


def main() -> None:
    logger = get_logger()
    with get_db() as db:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            for row in cursor:
                logger.info(RedactingFormatter.SEPARATOR.join(row))


if __name__ == '__main__':
    main()
