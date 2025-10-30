#!/usr/bin/python3
"""
Generator function that streams rows from the user_data table one by one.
"""

from seed import connect_to_prodev


def stream_users():
    """
    Generator that yields user records from the database one by one.

    Yields:
        dict: A dictionary containing user_id, name, email, and age
    """
    db = connect_to_prodev()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    db.close()
