import sqlite3
import functools
from datetime import datetime


def log_queries(func):
    """
    Decorator that logs SQL queries before executing them.

    This decorator wraps a function and logs any SQL query passed to it
    before the function executes, providing visibility into database operations.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'query' in kwargs:
            query = kwargs['query']
        elif args and isinstance(args[0], str):
            query = args[0]
        else:
            query = "Query not found"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing query: {query}")

        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Test the decorated function - the query will be logged automatically
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users")
