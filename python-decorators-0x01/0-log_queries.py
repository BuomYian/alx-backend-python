import sqlite3
import functools


def log_queries(func):
    """Decorator that logs SQL queries before executing them.

    This decorator wraps a function and logs any SQL query passed to it before the function executes, providing better traceability of database operations.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'query' in kwargs:
            query = kwargs['query']
        elif args and isinstance(args[0], str):
            query = args[0]
        else:
            query = "Query not found"

        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the database using the provided SQL query."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Test the decorator function - the query will be logged automatically
if __name__ == "__main__":
    users = fetch_all_users("SELECT * FROM users;")
    print(f"Retrieved {len(users)} users")
