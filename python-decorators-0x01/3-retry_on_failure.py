import time
import sqlite3
import functools


def with_db_connection(func):
    """Decorator that manages database connection lifecycle"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(':memory:')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=1):
    """
    Decorator that retries a function if it raises an exception.

    Args:
        retries: Number of times to retry the function
        delay: Delay in seconds between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= retries:
                        print(
                            f"Failed after {retries} attempts. Last error: {e}")
                        raise
                    print(
                        f"Attempt {attempts} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
