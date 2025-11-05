"""
Custom context manager for database connection management.
Demonstrates __enter__ and __exit__ methods for automatic resource cleanup.
"""
import sqlite3


class DatabaseConnection:
    """A context manager class for managing SQLite database connections.

    Ensures proper resource acquisition and release using the context manager
    protocol (__enter__ and __exit__ methods).
    """

    def __init__(self, db_path: str = "database.db"):
        """
        Initialize the DatabaseConnection context manager.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        """Establish the database connection when entering the context.

        Returns:
            The database connection object.
        """
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection when exiting the context.

        Args:
            exc_type: The type of exception raised (if any)
            exc_val: The value of the exception raised (if any)
            exc_tb: The traceback of the exception raised (if any)
        """
        if self.connection:
            self.connection.close()
        return False  # Propagate exceptions, if any


# Example usage:: Execcute a SELECT query using the context manager
if __name__ == "__main__":
    # Create a sample database and table for demonstration
    with DatabaseConnection("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            )
        """)
        # Insert sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                ("Alice Johnson", "alice@example.com", 28)
            )
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                ("Bob Smith", "bob@example.com", 35)
            )
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                ("Charlie Brown", "charlie@example.com", 42)
            )
            conn.commit()

        # Use the context manager to query the database
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        print("Users in the database:")
        print("-" * 65)
        for user in users:
            print(
                f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}")
        print("-" * 65)
