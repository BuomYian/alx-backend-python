import sqlite3


class ExecuteQuery:
    """Context manager for executing database queries with automatic connection management."""

    def __init__(self, db_name, query, params=()):
        """
        Initialize the context manager with database name, query, and parameters.

        Args:
            db_name (str): Name of the SQLite database file
            query (str): SQL query to execute
            params (tuple): Parameters for parameterized query (default: empty tuple)
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        """
        Open the database connection and execute the query.

        Returns:
            list: The result of the query execution
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.query, self.params)
            self.result = self.cursor.fetchall()

            return self.result
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            if self.connection:
                self.connection.close()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the database connection safely.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)

        Returns:
            False: Allow exceptions to propagate
        """
        if self.connection:
            self.connection.close()
        return False


# Example usage: Execute a parameterized SELECT query using the context manager
if __name__ == "__main__":
    # Setup: Create sample database and populate with data
    setup_conn = sqlite3.connect("example.db")
    setup_cursor = setup_conn.cursor()

    # Create users table if it doesn't exist
    setup_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    # Clear existing data and insert sample data
    setup_cursor.execute("DELETE FROM users")
    setup_cursor.executemany(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        [
            ("Alice", 30),
            ("Bob", 22),
            ("Charlie", 28),
            ("David", 26),
            ("Eve", 24),
        ]
    )
    setup_conn.commit()
    setup_conn.close()

    # Use the ExecuteQuery context manager to run a parameterized query
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    print(f"Executing query: {query}")
    print(f"With parameters: age > {params[0]}\n")

    with ExecuteQuery("example.db", query, params) as results:
        print("Results:")
        print(f"{'ID':<5} {'Name':<15} {'Age':<5}")
        print("-" * 25)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<5}")
        print(f"\nTotal rows returned: {len(results)}")
