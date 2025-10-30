#!/usr/bin/python3
"""
ALX Backend Python - Batch Processing with Generators
Demonstrates batch processing of database records using generators
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches users from the database in batches.

    Args:
        batch_size (int): Number of records to fetch in each batch

    Yields:
        list: A batch of user dictionaries with user_id, name, email, and age
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev',
            port=3306
        )
        cursor = connection.cursor(dictionary=True)

        # Fetch all users and yield them in batches
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        # Yield remaining records if any
        if batch:
            yield batch

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error: {e}")


def batch_processing(batch_size):
    """
    Processes batches of users and filters those over age 25.

    Args:
        batch_size (int): Number of records to process in each batch
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
