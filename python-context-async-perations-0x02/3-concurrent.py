import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users from the database asynchronously"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results


async def async_fetch_older_users():
    """Fetch users older than 40 from the database asynchronously"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            return results


async def init__database():
    """Create and populate the users table"""
    async with aiosqlite.connect("users.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')

        # Clear sample data
        await db.execute("DELETE FROM users")

        # Insert sample data
        sample_users = [
            ('Alice', 35),
            ('Bob', 28),
            ('Charlie', 45),
            ('Diana', 52),
            ('Eve', 30),
            ('Frank', 41),
        ]

        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", sample_users)
        await db.commit()


async def fetch_concurrently():
    """Execute both fetch functions concurrently"""
    # First, initialize the database
    await init__database()

    # Run both queries concurrently using asyncio.gather
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    # Display results
    print("=" * 50)
    print("All Users")
    print("=" * 50)
    for user in all_users:
        print(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")
    print("\n" + "=" * 50)
    print("Users Older Than 40")
    print("=" * 50)
    for user in older_users:
        print(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")
    print("\n" + "=" * 50)

    print(f"Total Users: {len(all_users)}")
    print(f"Total Users Older Than 40: {len(older_users)}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
