#!/usr/bin/python3
"""
ALX Backend Python - Python Generators Project
Memory-efficient aggregation using generators
"""

from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.

    Yields:
        int: User age from the database
    """
    connection = connect_to_prodev()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:
            yield age

        cursor.close()
    finally:
        connection.close()


def average_age():
    """
    Calculates the average age of all users using the stream_user_ages generator.
    Uses memory-efficient approach without loading all data into memory.

    Returns:
        float: Average age of all users, or None if no users exist
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        return None

    return total_age / count
