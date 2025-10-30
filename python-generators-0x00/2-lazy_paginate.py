#!/usr/bin/python3
"""
Lazy pagination module for fetching users in pages using generators.
"""
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.

    Args:
        page_size: Number of users per page
        offset: Starting position in the database

    Returns:
        List of user dictionaries
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads pages of users one at a time.

    Args:
        page_size: Number of users per page

    Yields:
        List of user dictionaries for each page
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
    return
